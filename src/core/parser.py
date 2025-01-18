from pathlib import Path
from typing import Set, Dict, List, Optional, Tuple, Generator, DefaultDict
from collections import defaultdict
import re
import csv
import logging
from datetime import datetime
from .models import ClassDef, InidbiClass
from .base_parser import BaseParser

logger = logging.getLogger(__name__)

class ClassParser(BaseParser):
    """Unified parser for all class definition formats"""
    
    def __init__(self):
        super().__init__()
        # Regular class parsing patterns
        self._class_pattern = re.compile(
            r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        )
        self._config_pattern = re.compile(r'#include\s+"([^"]+)"')
        
        # INIDBI2 patterns
        self._category_pattern = re.compile(r'\[CategoryData_(\w+)\]')
        self._header_pattern = re.compile(r'header\s*=\\s*(.+)')

        # Add tracking for class relationships
        self._inheritance_graph: DefaultDict[str, Set[str]] = defaultdict(set)
        self._class_sources: Dict[str, Set[str]] = defaultdict(set)

    def _find_included_files(self, content: str, base_path: Path) -> Generator[Path, None, None]:
        """Find and resolve #include statements"""
        for match in self._config_pattern.finditer(content):
            include_path = match.group(1)
            resolved_path = base_path.parent / include_path
            if resolved_path.exists():
                yield resolved_path

    def parse_file(self, path: Path) -> Set[ClassDef]:
        """Parse class file and extract definitions"""
        classes = set()
        
        try:
            content = path.read_text(encoding='utf-8')
            source = path.stem
            classes.update(self._parse_content(content, source))
                
            # Use base class inheritance validation
            available = classes | set(self._get_existing_classes())
            for class_def in classes:
                self.validate_inheritance(class_def, available)
                
        except Exception as e:
            logger.error(f"Failed to parse {path}: {e}")
            
        return classes

    def _parse_content(self, content: str, source: str) -> Set[ClassDef]:
        """Parse content based on format detection"""
        if '[CategoryData_' in content:
            return self._parse_inidbi_content(content, source)
        return self._parse_class_content(content, source)

    def _parse_class_content(self, content: str, source: str) -> Set[ClassDef]:
        """Parse regular class definitions including nested classes"""
        classes = set()
        
        for match in self._class_pattern.finditer(content):
            name, parent, body = match.groups()
            
            # Extract properties and nested content
            properties = {}
            nested_content = ""
            nested_level = 0
            
            for line in body.split(";"):
                line = line.strip()
                if not line:
                    continue
                    
                if "class" in line:
                    nested_content += line + ";"
                    nested_level += line.count("{")
                    nested_level -= line.count("}")
                elif nested_level > 0:
                    nested_content += line + ";"
                    nested_level += line.count("{")
                    nested_level -= line.count("}")
                elif "=" in line:
                    key, value = line.split("=", 1)
                    properties[key.strip()] = value.strip()
            
            # Create main class
            class_def = ClassDef(name=name, parent=parent, properties=properties, source=source)
            classes.add(class_def)
            
            # Handle nested classes
            if nested_content:
                nested_matches = self._class_pattern.finditer(nested_content)
                for nested_match in nested_matches:
                    nested_name, nested_parent, nested_body = nested_match.groups()
                    nested_properties, _ = self._extract_properties_and_nested(nested_body)
                    
                    nested_class = ClassDef(
                        name=f"{name}.{nested_name}",
                        parent=name,
                        properties=nested_properties,
                        source=source
                    )
                    classes.add(nested_class)
                    class_def.nested_classes.add(nested_class)
                    
            # Update inheritance tracking
            if parent:
                self._inheritance_graph[parent].add(name)
            self._class_sources[name].add(source)
                
        return classes

    def _parse_inidbi_content(self, content: str, source: str) -> Set[ClassDef]:
        """Parse INIDBI2 format content"""
        classes = set()
        current_category = None
        
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(';'):
                continue
                
            if cat_match := self._category_pattern.match(line):
                current_category = cat_match.group(1)
                continue
                
            if current_category and '=' in line:
                if class_def := self._parse_inidbi_line(line, current_category, source):
                    classes.add(class_def)
                    
        return classes

    def _create_class_def(self, name: str, parent: str, body: str, source: str) -> ClassDef:
        """Create class definition with properties"""
        properties, _ = self._extract_properties_and_nested(body)
        return ClassDef(name=name, parent=parent, properties=properties, source=source)

    def _parse_inidbi_line(self, line: str, category: str, source: str) -> Optional[ClassDef]:
        """Parse INIDBI2 format line"""
        try:
            idx, data = line.split('=', 1)
            fields = next(csv.reader([data]))
            if len(fields) < 8:
                return None
                
            name, mod, _, parent, inherits, is_simple, num_props, scope, *rest = fields
            model = rest[0] if rest else None
            display_name = rest[1] if len(rest) > 1 else None
            
            meta = InidbiClass(
                category=category,
                source_mod=mod,
                properties={},
                inherits_from=inherits if inherits else None,
                is_simple_object=is_simple.lower() == 'true',
                num_properties=int(num_props) if num_props.isdigit() else 0,
                scope=int(scope) if scope.isdigit() else 0,
                model=model,
                display_name=display_name
            )
            
            return ClassDef(
                name=name,
                parent=parent if parent else None,
                source=mod,
                properties={},
                inidbi_meta=meta
            )
            
        except Exception as e:
            logger.error(f"Error parsing INIDBI line: {line} - {e}")
            return None

    def _extract_properties_and_nested(self, body: str) -> Tuple[Dict[str, str], str]:
        """
        Extract properties and identify nested class content
        
        Returns:
            Tuple of (properties dict, nested class content)
        """
        properties = {}
        nested_content = ""
        
        # Track nested class brackets
        bracket_level = 0
        current_property = []
        
        for line in body.split(";"):
            line = line.strip()
            if not line:
                continue
                
            # Track nested class definitions
            bracket_level += line.count("{") - line.count("}")
            
            if bracket_level > 0 or (bracket_level == 0 and "{" in line):
                nested_content += line + ";"
            elif "=" in line and bracket_level == 0:
                key, value = line.split("=", 1)
                properties[key.strip()] = value.strip()
                
        return properties, nested_content

    def validate_class(self, class_def: ClassDef, available_classes: Set[ClassDef]) -> List[str]:
        """Enhanced validation including INIDBI2 specific checks"""
        warnings = []
        
        # Existing validation
        warnings.extend(super().validate_class(class_def, available_classes))
        
        # INIDBI2 specific validation
        if class_def.inidbi_meta:
            # Check inheritance consistency 
            if (class_def.parent != class_def.inidbi_meta.inherits_from and 
                class_def.inidbi_meta.inherits_from is not None):
                warnings.append(
                    f"Inheritance mismatch for {class_def.name}: "
                    f"parent is '{class_def.parent}' but inheritsFrom is "
                    f"'{class_def.inidbi_meta.inherits_from}'"
                )
            
            # Validate scope
            if class_def.inidbi_meta.scope not in {0, 1, 2}:
                warnings.append(f"Invalid scope {class_def.inidbi_meta.scope} for {class_def.name}")
            
            # Check model path if specified
            if class_def.inidbi_meta.model:
                if not any(class_def.inidbi_meta.model.endswith(ext) 
                          for ext in {'.p3d', '.paa'}):
                    warnings.append(f"Invalid model path format: {class_def.inidbi_meta.model}")
        
        return warnings

    def build_inheritance_graph(self, classes: Set[ClassDef]) -> None:
        """
        Build complete inheritance graph from class definitions
        
        Args:
            classes: Set of class definitions to analyze
        """
        for class_def in classes:
            if class_def.parent:
                self._inheritance_graph[class_def.parent].add(class_def.name)
            self._class_sources[class_def.name].add(class_def.source)

    def get_derived_classes(self, base_class: str) -> Set[str]:
        """
        Get all classes that inherit from given base class
        
        Args:
            base_class: Name of base class to check
            
        Returns:
            Set of class names that inherit from base_class
        """
        derived = set()
        to_process = {base_class}
        
        while to_process:
            current = to_process.pop()
            children = self._inheritance_graph[current]
            new_children = children - derived
            derived.update(new_children)
            to_process.update(new_children)
            
        return derived

    def analyze_class_usage(self, classes: Set[ClassDef]) -> Dict[str, Dict[str, int]]:
        """Analyze class usage and references"""
        usage_stats = defaultdict(lambda: defaultdict(int))

        for class_def in classes:
            # Track inheritance
            if class_def.parent:
                usage_stats[class_def.parent]["child_count"] += 1
            # Track property references more thoroughly
            for prop_value in class_def.properties.values():
                # Clean and check both bare and quoted values
                value = str(prop_value).strip()
                clean_value = value.strip('"\'')
                
                # Check if property value references a known class
                for cls in classes:
                    if cls.name == clean_value:
                        usage_stats[clean_value]["reference_count"] += 1
                        break

        return usage_stats

    def validate_class_hierarchy(self, class_def: ClassDef, available: Set[ClassDef]) -> List[str]:
        """Validate class hierarchy and detect circular inheritance"""
        warnings = []
        visited = set()
        inheritance_chain = []

        # Ensure the class_def is included
        full_set = available | {class_def}

        def check_inheritance_chain(current: ClassDef) -> None:
            if current.name in inheritance_chain:
                cycle = inheritance_chain[inheritance_chain.index(current.name):] + [current.name]
                warnings.append(f"Circular inheritance detected: {' -> '.join(cycle)}")
                return

            if current.name in visited:
                return

            visited.add(current.name)
            inheritance_chain.append(current.name)

            if current.parent:
                parent_def = next((c for c in full_set if c.name == current.parent), None)
                if parent_def:
                    check_inheritance_chain(parent_def)
                else:
                    warnings.append(f"Missing parent class '{current.parent}' for '{current.name}'")

            inheritance_chain.pop()

        check_inheritance_chain(class_def)
        return warnings

    def _is_compatible_override(self, parent_value: str, child_value: str) -> bool:
        """Check if property override is type-compatible"""
        # Basic type compatibility check - could be expanded
        def get_value_type(val: str) -> str:
            if val.startswith('"'):
                return "string"
            if val.replace(".", "").isdigit():
                return "number"
            return "other"
            
        return get_value_type(parent_value) == get_value_type(child_value)

    def get_inheritance_chain(self, class_name: str) -> List[ClassDef]:
        """Get complete inheritance chain for a class"""
        chain = []
        visited = set()
        
        def _get_parent_recursive(current: ClassDef):
            if current.name in visited:
                return
            visited.add(current.name)
            chain.append(current)
            
            if current.parent:
                parent = next((c for c in self._get_existing_classes() 
                             if c.name == current.parent), None)
                if parent:
                    _get_parent_recursive(parent)
        
        start_class = next((c for c in self._get_existing_classes() 
                           if c.name == class_name), None)
        if start_class:
            _get_parent_recursive(start_class)
            
        return chain

