# Mission Checker

A validation tool for Arma 3 mission content that detects missing dependencies, validates class hierarchies, and verifies assets.

## Features

- Scans and validates mission folders for missing or invalid assets
- Parses and validates class definitions and inheritance hierarchies
- Caches results for improved performance
- Supports INIDBI2 format class definitions
- Handles PBO archives and direct asset files
- Validates asset references in class configurations
- Efficient multi-threaded scanning with progress tracking

## Installation

```bash
git clone https://github.com/yourusername/mission_checker.git
cd mission_checker
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
python -m mission_checker.cli --folder "path/to/mission" [--cache ".cache"] [--strict]
```

Options:
- `--folder`: Path to mission folder (required)
- `--cache`: Path to cache directory (default: ".cache")
- `--strict`: Treat warnings as errors

### Programmatic Usage

```python
from pathlib import Path
from mission_checker.core.validator import MissionValidator

# Initialize validator
validator = MissionValidator(
    cache_dir=Path(".cache"),
    file_patterns=[
        r".*\.sqf$",
        r".*\.pbo$", 
        r".*\.(paa|p3d)$"
    ]
)

# Validate mission folder
warnings = validator.validate_mission_folder(Path("path/to/mission"))

if warnings:
    print("Validation warnings:")
    for warning in warnings:
        print(f"- {warning}")
```

## Project Structure

```
mission_checker/
├── src/
│   ├── core/
│   │   ├── validator.py    # High-level validation logic
│   │   ├── scanner.py      # Asset scanning
│   │   ├── parser.py       # Class definition parsing
│   │   ├── database.py     # Class database management
│   │   ├── cache.py        # Result caching
│   │   ├── models.py       # Data models
│   │   └── base_parser.py  # Base parsing functionality
│   ├── cli.py             # Command-line interface
│   └── check_mission.py   # Main validation script
└── README.md
```

## Components

### MissionValidator

High-level validator that coordinates:
- Asset scanning
- Class parsing and validation
- Cache management
- Error handling and reporting

### AssetScanner

Scans directories for:
- PBO archives
- Asset files (.paa, .p3d, etc.)
- SQF scripts
- Maintains file checksums
- Supports parallel processing

### ClassParser

Parses and validates:
- Class definitions
- Inheritance hierarchies
- Property definitions
- INIDBI2 format support
- Nested class structures

### CacheManager

Thread-safe caching system:
- SQLite-based storage
- Asset checksums
- Scan results
- Class definitions
- Automatic cache invalidation

## Error Handling

The validator provides detailed error information through:
- Structured warning messages
- Validation error details
- Runtime error tracking
- Logging system integration

## Requirements

- Python 3.8+
- SQLite 3
- Threading support
- Standard library modules
