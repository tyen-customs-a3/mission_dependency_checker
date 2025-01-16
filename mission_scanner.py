import re
import os
from typing import Set, Dict, Tuple
from database import ClassEntry, AssetEntry, scan_for_assets

class MissionDependencyScanner:
    def __init__(self, class_database: Dict[str, Set[ClassEntry]], 
                 asset_database: Set[str], 
                 mission_name: str):
        self.class_database = class_database
        self.asset_database = asset_database.copy()  # Create a copy to add mission-local assets
        self.mission_name = mission_name
        # Flatten database for easier searching
        self.all_classes = {
            entry.name for entries in class_database.values() 
            for entry in entries
        }
        # Asset database is already a set of paths
        self.all_assets = {self._normalize_path(path) for path in asset_database}
        self.missing_classes = set()
        self.found_classes = set()
        self.missing_assets = set()
        self.found_assets = set()
        
        # Add default/engine classes that always exist
        self.default_classes = {
            'itemMap',
            '#lightpoint',
            '#particlesource'
        }
        self.all_classes.update(self.default_classes)

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
        
        # Build initial parent map from mod database
        for entries in class_database.values():
            for entry in entries:
                if entry.parent:
                    self.parent_map[entry.name] = entry.parent
        
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
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)  # Remove single line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Remove multi-line comments
        
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
        # Remove leading a3/ and z/ if present since extracted paths don't have them
        path = re.sub(r'^/?(?:a3/|z/)', '', path.lower())
        # Remove leading slash if present 
        path = re.sub(r'^/', '', path)
        # Normalize slashes
        return path.replace('\\', '/').replace('//', '/')

    def _path_matches(self, search_path: str, database_paths: Set[str]) -> bool:
        """Check if path matches any database path, including suffix matches"""
        norm_search = self._normalize_path(search_path)
        # Try exact match first
        if norm_search in database_paths:
            return True
        # Try suffix match
        return any(db_path.endswith(norm_search) for db_path in database_paths)

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
            
            # Check each class against database
            for class_name in class_names:
                if class_name in self.all_classes:
                    self.found_classes.add(class_name)
                elif not (self.is_loadout_file(file_path) and class_name in self.role_classes):
                    # Don't report missing classes for role definitions in loadout files
                    if not class_name.lower() in {'true', 'false', 'nil', 'null', 'obj', 'player', 'this'}:
                        self.missing_classes.add(class_name)
            
            # Check assets against database
            for asset_path in asset_paths:
                normalized_path = self._normalize_path(asset_path)
                if self._path_matches(normalized_path, self.all_assets):
                    self.found_assets.add(normalized_path)
                else:
                    self.missing_assets.add(normalized_path)
            
            return class_names, asset_paths

        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)}")
            return set(), set()

    def print_report(self):
        """Print scanning results"""
        print(f"\nMission: {self.mission_name}")
        print("=" * (len(self.mission_name) + 9))
        
        print(f"\nFound Classes: {len(self.found_classes)}")
        for class_name in sorted(self.found_classes):
            # Find which mod it belongs to
            for mod, entries in self.class_database.items():
                if any(entry.name == class_name for entry in entries):
                    print(f"  {class_name} [{mod}]")
                    break
        
        print(f"\nMissing Classes: {len(self.missing_classes)}")
        for class_name in sorted(self.missing_classes):
            print(f"  {class_name}")
        
        print(f"\nMissing Assets: {len(self.missing_assets)}")
        for asset_path in sorted(self.missing_assets):
            print(f"  {asset_path}")
        print("\n" + "-" * 60)

def extract_mission_name(path: str) -> str:
    """Extract mission name from path like 'co40_last_mile.tem_chamw'"""
    base = os.path.basename(path)
    # Remove map name and get just the mission name part
    mission_name = base.split('.')[0]
    return mission_name

def scan_mission_folder(missions_root: str, class_database: Dict[str, Set[ClassEntry]], 
                       asset_database: Dict[str, Set[AssetEntry]], cache_mgr=None):
    """Scan multiple missions in the missions folder"""
    reports = []
    
    mission_folders = [
        d for d in os.listdir(missions_root) 
        if os.path.isdir(os.path.join(missions_root, d))
    ]
    
    for mission_folder in sorted(mission_folders):
        mission_path = os.path.join(missions_root, mission_folder)
        mission_name = extract_mission_name(mission_folder)
        
        # Try to get cached results first
        cached_results = None
        if cache_mgr:
            cached_results = cache_mgr.get_cached_mission(mission_path)
            
        scanner = MissionDependencyScanner(class_database, asset_database, mission_name)
        
        if cached_results:
            print(f"Using cached results for {mission_name}")
            scanner.missing_classes, scanner.missing_assets = cached_results
        else:
            print(f"Scanning {mission_name}...")
            # Scan all .hpp, .cpp and .sqf files in the mission folder
            for root, _, files in os.walk(mission_path):
                for file in files:
                    if file.endswith(('.hpp', '.cpp', '.sqf')):
                        file_path = os.path.join(root, file)
                        scanner.scan_file(file_path)
                        
            # Cache the results
            if cache_mgr:
                cache_mgr.cache_mission(mission_path, 
                    (scanner.missing_classes, scanner.missing_assets))
        
        reports.append(scanner)
    
    return reports