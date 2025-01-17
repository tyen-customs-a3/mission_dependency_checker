import re
import os
from typing import Set, Dict, Tuple, Optional
from database_class import ClassEntry
from database_asset import scan_for_assets
import logging

logger = logging.getLogger(__name__)

class MissionDependencyScanner:
    def __init__(self, class_database: Dict[str, Set[ClassEntry]], 
                 asset_database: Set[str],  # Change from Dict to Set
                 mission_name: str):
        self.class_database = class_database
        self.asset_database = asset_database.copy()  # Create a copy to add mission-local assets
        self.mission_name = mission_name
        # Create a flat set of all class names for direct lookup
        self.all_classes = {
            entry.class_name 
            for entries in class_database.values() 
            for entry in entries
        }
        # Add default classes
        self.default_classes = {
            'itemMap',
            '#lightpoint',
            '#particlesource'
        }
        self.all_classes.update(self.default_classes)
        
        self.missing_classes = set()
        self.found_classes = set()
        self.missing_assets = set()
        self.found_assets = set()
        self.mission_classes = set()

        # Add ai-related classes to skip
        self.skip_classes = {
            'ai',
            'ai_action',
            'ai_attribute', 
            'ai_cache',
            'ai_common',
            'ai_data',
            'ai_spawn',
            'ai_task',
            'pca',
            'common',
            'player_eh',
            'player_jip',
            'player_loadout',
            'CfgBuildings',
            'CfgLootSettings',
            'CfgLootTables',
            'coverMapLocal',
            'player_coverMapLocal',

            'backpacks',
            'uniforms',
            'vests',
            'mission',
            'defaults',
        }
        
        # Add prefixes of class names to ignore (stored in lowercase)
        self.ignore_prefixes = {
            prefix.lower() for prefix in {
                'Rcs',   # Resource selection system classes
                'CBA_',  # CBA mod classes
                'ctrl',  # UI control classes
            }
        }
        
        # Add common loadout base classes to skip
        self.loadout_base_classes = {
            'baseMan', 'rm', 'crew'
        }
        
        # Add common role classes to skip checking
        self.role_classes = {
            'rm', 'ar', 'aar', 'rat', 'dm', 'mmg', 'mmga', 'hmg', 'hmga',
            'mat', 'mata', 'hat', 'hata', 'mtr', 'mtrag', 'sam', 'samag',
            'sl', 'ft', 'tl', 'co', 'xo', 'sn', 'sp', 'vc', 'vd', 'vg',
            'pp', 'pcc', 'pc', 'eng', 'engm', 'uav', 'div', 'cls', 'pil',
            'fac', 'ar_c', 'crew_c', 'r_c', 'rm_lat', 'rm_fa'
        }

        # Add prefixes of variables to ignore in configs
        self.config_vars = {
            'GUI_',         # GUI variables like GUI_BCG_RGB_R
            'IGUI_',       # Interface GUI variables
            'SafeZone',    # SafeZone variables
            'pixel',       # pixel sizing variables
            'safezone'     # lowercase variants
            'ai'           # AI variables
        }

        # Add nested class prefixes to ignore
        self.nested_ignore_prefixes = {
            'ai',     # AI function categories
            'pca',    # PCA mod functions
            'player', # Player related functions
        }
        
        # Scan mission folder for assets and add them to the database
        mission_assets = scan_for_assets(mission_name)
        self.asset_database.update(mission_assets)

        # Build inheritance maps
        self.parent_map = {}  # Direct parent lookup: child -> parent
        self.inheritance_tree = {}  # Full inheritance chain: class -> set(all ancestors)
        
        # Build initial parent map from mod database including all relationships
        for entries in class_database.values():
            for entry in entries:
                if entry.parent:
                    self.parent_map[entry.class_name] = entry.parent
        
        # Build complete inheritance tree
        self._build_inheritance_tree()

    def _build_inheritance_tree(self):
        """Build complete inheritance tree for all known classes"""
        self.inheritance_tree.clear()
        
        def get_all_parents(class_name: str, visited: set) -> set:
            """Recursively get all parent classes"""
            if class_name in visited:  # Prevent infinite recursion
                return set()
                
            visited.add(class_name)
            all_parents = set()
            
            # Get direct parent first
            parent = self.parent_map.get(class_name)
            if parent:
                all_parents.add(parent)
                # Get all parents of this parent
                parent_ancestors = get_all_parents(parent, visited)
                all_parents.update(parent_ancestors)
                
            return all_parents

        # Process each class to build its complete inheritance chain
        for class_name in list(self.parent_map.keys()):
            if class_name not in self.inheritance_tree:
                self.inheritance_tree[class_name] = get_all_parents(class_name, set())

    def _get_all_parents(self, class_name: str, visited: set) -> set:
        """Recursively get all parent classes including indirect ancestors"""
        if class_name in self.inheritance_tree:
            return self.inheritance_tree[class_name]
            
        if class_name in visited:  # Prevent infinite recursion
            return set()
            
        visited.add(class_name)
        parents = set()
        
        # Add direct parent
        parent = self.parent_map.get(class_name)
        if parent:
            parents.add(parent)
            # Add parent's ancestors recursively
            parents.update(self._get_all_parents(parent, visited))
        
        self.inheritance_tree[class_name] = parents
        return parents

    def _update_inheritance(self, new_classes: Dict[str, str]):
        """Update inheritance info with newly discovered classes"""
        # Add new parent relationships
        self.parent_map.update(new_classes)
        
        # Update class paths with new relationships
        for child, parent in new_classes.items():
            path = f"{parent}/{child}"
            self.class_paths.add(path)
            
        # Rebuild entire inheritance tree to include new relationships
        self._build_inheritance_tree()
        
        # Also update the all_classes set with new valid classes
        self.all_classes.update(
            name for name, parent in new_classes.items() 
            if not self._should_ignore_class(name)
        )

    def is_loadout_file(self, file_path: str) -> bool:
        """Check if file is a loadout configuration"""
        return 'loadout' in file_path.lower() and file_path.endswith(('.hpp', '.cpp'))

    def _has_ignored_parent(self, class_name: str, visited=None) -> bool:
        """Recursively check if any parent class should be ignored"""
        if visited is None:
            visited = set()
        
        if class_name in visited:  # Prevent infinite recursion on circular dependencies
            return False
        visited.add(class_name)
        
        # Check if this class should be ignored
        if self._should_ignore_class(class_name):
            return True
            
        # Check parent class if it exists
        current = class_name
        while current in self.parent_map:
            parent = self.parent_map[current]
            if parent in visited:  # Handle circular dependencies
                break
            if self._should_ignore_class(parent):
                return True
            current = parent
            visited.add(current)
            
        return False

    def _should_ignore_class(self, class_name: str) -> bool:
        """Check if class should be ignored based on name or inheritance"""
        class_name_lower = class_name.lower()

        # Quick check for direct matches in skip classes
        if class_name_lower in {name.lower() for name in self.skip_classes}:
            return True

        # Check prefixes
        if any(class_name_lower.startswith(prefix) for prefix in self.ignore_prefixes):
            return True
        if any(class_name_lower.startswith(prefix) for prefix in self.nested_ignore_prefixes):
            return True

        # Check inheritance
        if class_name in self.inheritance_tree:
            parents = self.inheritance_tree[class_name]
            # Check if any parent should be ignored
            for parent in parents:
                parent_lower = parent.lower()
                if parent_lower in {name.lower() for name in self.skip_classes}:
                    return True
                if any(parent_lower.startswith(prefix) for prefix in self.ignore_prefixes):
                    return True
                if any(parent_lower.startswith(prefix) for prefix in self.nested_ignore_prefixes):
                    return True

        return False

    def _is_config_value_context(self, content: str, start_pos: int) -> bool:
        """Check if position is within a config value context like colorFrame[] = {...}"""
        # Look backwards for common config array markers
        line_start = content.rfind('\n', 0, start_pos) + 1
        line = content[line_start:start_pos].strip().lower()
        config_markers = ['color', 'rgb', 'rgba', 'size', 'scale', 'offset', 'getvariable']
        return any(marker in line for marker in config_markers)

    def extract_class_names(self, content: str, is_loadout: bool = False) -> Set[str]:
        """Extract potential class names from content"""
        class_names = set()
        new_inheritance = {}
        
        # First scan for class definitions in mission
        class_def_pattern = r'class\s+(\w+)(?:\s*:\s*(\w+))?'
        for match in re.finditer(class_def_pattern, content):
            class_name = match.group(1)
            parent = match.group(2)
            
            # Add to mission-defined classes
            self.mission_classes.add(class_name)
            
            # Handle inheritance if present
            if parent and not self._should_ignore_class(parent):
                class_names.add(parent)
                new_inheritance[class_name] = parent

        # Extract all inheritance relationships first
        inheritance_pattern = r'class\s+(\w+)\s*:\s*(\w+)'
        for match in re.finditer(inheritance_pattern, content):
            child = match.group(1)
            parent = match.group(2)
            if not self._should_ignore_class(parent):  # Only add if parent isn't ignored
                class_names.add(child)
                class_names.add(parent)
                new_inheritance[child] = parent

        # Update inheritance data before continuing
        if new_inheritance:
            self._update_inheritance(new_inheritance)

        # Continue with rest of extraction
        if is_loadout:
            # Extract equipment classes from arrays
            array_pattern = r'(?:uniform|vest|backpack|headgear|goggles|primaryWeapon|secondaryWeapon|sidearmWeapon)\[\]\s*=\\s*[\[{]([^}\]]+)[\]}]'
            for match in re.finditer(array_pattern, content):
                values = match.group(1)
                class_names.update(re.findall(r'["\']([A-Za-z0-9_]+)(?:\[[^\]]+\])?["\']', values))
        else:
            # Process non-loadout files
            # Remove traits sections first
            traits_pattern = r'traits\[\]\s*=\\s*\{[^}]*\}'
            content = re.sub(traits_pattern, '', content)
            
            # Extract quoted strings that could be class names
            direct_pattern = r'["\']([A-Za-z0-9_]+)(?:\[[^\]]+\])?["\']'
            for match in re.finditer(direct_pattern, content):
                if not self._is_config_value_context(content, match.start()):
                    class_names.add(match.group(1))
            
            # Look for array assignments
            array_pattern = r'(?:(\w+)\[\]|\b_item\w+)\s*=\\s*[\[{]([^}\]]+)[\]}]'
            for match in re.finditer(array_pattern, content):
                if match.group(1) and not ('traits' in match.group(1) or 'arsenal' in match.group(1).lower()):
                    values = match.group(2)
                    class_names.update(re.findall(r'["\']([A-Za-z0-9_]+)(?:\[[^\]]+\])?["\']', values))
            
            # Look for direct class definitions
            class_pattern = r'class\s+(\w+)'
            matches = re.findall(class_pattern, content)
            class_names.update(matches)
            
        # Filter ignored classes using updated inheritance tree
        return {name for name in class_names if not self._should_ignore_class(name)}

    def extract_sqf_class_names(self, content: str) -> Set[str]:
        """Extract class names from SQF scripting files"""
        class_names = set()
        
        # Skip these as they are common variable names or engine entities, not classes
        skip_names = {
            '_vehicleType',
            '_className',
            '_type',
            '_class',
            'arsenal',
            'itemMap',  # Always exists
            '#lightpoint',  # Engine entity
            '#particlesource',  # Engine entity
            'building'  # Common vehicle type
        }
        
        # Common SQF patterns that reference classes
        patterns = [
            r'typeOf\s+[_a-zA-Z0-9]+\s*==\s*["\']([^"\']+)["\']',  # typeOf _unit == "ClassName"
            r'createVehicle\s*\[["\']([^"\']+)["\']',  # createVehicle ["ClassName",...
            r'createUnit\s*\[["\']([^"\']+)["\']',     # createUnit ["ClassName",...
            r'([A-Za-z0-9_]+)\s*createVehicle',        # "ClassName" createVehicle
            r'addWeapon\s*["\']([^"\']+)["\']',        # addWeapon "ClassName"
            r'addMagazine\s*["\']([^"\']+)["\']',      # addMagazine "ClassName"
            r'addItem\s*["\']([^"\']+)["\']',          # addItem "ClassName"
            r'addBackpack\s*["\']([^"\']+)["\']',      # addBackpack "ClassName"
            r'addHeadgear\s*["\']([^"\']+)["\']',       # addHeadgear "ClassName"
            r'addGoggles\s*["\']([^"\']+)["\']',       # addGoggles "ClassName"
            r'addVest\s*["\']([^"\']+)["\']',          # addVest "ClassName"
            r'addUniform\s*["\']([^"\']+)["\']',       # addUniform "ClassName"
            r'addPrimaryWeaponItem\s*["\']([^"\']+)["\']',  # addPrimaryWeaponItem "ClassName"
            r'selectWeapon\s*["\']([^"\']+)["\']',     # selectWeapon "ClassName"
            r'_weapon\s*=\s*["\']([^"\']+)["\']',      # _weapon = "ClassName"
            r'_backpack\s*=\s*["\']([^"\']+)["\']',    # _backpack = "ClassName"
            r'_uniform\s*=\s*["\']([^"\']+)["\']',     # _uniform = "ClassName"
            r'_vest\s*=\s*["\']([^"\']+)["\']',        # _vest = "ClassName"
            r'_headgear\s*=\s*["\']([^"\']+)["\']',    # _headgear = "ClassName"
            
            # Arsenal related patterns
            r'_item\w+\s*=\s*\[["\']([^"\']+)["\']',  # _itemXYZ = ["ClassName",...
            r'createVehicleLocal\s*\[["\']([^"\']+)["\']', # createVehicleLocal ["ClassName"
            
            # ACE arsenal calls
            r'ace_arsenal_fnc_\w+\s*\[[^,]+,\s*\[["\']([^"\']+)["\']', # ace_arsenal_fnc_xyz [..., ["ClassName"
            
            # Extra uniform/gear patterns
            r'uniform\s+["\']([^"\']+)["\']',  # uniform "ClassName"
            r'headgear\s+["\']([^"\']+)["\']', # headgear "ClassName" 
            r'vest\s+["\']([^"\']+)["\']'      # vest "ClassName"
        ]
        
        # Remove comments first
        content = re.sub(r'//.*$', '', content, re.MULTILINE)  # Remove single line comments
        content = re.sub(r'/\*.*?\*/', '', content, re.DOTALL)  # Remove multi-line comments
        
        # Extract class names using patterns
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                class_name = match.group(1).strip()
                if class_name and class_name not in skip_names:  # Skip if it's a known variable name
                    class_names.add(class_name)
        
        # Filter out ignored classes
        return {name for name in class_names if not self._has_ignored_parent(name)}

    def _normalize_path(self, path: str) -> str:
        """Normalize asset path for consistent comparison"""
        # Convert to lowercase and normalize slashes
        path = path.lower().replace('\\', '/').replace('//', '/')
        
        # Remove common prefixes
        prefixes = ['a3/', 'z/', './', '../']
        for prefix in prefixes:
            if path.startswith(prefix):
                path = path[len(prefix):]
        
        # Remove leading slash if present 
        path = path.lstrip('/')
        
        # Handle addons prefix
        if 'addons/' in path:
            path = path[path.find('addons/') + 7:]
            
        return path

    def _path_matches(self, search_path: str, database_paths: Set[str]) -> bool:
        """Check if path matches any database path, including partial matches"""
        norm_search = self._normalize_path(search_path)
        
        # Try exact match first
        if norm_search in database_paths:
            return True
            
        # Try suffix match
        if any(db_path.endswith(norm_search) for db_path in database_paths):
            return True
            
        # Try partial path matching
        search_parts = norm_search.split('/')
        if len(search_parts) > 1:
            # Try matching just the last two path components
            partial_path = '/'.join(search_parts[-2:])
            matches = [p for p in database_paths if partial_path in p]
            if matches:
                return True
                
        return False

    def extract_asset_paths(self, content: str) -> Set[str]:
        """Extract asset paths from content"""
        asset_paths = set()
        
        # Common asset path patterns - now handling paths with or without a3/ prefix
        patterns = [
            r'[/\\][a-z0-9_/\\]+\.p3d\b',  # 3D models 
            r'[/\\][a-z0-9_/\\]+\.paa\b',  # Textures
            r'[/\\][a-z0-9_/\\]+\.wss\b',  # Sounds
            r'[/\\][a-z0-9_/\\]+\.ogg\b',  # Sounds
            r'[/\\][a-z0-9_/\\]+\.wav\b',  # Sounds
            r'[/\\][a-z0-9_/\\]+\.jpg\b',  # Images
            r'[/\\][a-z0-9_/\\]+\.png\b'   # Images
        ]
        
        # Remove comments first
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Extract paths using patterns
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                path = match.group(0)
                # Normalize path
                path = self._normalize_path(path)
                asset_paths.add(path)
        
        return asset_paths

    def find_class_in_database(self, class_name: str) -> Optional[ClassEntry]:
        """Search for a class by direct name match"""
        # Check all entries in all mods
        for entries in self.class_database.values():
            for entry in entries:
                if entry.class_name == class_name:
                    return entry
        return None

    def scan_file(self, file_path: str) -> Tuple[Set[str], Set[str]]:
        """Scan a single mission file for dependencies and assets"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get class dependencies
            class_names = self.extract_sqf_class_names(content) if file_path.lower().endswith('.sqf') \
                        else self.extract_class_names(content, self.is_loadout_file(file_path))
            
            # Get asset dependencies
            asset_paths = self.extract_asset_paths(content)
            
            # Check each class name directly
            for class_name in class_names:
                if class_name in self.mission_classes:
                    continue  # Skip classes defined in mission
                
                if class_name in self.all_classes:
                    self.found_classes.add(class_name)
                elif not (self.is_loadout_file(file_path) and class_name in self.role_classes):
                    # Don't report missing classes for role definitions in loadout files
                    if not class_name.lower() in {'true', 'false', 'nil', 'null', 'obj', 'player', 'this'}:

                        # Create array of special case class names to ignore
                        ignore_classes = {
                            'baseMan',
                            'marksman', 'ar', 'officer', 'rm_mat', 'medic', 'rm_lt', 'gren', 'rm', 'rm_lat', 'engineer', 'ab',
                            'OPFOR_LOADOUT', 'ammo'
                        }

                        if class_name in ignore_classes:
                            continue

                        self.missing_classes.add(class_name)
                        print(f"Class missing: {class_name}")
            
            # Check assets against database with better logging
            for asset_path in asset_paths:
                normalized_path = self._normalize_path(asset_path)
                
                if self._path_matches(normalized_path, self.all_assets):
                    self.found_assets.add(normalized_path)
            
            return class_names, asset_paths

        except Exception as e:
            print(f"ERROR: Error scanning {file_path}: {str(e)}")
            return set(), set()

    def print_report(self):
        """Print scanning results"""
        print(f"\nMission: {self.mission_name}")
        print("=" * (len(self.mission_name) + 9))
        
        print(f"\nMission-defined Classes: {len(self.mission_classes)}")
        for class_name in sorted(self.mission_classes):
            print(f"  {class_name}")
            
        print(f"\nFound Classes: {len(self.found_classes)}")
        for class_name in sorted(self.found_classes):
            entry = self.find_class_in_database(class_name)
            if entry:
                print(f"  {class_name} [{entry.source}]")
            else:
                print(f"  {class_name}")
        
        print(f"\nMissing Classes: {len(self.missing_classes)}")
        for class_name in sorted(self.missing_classes):
            print(f"  {class_name}")
            # Try to find similar classes
            similar = [
                other for other in self.all_classes 
                if class_name.lower() in other.lower()
            ][:3]  # Show up to 3 similar classes
            if similar:
                print("    Similar classes found:")
                for s in similar:
                    print(f"    - {s}")
        
        print(f"\nMissing Assets: {len(self.missing_assets)}")
        for asset_path in sorted(self.missing_assets):
            print(f"  {asset_path}")
        print("\n" + "-" * 60)
