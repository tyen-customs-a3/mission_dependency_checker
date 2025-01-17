import os
import json
import re
import logging
import sqlite3
from typing import Dict, Set, Optional, List, Union, Any
from datetime import datetime
from database_types import ClassEntry
from database_sql import ClassDatabase
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from itertools import islice

logger = logging.getLogger(__name__)

# Remove duplicate ClassEntry class definition since it's now in database_types.py

def parse_class_hierarchy(data: Union[str, Dict[str, Any]]) -> Dict[str, ClassEntry]:
    """Parse class data into ClassEntry objects"""
    classes: Dict[str, ClassEntry] = {}
    
    try:
        # Handle string input (file paths)
        if isinstance(data, str):
            if data.endswith('.ini'):
                return parse_inidbi2_file(data)
            else:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    logger.error("Failed to parse input as JSON")
                    return classes

        # Handle dictionary input
        if isinstance(data, dict):
            if 'class_name' in data:  # Single entry
                return {data['class_name']: ClassEntry(**data)}
            elif isinstance(next(iter(data.values()), None), dict):  # Multiple entries
                return {k: ClassEntry(**v) for k, v in data.items()}

        # Handle list input
        if isinstance(data, list):
            return {entry['class_name']: ClassEntry(**entry) 
                   for entry in data if isinstance(entry, dict)}

    except Exception as e:
        logger.error(f"Error in parse_class_hierarchy: {e}")

    return classes

def batch_generator(iterable, batch_size=1000):
    """Helper to create batches from an iterable"""
    iterator = iter(iterable)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch

def parse_inidbi2_file(file_path: str) -> Dict[str, Set[ClassEntry]]:
    """Parse an INIDBI2 format ini file into ClassEntry objects, grouped by source"""
    db = ClassDatabase(':memory:')
    entries = []
    processed_count = 0
    
    try:
        # First pass: group entries by category for batch processing
        with open(file_path, 'r', encoding='utf-8', buffering=1024*1024) as f:
            current_section = None
            
            for line in f:
                line = line.strip()
                if not line or line.startswith(';'):
                    continue
                
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    continue
                
                if '=' not in line or not current_section or not current_section.startswith('CategoryData_'):
                    continue
                
                category = current_section[12:]
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Check if key is a number (index)
                if key.isdigit() or key == '':
                    try:
                        # Split the CSV value and clean each part
                        parts = [p.strip(' "') for p in value.split(',')]
                        if len(parts) >= 5:  # Ensure minimum required fields
                            entry = ClassEntry(
                                class_name=parts[0],
                                source=parts[1],
                                category=category,
                                parent=parts[3] if parts[3] and parts[3] != '""' else None,
                                inherits_from=parts[4] if parts[4] and parts[4] != '""' else None,
                                is_simple_object=parts[5].lower() == 'true' if len(parts) > 5 else False,
                                num_properties=int(parts[6]) if len(parts) > 6 and parts[6].isdigit() else 0,
                                scope=int(parts[7]) if len(parts) > 7 and parts[7].isdigit() else 0,
                                model=parts[8] if len(parts) > 8 and parts[8] != '""' else None,
                                display_name=parts[9] if len(parts) > 9 and parts[9] != '""' else None
                            )
                            entries.append(entry)
                            
                            if len(entries) >= 1000:
                                db.add_class_entries(entries)
                                processed_count += len(entries)
                                entries = []
                                logger.info(f"Processed {processed_count:,} entries...")
                    except Exception as e:
                        logger.debug(f"Error parsing line: {line} - {e}")
                        continue
        
        # Add remaining entries
        if entries:
            db.add_class_entries(entries)
            processed_count += len(entries)
        
        logger.info(f"Total processed entries: {processed_count}")
        return db.get_class_entries()
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        raise
