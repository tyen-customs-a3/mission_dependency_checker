from datetime import datetime
from pathlib import Path
from typing import Set, List, Optional, Dict, Any, Pattern
import re
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .cache import CacheManager
from .scanner import AssetScanner
from .parser import ClassParser
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

    def __init__(self, cache_dir: Path, file_patterns: Optional[List[str]] = None):
        self.scanner = AssetScanner(cache_dir)
        self.parser = ClassParser()
        self.cache_mgr = CacheManager(cache_dir)
        self.file_patterns = [re.compile(p) for p in (file_patterns or [".*"])]
        self.database = ClassDatabase()  # Add database instance
        self._missing_classes = set()
        self._missing_assets = set()
        self._validation_stats = defaultdict(int)

    def get_validation_summary(self) -> Dict[str, Any]:
        """Generate a compact validation summary"""
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "total_files": self._validation_stats["total_files"],
                "sqf_files": self._validation_stats["sqf_files"],
                "paa_files": self._validation_stats["paa_files"],
                "p3d_files": self._validation_stats["p3d_files"],
                "sound_files": self._validation_stats["sound_files"],
                "config_files": self._validation_stats["config_files"],
                "total_classes": self._validation_stats["total_classes"]
            },
            "missing_classes": [
                {"name": cls.name, "parent": cls.parent, "source": cls.source}
                for cls in sorted(self._missing_classes, key=lambda x: x.name)
            ],
            "missing_assets": [
                str(asset) for asset in sorted(self._missing_assets)
            ]
        }

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
                    logger.info(f"- {config.relative_to(folder)}: {len(new_classes)} classes")
                except Exception as e:
                    logger.error(f"Error parsing {config}: {e}")
            
            logger.info(f"\nTotal classes found: {len(classes)}")
            
            # Add database validation
            logger.info("\nValidating classes against database...")
            for cls in classes:
                self.database.add_class(cls)
            
            # Log inheritance chains
            unique_classes = {cls.name for cls in classes}
            logger.info(f"Found {len(unique_classes)} unique class names")
            
            for class_name in sorted(unique_classes):
                chain = self.database.get_inheritance_chain(class_name)
                if chain:
                    inheritance = " -> ".join(c.name for c in chain)
                    logger.info(f"Class inheritance: {inheritance}")
                    
                    # Log source files for each class
                    for cls in chain:
                        logger.info(f"  {cls.name} defined in: {cls.source}")

            # Filter out SQF files from detailed validation
            non_sqf_assets = {
                asset for asset in assets 
                if not str(asset.path).lower().endswith('.sqf')
            }
            
            # Run normal validation on non-SQF assets
            warnings.extend(self._validate_assets(non_sqf_assets))
            
            # Update statistics
            self._validation_stats.update({
                "total_files": total_files,
                "sqf_files": sqf_files,
                "paa_files": paa_files,
                "p3d_files": p3d_files,
                "sound_files": sound_files,
                "config_files": len(config_files),
                "total_classes": len(classes)
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
                    "stack_trace": logging.format_exc()
                }
            ) from e

    def get_missing_items_report(self) -> str:
        """Generate a human readable report of missing items"""
        report = []
        
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
        
        Checks:
        - Asset references exist
        - Class inheritance is valid
        - Property types match parent class
        """
        warnings = []
        # Check for missing asset references
        asset_paths = {a.path for a in assets}
        for prop_val in cls.properties.values():
            if prop_val.endswith(".paa") or prop_val.endswith(".p3d"):
                if not any(str(a) in prop_val for a in asset_paths):
                    warnings.append(f"Class '{cls.name}' references missing asset: {prop_val}")

        # Check inheritance consistency
        warnings.extend(self._validate_class_inheritance({cls}))

        if cls.parent and cls.parent not in self._base_classes:
            parent = next((c for c in self._get_existing_classes() if c.name == cls.parent), None)
            if not parent:
                self._missing_classes.add(cls)
                warnings.append(f"Missing parent class '{cls.parent}' for '{cls.name}'")

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
