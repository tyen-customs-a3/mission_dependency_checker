import os
import json
import re
import logging
import sqlite3
from typing import Dict, Set, Optional, List, Union, Any
from datetime import datetime
from database_types import ClassEntry
from database_sql import ClassDatabase

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

def parse_inidbi2_file(file_path: str) -> Dict[str, Set[ClassEntry]]:
    """Parse an INIDBI2 format ini file into ClassEntry objects, grouped by source"""
    db = ClassDatabase(':memory:')
    entries = []
    current_section = None
    processed_count = 0
    result_by_source: Dict[str, Set[ClassEntry]] = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8', buffering=1024*1024) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(';'):
                    continue
                
                if line.startswith('[') and line.endswith(']'):
                    # Process any pending entries when section changes
                    if entries:
                        db.add_class_entries(entries)
                        processed_count += len(entries)
                        entries = []
                    current_section = line[1:-1]
                    continue
                
                if '=' not in line or not current_section:
                    continue
                
                if current_section.startswith('CategoryData_'):
                    category = current_section[12:]
                    key, value = line.split('=', 1)
                    
                    if key.strip() == 'header':
                        continue
                        
                    try:
                        parts = [p.strip(' "') for p in value.strip().split(',')]
                        if len(parts) >= 4:
                            entries.append(ClassEntry(
                                class_name=parts[0],
                                source=parts[1],
                                category=category,
                                parent=parts[3] if parts[3] and parts[3] != '""' else None
                            ))
                            
                            if len(entries) >= 1000:
                                db.add_class_entries(entries)
                                processed_count += len(entries)
                                entries = []
                                logger.info(f"Processed {processed_count:,} entries...")
                                
                    except Exception as e:
                        logger.debug(f"Error parsing line: {line} - {e}")
        
        # Add remaining entries
        if entries:
            db.add_class_entries(entries)
            processed_count += len(entries)
        
        # Get results and properly organize by source
        raw_entries = db.get_class_entries()
        
        # raw_entries is already grouped by source, just return it
        return raw_entries
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        raise
