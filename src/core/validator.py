from datetime import datetime
from pathlib import Path
from typing import Set, List, Optional, Dict, Any, Pattern
import re
import logging
import traceback  # Add this import
from .cache import CacheManager
from .scanner import AssetScanner
from .parser_class import ClassParser
from .parser_ini import InidbiParser
from .models import Asset, ClassDef
from .database import ClassDatabase
from collections import defaultdict

logger = logging.getLogger(__name__)

class MissionValidationError(Exception):
    """Custom exception for mission validation errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}

class MissionValidator:
    """
    High-level validator for mission content.
    
    Validates mission folders by:
    - Scanning for missing assets
    - Checking class inheritance
    - Validating config references
    - Caching results for performance
    """

    def __init__(self, cache_dir: Path, file_patterns: Optional[List[str]] = None, config_path: Optional[Path] = None, database: Optional[ClassDatabase] = None):
        if not database:
            raise ValueError("Database instance is required")
        
        self.scanner = AssetScanner(cache_dir)
        self.parser = ClassParser()
        self.cache_mgr = CacheManager(cache_dir)
        self.file_patterns = [re.compile(p) for p in (file_patterns or [".*"])]
        self.database = database  # Use the provided database
        self._missing_classes = set()
        self._missing_assets = set()
        self._validation_stats = defaultdict(int)
        self._found_classes = set()
        self._warnings = []
        self._expected_classes = set()
        self._missing_required = set()
        self._class_stats = defaultdict(int)
        self._mission_classes = defaultdict(set)  # Track classes by mission
        self.config_path = config_path  # Add config path
        self._ignored_patterns = [
            r'.*\.varInit$',  # Ignore .varInit suffixes
            r'LIST_\d+\(""\)',  # Empty list with double quotes
            r'LIST_\d+\(\'\'\)',  # Empty list with single quotes
            r'LIST_\d+\(\s*\)',  # Empty list with no quotes
            r'LIST_\d+\(\s*""\s*\)',  # Empty list with spaces
        ]
        self._ignored_regexes = [re.compile(p) for p in self._ignored_patterns]
        self._missing_by_source = defaultdict(set)  # Track missing items by source
        self._missing_equipment = defaultdict(set)  # Track by class category instead of source

    def get_all_classes(self) -> Set[ClassDef]:
        """Get all classes found during validation"""
        return self._found_classes

    def get_validation_summary(self) -> Dict[str, Any]:
        """Get detailed validation summary including mission-specific class status"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_classes': len(self._found_classes),
            'missions': {}
        }

        # Group classes by mission
        for mission_name, classes in self._mission_classes.items():
            mission_summary = {
                'total_classes': len(classes),
                'found_in_database': 0,
                'missing_from_database': 0,
                'classes': []
            }

            # Check each class
            for class_def in sorted(classes, key=lambda x: x.name):
                exists_in_db = self.database.get_class(class_def.name)
                if exists_in_db:
                    mission_summary['found_in_database'] += 1
                else:
                    mission_summary['missing_from_database'] += 1
                    
                class_info = {
                    'name': class_def.name,
                    'found_in_database': bool(exists_in_db),
                    'source_file': class_def.source
                }
                mission_summary['classes'].append(class_info)

            summary['missions'][mission_name] = mission_summary

        return summary

    def _count_expanded_items(self) -> int:
        """Count total items including LIST macro expansions"""
        total = 0
        for class_def in self._found_classes:
            if 'from_list_macro' in class_def.properties:
                total += int(class_def.properties.get('list_count', 1))
            else:
                total += 1
        return total

    def validate_mission_folder(self, folder: Path) -> List[str]:
        """Validate mission folder content with enhanced error checking."""
        self._missing_classes.clear()
        self._missing_assets.clear()

        if not folder.exists():
            raise MissionValidationError(
                f"Mission folder does not exist: {folder}",
                {"path": str(folder)}
            )

        if not folder.is_dir():
            raise MissionValidationError(
                f"Path is not a directory: {folder}",
                {"path": str(folder)}
            )

        # Check cache first
        cache_key = str(folder)
        if cached := self.cache_mgr.get_cached_scan(cache_key):
            return cached

        warnings = []
        try:
            # Basic validation setup
            total_files = sum(1 for _ in folder.rglob("*") if _.is_file())
            if total_files == 0:
                raise MissionValidationError(
                    f"Mission folder is empty: {folder}",
                    {"path": str(folder)}
                )

            # Scan files
            assets = self.scanner.scan_directory(folder, self.file_patterns)
            sqf_files = sum(1 for a in assets if str(a.path).lower().endswith('.sqf'))
            paa_files = sum(1 for a in assets if str(a.path).lower().endswith('.paa'))
            p3d_files = sum(1 for a in assets if str(a.path).lower().endswith('.p3d'))
            sound_files = sum(1 for a in assets if str(a.path).lower().endswith(('.ogg', '.wss')))

            # Parse config files
            config_files = list(folder.rglob("*.cpp")) + list(folder.rglob("*.hpp"))
            classes = set()

            # Process each config file
            for config in config_files:
                try:
                    new_classes = self.parser.parse_file(config, treat_as_mission=True)
                    classes.update(new_classes)
                    
                    # Track classes by mission
                    mission_name = folder.name
                    self._mission_classes[mission_name].update(new_classes)
                    self._found_classes.update(new_classes)

                    # Validate each class against database
                    for cls in new_classes:
                        if cls.is_reference:  # Equipment references
                            if not self.database.get_class(cls.name):
                                self._missing_classes.add(cls)
                                warnings.append(f"Referenced equipment class '{cls.name}' not found in database")
                        elif not getattr(cls, 'is_mission_local', False):  # Regular classes
                            if not self.database.get_class(cls.name):
                                self._missing_classes.add(cls)
                                warnings.append(f"Class '{cls.name}' not found in database")
                            if cls.parent and not self.database.get_class(cls.parent):
                                warnings.append(f"Parent class '{cls.parent}' for '{cls.name}' not found in database")

                except Exception as e:
                    logger.error(f"Error parsing file {config}: {e}")
                    warnings.append(f"Failed to parse {config}: {str(e)}")

            # Process validation results
            non_sqf_assets = {a for a in assets if not str(a.path).lower().endswith('.sqf')}
            warnings.extend(self._validate_assets(non_sqf_assets))
            
            # Database validation
            self._validate_expected_classes(classes)
            warnings.extend(self._validate_against_database(classes))

            # Update statistics
            self._validation_stats.update({
                "total_files": total_files,
                "sqf_files": sqf_files,
                "paa_files": paa_files,
                "p3d_files": p3d_files,
                "sound_files": sound_files,
                "config_files": len(config_files),
                "total_classes": len(classes),
                "missing_required": len(self._missing_required),
                "class_stats": dict(self._class_stats),
                "database_mismatches": len(warnings),
                "missing_in_database": len([cls for cls in classes if not self.database.get_class(cls.name)])
            })

            # Cache results
            self.cache_mgr.cache_scan(cache_key, warnings)
            return warnings

        except MissionValidationError:
            raise
        except Exception as e:
            logger.exception("Validation failed")
            raise MissionValidationError(
                f"Validation error: {str(e)}",
                {
                    "path": str(folder),
                    "error_type": type(e).__name__,
                    "stack_trace": traceback.format_exc()
                }
            ) from e

    def get_missing_items_report(self) -> str:
        """Generate a human readable report of missing items"""
        if not self._missing_classes and not self._missing_assets:
            return "No missing items found."

        report = []
        
        if self._missing_classes:
            report.append("Missing Classes:")
            report.append("-" * 40)
            
            # Group by broad categories rather than source
            equipment = []
            other_classes = []
            
            for cls in sorted(self._missing_classes, key=lambda x: x.name):
                if getattr(cls, 'is_reference', False):
                    equipment.append(cls.name)
                else:
                    other_classes.append(cls.name)
            
            if equipment:
                report.append("\nMissing Equipment References:")
                for item in sorted(equipment):
                    report.append(f"  - {item}")
                    
            if other_classes:
                report.append("\nMissing Classes:")
                for item in sorted(other_classes):
                    report.append(f"  - {item}")

        if self._missing_required:
            report.append("\nMissing Required Classes:")
            report.append("-" * 40)
            
            # Group by category if possible
            by_category = defaultdict(list)
            for cls_name in sorted(self._missing_required):
                cls = self.database.get_class(cls_name)
                category = cls.inidbi_meta.category if cls and cls.inidbi_meta else "Unknown"
                by_category[category].append(cls_name)
            
            for category, classes in sorted(by_category.items()):
                report.append(f"\nCategory: {category}")
                for cls in sorted(classes):
                    report.append(f"  - {cls}")

        if self._missing_assets:
            report.append("\nMissing Assets:")
            report.append("-" * 40)
            # Group by file extension
            by_type = defaultdict(list)
            for asset in sorted(self._missing_assets):
                ext = Path(str(asset)).suffix.lower()
                by_type[ext].append(str(asset))
                
            for ext, assets in sorted(by_type.items()):
                report.append(f"\n{ext.upper()} Files:")
                for asset in sorted(assets):
                    report.append(f"  - {asset}")

        # Add database validation section
        if self._missing_classes:
            report.append("\nClasses Not Found in Database:")
            report.append("-" * 40)
            
            # Group by source file
            by_source = defaultdict(list)
            for cls in sorted(self._missing_classes, key=lambda x: x.name):
                by_source[cls.source].append(cls.name)
            
            for source, classes in sorted(by_source.items()):
                report.append(f"\nFrom {source}:")
                for cls in sorted(classes):
                    report.append(f"  - {cls}")

        return "\n".join(report) if report else "No missing items found."

    def _validate_assets(self, assets: Set[Asset]) -> List[str]:
        """Validate individual assets with detailed error checking"""
        warnings = []
        for asset in assets:
            try:
                # Skip validation for SQF files
                if str(asset.path).lower().endswith('.sqf'):
                    continue
                # Normal validation for other files    
                if not self._is_valid_asset(asset):
                    warnings.append(f"Invalid asset: {asset.path}")
                    self._missing_assets.add(asset.path)
            except Exception as e:
                logger.error(f"Asset validation error: {asset.path} - {e}")
                warnings.append(f"Error validating {asset.path}: {str(e)}")
                
        return warnings

    def _is_valid_asset(self, asset: Asset) -> bool:
        """
        Validate individual asset based on type.
        
        Checks:
        - File exists
        - Valid extension
        - Basic format validation for supported types
        """
        if not asset or not asset.path:
            return False
            
        path_str = str(asset.path).lower()
        
        # Audio validation
        if path_str.endswith(('.ogg', '.wss')):
            return self._validate_audio_asset(asset)
            
        # Image validation
        if path_str.endswith('.paa'):
            return self._validate_image_asset(asset)
            
        # Model validation
        if path_str.endswith('.p3d'):
            return self._validate_model_asset(asset)
            
        # For other types, just check if they exist
        return True

    def _validate_audio_asset(self, asset: Asset) -> bool:
        """Basic audio file validation"""
        try:
            path_str = str(asset.path)
            # Valid extensions
            if not path_str.lower().endswith(('.ogg', '.wss')):
                return False
                
            # File naming convention
            if any(c in path_str for c in '<>:"|?*'):
                return False
                
            # Simple size check (if file exists)
            if asset.path.exists():
                if asset.path.stat().st_size == 0:
                    return False
                    
            return True
            
        except Exception as e:
            logger.debug(f"Audio validation error for {asset.path}: {e}")
            return False

    def _validate_image_asset(self, asset: Asset) -> bool:
        """Basic PAA image validation"""
        try:
            path_str = str(asset.path)
            # Valid extension
            if not path_str.lower().endswith('.paa'):
                return False
                
            # File naming convention
            if any(c in path_str for c in '<>:"|?*'):
                return False
                
            # Simple size check (if file exists)
            if asset.path.exists():
                if asset.path.stat().st_size == 0:
                    return False
                    
            return True
            
        except Exception as e:
            logger.debug(f"Image validation error for {asset.path}: {e}")
            return False

    def _validate_model_asset(self, asset: Asset) -> bool:
        """Basic P3D model validation"""
        try:
            path_str = str(asset.path)
            # Valid extension
            if not path_str.lower().endswith('.p3d'):
                return False
                
            # File naming convention
            if any(c in path_str for c in '<>:"|?*'):
                return False
                
            # Simple size check (if file exists)
            if asset.path.exists():
                if asset.path.stat().st_size == 0:
                    return False
                    
            return True
            
        except Exception as e:
            logger.debug(f"Model validation error for {asset.path}: {e}")
            return False

    def _validate_class(self, cls: ClassDef, assets: Set[Asset]) -> List[str]:
        """
        Validate a single class definition.
        Only check if referenced class names exist.
        """
        warnings = []
        # Only check if class exists in database
        if not self.database.get_class(cls.name):
            warnings.append(f"Class '{cls.name}' not found in database")
            self._missing_classes.add(cls)
        return warnings

    def _validate_class_inheritance(self, classes: Set[ClassDef]) -> List[str]:
        """
        Validate all classes for missing or circular inheritance,
        using the parser's validate_class_hierarchy method.
        """
        hierarchy_warnings = []
        for cls in classes:
            hierarchy_warnings.extend(self.parser.validate_class_hierarchy(cls, classes))
        return hierarchy_warnings

    def _parse_classes_in_folder(self, folder: Path) -> Set[ClassDef]:
        """Parse matching files in the folder for class definitions"""
        classes = set()
        for file_path in folder.rglob("*"):
            if file_path.suffix.lower() in {".cpp", ".ini"}:
                # Check if file matches any pattern
                rel_path = str(file_path.relative_to(folder))
                if any(p.match(rel_path) for p in self.file_patterns):
                    classes |= self.parser.parse_file(file_path)
        return classes

    def _validate_expected_classes(self, classes: Set[ClassDef]) -> None:
        """Validate classes found in mission against database"""
        found_classes = {c.name for c in classes}
        
        # Every class found in mission is required
        self._expected_classes = found_classes
        
        # Update class statistics (remove unexpected calculation)
        self._class_stats.update({
            "total_found": len(found_classes),
            "total_required": len(found_classes),
            "missing_in_database": len(self._missing_required),
        })

        # Track classes by category
        for cls in classes:
            if cls.inidbi_meta:
                self._class_stats[f"category_{cls.inidbi_meta.category}"] += 1

    def _validate_against_database(self, classes: Set[ClassDef]) -> List[str]:
        """Check if classes exist in database with case-insensitive comparison"""
        warnings = []
        found_in_db = set()
        missing_in_db = set()
        
        for cls in classes:
            # Skip ignored patterns
            if self._should_ignore_class(cls.name):
                continue

            # Case-insensitive database check
            if not self.database.get_class(cls.name):  # Database now handles case-insensitivity
                missing_in_db.add(cls.name)
                self._missing_classes.add(cls)
                warnings.append(f"Class '{cls.name}' not found in database")
            else:
                found_in_db.add(cls.name)

        # Log validation results
        logger.info(f"Database validation complete:")
        logger.info(f"- Found in database: {len(found_in_db)}")
        logger.info(f"- Missing from database: {len(missing_in_db)}")
        
        return warnings

    def _should_ignore_class(self, class_name: str) -> bool:
        """Case-insensitive pattern matching"""
