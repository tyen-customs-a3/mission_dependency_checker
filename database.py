import os
import json
import re
import logging
import subprocess
from pathlib import Path
from typing import Dict, Set, Optional, List, Tuple, Union, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime
import csv

# Simple console logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass(frozen=True)  # Make the class immutable and hashable
class ClassEntry:
    """Represents an Arma 3 class entry matching the JSON structure"""
    class_name: str  # Changed from class_ to class_name
    source: str
    category: str
    children: Optional[tuple] = None
    parent: Optional[str] = None  # For inheritance tracking
    path: Optional[str] = None    # For full path tracking
    
    def __hash__(self):
        return hash((self.class_name, self.source, self.category, self.path))
    
    def __eq__(self, other):
        if not isinstance(other, ClassEntry):
            return False
        # Compare using full paths if available
        if self.path and other.path:
            return self.path == other.path and self.source == self.source
        # Fallback to class name comparison
        return (self.class_name == self.class_name and 
                self.source == self.source and 
                self.category == self.category)

    def get_full_path(self) -> str:
        """Get the full class path including parent hierarchy"""
        if self.path:
            return self.path
        if self.parent:
            return f"{self.parent}/{self.class_name}"  # Changed to use forward slash
        return self.class_name

    @property
    def name(self) -> str:
        """Compatibility property for code still using name"""
        return self.class_name

@dataclass
class AssetEntry:
    path: str
    source: str

def load_class_database(json_file: str) -> Dict[str, Set[ClassEntry]]:
    """Load class database from the JSON generated by getconfigs.sqf"""
    database: Dict[str, Set[ClassEntry]] = {}
    path_database: Dict[str, ClassEntry] = {}  # Track by full path
    
    def process_class_entry(entry: dict, parent_path: Optional[str] = None) -> ClassEntry:
        class_name = entry['class']
        path = f"{parent_path}_{class_name}" if parent_path else class_name
        
        return ClassEntry(
            class_name=class_name,  # Updated to use class_name
            source=entry['source'],
            category=entry['category'],
            children=tuple(entry.get('children', ())),
            path=path
        )
    
    def process_class_tree(entry: dict, parent: Optional[str] = None, parent_path: Optional[str] = None):
        class_entry = process_class_entry(entry, parent_path)
        class_entry.parent = parent
        
        # Add to source-based dictionary
        if class_entry.source not in database:
            database[class_entry.source] = set()
        database[class_entry.source].add(class_entry)
        
        # Process children recursively
        if 'children' in entry:
            for child in entry['children']:
                process_class_tree(child, class_entry.class_name, class_entry.path)
    
    with open(json_file, 'r') as f:
        data = json.load(f)
        
    # Process each root class
    for entry in data:
        process_class_tree(entry)
        
    # Add lookup by path method to database
    database.get_by_path = lambda path: path_database.get(path)  # type: ignore
    
    logger.info(f"Loaded {len(path_database)} unique classes")
    return database

def scan_for_assets(folder_path: str) -> Set[str]:
    """Scan folder for asset files"""
    assets = set()
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.paa', '.p3d', '.wss', '.ogg', '.wav', '.jpg', '.png')):
                rel_path = os.path.relpath(os.path.join(root, file), folder_path)
                # Normalize path
                norm_path = rel_path.replace('\\', '/').lower()
                assets.add(norm_path)
                
    return assets

def print_database(database: Dict[str, Set[ClassEntry]]):
    """Print the class database in a formatted way."""
    print("\nClass Database:")
    print("==============")
    
    for source, classes in database.items():
        print(f"\nSource: {source}")
        print("-" * (len(source) + 8))
        
        for entry in sorted(classes, key=lambda x: x.get_full_path()):
            path_info = f" [{entry.get_full_path()}]"
            print(f"  {entry.class_name}{path_info}")

