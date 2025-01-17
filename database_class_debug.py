import os
import csv
import logging
from typing import Dict, Set, List
from datetime import datetime
from database_class import ClassEntry

logger = logging.getLogger(__name__)

# Store timestamp per task to reuse across function calls
_task_folders = {}

def _get_debug_folder(output_dir: str, task_name: str) -> str:
    """Create and return debug folder for task, ensuring same timestamp is used"""
    if task_name not in _task_folders:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        _task_folders[task_name] = os.path.join(output_dir, f"{task_name}_{timestamp}")
        os.makedirs(_task_folders[task_name], exist_ok=True)
    return _task_folders[task_name]

def write_debug_class_dump(database: Dict[str, Set[ClassEntry]], output_dir: str, task_name: str) -> None:
    """Write a human-readable dump of the class database in a table format"""
    debug_folder = _get_debug_folder(output_dir, task_name)
    output_file = os.path.join(debug_folder, "class_dump.txt")
    
    # Define column widths
    col_widths = {
        'class': 40,
        'category': 20,
        'source': 25,
        'parent': 40
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"CLASS DATABASE DUMP - {task_name}\n")
        f.write("=" * 50 + "\n\n")
        
        # Write header
        header = (
            f"{'Class Name':<{col_widths['class']}} "
            f"{'Category':<{col_widths['category']}} "
            f"{'Source':<{col_widths['source']}} "
            f"{'Parent':<{col_widths['parent']}}\n"
        )
        f.write(header)
        f.write("-" * (sum(col_widths.values()) + 5) + "\n")
        
        # Write data rows - collect all entries
        all_entries = []
        for entries in database.values():
            all_entries.extend(entries)  # Sets are iterable
        
        # Sort entries by source and class name using ClassEntry's comparison methods
        for entry in sorted(all_entries):
            # Truncate long strings and add ellipsis if needed
            class_name = entry.class_name[:col_widths['class']-3] + "..." if len(entry.class_name) > col_widths['class'] else entry.class_name
            category = entry.category[:col_widths['category']-3] + "..." if len(entry.category) > col_widths['category'] else entry.category
            source_str = entry.source[:col_widths['source']-3] + "..." if len(entry.source) > col_widths['source'] else entry.source
            parent = (entry.parent or "")[:col_widths['parent']-3] + "..." if entry.parent and len(entry.parent) > col_widths['parent'] else (entry.parent or "")
            
            line = (
                f"{class_name:<{col_widths['class']}} "
                f"{category:<{col_widths['category']}} "
                f"{source_str:<{col_widths['source']}} "
                f"{parent:<{col_widths['parent']}}\n"
            )
            f.write(line)
    
    logger.info(f"Class database dump written to: {output_file}")

def write_debug_class_csv(database: Dict[str, ClassEntry], output_dir: str, task_name: str) -> None:
    """Write parsed class database to debug CSV file"""
    debug_folder = _get_debug_folder(output_dir, task_name)
    output_file = os.path.join(debug_folder, "class_database.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar='\\')
        writer.writerow(['ClassName', 'Source', 'Category', 'Parent'])
        
        # Write entries directly from the dictionary
        for entry in sorted(database.values()):
            writer.writerow([
                entry.class_name,
                entry.source,
                entry.category,
                entry.parent or ''  # Handle None case
            ])
    
    logger.info(f"Class database CSV written to: {output_file}")
