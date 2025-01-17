from pathlib import Path
from database_asset import scan_folder
from database_class import extract_classes_from_cpp, parse_class_hierarchy
from database_class_debug import write_debug_class_dump, write_debug_class_csv
from report import save_report, print_quick_summary
from cache_manager import CacheManager
from scanner import scan_mission_folder
import logging
import traceback
import sys
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List
import hashlib

@dataclass
class ScanTask:
    name: str
    mods_folder: Path
    mission_folder: Path
    cpp_file_path: Path

def get_task_hash(task) -> str:
    """Generate a hash for the task based on its configuration"""
    task_data = f"{task.mods_folder}_{task.mission_folder}"
    return hashlib.md5(task_data.encode()).hexdigest()

def process_scan_task(task: ScanTask, cache_mgr: CacheManager, logger: logging.Logger) -> bool:
    """Process a single scan task"""
    try:
        # Generate task name and hash for caching
        task_name = Path(task.mods_folder).name
        task_hash = get_task_hash(task)

        logger.info(f"Processing task for {task_name}...")
        logger.info(f"Scanning mods folder: {task.mods_folder}")
        logger.setLevel(logging.DEBUG)
        
        # Validate paths exist
        if not task.cpp_file_path.exists():
            logger.error(f"Error: Config file not found: {task.cpp_file_path}")
            return False
        
        class_database = {}

        # Process the cpp file containing class data
        logger.info(f"\nScanning cpp file: {task.cpp_file_path}")
        try:
            class_entries_by_category = extract_classes_from_cpp(str(task.cpp_file_path))
            
            # Build class database
            logger.info(f"Building class database for {task.name}...")
            
            # Process all entries at once
            all_entries = parse_class_hierarchy(class_entries_by_category)
            
            # Organize by source into a dict of sets
            class_database = {}
            for entry in all_entries.values():
                if entry.source not in class_database:
                    class_database[entry.source] = set()
                class_database[entry.source].add(entry)
            
            logger.info(f"Total classes processed: {len(all_entries)}")
            
        except Exception as e:
            logger.error(f"Failed to extract classes: {e}")
            traceback.print_exc()
            return False

        # Write debug files to debug directory
        write_debug_class_dump(class_database, "debug", task.name)
        write_debug_class_csv(all_entries, "debug", task.name)
        
        logger.info(f"Class database built for {task.name}")

        logger.info(f"\nScanning mods folder: {task.mods_folder}")

        # Scan mods folder for assets with caching support
        asset_database = scan_folder(
            str(task.mods_folder),
            task_name,
            task_hash,
            cache_mgr
        )

        # Validate and scan missions
        if not task.mission_folder.exists():
            logger.error(f"Error: Mission folder does not exist: {task.mission_folder}")
            return False
            
        logger.info(f"\nScanning mission folder: {task.mission_folder}")
        mission_reports = scan_mission_folder(str(task.mission_folder), class_database, asset_database, cache_mgr)
        
        # Generate reports
        print_quick_summary(mission_reports)
        save_report(mission_reports, include_found=False, task_name=task.name)
        return True

    except Exception as e:
        logger.error(f"Error processing task: {e}")
        return False

def main():
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)s: %(message)s'
        )
        logger = logging.getLogger(__name__)
        logger.info("Starting mission scanner...")

        # Initialize cache manager
        cache_mgr = CacheManager()
        
        # Define scan tasks
        scan_tasks = [
            ScanTask(
                name="pcanext",
                mods_folder=Path(r"C:\pcanext"),
                mission_folder=Path(r"C:\pca_missions"),
                cpp_file_path=Path(__file__).parent / "classes" / "classes_pcanext.cpp"
            ),
            # ScanTask(
            #     name="pca",
            #     mods_folder=Path(r"C:\pca"),
            #     mission_folder=Path(r"C:\pca_missions"),
            #     cpp_file_path=Path(__file__).parent / "classes" / "classes_pca.cpp"
            # ),
        ]

        # Process each task
        for task in scan_tasks:
            logger.info(f"\nProcessing scan task: {task.name}")
            if not process_scan_task(task, cache_mgr, logger):
                logger.error(f"Failed to process task: {task.name}")
                
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\nMission scanner finished.")

if __name__ == "__main__":
    main()