def parse_class_hierarchy(json_data: str) -> Dict[str, ClassEntry]:
    """Parse class hierarchy JSON data into ClassEntry objects"""
    classes = {}
    try:
        # Add debug logging
        logger.info("Parsing class hierarchy data")
        
        if isinstance(json_data, str):
            logger.debug(f"Input is string, length: {len(json_data)}")
            data = json.loads(json_data)
        else:
            logger.debug(f"Input is {type(json_data)}")
            data = json_data

        if isinstance(data, dict):
            logger.debug("Converting single dict to list")
            data = [data]
        
        def process_class(class_data: dict, parent: Optional[str] = None, depth: int = 0):
            if not isinstance(class_data, dict):
                logger.warning(f"Invalid class data type: {type(class_data)}")
                return

            try:
                # Handle minimized key names
                class_name = class_data.get("c") or class_data.get("class", "unknown")
                source = class_data.get("s") or class_data.get("source", "unknown")
                category = class_data.get("t") or class_data.get("category", "unknown")
                parent_name = class_data.get("p") or class_data.get("parent", parent)  # Use passed parent if none specified
                error = class_data.get("e")  # Check for error flag
                
                if error:
                    logger.warning(f"Skipping class with error: {class_name}")
                    return

                children = tuple(class_data.get("children", ()))
                path = f"{parent_name}/{class_name}" if parent_name else class_name

                logger.debug(f"{'  ' * depth}Processing class: {class_name} from {source}")

                # Create and store the entry
                entry = ClassEntry(
                    class_name=class_name,
                    source=source,
                    category=category,
                    children=children if children else None,
                    parent=parent_name,  # Store parent relationship
                    path=path
                )
                
                if class_name in classes:
                    logger.warning(f"Duplicate class found: {class_name}")
                    
                classes[class_name] = entry
                logger.debug(f"{'  ' * depth}Added class {class_name}")

                # Process children
                if children:
                    logger.debug(f"{'  ' * depth}Processing {len(children)} children of {class_name}")
                    for child in children:
                        if isinstance(child, dict):
                            process_class(child, class_name, depth + 1)

            except Exception as e:
                logger.error(f"Error processing class {class_data.get('class', 'unknown')}: {e}")

        # Process root classes
        for i, root_class in enumerate(data):
            logger.info(f"Processing root class {i}")
            process_class(root_class)

        logger.info(f"Successfully parsed {len(classes)} classes")

    except Exception as e:
        logger.error(f"Error in parse_class_hierarchy: {e}")
        if isinstance(json_data, str):
            logger.debug(f"First 100 chars of input: {json_data[:100]}")

    return classes

def parse_csv_line(line: str) -> Optional[Dict[str, str]]:
    """Parse a CSV line into a dictionary"""
    try:
        # Handle special case of trailing junk data
        if '"}' in line:
            line = line[:line.index('"}')]
            
        # Remove any extra quotes at the end
        line = line.rstrip('"')
        
        # Split by double-double quotes with comma
        parts = line.split('","')
        if len(parts) == 4:
            # Clean up the parts (remove remaining quotes and clean)
            parts = [p.strip().strip('"').replace('""', '"') for p in parts]
            # Verify all parts are valid
            if all(len(p) > 0 for p in parts[:3]):  # parent can be empty
                return {
                    'class': parts[0],
                    'source': parts[1],
                    'category': parts[2],
                    'parent': parts[3]
                }
    except Exception as e:
        logger.error(f"Failed to parse CSV line: {line} - {str(e)}")
    return None

def parse_cpp_value(value: str) -> List[str]:
    """Parse the specific cpp value format into individual CSV lines"""
    # Remove outer quotes and trailing junk
    value = value.strip('"')
    if '"}' in value:
        value = value[:value.index('"}')]
        
    # Split on explicit newlines marked by \n
    lines = value.split(r'\n')
    # Clean each line and filter empty ones
    return [
        line.strip().strip('"')
        for line in lines
        if line.strip() and not line.strip().startswith('""}')
    ]

def write_debug_csv(data: List[dict], source_file: str, category: str):
    """Write parsed data to debug CSV file"""
    debug_dir = "debug"
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(debug_dir, f"parsed_classes_{category}_{timestamp}.csv")
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar='\\')
        writer.writerow(['ClassName', 'Source', 'Category', 'Parent'])
        for entry in data:
            if not all(key in entry for key in ['class', 'source', 'category']):
                logger.warning(f"Skipping invalid entry: {entry}")
                continue
            writer.writerow([
                entry['class'],
                entry['source'],
                entry['category'],
                entry.get('parent', '')  # parent is optional
            ])
    logger.info(f"Debug CSV written to: {filename}")

def extract_classes_from_cpp(file_path: str) -> Dict[str, List[dict]]:
    """Extract CSV config data from .cpp file, organized by category"""
    config_data = {}
    current_category = None
    batch_count = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()
        
        inside_data = False
        reading_value = False
        value_buffer = ""

        for line in lines:
            line = line.strip()
            
            # Check for metadata
            if '_count' in line.lower():
                category_match = re.search(r'extractedCsv_(\w+)_count', line)
                if category_match and 'value=' in line:
                    current_category = category_match.group(1)
                    batch_count = int(line.split('=')[1].rstrip(';'))
                    config_data[current_category] = []
                continue
            
            # Check for data chunks
            if 'extractedCsv_' in line.lower():
                category_match = re.search(r'extractedCsv_(\w+)_\d+', line)
                if category_match:
                    current_category = category_match.group(1)
                    if current_category not in config_data:
                        config_data[current_category] = []
                    inside_data = True
                continue
            
            if inside_data and 'value=' in line:
                reading_value = True
                value_buffer = line[6:].rstrip(';')  # Remove 'value=' and trailing semicolon
                if line.endswith(';'):
                    reading_value = False
                    process_batch_data(value_buffer, current_category, config_data)
                    value_buffer = ""
                    inside_data = False
                continue
            
            if reading_value:
                value_buffer += line
                if line.endswith(';'):
                    reading_value = False
                    value_buffer = value_buffer.rstrip(';')
                    process_batch_data(value_buffer, current_category, config_data)
                    value_buffer = ""
                    inside_data = False

    return config_data

