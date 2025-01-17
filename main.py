from pathlib import Path
from database_asset import scan_folder, find_arma3_install, scan_arma3_base
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
from typing import List, Set
import hashlib

# Get logger for this module
logger = logging.getLogger(__name__)

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

def initialize_vanilla_assets(cache_mgr: CacheManager) -> Set[str]:
    """Initialize or load vanilla Arma 3 assets"""
    # Try to get cached vanilla assets first
    vanilla_assets = cache_mgr.get_vanilla_assets()
    if vanilla_assets:
        logger.info(f"Loaded {len(vanilla_assets)} cached vanilla assets")
        return vanilla_assets

    # Scan vanilla assets if not cached
    arma3_path = find_arma3_install()
    if (arma3_path):
        logger.info("Scanning Arma 3 installation for vanilla assets...")
        vanilla_assets = scan_arma3_base(arma3_path, "arma3_base", cache_mgr)
        cache_mgr.store_vanilla_assets(vanilla_assets)
        logger.info(f"Cached {len(vanilla_assets)} vanilla assets")
        return vanilla_assets
    
    return set()

def process_scan_task(task: ScanTask, cache_mgr: CacheManager, vanilla_assets: Set[str], logger: logging.Logger) -> bool:
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

        logger.info(f"Class database built for {task.name}")

        logger.info(f"\nScanning mods folder: {task.mods_folder}")

        # Start with vanilla assets and add mod assets
        asset_database = vanilla_assets.copy()
        logger.info(f"Starting with {len(asset_database)} vanilla assets")

        # Scan mods folder for additional assets
        mod_assets = scan_folder(
            str(task.mods_folder),
            task_name,
            task_hash,
            cache_mgr
        )
        asset_database.update(mod_assets)
        logger.info(f"Added {len(mod_assets)} mod assets, total: {len(asset_database)}")

        # Validate and scan missions
        if not task.mission_folder.exists():
            logger.error(f"Error: Mission folder does not exist: {task.mission_folder}")
            return False
            
        logger.info(f"\nScanning mission folder: {task.mission_folder}")
        mission_reports = scan_mission_folder(str(task.mission_folder), class_database, asset_database, cache_mgr)
        
        # Generate reports first to get the output folder
        print_quick_summary(mission_reports)
        output_folder, _ = save_report(mission_reports, include_found=False, task_name=task.name)
        
        # Write debug files to the same output folder
        write_debug_class_dump(class_database, output_folder, task.name)
        write_debug_class_csv(all_entries, output_folder, task.name)
        
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

        # Initialize cache manager and load vanilla assets once
        cache_mgr = CacheManager()
        vanilla_assets = initialize_vanilla_assets(cache_mgr)
        logger.info(f"Initialized with {len(vanilla_assets)} vanilla Arma 3 assets")
        
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

        for task in scan_tasks:
            logger.info(f"\nProcessing scan task: {task.name}")
            if not process_scan_task(task, cache_mgr, vanilla_assets, logger):
                logger.error(f"Failed to process task: {task.name}")
                
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\nMission scanner finished.")

if __name__ == "__main__":
    main()
