import os
import logging
from typing import List
from mission_dependency_scanner import MissionDependencyScanner
from database_asset import find_arma3_install, scan_arma3_base

logger = logging.getLogger(__name__)

def extract_mission_name(path: str) -> str:
    """Extract mission name from path like 'co40_last_mile.tem_chamw'"""
    base = os.path.basename(path)
    # Remove map name and get just the mission name part
    mission_name = base.split('.')[0]
    return mission_name

def scan_mission_folder(missions_root: str, class_database, asset_database, cache_mgr=None):
    """Scan multiple missions in the missions folder"""
    reports = []
    
    mission_folders = [
        d for d in os.listdir(missions_root) 
        if os.path.isdir(os.path.join(missions_root, d))
    ]
    
    for mission_folder in sorted(mission_folders):
        mission_path = os.path.join(missions_root, mission_folder)
        mission_name = extract_mission_name(mission_folder)

        scanner = MissionDependencyScanner(class_database, asset_database, mission_name)
        
        print(f"Scanning {mission_name}...")
        # Use the new scan_mission method instead of scanning individual files
        scanner.scan_mission(mission_path)
        reports.append(scanner)
    
    return reports