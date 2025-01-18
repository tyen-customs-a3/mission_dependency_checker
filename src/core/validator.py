from datetime import datetime
from pathlib import Path
from typing import Set, List, Optional, Dict, Any, Pattern
import re
import logging
import traceback  # Add this import
from .cache import CacheManager
from .scanner import AssetScanner
from .parser import ClassParser, InidbiParser  # Add InidbiParser
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
            r'LIST_\d+\(""\)',  # Fix regex pattern for empty LIST macro
        ]
        self._ignored_regexes = [re.compile(p) for p in self._ignored_patterns]

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
                'classes': []
            }

            # Check each class
            found_count = 0
            missing_count = 0
            class_details = []

            for class_def in sorted(classes, key=lambda x: x.name):
                exists_in_db = self.database.get_class(class_def.name)
                class_info = {
                    'name': class_def.name,
                    'found_in_database': exists_in_db,
                    'source_file': class_def.source,
                }
                class_details.append(class_info)
                if exists_in_db:
                    found_count += 1
                else:
                    missing_count += 1

            mission_summary['classes'] = class_details
            mission_summary['found_in_database'] = found_count
            mission_summary['missing_from_database'] = missing_count

            summary['missions'][mission_name] = mission_summary

        summary['warnings'] = self._warnings
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
        """
        Validate mission folder content with enhanced error checking.
        
        Args:
            folder: Path to mission folder
            
        Returns:
            List of validation warnings/errors
            
        Raises:
            MissionValidationError: For validation-specific errors
            RuntimeError: For scanning/parsing errors
        """
        # Clear missing items at start of validation
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
            # Count files to validate
            total_files = sum(1 for _ in folder.rglob("*") if _.is_file())
            if total_files == 0:
                raise MissionValidationError(
                    f"Mission folder is empty: {folder}",
                    {"path": str(folder)}
                )
            
            logger.info(f"Found {total_files} total files to scan")

            # Scan folder
            assets = self.scanner.scan_directory(
                folder,
                self.file_patterns
            )
            
            # Count asset types
            sqf_files = sum(1 for a in assets if str(a.path).lower().endswith('.sqf'))
            paa_files = sum(1 for a in assets if str(a.path).lower().endswith('.paa'))
            p3d_files = sum(1 for a in assets if str(a.path).lower().endswith('.p3d'))
            sound_files = sum(1 for a in assets if str(a.path).lower().endswith(('.ogg', '.wss')))
            
            logger.info(f"Found assets: {len(assets)} total")
            logger.info(f"- {sqf_files} SQF scripts")
            logger.info(f"- {paa_files} PAA textures")
            logger.info(f"- {p3d_files} P3D models") 
            logger.info(f"- {sound_files} Sound files")
            
            # Parse config files
            logger.info("\nScanning config files...")
            config_files = list(folder.rglob("*.cpp")) + list(folder.rglob("*.hpp"))
            logger.info(f"Found {len(config_files)} config files")
            
            classes = set()
            for config in config_files:
                try:
                    new_classes = self.parser.parse_file(config)
                    classes.update(new_classes)
                    # Track classes by mission
                    mission_name = folder.name
                    self._mission_classes[mission_name].update(new_classes)
                    logger.info(f"- {config.relative_to(folder)}: {len(new_classes)} classes")
                except Exception as e:
                    logger.error(f"Error parsing {config}: {e}")
            
            logger.info(f"\nTotal classes found: {len(classes)}")
            
            # Add database validation (with reduced logging)
            logger.info("\nValidating classes against database...")
            logger.info("\nValidating classes against database...")
            unique_classes = {cls.name for cls in classes}
            logger.info(f"Found {len(unique_classes)} unique class names")
            
            # Filter out SQF files from detailed validation
            logger.info(f"Found {len(unique_classes)} unique class names")
            
            # Filter out SQF files from detailed validation
            non_sqf_assets = {
                asset for asset in assets 
                if not str(asset.path).lower().endswith('.sqf')
            }
            
            # Run normal validation on non-SQF assets
            warnings.extend(self._validate_assets(non_sqf_assets))
            
            # After parsing config files, check expected classes
            self._validate_expected_classes(classes)

            # After parsing config files, validate against database
            logger.info("\nValidating classes against database...")
            db_warnings = self._validate_against_database(classes)
            warnings.extend(db_warnings)

            # Update statistics with accurate counts
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
                "database_mismatches": len(db_warnings),
                "missing_in_database": len([cls for cls in classes if not self.database.get_class(cls.name)]),
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
                    "stack_trace": traceback.format_exc()  # Use traceback instead
                }
            ) from e

    def get_missing_items_report(self) -> str:
        """Generate a human readable report of missing items"""
        report = []
        
        # Add missing required classes section
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

        if self._missing_classes:
            report.append("\nMissing Classes:")
            report.append("-" * 40)
            # Group by parent class
            by_parent = defaultdict(list)
            for cls in sorted(self._missing_classes):
                parent = cls.parent if hasattr(cls, 'parent') else 'Unknown'
                by_parent[parent].append(cls.name if hasattr(cls, 'name') else str(cls))
                
            for parent, classes in sorted(by_parent.items()):
                report.append(f"\nExtending '{parent}':")
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
        """Check if classes exist in database, ignoring certain patterns"""
        warnings = []
        found_in_db = set()
        missing_in_db = set()
        
        logger.info(f"Starting database validation of {len(classes)} classes...")
        
        for cls in classes:
            # Skip ignored patterns
            if self._should_ignore_class(cls.name):
                logger.debug(f"Ignoring class: {cls.name}")
                continue

            exists = bool(self.database.get_class(cls.name))
            if exists:
                found_in_db.add(cls.name)
            else:
                missing_in_db.add(cls.name)
                warnings.append(f"Class '{cls.name}' from {cls.source} not found in database")
                
        # Add more detailed logging
        logger.info(f"Database validation complete:")
        logger.info(f"- Found in database: {len(found_in_db)}")
        logger.info(f"- Missing from database: {len(missing_in_db)}")
        if missing_in_db:
            logger.info("Missing classes:")
            for cls in sorted(missing_in_db):
                logger.info(f"  - {cls}")
                
        return warnings

    def _should_ignore_class(self, class_name: str) -> bool:
        """Check if class name matches any ignore patterns"""
        return any(pattern.match(class_name) for pattern in self._ignored_regexes)
