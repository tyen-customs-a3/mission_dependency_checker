import os
import sys
from pathlib import Path
import argparse

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.database import ClassDatabase
from src.core.validator import MissionValidator, MissionValidationError
from src.core.parser_ini import InidbiParser
import logging
from typing import Optional, Dict, Any
import sys
from datetime import datetime
import yaml

def validate_paths(paths: Dict[str, Path]) -> Optional[str]:
    """Validate all required paths exist"""
    missing = []
    for name, path in paths.items():
        if not path.exists():
            missing.append(f"{name}: {path}")
    return "\n- ".join(missing) if missing else None

def log_error(error: MissionValidationError, log_file: str) -> None:
    """Log detailed error information"""
    logger = logging.getLogger(__name__)
    logger.error(f"Validation failed: {str(error)}")
    
    if error.details:
        logger.error("Error details:")
        for key, value in error.details.items():
            logger.error(f"  {key}: {value}")

def validate_ini_file(ini_path: Path) -> Optional[str]:
    """Validate INIDBI config file"""
    try:
        if not ini_path.exists():
            return f"INIDBI config file not found: {ini_path}"
            
        parser = InidbiParser()
        classes = parser.parse_file(ini_path)
        
        if not classes:
            return "No classes found in INIDBI config file"
            
        logging.info(f"\nINIDB Config Analysis:")
        logging.info(f"Found {len(classes)} base class definitions")
        
        return None
        
    except Exception as e:
        return f"Error parsing INIDBI config: {str(e)}"

def write_validation_report(validator: MissionValidator, mission_path: Path) -> Path:
    """Write enhanced validation report to disk"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    mission_name = mission_path.name
    report_path = report_dir / f"validation_{mission_name}_{timestamp}.txt"
    
    # Generate human readable report
    with open(report_path, 'w') as f:
        # Write header
        f.write("Mission Validation Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Mission: {mission_name}\n\n")

        summary = validator.get_validation_summary()
        
        # Write overall statistics
        f.write("Overall Statistics\n")
        f.write("-" * 20 + "\n")
        total_classes = sum(m['total_classes'] for m in summary['missions'].values())
        total_found = sum(m['found_in_database'] for m in summary['missions'].values())
        total_missing = sum(m['missing_from_database'] for m in summary['missions'].values())
        
        f.write(f"Total Classes Found: {total_classes}\n")
        f.write(f"Found in Database: {total_found}\n")
        f.write(f"Missing from Database: {total_missing}\n\n")

        # Write per-mission details
        f.write("Mission Details\n")
        f.write("-" * 20 + "\n")
        
        for mission_name, mission_data in sorted(summary['missions'].items()):
            f.write(f"\n{mission_name}:\n")
            f.write(f"  Classes Found: {mission_data['total_classes']}\n")
            f.write(f"  Validated: {mission_data['found_in_database']}\n")
            f.write(f"  Missing: {mission_data['missing_from_database']}\n")
            
            if mission_data['missing_from_database'] > 0:
                f.write("\n  Missing Classes:\n")
                for cls in sorted(c['name'] for c in mission_data['classes'] if not c['found_in_database']):
                    f.write(f"    - {cls}\n")
            f.write("\n")

        # Write warnings section if any
        if summary.get('warnings'):
            f.write("\nWarnings\n")
            f.write("-" * 20 + "\n")
            for warning in sorted(summary['warnings']):
                f.write(f"! {warning}\n")

        # Write missing equipment section
        missing_report = validator.get_missing_items_report()
        if missing_report != "No missing items found.":
            f.write("\n")
            f.write(missing_report)
            f.write("\n")

    # Also write machine-readable YAML version
    yaml_path = report_path.with_suffix('.yml')
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(summary, f)

    return report_path

def main():
    # Add argument parsing
    parser = argparse.ArgumentParser(description="Check mission files for required classes")
    parser.add_argument("--mission", default=r"C:\pca_missions", help="Path to mission folder")
    parser.add_argument("--mods", default=r"C:\pcanext", help="Path to mods folder")
    parser.add_argument("--config", help="Path to INIDBI config file", 
                       default=str(Path(__file__).parent.parent / "data" / "ConfigExtract_pcanext.ini"))
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('mission_checker.log')
        ]
    )

    # Paths configuration
    paths = {
        "Mods": Path(args.mods),
        "Missions": Path(args.mission),
        "Config": Path(args.config)
    }
    cache_dir = Path(__file__).parent.parent / ".cache"

    # Validate paths
    if missing := validate_paths(paths):
        print("Error: Required paths do not exist:\n-", missing)
        sys.exit(1)

    # Validate INIDBI config
    if error := validate_ini_file(paths["Config"]):
        print(f"Config validation error: {error}")
        sys.exit(1)

    # Correct database population
    print("\nBuilding class database from config...")
    database = ClassDatabase()
    if paths["Config"].exists():
        ini_parser = InidbiParser()
        classes_by_source = ini_parser.parse_file(paths["Config"])
        total_classes = 0
        for source, class_set in classes_by_source.items():
            for cls in class_set:
                database.add_class(cls)
                total_classes += 1
        print(f"Loaded {total_classes} total classes from {len(classes_by_source)} sources")
    else:
        print("Warning: No config file found, database will be empty")

    # Initialize validator with the populated database
    validator = MissionValidator(
        cache_dir=cache_dir,
        file_patterns=[r".*\.sqf$", r".*\.pbo$", r".*\.(paa|p3d)$"],
        config_path=paths["Config"],
        database=database  # Pass our pre-populated database
    )

    print(f"\nValidating missions in: {paths['Missions']}")
    print(f"Using mod config from: {paths['Config']}")
    print(f"Looking for mods in: {paths['Mods']}")
    print("-" * 60)

    try:
        print("\nScanning mission folder...")
        warnings = validator.validate_mission_folder(paths["Missions"])
        
        # Write full report to disk
        report_path = write_validation_report(validator, paths["Missions"])
        print(f"\nDetailed report written to: {report_path}")
        
        # Show class analysis
        print("\nClass Analysis:")
        print("-" * 60)
        print(f"Total classes found: {len(validator.get_all_classes())}")
        
        # Show validation issues if any
        if warnings:
            print("\nValidation Issues:")
            print("-" * 60)
            
            # Show missing items report
            missing_report = validator.get_missing_items_report()
            if missing_report != "No missing items found.":
                print(missing_report)

            return len(warnings)
            
        print("\n✓ No validation issues found")
        return 0

    except MissionValidationError as e:
        print(f"\nError: {str(e)}")
        print(f"Check {report_path} for details")
        return 1
        
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        print(f"Check {report_path} for details")
        return 2

if __name__ == "__main__":

    sys.exit(main())
