import os
import csv
import logging
from typing import Dict, Set, List
from datetime import datetime
from database_class import ClassEntry

logger = logging.getLogger(__name__)

def write_debug_class_dump(database: Dict[str, Set[ClassEntry]], output_dir: str, task_name: str) -> None:
    """Write a human-readable dump of the class database in a table format"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"class_dump_{task_name}_{timestamp}.txt")
    
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
        
        # Write data rows
        all_entries = []
        for source, entries in database.items():
            all_entries.extend((entry, source) for entry in entries)
        
        # Sort by source and then class name
        for entry, source in sorted(all_entries, key=lambda x: (x[1], x[0].class_name)):
            # Truncate long strings and add ellipsis if needed
            class_name = entry.class_name[:col_widths['class']-3] + "..." if len(entry.class_name) > col_widths['class'] else entry.class_name
            category = entry.category[:col_widths['category']-3] + "..." if len(entry.category) > col_widths['category'] else entry.category
            source_str = source[:col_widths['source']-3] + "..." if len(source) > col_widths['source'] else source
            parent = (entry.parent or "")[:col_widths['parent']-3] + "..." if entry.parent and len(entry.parent) > col_widths['parent'] else (entry.parent or "")
            
            line = (
                f"{class_name:<{col_widths['class']}} "
                f"{category:<{col_widths['category']}} "
                f"{source_str:<{col_widths['source']}} "
                f"{parent:<{col_widths['parent']}}\n"
            )
            f.write(line)
    
    logger.info(f"Class database dump written to: {output_file}")

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
