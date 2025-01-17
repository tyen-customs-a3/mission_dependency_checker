import os
import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from mission_dependency_scanner import MissionDependencyScanner
from database_asset import find_arma3_install, scan_arma3_base

logger = logging.getLogger(__name__)
print_lock = Lock()

def extract_mission_name(path: str) -> str:
    """Extract mission name from path like 'co40_last_mile.tem_chamw'"""
    base = os.path.basename(path)
    # Remove map name and get just the mission name part
    mission_name = base.split('.')[0]
    return mission_name

def scan_single_mission(mission_folder: str, missions_root: str, class_database, asset_database, cache_mgr=None):
    """Scan a single mission - helper function for parallel processing"""
    try:
        mission_path = os.path.join(missions_root, mission_folder)
        mission_name = extract_mission_name(mission_folder)

        scanner = MissionDependencyScanner(class_database, asset_database, mission_name)
        
        with print_lock:
            print(f"Scanning {mission_name}...")
        
        scanner.scan_mission(mission_path)
        return scanner
    except Exception as e:
        logger.error(f"Error scanning mission {mission_folder}: {e}")
        return None

def scan_mission_folder(missions_root: str, class_database, asset_database, cache_mgr=None, max_workers=4):
    """Scan multiple missions in the missions folder using parallel processing"""
    mission_folders = [
        d for d in os.listdir(missions_root) 
        if os.path.isdir(os.path.join(missions_root, d))
    ]
    
    reports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                scan_single_mission, 
                mission_folder, 
                missions_root, 
                class_database, 
                asset_database, 
                cache_mgr
            )
            for mission_folder in sorted(mission_folders)
        ]
        
        # Collect results as they complete
        for future in futures:
            try:
                scanner = future.result()
                reports.append(scanner)
            except Exception as e:
                logger.error(f"Mission scan failed: {e}")
    
    return reports