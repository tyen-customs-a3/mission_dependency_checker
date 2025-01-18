import argparse
import sys
from pathlib import Path
from .core.validator import MissionValidator

def main():
    """
    Entry point for mission validation via CLI.
    Example usage: python -m mission_checker.cli --folder "path/to/mission"
    """
    parser = argparse.ArgumentParser(description="Validate a mission folder.")
    parser.add_argument("--folder", required=True, help="Path to the mission folder")
    parser.add_argument("--cache", default=".cache", help="Path to the cache directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")
    args = parser.parse_args()

    folder_path = Path(args.folder)
    if not folder_path.exists():
        print(f"Error: folder '{folder_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    cache_dir = Path(args.cache)
    validator = MissionValidator(cache_dir)
    warnings = validator.validate_mission_folder(folder_path)

    if warnings:
        print("Validation Warnings/Errors:")
        for w in warnings:
            print(f" - {w}")
        if args.strict:
            sys.exit(1)
    else:
        print("Mission folder validated successfully.")