class InidbiParser(BaseParser):
    """Parser for INIDBI2 format files"""
    
    def __init__(self):
        super().__init__()
        self._category_pattern = re.compile(r'\[CategoryData_(\w+)\]')
        self._header_pattern = re.compile(r'header="([^"]+)"')
        self._row_pattern = re.compile(r'(\d+)="([^"]+)"')
        # Define default header fields
        self._default_headers = [
            "ClassName", "Source", "Category", "Parent",
            "InheritsFrom", "IsSimpleObject", "NumProperties", 
            "Scope", "Model", "DisplayName"
        ]

    def parse_file(self, path: Path) -> Set[ClassDef]:
        """Parse INIDBI2 format file and return flat set of classes"""
        try:
            classes = set()
            current_category = None
            header_fields = self._default_headers  # Use default headers
            
            content = path.read_text(encoding='utf-8', errors='ignore')
            
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith(';'):
                    continue
                    
                # Check for header definition
                if line.startswith('header='):
                    try:
                        header_str = line.split('=', 1)[1].strip('"')
                        header_fields = [f.strip() for f in header_str.split(',')]
                        continue
                    except Exception:
                        header_fields = self._default_headers
                    
                # Handle category headers    
                if line.startswith('['):
                    if cat_match := self._category_pattern.match(line):
                        current_category = cat_match.group(1)
                    continue
                    
                # Parse data lines
                if '=' in line and current_category:
                    try:
                        _, data = line.split('=', 1)
                        if class_def := self._parse_class_data(data.strip('"'), current_category, header_fields):
                            classes.add(class_def)
                    except Exception as e:
                        logger.error(f"Error parsing line '{line}': {e}")
            
            logger.info(f"Parsed {len(classes)} classes from {path}")
            return classes
            
        except Exception as e:
            logger.error(f"Failed to parse INIDBI file {path}: {e}")
            return set()

    def _parse_class_data(self, data: str, category: str, header_fields: List[str]) -> Optional[ClassDef]:
        """Parse class data from CSV format with flexible headers"""
        try:
            fields = next(csv.reader([data]))
            if len(fields) < 5:  # Minimum required fields
                return None
                
            # Create dict with default values for missing fields
            data_dict = dict(zip(self._default_headers, [""] * len(self._default_headers)))
            # Update with actual values
            data_dict.update(dict(zip(header_fields[:len(fields)], fields)))
            
            meta = InidbiClass(
                category=category,
                source_mod=data_dict.get("Source", "unknown"),
                properties={},
                inherits_from=data_dict.get("InheritsFrom"),
                is_simple_object=data_dict.get("IsSimpleObject", "false").lower() == "true",
                num_properties=int(data_dict.get("NumProperties", 0)),
                scope=int(data_dict.get("Scope", 0)),
                model=data_dict.get("Model"),
                display_name=data_dict.get("DisplayName")
            )
            
            return ClassDef(
                name=data_dict.get("ClassName", "Unknown"),
                parent=data_dict.get("Parent"),
                source=data_dict.get("Source", "unknown"),
                properties={},
                inidbi_meta=meta
            )
            
        except Exception as e:
            logger.error(f"Error parsing INIDBI data: {data} - {e}")
            return None

# ...existing code...
