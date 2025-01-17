import os
import json
import re
import logging
import sqlite3
from typing import Dict, Set, Optional, List, Union, Any
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ClassEntry:
    """Represents an Arma 3 class entry"""
    class_name: str
    source: str
    category: str
    parent: Optional[str] = None
    
    def __hash__(self):
        return hash((self.class_name, self.source, self.category, self.parent))
    
    def __lt__(self, other):
        if not isinstance(other, ClassEntry):
            return NotImplemented
        return (self.source, self.class_name) < (other.source, other.class_name)

    def __eq__(self, other):
        if not isinstance(other, ClassEntry):
            return NotImplemented
        return (self.class_name == other.class_name and 
                self.source == other.source and 
                self.category == other.category and 
                self.parent == other.parent)

def parse_class_hierarchy(data: Union[str, List[dict], dict]) -> Dict[str, ClassEntry]:  # Changed return type
    """Parse class data into ClassEntry objects"""
    classes: Dict[str, ClassEntry] = {}  # Changed to store ClassEntry directly
    entry_count = 0
    dropped_count = 0
    
    try:
        # Handle string input (file paths or JSON strings)
        if isinstance(data, str):
            if data.endswith('.cpp'):
                data = extract_classes_from_cpp(data)
            else:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    logger.error("Failed to parse input as JSON")
                    return classes

        # Handle direct entry
        if isinstance(data, dict) and all(key in data for key in ['class', 'source', 'category']):
            class_entry = ClassEntry(
                class_name=data['class'],
                source=data['source'],
                category=data['category'],
                parent=data.get('parent') if data.get('parent') not in ['-', ''] else None
            )
            classes[class_entry.class_name] = class_entry
            return classes

        # Handle category-based structure from extract_classes_from_cpp
        if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
            for category, entries in data.items():
                if not isinstance(entries, list):
                    continue
                    
                for entry in entries:
                    try:
                        if not isinstance(entry, dict):
                            logger.debug(f"Skipping non-dict entry: {entry}")
                            dropped_count += 1
                            continue
                            
                        class_name = entry.get('class')
                        if not class_name:
                            logger.debug(f"Skipping entry without class name: {entry}")
                            dropped_count += 1
                            continue
                        
                        # Get parent value - only convert to None if it's completely empty
                        parent = entry.get('parent', '')
                        if parent in ['-', '', None, '""']:
                            parent = None
                        
                        # Create entry with proper parent handling
                        class_entry = ClassEntry(
                            class_name=class_name,
                            source=entry.get('source', 'unknown'),
                            category=entry.get('category', category),
                            parent=parent  # Will be None only if truly empty
                        )
                        
                        classes[class_name] = class_entry
                        entry_count += 1
                        logger.debug(f"Added class: {class_name} with parent: {parent}")
                        
                    except Exception as e:
                        logger.debug(f"Error processing entry: {entry} - {e}")
                        dropped_count += 1
                        continue

        # Handle list of entries
        elif isinstance(data, list):
            for entry in data:
                try:
                    if not isinstance(entry, dict):
                        continue
                        
                    class_name = entry.get('class')
                    if not class_name:
                        continue
                    
                    class_entry = ClassEntry(
                        class_name=class_name,
                        source=entry.get('source', 'unknown'),
                        category=entry.get('category', 'unknown'),
                        parent=entry.get('parent') if entry.get('parent') not in ['-', ''] else None
                    )
                    
                    classes[class_name] = class_entry
                    entry_count += 1
                    
                except Exception as e:
                    logger.debug(f"Skipping invalid entry: {entry} - {e}")
                    continue

        # Log processing results with more detail
        logger.info(f"Successfully processed {entry_count} classes")
        logger.info(f"Dropped {dropped_count} invalid entries")
        logger.info(f"Classes with parents: {sum(1 for e in classes.values() if e.parent)}")
        logger.info(f"Classes without parents: {sum(1 for e in classes.values() if not e.parent)}")
        
        if entry_count > 0:
            logger.info(f"Sample of processed classes:")
            sample_size = min(5, len(classes))
            for class_name in list(classes.keys())[:sample_size]:
                entry = classes[class_name]
                logger.info(f"  {entry.class_name} [{entry.source}] ({entry.category}) -> Parent: {entry.parent or 'None'}")

    except Exception as e:
        logger.error(f"Error in parse_class_hierarchy: {e}")
        if isinstance(data, dict):
            logger.debug(f"Data structure: {list(data.keys())[:5]}")

    return classes

def parse_csv_line(line: str) -> Optional[Dict[str, str]]:
    """Parse a CSV line into a dictionary
    
    Format examples:
    "4Rnd_Titan_long_missiles","A3","CfgMagazines","4Rnd_GAA_missiles"
    "ACE_2Rnd_12Gauge_Pellets_No3_Buck","@ace","CfgMagazines","ACE_2Rnd_12Gauge_Pellets_No0_Buck"
    "rhs_mag_M397_HET","@rhsusaf","CfgMagazines",""
    "rhs_6b23","@rhsafrf","CfgWeapons"",",""
    """
    try:
        # Clean up the line
        line = line.strip().strip('"')
        if not line:
            return None
            
        # Split into fields using explicit comma separation
        parts = [p.strip().strip('"') for p in line.split('","')]
        
        # Require at least class name, source, and category
        if len(parts) >= 3:
            # Clean up category field - remove any trailing quotes and commas
            category = parts[2].rstrip('",')
            
            return {
                'class': parts[0],
                'source': parts[1],
                'category': category,
                'parent': parts[3] if len(parts) > 3 and parts[3] else None
            }
    except Exception as e:
        logger.error(f"Failed to parse CSV line: {line} - {str(e)}")
    return None

