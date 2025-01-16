import os
import re
from collections import defaultdict
from typing import Dict, Set, Optional
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class ClassEntry:
    def __init__(self, name: str, parent: Optional[str] = None, file_path: str = ""):
        self.name = name
        self.parent = parent
        self.file_path = file_path

    def __eq__(self, other):
        if not isinstance(other, ClassEntry):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class AssetEntry:
    def __init__(self, path: str, file_path: str = ""):
        self.path = path
        self.file_path = file_path

    def __eq__(self, other):
        if not isinstance(other, AssetEntry):
            return False
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)

def parse_class_definitions(file_path: str) -> Set[ClassEntry]:
    """Parse class definitions from a file and return a set of ClassEntry objects."""
    classes = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments first
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        def extract_nested_classes(text: str, parent_class: Optional[str] = None) -> Set[ClassEntry]:
            """Recursively extract nested class definitions"""
            nested_classes = set()
            
            # Match class definition and its entire content block
            class_pattern = r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
            
            for match in re.finditer(class_pattern, text):
                class_name = match.group(1)
                direct_parent = match.group(2)  # Explicit parent from inheritance
                class_content = match.group(3)
                
                # If this class has a parent from inheritance use that, otherwise use the containing class
                effective_parent = direct_parent if direct_parent else parent_class
                
                # Add this class
                entry = ClassEntry(class_name, effective_parent, file_path)
                nested_classes.add(entry)
                
                # Recursively process nested classes
                nested_classes.update(extract_nested_classes(class_content, class_name))
            
            return nested_classes
        
        # Start recursive extraction from root level
        classes.update(extract_nested_classes(content))
            
    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
    
    return classes

def get_top_level_folder(file_path: str) -> str:
    """Extract the top-level folder name from the file path."""
    parts = file_path.split(os.sep)
    for part in parts:
        if part.startswith('@'):
            return part
    return "unassigned"  # Default group if no @ folder found

class ThreadSafeDict:
    def __init__(self):
        self._dict = {}  # Changed from defaultdict to regular dict
        self._asset_dict = {}  # New dictionary for assets
        self._lock = Lock()
    
    def update(self, group: str, classes: Set[ClassEntry], assets: Set[AssetEntry] = None):
        with self._lock:
            if group not in self._dict:
                self._dict[group] = set()
            if assets and group not in self._asset_dict:
                self._asset_dict[group] = set()
            
            new_entries = {ClassEntry(entry.name, entry.parent, entry.file_path) for entry in classes}
            self._dict[group].update(new_entries)
            
            if assets:
                new_assets = {AssetEntry(asset.path, asset.file_path) for asset in assets}
                self._asset_dict[group].update(new_assets)
    
    def get_data(self) -> tuple[Dict[str, Set[ClassEntry]], Dict[str, Set[AssetEntry]]]:
        with self._lock:
            class_data = {
                group: {ClassEntry(entry.name, entry.parent, entry.file_path) 
                       for entry in entries}
                for group, entries in self._dict.items()
            }
            asset_data = {
                group: {AssetEntry(asset.path, asset.file_path) 
                       for asset in entries}
                for group, entries in self._asset_dict.items()
            }
            return class_data, asset_data

def process_file(file_path: str) -> tuple[str, Set[ClassEntry]]:
    """Process a single file and return (group, classes)"""
    group = get_top_level_folder(file_path)
    classes = parse_class_definitions(file_path)
    return group, classes

def scan_for_assets(folder_path):
    """Scan a folder for .paa files and return their relative paths"""
    asset_paths = set()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.paa'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path).replace('\\', '/')
                asset_paths.add(rel_path.lower())
    return asset_paths

def scan_folder(folder_path):
    """Scan folder for classes and assets"""
    class_database = defaultdict(set)
    asset_database = set()  # Simple set of asset paths
    
    # Scan for classes
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.hpp', '.cpp')):
                file_path = os.path.join(root, file)
                group = get_top_level_folder(file_path)
                classes = parse_class_definitions(file_path)
                class_database[group].update(classes)
    
    # Scan for assets
    asset_database.update(scan_for_assets(folder_path))
    
    return dict(class_database), asset_database

def print_database(database: Dict[str, Set[ClassEntry]]):
    """Print the class database in a formatted way."""
    print("\nClass Database:")
    print("==============")
    
    for group, classes in database.items():
        print(f"\nGroup: {group}")
        print("-" * (len(group) + 7))
        
        for entry in sorted(classes, key=lambda x: x.name):
            parent_info = f" : {entry.parent}" if entry.parent else ""
            print(f"  {entry.name}{parent_info}")
            print(f"    File: {entry.file_path}")
