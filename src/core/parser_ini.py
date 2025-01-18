from pathlib import Path
from typing import Set, Dict, List, Optional, Tuple, Generator, DefaultDict
from collections import defaultdict
import re
import csv
import logging
from .models import ClassDef, InidbiClass
from .base_parser import BaseParser

logger = logging.getLogger(__name__)

class InidbiParser(BaseParser):
    """Base class for parsing INIDBI format class definitions"""
    def __init__(self):
        super().__init__()
        self._default_headers = [
            "ClassName", "Source", "Category", "Parent",
            "InheritsFrom", "IsSimpleObject", "NumProperties", 
            "Scope", "Model", "DisplayName"
        ]
        self._sources = set()
        self._class_lookup: Dict[str, ClassDef] = {}

    def parse_file(self, path: Path) -> Dict[str, Set[ClassDef]]:
        """Parse INIDBI format with proper quote handling"""
        try:
            classes_by_source = defaultdict(set)
            self._class_lookup.clear()
            self._sources.clear()
            
            current_category = None
            header_fields = self._default_headers
            
            lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith(';'):
                    continue

                # Handle category headers
                if line.startswith('[CategoryData_'):
                    current_category = line[13:-1]
                    continue

                # Handle header line
                if line.startswith('header='):
                    header_line = line[7:].strip('"')
                    header_fields = next(csv.reader([header_line]))
                    header_fields = [f.strip() for f in header_fields]
                    continue

                # Handle data lines
                if current_category and '=' in line:
                    if line.startswith('header='):
                        continue
                        
                    try:
                        idx, data = line.split('=', 1)
                        data = data.strip().strip('"')
                        fields = next(csv.reader([data]))
                        
                        if class_def := self._create_class(fields, current_category, header_fields):
                            source = class_def.source
                            classes_by_source[source].add(class_def)
                            self._sources.add(source)
                            self._class_lookup[class_def.name] = class_def
                            
                    except Exception as e:
                        logger.debug(f"Skipping malformed line: {line} - {e}")
                        continue

            logger.info(f"Parsed {sum(len(classes) for classes in classes_by_source.values())} "
                       f"total classes from {len(classes_by_source)} sources")
                       
            return dict(classes_by_source)
            
        except Exception as e:
            logger.error(f"Failed to parse INIDBI file {path}: {e}")
            return {}

    def _create_class(self, fields: List[str], category: str, headers: List[str]) -> Optional[ClassDef]:
        """Fixed class creation logic"""
        try:
            # Ensure we have minimum required fields
            if len(fields) < 3:  # Need at least classname, source, category
                return None
                
            # Map fields to headers, handling any missing fields
            data = {}
            for i, header in enumerate(headers):
                if i < len(fields):
                    data[header] = fields[i].strip()
                else:
                    data[header] = ""
            
            name = data.get("ClassName", "").strip()
            if not name:  # Skip if no class name
                return None
                
            source = data.get("Source", "unknown").strip()
            parent = data.get("Parent", "").strip() or None
            
            # Handle empty or invalid fields gracefully
            try:
                num_properties = int(data.get("NumProperties", 0))
            except ValueError:
                num_properties = 0

            try:
                scope = int(data.get("Scope", 0))
            except ValueError:
                scope = 0

            meta = InidbiClass(
                category=category,
                source_mod=source,
                properties=data,  # Store all fields in properties
                inherits_from=data.get("InheritsFrom", "").strip() or None,
                is_simple_object=data.get("IsSimpleObject", "false").lower() == "true",
                num_properties=num_properties,
                scope=scope,
                model=data.get("Model", "").strip(),
                display_name=data.get("DisplayName", "").strip()
            )
            
            return ClassDef(
                name=name,
                parent=parent,
                source=source,
                properties=data,  # Include all fields in properties
                inidbi_meta=meta
            )
            
        except Exception as e:
            logger.debug(f"Error creating class from fields: {fields} - {e}")
            return None

    def get_class(self, class_name: str) -> Optional[ClassDef]:
        """Get class definition by exact name"""
        return self._class_lookup.get(class_name)

    def find_classes(self, name_pattern: str) -> Set[ClassDef]:
        """Find classes matching a pattern"""
        pattern = re.compile(name_pattern)
        return {
            cls for cls in self._class_lookup.values()
            if pattern.match(cls.name)
        }
