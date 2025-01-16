from database import scan_folder, parse_class_hierarchy, extract_classes_from_cpp
from mission_scanner import scan_mission_folder
from cache_manager import CacheManager
import os
from datetime import datetime
import logging

def save_report(mission_reports, output_dir="reports", include_found=False):
    """Save mission reports in clear text format"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"mission_report_{timestamp}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("MISSION SCANNER REPORT\n")
        f.write("====================\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for scanner in mission_reports:
            f.write(f"Mission: {scanner.mission_name}\n")
            f.write("=" * (len(scanner.mission_name) + 9) + "\n")
            
            if scanner.missing_classes:
                f.write("\nMissing Classes:\n")
                f.write("-" * 15 + "\n")
                for class_name in sorted(scanner.missing_classes):
                    f.write(f"  {class_name}\n")
            
            if scanner.missing_assets:
                f.write("\nMissing Assets:\n")
                f.write("-" * 14 + "\n")
                for asset in sorted(scanner.missing_assets):
                    f.write(f"  {asset}\n")
            
            if include_found:
                if scanner.found_classes:
                    f.write("\nFound Classes:\n")
                    f.write("-" * 13 + "\n")
                    by_source = {}
                    for class_name in sorted(scanner.found_classes):
                        source = next((mod for mod, entries in scanner.class_database.items() 
                                     if any(entry.name == class_name for entry in entries)), "unknown")
                        if source not in by_source:
                            by_source[source] = []
                        by_source[source].append(class_name)
                    
                    for source in sorted(by_source.keys()):
                        f.write(f"\n  {source}:\n")
                        for class_name in sorted(by_source[source]):
                            f.write(f"    {class_name}\n")
                
                if scanner.found_assets:
                    f.write("\nFound Assets:\n")
                    f.write("-" * 12 + "\n")
                    for asset in sorted(scanner.found_assets):
                        f.write(f"  {asset}\n")
            
            f.write("\n" + "=" * 60 + "\n\n")
    
    print(f"\nReport saved to: {output_file}")

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

def main():
    try:
        logger = logging.getLogger(__name__)
        logger.info("Starting mission scanner...")

        # Initialize cache manager and empty databases
        cache_mgr = CacheManager()
        class_database = {}
        asset_database = set()
        
        # Define paths
        mods_folder = r"C:\pcanext"
        mission_folder = r"C:\pca_missions"
        cpp_file_path = os.path.join(os.path.dirname(__file__), "classes", "classes_pcanext.cpp")
        cpp_file_path = r"C:\Users\Tyen\Desktop\outou\Tyen.vars.Arma3Profile.cpp"

        # Process the cpp file containing class data
        logger.info(f"\nScanning cpp file: {cpp_file_path}")
        class_entries_by_category = extract_classes_from_cpp(cpp_file_path)
        
        # Process entries and build class database by category
        class_database = {}
        for category, entries in class_entries_by_category.items():
            logger.info(f"Processing category: {category}")
            for entry in entries:
                class_entry = parse_class_hierarchy(entry)
                if not class_entry:
                    continue
                    
                for entry in class_entry.values():
                    if entry.source not in class_database:
                        class_database[entry.source] = set()
                    class_database[entry.source].add(entry)

        # Sort the class database alphabetically
        for source, entries in class_database.items():
            class_database[source] = sorted(entries, key=lambda x: x.name)

        # Print database summary
        logger.info("\nClass Database Summary:")
        for source, entries in class_database.items():
            logger.info(f"{source}: {len(entries)} classes")

        # Scan mods folder for assets
        if not os.path.exists(mods_folder):
            logger.error("Error: Mods folder does not exist!")
            return

        logger.info(f"\nScanning mods folder: {mods_folder}")
        asset_database = scan_folder(mods_folder)
        
        # Scan missions
        logger.info(f"\nScanning mission folder: {mission_folder}")
        mission_reports = scan_mission_folder(mission_folder, class_database, asset_database, cache_mgr)
        
        # Generate reports
        print_quick_summary(mission_reports)
        save_report(mission_reports, include_found=False)
        
    finally:
        print("\nMission scanner finished.")

if __name__ == "__main__":
    main()
