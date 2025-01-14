import re
import os
from typing import Set, Dict
from database import ClassEntry

class MissionDependencyScanner:
    def __init__(self, class_database: Dict[str, Set[ClassEntry]], mission_name: str):
        self.class_database = class_database
        self.mission_name = mission_name
        # Flatten database for easier searching
        self.all_classes = {
            entry.name for entries in class_database.values() 
            for entry in entries
        }
        self.missing_classes = set()
        self.found_classes = set()
        
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

    def is_loadout_file(self, file_path: str) -> bool:
        """Check if file is a loadout configuration"""
        return 'loadout' in file_path.lower() and file_path.endswith(('.hpp', '.cpp'))

    def extract_class_names(self, content: str, is_loadout: bool = False) -> Set[str]:
        """Extract potential class names from content"""
        class_names = set()
        
        # Remove all classes that should be ignored and their contents using regex
        for ignored_class in self.skip_classes:
            pattern = rf'class\s+{ignored_class}\s*\{{[^{{]*(?:\{{[^{{]*\}}[^{{]*)*\}}'
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            
        # Remove displayName assignments as these are role descriptions, not class names
        content = re.sub(r'displayName\s*=\s*["\']([^"\']+)["\']', '', content)
        
        # Handle loadout files differently
        if is_loadout:
            # Extract only equipment classes from arrays
            array_pattern = r'(?:uniform|vest|backpack|headgear|goggles|primaryWeapon|secondaryWeapon|sidearmWeapon)\[\]\s*=\\s*[\[{]([^}\]]+)[\]}]'
            for match in re.finditer(array_pattern, content):
                values = match.group(1)
                class_names.update(re.findall(r'["\']([A-Za-z0-9_]+)(?:\[[^\]]+\])?["\']', values))
        else:
            # Add patterns for class inheritance
            inheritance_pattern = r'class\s+(\w+)\s*:\s*(\w+)'
            for match in re.finditer(inheritance_pattern, content):
                class_name = match.group(2)  # Get parent class name
                if (class_name not in {'baseMan', 'rm', 'crew'} and  # Skip common base classes
                    class_name not in self.skip_classes):  # Skip ai-related classes
                    class_names.add(class_name)
        
            # Ignore special engine entities and default classes 
            special_classes = self.default_classes
        
            # Pattern to find array assignments like uniform[] = { "Class1", "Class2" } or _itemUniform = ["Class1", "Class2"]
            array_pattern = r'(?:(\w+)\[\]|\b_item\w+)\s*=\\s*[\[{]([^}\]]+)[\]}]'
        
            # Find all array assignments
            for match in re.finditer(array_pattern, content):
                array_name = match.group(1)
                # Skip traits array and arsenal init call arguments
                if array_name and ('traits' in array_name or 'arsenal' in array_name.lower()):
                    continue
                
                # Extract values from the array
                values = match.group(2)
                # Find all quoted strings, handling optional [] attachments
                class_names.update(re.findall(r'["\']([A-Za-z0-9_]+)(?:\[[^\]]+\])?["\']', values))
        
            # Fixed: Remove problematic look-behind and use alternative approach
            # Extract quoted strings that aren't in traits array
            traits_pattern = r'traits\[\]\s*=\s*\{[^}]*\}'
            traits_sections = re.findall(traits_pattern, content)
        
            # Remove traits sections from content before looking for other class names
            working_content = content
            for section in traits_sections:
                working_content = working_content.replace(section, '')
            
            # Now look for quoted strings in the remaining content
            direct_pattern = r'["\']([A-Za-z0-9_]+)(?:\[[^\]]+\])?["\']'
            matches = re.findall(direct_pattern, working_content)
            class_names.update(name for name in matches if name not in self.skip_classes)
        
            # Also look for direct class definitions, excluding ai-related
            class_pattern = r'class\s+(\w+)'
            matches = re.findall(class_pattern, content)
            class_names.update(name for name in matches if name not in self.skip_classes)
        
        return class_names

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
        
        return class_names

    def scan_file(self, file_path: str) -> Set[str]:
        """Scan a single mission file for class dependencies"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine if this is a loadout file
            is_loadout = self.is_loadout_file(file_path)
            
            # Use different parsers based on file extension
            if file_path.lower().endswith('.sqf'):
                class_names = self.extract_sqf_class_names(content)
            else:
                class_names = self.extract_class_names(content, is_loadout)
            
            # Check each class against database
            for class_name in class_names:
                if class_name in self.all_classes:
                    self.found_classes.add(class_name)
                elif not (is_loadout and class_name in self.role_classes):
                    # Don't report missing classes for role definitions in loadout files
                    if not class_name.lower() in {'true', 'false', 'nil', 'null', 'obj', 'player', 'this'}:
                        self.missing_classes.add(class_name)
            
            return class_names

        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)}")
            return set()

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
        print("\n" + "-" * 60)

def extract_mission_name(path: str) -> str:
    """Extract mission name from path like 'co40_last_mile.tem_chamw'"""
    base = os.path.basename(path)
    # Remove map name and get just the mission name part
    mission_name = base.split('.')[0]
    return mission_name

def scan_mission_folder(missions_root: str, class_database: Dict[str, Set[ClassEntry]]):
    """Scan multiple missions in the missions folder"""
    reports = []
    
    # Get immediate subdirectories (mission folders)
    mission_folders = [
        d for d in os.listdir(missions_root) 
        if os.path.isdir(os.path.join(missions_root, d))
    ]
    
    for mission_folder in sorted(mission_folders):
        mission_path = os.path.join(missions_root, mission_folder)
        mission_name = extract_mission_name(mission_folder)
        
        scanner = MissionDependencyScanner(class_database, mission_name)
        
        # Scan all .hpp, .cpp and .sqf files in the mission folder
        for root, _, files in os.walk(mission_path):
            for file in files:
                if file.endswith(('.hpp', '.cpp', '.sqf')):
                    file_path = os.path.join(root, file)
                    scanner.scan_file(file_path)
        
        reports.append(scanner)
    
    return reports
