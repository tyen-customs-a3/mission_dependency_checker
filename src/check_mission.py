from pathlib import Path
from core.validator import MissionValidator, MissionValidationError
from core.parser import InidbiParser  # Add this import
import logging
from typing import Optional, Dict, Any
import sys
import json
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
        
        # Count classes by category
        categories = {}
        for cls in classes:
            if hasattr(cls, 'inidbi_meta') and cls.inidbi_meta:
                cat = cls.inidbi_meta.category
                categories[cat] = categories.get(cat, 0) + 1
                
        for cat, count in sorted(categories.items()):
            logging.info(f"- {cat}: {count} classes")
            
        return None
        
    except Exception as e:
        return f"Error parsing INIDBI config: {str(e)}"

def write_validation_report(validator: MissionValidator, mission_path: Path) -> Path:
    """Write validation report to disk"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    # Generate report filename from mission name
    mission_name = mission_path.name
    report_path = report_dir / f"validation_{mission_name}_{timestamp}.yml"
    
    # Get validation summary
    summary = validator.get_validation_summary()
    
    # Write YAML report
    with open(report_path, 'w') as f:
        yaml.safe_dump(summary, f, default_flow_style=False, sort_keys=False)
        
    return report_path

def main():
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
        "Mods": Path(r"C:\pcanext_test"),
        "Missions": Path(r"C:\pca_missions_quick"),
        "Config": Path(__file__).parent.parent / "data" / "ConfigExtract_pcanext.ini"
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

    # Initialize validator
    validator = MissionValidator(
        cache_dir=cache_dir,
        file_patterns=[
            r".*\.sqf$",
            r".*\.pbo$",
            r".*\.(paa|p3d)$"
        ]
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
        
        # Only show issues in terminal
        if not warnings:
            print("\n✓ No validation issues found")
            return 0
            
        print("\nValidation Issues:")
        print("-" * 60)
        
        # Get missing items report
        missing_report = validator.get_missing_items_report()
        if missing_report != "No missing items found.":
            print(missing_report)
            
        # Only show critical warnings that aren't about missing items
        critical_warnings = [
            w for w in warnings 
            if not any(x in w.lower() for x in ["missing", "not found", "undefined"])
        ]
        
        if critical_warnings:
            print("\nOther Issues:")
            print("-" * 60)
            for warning in sorted(critical_warnings):
                print(f"! {warning}")
        
        return len(warnings)

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
