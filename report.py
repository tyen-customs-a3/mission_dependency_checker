import os
from datetime import datetime
import logging
from mission_dependency_scanner import MissionDependencyScanner

logger = logging.getLogger(__name__)

def save_report(mission_reports, output_dir="reports", include_found=False, task_name=""):
    """Save mission reports in clear text format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_folder = os.path.join(output_dir, f"{task_name}_{timestamp}" if task_name else f"default_{timestamp}")
    
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)
    
    output_file = os.path.join(task_folder, "mission_report.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"MISSION SCANNER REPORT - {task_name or 'Default'}\n")
        f.write("=" * (len(task_name) + 24) + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        passing_missions = []
        
        for scanner in mission_reports:
            if not scanner.missing_classes and not scanner.missing_assets:
                passing_missions.append(scanner.mission_name)
                continue
            
            f.write(f"Mission: {scanner.mission_name}\n")
            f.write("=" * (len(scanner.mission_name) + 9) + "\n")
            
            if scanner.missing_classes:
                f.write("Missing Classes:\n")
                for class_name in sorted(scanner.missing_classes):
                    f.write(f"  {class_name}\n")
            
            if scanner.missing_assets:
                f.write("Missing Assets:\n")
                for asset in sorted(scanner.missing_assets):
                    f.write(f"  {asset}\n")
            
            if include_found:
                if scanner.found_classes:
                    f.write("Found Classes:\n")
                    by_source = {}
                    for class_name in sorted(scanner.found_classes):
                        source = next((mod for mod, entries in scanner.class_database.items() 
                                     if any(entry.name == class_name for entry in entries)), "unknown")
                        if source not in by_source:
                            by_source[source] = []
                        by_source[source].append(class_name)
                    
                    for source in sorted(by_source.keys()):
                        f.write(f"  {source}:\n")
                        for class_name in sorted(by_source[source]):
                            f.write(f"    {class_name}\n")
                
                if scanner.found_assets:
                    f.write("Found Assets:\n")
                    for asset in sorted(scanner.found_assets):
                        f.write(f"  {asset}\n")
            
            f.write("=" * 60 + "\n")
        
        if passing_missions:
            f.write("\nPassing Missions:\n")
            f.write("=================\n")
            for mission in sorted(passing_missions):
                f.write(f"  {mission}\n")
    
    print(f"\nReport saved to: {output_file}")

    return task_folder, timestamp  # Return these for use with debug files

def print_quick_summary(mission_reports):
    """Print a quick summary of missing classes across all missions"""
    print("\nQUICK SUMMARY")
    print("=============")
    
    # Count total missing classes per mission
    for scanner in mission_reports:
        if scanner.missing_classes or scanner.missing_assets:
            print(f"\n{scanner.mission_name}:")
            if scanner.missing_classes:
                print(f"  Missing Classes: {len(scanner.missing_classes)}")
                for class_name in sorted(scanner.missing_classes):
                    print(f"    - {class_name}")
            if scanner.missing_assets:
                print(f"  Missing Assets: {len(scanner.missing_assets)}")
                for asset_path in sorted(scanner.missing_assets):
                    print(f"    - {asset_path}")
