from database import scan_folder
from mission_scanner import scan_mission_folder
import os
import json
from datetime import datetime

def save_report(mission_reports, output_dir="reports", include_found=False):
    """
    Save mission reports to JSON file
    include_found: If True, includes found classes in the report. If False, only missing classes are saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"mission_report_{timestamp}.json")
    
    report_data = {
        "timestamp": timestamp,
        "missions": []
    }
    
    for scanner in mission_reports:
        mission_data = {
            "name": scanner.mission_name,
            "missing_classes": sorted(list(scanner.missing_classes))
        }
        
        # Only include found classes if flag is set
        if include_found:
            mission_data["found_classes"] = {}
            for class_name in sorted(scanner.found_classes):
                for mod, entries in scanner.class_database.items():
                    if any(entry.name == class_name for entry in entries):
                        if mod not in mission_data["found_classes"]:
                            mission_data["found_classes"][mod] = []
                        mission_data["found_classes"][mod].append(class_name)
                        break
                    
        report_data["missions"].append(mission_data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)
        
    print(f"\nReport saved to: {output_file}")

def print_quick_summary(mission_reports):
    """Print a quick summary of missing classes across all missions"""
    print("\nQUICK SUMMARY")
    print("=============")
    
    # Count total missing classes per mission
    for scanner in mission_reports:
        if scanner.missing_classes:
            print(f"{scanner.mission_name}: {len(scanner.missing_classes)} missing classes")
            for class_name in sorted(scanner.missing_classes):
                print(f"  - {class_name}")

def main():
    # Scan mods folder first to build class database
    mods_folder = r"C:\pca_extracted"
    mission_folder = r"C:\pca_missions"

    if not os.path.exists(mods_folder):
        print("Error: Mods folder does not exist!")
        return

    print(f"\nScanning mods folder: {mods_folder}")
    class_database = scan_folder(mods_folder)
    
    print(f"\nScanning mission folder: {mission_folder}")
    mission_reports = scan_mission_folder(mission_folder, class_database)
    
    # Print quick summary before detailed report
    print_quick_summary(mission_reports)
    
    print("\nMISSION ANALYSIS REPORT")
    print("=====================")
    
    # Save report to disk - set include_found=True if you want to include found classes
    save_report(mission_reports, include_found=False)

if __name__ == "__main__":
    main()