def parse_cpp_value(value: str) -> List[str]:
    """Parse the specific cpp value format into individual CSV lines
    
    Example CPP format:
    name="extractedcsv_CfgMagazines_1";
    value="\"ClassName\",\"Source\",\"Category\",\"Parent\"\n
    \"4Rnd_Titan_long_missiles\",\"A3\",\"CfgMagazines\",\"4Rnd_GAA_missiles\"\n
    \"ACE_2Rnd_12Gauge_Pellets_No3_Buck\",\"@ace\",\"CfgMagazines\",\"ACE_2Rnd_12Gauge_Pellets_No0_Buck\"";
    
    Format spec:
    - Each chunk starts with name="extractedcsv_CATEGORY_NUMBER";
    - value="..." contains CSV data
    - CSV data has header line
    - Lines separated by literal '\n'
    - Fields are double-quoted and escaped
    """
    # Clean up the input string
    value = value.strip().strip('"')
    
    # Split on literal '\n' string
    lines = value.split('\\n')
    
    # Filter and clean lines
    return [
        line.strip().strip('"')
        for line in lines
        if line.strip() and not line.strip().startswith('ClassName')  # Skip header
    ]

def extract_classes_from_cpp(file_path: str) -> Dict[str, List[dict]]:
    """Extract CSV config data from .cpp file, organized by category
    
    File structure example:
    class CfgPatches {
        class MyMod {
            name="extractedcsv_CfgMagazines_count";
            value="27";
        };
        class Data1 {
            name="extractedcsv_CfgMagazines_1";
            value="...CSV data...";
        };
        class Data2 {
            name="extractedcsv_CfgMagazines_2";
            value="...CSV data...";
        };
    };
    
    Structure spec:
    - Categories defined by extractedcsv_CATEGORY
    - Count stored in extractedcsv_CATEGORY_count
    - Data chunks numbered 1 to count
    - Single chunk without number if count missing
    """
    config_data = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()
        
        # Track categories and their chunks
        categories = set()
        current_class = None
        inside_data = False
        chunk_counts = {}  # Store chunk counts per category
        
        # First pass - collect categories and their chunk counts
        for line in lines:
            line = line.strip()
            if 'name=' in line:
                # Look for count indicators
                if '_count";' in line:
                    count_match = re.search(r'extractedcsv_(\w+)_count', line)
                    if count_match:
                        category = count_match.group(1)
                        # Find the count value in the next line with 'value='
                        continue
                else:
                    # Extract category from chunk name
                    name_match = re.search(r'name="extractedcsv_(\w+)(?:_\d+)?";', line)
                    if name_match:
                        category = name_match.group(1)
                        categories.add(category)
                        if category not in config_data:
                            config_data[category] = []

            # Look for count values
            elif 'value=' in line and current_class:
                count_str = line[line.find('value="')+7:line.rfind('";')]
                try:
                    chunk_counts[current_class] = int(count_str)
                except ValueError:
                    pass
                current_class = None

        logger.info(f"Found categories: {categories}")
        logger.info(f"Chunk counts: {chunk_counts}")

        # Second pass - process chunks
        for category in categories:
            chunk_count = chunk_counts.get(category, 0)
            if chunk_count == 0:
                # Look for a single chunk without number
                pattern = f'name="extractedcsv_{category}";'
                chunk_data = []
                inside_chunk = False
                
                for line in lines:
                    line = line.strip()
                    if pattern in line:
                        inside_chunk = True
                    elif inside_chunk and 'value=' in line:
                        data = line[line.find('value="')+7:line.rfind('";')]
                        chunk_data = parse_cpp_value(data)
                        break
                
                if chunk_data:
                    for csv_line in chunk_data:
                        if parsed := parse_csv_line(csv_line):
                            if not parsed['category']:
                                parsed['category'] = category
                            config_data[category].append(parsed)
            else:
                # Process multiple chunks
                for chunk_num in range(1, chunk_count + 1):
                    pattern = f'name="extractedcsv_{category}_{chunk_num}";'
                    chunk_data = []
                    inside_chunk = False
                    
                    for line in lines:
                        line = line.strip()
                        if pattern in line:
                            inside_chunk = True
                        elif inside_chunk and 'value=' in line:
                            data = line[line.find('value="')+7:line.rfind('";')]
                            chunk_data = parse_cpp_value(data)
                            break
                    
                    if chunk_data:
                        for csv_line in chunk_data:
                            if parsed := parse_csv_line(csv_line):
                                if not parsed['category']:
                                    parsed['category'] = category
                                config_data[category].append(parsed)

        # Print detailed summary
        total_entries = sum(len(entries) for entries in config_data.values())
        logger.info(f"\nDatabase extraction summary:")
        logger.info(f"Total categories: {len(categories)}")
        logger.info(f"Total entries: {total_entries}")
        for category, entries in config_data.items():
            logger.info(f"Category {category}: {len(entries)} entries")
            if entries:
                logger.info(f"First entry: {entries[0]}")
                logger.info(f"Last entry: {entries[-1]}")

    return config_data
