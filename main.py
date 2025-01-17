from pathlib import Path
from database_asset import scan_folder, find_arma3_install, scan_arma3_base
from database_class import parse_class_hierarchy
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
from compare import compare_task_results
from report import save_comparison_report, print_comparison_summary

# Get logger for this module
logger = logging.getLogger(__name__)

@dataclass
class ScanTask:
    name: str
    mods_folder: Path
    mission_folder: Path
    ini_file_path: Path  # Changed from cpp_file_path

def get_task_hash(task) -> str:
    """Generate a hash for the task based on its configuration"""
    task_data = f"{task.mods_folder}_{task.mission_folder}"
    return hashlib.md5(task_data.encode()).hexdigest()

def initialize_vanilla_assets(cache_mgr: CacheManager) -> Set[str]:
    """Initialize vanilla assets, using cache if available"""
    # Try to get cached assets first
    vanilla_assets = cache_mgr.get_vanilla_assets()
    if (vanilla_assets is not None):
        logger.info(f"Loaded {len(vanilla_assets)} vanilla assets from cache")
        # Debug check for specific assets
        debug_assets = [
            'a3/ui_f/data/gui/cfg/communicationmenu/transport_ca.paa',
            'a3/ui_f/data/igui/cfg/weaponicons/mg_ca.paa'
        ]
        for asset in debug_assets:
            if asset not in vanilla_assets:
                logger.warning(f"Cached vanilla assets missing: {asset}")
        return vanilla_assets

    # If not cached, scan Arma 3 installation
    arma_path = find_arma3_install()
    if not arma_path:
        logger.error("Could not find Arma 3 installation")
        return set()

    # Enable debug logging temporarily for asset scanning
    asset_logger = logging.getLogger('database_asset')
    original_level = asset_logger.level
    asset_logger.setLevel(logging.DEBUG)

    try:
        logger.info("Scanning vanilla Arma 3 assets...")
        vanilla_assets = scan_arma3_base(arma_path, "vanilla", cache_mgr)
        
        # Cache the results for future use
        if vanilla_assets:
            cache_mgr.update_vanilla_assets(vanilla_assets, arma_path)
            logger.info(f"Cached {len(vanilla_assets)} vanilla assets")
        
        return vanilla_assets
    finally:
        # Restore original logging level
        asset_logger.setLevel(original_level)

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
        if not task.ini_file_path.exists():
            logger.error(f"Error: INIDBI2 file not found: {task.ini_file_path}")
            return False
        
        class_database = {}

        # Parse all entries at once using INIDBI2 parser
        logger.info(f"\nParsing INIDBI2 file: {task.ini_file_path}")
        try:
            class_database = parse_class_hierarchy(str(task.ini_file_path))
            if not class_database:
                logger.error("No classes extracted from INIDBI2 file")
                return False
                
            logger.info(f"Loaded classes from {len(class_database)} sources")
            
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
        write_debug_class_csv(class_database, output_folder, task.name)  # Changed to pass class_database instead of all_entries
        
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
                ini_file_path=Path(__file__).parent / "data" / "ConfigExtract_pcanext.ini"
            ),
            ScanTask(
                name="pca",
                mods_folder=Path(r"C:\pca"),
                mission_folder=Path(r"C:\pca_missions"),
                ini_file_path=Path(__file__).parent / "data" / "ConfigExtract_pca.ini"
            ),
        ]

        # Store task results for comparison
        task_results = {}
        
        for task in scan_tasks:
            logger.info(f"\nProcessing scan task: {task.name}")
            mission_reports = []
            if process_scan_task(task, cache_mgr, vanilla_assets, logger):
                task_results[task.name] = mission_reports
            else:
                logger.error(f"Failed to process task: {task.name}")
        
        # Compare results if we have multiple tasks
        if len(task_results) >= 2:
            task_names = list(task_results.keys())
            for i in range(len(task_names) - 1):
                for j in range(i + 1, len(task_names)):
                    task1_name = task_names[i]
                    task2_name = task_names[j]
                    
                    logger.info(f"\nComparing results: {task1_name} vs {task2_name}")
                    comparison_results = compare_task_results(
                        task1_name, task_results[task1_name],
                        task2_name, task_results[task2_name]
                    )
                    
                    print_comparison_summary(comparison_results)
                    save_comparison_report(comparison_results, task_name=f"{task1_name}_vs_{task2_name}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\nMission scanner finished.")

if __name__ == "__main__":
    main()
