import re
import os
from typing import Set, Dict
from database_class import ClassEntry
import logging

logger = logging.getLogger(__name__)

class MissionDependencyScanner:
    def __init__(self, class_database: Dict[str, Set[ClassEntry]], 
                 asset_database: Set[str],
                 mission_name: str):
        self.class_database = class_database
        self.mission_name = mission_name
        self.asset_database = asset_database
        
        # Track mission-specific data
        self.mission_classes = set()  # Just track class names defined in mission
        self.class_references = set()  # All referenced classes
        self.missing_classes = set()
        self.found_classes = set()
        
        # Create set of all known mod classes
        self.all_mod_classes = {
            entry.class_name 
            for entries in class_database.values() 
            for entry in entries
        }

        # Common classes to ignore
        self.ignore_classes = {
            'true', 'false', 'nil', 'null', 'obj', 'player', 'this',
            'itemMap', '#lightpoint', '#particlesource',
            'baseMan', 'rm', 'crew',
            'CfgPatches', 'CfgFunctions', 'CfgVehicles'
        }

        # Add back asset tracking
        self.missing_assets = set()
        self.found_assets = set()
        self.all_assets = asset_database

    def scan_mission(self, mission_path: str):
        """Scan entire mission folder"""
        # First pass: Find mission-defined classes from loadouts
        for root, _, files in os.walk(mission_path):
            for file in files:
                if 'loadout' in file.lower() and file.endswith(('.hpp', '.cpp')):
                    self._scan_loadout_file(os.path.join(root, file))

        # Second pass: Find all class references
        for root, _, files in os.walk(mission_path):
            for file in files:
                if file.endswith(('.hpp', '.cpp', '.sqf')):
                    if 'loadout' not in file.lower():
                        self._scan_file_for_references(os.path.join(root, file))

        # Analyze dependencies
        self._analyze_dependencies()

    def _scan_loadout_file(self, file_path: str):
        """Extract class definitions from loadout files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple class definition pattern
            class_pattern = r'class\s+(\w+)'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                if class_name not in self.ignore_classes:
                    self.mission_classes.add(class_name)

            # Also scan for equipment references
            self._extract_config_references(content)

        except Exception as e:
            logger.error(f"Error scanning loadout file {file_path}: {e}")

    def _scan_file_for_references(self, file_path: str):
        """Scan for class references and assets in mission files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract class references
            if file_path.endswith('.sqf'):
                self._extract_sqf_references(content)
            else:
                self._extract_config_references(content)

            # Extract and check assets
            asset_paths = self._extract_asset_paths(content)
            for path in asset_paths:
                if path in self.all_assets:
                    self.found_assets.add(path)
                else:
                    self.missing_assets.add(path)

        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")

    def _extract_sqf_references(self, content: str):
        """Extract class references from SQF code"""
        patterns = [
            r'createVehicle\s*\[\s*["\']([^"\']+)["\']',
            r'createUnit\s*\[\s*["\']([^"\']+)["\']',
            r'typeOf\s+\w+\s*==\s*["\']([^"\']+)["\']',
            r'add(?:Weapon|Magazine|Item|Backpack|Uniform|Vest|Goggles|Headgear)\s*["\']([^"\']+)["\']'
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                class_name = match.group(1)
                if class_name not in self.ignore_classes:
                    self.class_references.add(class_name)

    def _extract_config_references(self, content: str):
        """Extract class references from config/loadout files"""
        # First handle array assignments
        patterns = [
            r'(?:uniform|vest|backpack|headgear|goggles|primaryWeapon|secondaryWeapon|sidearmWeapon)\[\]\s*=\\s*\{([^}]+)\}',
            r'(?:magazines|items|linkedItems)\[\]\s*=\s*\{([^}]+)\}'
        ]

        # Helper to validate class names
        def is_valid_class_name(name: str) -> bool:
            # Filter out syntax elements and other non-class strings
            invalid_patterns = [
                r'^LIST_\d+$',                  # LIST_2 macro name
                r'^[,\(\)\[\]\{\}]+$',          # Pure syntax
                r'^$',                          # Empty string
                r'^[\d\.]+$',                   # Pure numbers
                r'default',                     # Common config keyword
                r'^traits$'                     # Loadout section header
            ]
            return not any(re.match(p, name) for p in invalid_patterns)

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                values = match.group(1)
                
                # Handle LIST_X macros first
                list_matches = re.finditer(r'LIST_\d+\(["\']([^"\']+)["\']\)', values)
                for list_match in list_matches:
                    class_name = list_match.group(1)
                    if class_name not in self.ignore_classes and is_valid_class_name(class_name):
                        self.class_references.add(class_name)
                
                # Then handle regular quoted strings, excluding those in LIST macros
                class_names = re.findall(r'["\']([^"\']+)["\']', values)
                for class_name in class_names:
                    if (class_name not in self.ignore_classes 
                        and not class_name.startswith('LIST_') 
                        and is_valid_class_name(class_name)):
                        self.class_references.add(class_name)

        # Also scan for direct LIST_X references outside arrays
        list_pattern = r'LIST_\d+\(["\']([^"\']+)["\']\)'
        for match in re.finditer(list_pattern, content):
            class_name = match.group(1)
            if class_name not in self.ignore_classes and is_valid_class_name(class_name):
                self.class_references.add(class_name)

    def _extract_asset_paths(self, content: str) -> Set[str]:
        """Extract asset paths from file content"""
        asset_paths = set()
        
        # Common asset path patterns
        patterns = [
            r'[/\\][a-z0-9_/\\]+\.p3d\b',  # 3D models 
            r'[/\\][a-z0-9_/\\]+\.paa\b',  # Textures
            r'[/\\][a-z0-9_/\\]+\.wss\b',  # Sounds
            r'[/\\][a-z0-9_/\\]+\.ogg\b',  # Sounds
            r'[/\\][a-z0-9_/\\]+\.wav\b',  # Sounds
            r'[/\\][a-z0-9_/\\]+\.jpg\b',  # Images
            r'[/\\][a-z0-9_/\\]+\.png\b'   # Images
        ]
        
        # Extract paths using patterns
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                path = match.group(0).lower().replace('\\', '/').lstrip('/')
                asset_paths.add(path)
        
        return asset_paths

    def _analyze_dependencies(self):
        """Check class references against mission and mod databases"""
        for class_name in self.class_references:
            if class_name in self.mission_classes:
                continue
            if class_name in self.all_mod_classes:
                self.found_classes.add(class_name)
            else:
                self.missing_classes.add(class_name)

    def print_report(self):
        """Print analysis results"""
        print(f"\nMission Analysis: {self.mission_name}")
        print("=" * 50)
        
        print("\nMission-defined Classes:")
        for class_name in sorted(self.mission_classes):
            print(f"  {class_name}")
            
        print("\nMissing Classes:")
        for class_name in sorted(self.missing_classes):
            print(f"  {class_name}")
            similar = [c for c in self.all_mod_classes if class_name.lower() in c.lower()][:3]
            if similar:
                print("    Similar classes found:")
                for s in similar:
                    print(f"    - {s}")

        print("\nFound Classes:")
        for class_name in sorted(self.found_classes):
            for mod_name, entries in self.class_database.items():
                if any(entry.class_name == class_name for entry in entries):
                    print(f"  {class_name} [{mod_name}]")
                    break

        print("\nMissing Assets:")
        for asset in sorted(self.missing_assets):
            print(f"  {asset}")

        print("\nStatistics:")
        print(f"  Mission Classes: {len(self.mission_classes)}")
        print(f"  Missing Classes: {len(self.missing_classes)}")
        print(f"  Found Classes: {len(self.found_classes)}")
        print(f"  Missing Assets: {len(self.missing_assets)}")
