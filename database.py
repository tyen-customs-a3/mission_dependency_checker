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
            
        # Simple regex to match class definitions
        # Matches: class ClassName[: ParentClass] {
        class_pattern = r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*[{;]'
        matches = re.finditer(class_pattern, content)
        
        for match in matches:
            class_name = match.group(1)
            parent_class = match.group(2)  # Will be None if no parent class
            classes.add(ClassEntry(class_name, parent_class, file_path))
            
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

def scan_folder(root_dir: str, max_workers: int = 8) -> tuple[Dict[str, Set[ClassEntry]], Dict[str, Set[AssetEntry]]]:
    """Scan folder for files and assets"""
    class_database = ThreadSafeDict()
    files_to_process = []
    
    def normalize_path(path: str) -> str:
        """Normalize asset path relative to root directory"""
        rel_path = os.path.relpath(path, root_dir)
        # Remove z/ prefix if present
        rel_path = re.sub(r'^/?(?:a3/|z/)', '', rel_path)
        return rel_path.lower().replace('\\', '/')

    # Collect all files first
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.cpp', '.hpp')):
                files_to_process.append(os.path.join(root, file))
            elif file.lower().endswith(('.paa', '.wss', '.ogg', '.wav', '.p3d', '.jpg', '.png')):
                # Add asset files directly
                full_path = os.path.join(root, file)
                normalized_path = normalize_path(full_path)
                group = get_top_level_folder(full_path)
                class_database.update(group, set(), {AssetEntry(normalized_path, full_path)})

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_file, file_path): file_path 
            for file_path in files_to_process
        }
        
        # Process results as they complete
        for future in future_to_file:
            try:
                group, classes = future.result()
                class_database.update(group, classes)
            except Exception as e:
                file_path = future_to_file[future]
                print(f"Error processing {file_path}: {str(e)}")

    return class_database.get_data()

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