def process_batch_data(batch_data: str, category: str, config_data: Dict[str, List[dict]]) -> None:
    """Process a batch of CSV data"""
    if not batch_data or not category or category not in config_data:
        return

    csv_lines = parse_cpp_value(batch_data)
    for line in csv_lines:
        if not line.startswith('ClassName'):  # Skip header
            if parsed := parse_csv_line(line):
                config_data[category].append(parsed)

def parse_cpp_value(value: str) -> List[str]:
    """Parse the specific cpp value format into individual CSV lines"""
    value = value.strip('"')
    if '"}' in value:
        value = value[:value.index('"}')]
    
    # Handle escaped newlines and clean up the lines
    lines = value.split(r'\n')
    return [
        line.strip().strip('"').replace('\\"', '"')
        for line in lines
        if line.strip() and not line.strip().startswith('""}')
    ]

def parse_csv_line(line: str) -> Optional[Dict[str, str]]:
    """Parse a CSV line into a dictionary"""
    try:
        # Handle special case of trailing junk data
        if '"}' in line:
            line = line[:line.index('"}')]
        
        # Split by quotes and comma, handling escaped quotes
        parts = [p.strip().strip('"').replace('""', '"') 
                for p in line.split('","')]
        
        if len(parts) == 4:
            if all(len(p) > 0 for p in parts[:3]):  # parent can be empty
                return {
                    'class': parts[0],
                    'source': parts[1],
                    'category': parts[2],
                    'parent': parts[3]
                }
    except Exception as e:
        logger.error(f"Failed to parse CSV line: {line} - {str(e)}")
    return None

def parse_class_hierarchy(data: Union[str, List[dict], dict]) -> Dict[str, ClassEntry]:
    """Parse class hierarchy data into ClassEntry objects"""
    classes = {}
    
    try:
        if isinstance(data, str):
            if data.endswith(('.cpp', '.json')):
                data = extract_classes_from_cpp(data)
            else:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    logger.error("Failed to parse input as JSON")
                    return classes
        
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            logger.error(f"Invalid input type: {type(data)}")
            return classes

        for entry in data:
            if not isinstance(entry, dict):
                continue
                
            try:
                class_name = entry.get('class')
                if not class_name:
                    continue
                    
                source = entry.get('source', 'unknown')
                category = entry.get('category', 'unknown')
                parent = entry.get('parent')
                if parent == '' or parent == '-':
                    parent = None

                path = f"{parent}/{class_name}" if parent else class_name

                class_entry = ClassEntry(
                    class_name=class_name,
                    source=source,
                    category=category,
                    children=None,
                    parent=parent,
                    path=path
                )
                
                classes[class_name] = class_entry
                
            except Exception as e:
                logger.error(f"Error processing class: {str(e)}")

    except Exception as e:
        logger.error(f"Error in parse_class_hierarchy: {e}")

    return classes

def get_pbo_contents(pbo_path: str) -> List[str]:
    """Use extractpbo to list contents of a PBO file"""
    try:
        # Run extractpbo with -LB for brief listing format
        result = subprocess.run(['extractpbo', '-LBP', pbo_path], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            # Get all lines and return non-empty ones
            lines = result.stdout.splitlines()
            return [line.strip() for line in lines if line.strip()]
        return []
    except subprocess.SubProcessError:
        logger.error(f"Failed to read PBO: {pbo_path}")
        return []

def process_pbo(pbo_path: str) -> Tuple[Optional[str], Set[str]]:
    """Process a single PBO file and return its prefix and assets"""
    assets = set()
    prefix = None
    mod_name = Path(pbo_path).parent.name
    
    # Get list of files in PBO
    pbo_contents = get_pbo_contents(pbo_path)
    
    # Extract prefix
    for line in pbo_contents:
        if 'prefix=' in line:
            prefix = line.split('=')[1].strip()
            break
    
    if not prefix:
        return None, set()
    
    for line in pbo_contents:
        if line.lower().endswith(('.paa', '.p3d', '.wss', '.ogg', '.wav')):
            norm_path = f"{prefix}/{line}".replace('\\', '/').lower()
            assets.add(norm_path)
            
    return prefix, assets

def scan_folder(folder_path: str) -> Set[str]:
    """
    Scan a folder for PBO files and collect asset paths.
    Classes are handled separately through the cpp file.
    Returns: asset_database: Set[str]
    """
    asset_database: Set[str] = set()
    asset_lock = Lock()
    
    # Collect all PBO files first
    pbo_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pbo'):
                pbo_files.append(os.path.join(root, file))
    
    # Process PBOs in parallel
    with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() * 2)) as executor:
        future_to_pbo = {executor.submit(process_pbo, pbo): pbo for pbo in pbo_files}
        
        for future in as_completed(future_to_pbo):
            pbo = future_to_pbo[future]
            try:
                _, pbo_assets = future.result()  # Ignore prefix since we only need assets
                with asset_lock:
                    asset_database.update(pbo_assets)
            except Exception as e:
                logger.error(f"Error processing PBO {pbo}: {str(e)}")
    
    logger.info(f"Found {len(asset_database)} assets in {len(pbo_files)} PBOs")
    return asset_database  # Return only asset database since classes come from cpp
