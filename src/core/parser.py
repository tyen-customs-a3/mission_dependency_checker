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

        # Loadout-specific patterns
        self._list_macro_pattern = re.compile(r'LIST_(\d+)\("([^"]+)"\)')
        self._equipment_arrays = {
            'primaryWeapon', 'secondaryWeapon', 'handgunWeapon',
            'uniform', 'vest', 'backpack', 'magazines', 'items',
            'linkedItems', 'sidearmWeapon', 'attachment', 'scope',
            'silencer', 'bipod', 'backpackItems'  # Added backpackItems
        }
        self._processed_classes = set()  # Add set to track unique class names

        # Add ignore patterns
        self._ignore_patterns = [
            re.compile(r'.*\.varInit$'),
            re.compile(r'LIST_\d+\(""\)')  # Fix pattern
        ]

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
        """Parse class definitions with better nested class handling"""
        classes = set()
        
        # Find all top-level class definitions first
        matches = list(self._class_pattern.finditer(content))
        
        for match in matches:
            name, parent, body = match.groups()
            name = name.strip()
            
            # Skip if this is an empty or invalid class name
            if not name or name.isdigit():
                continue
                    
            properties = {}
            nested_classes = []
            current_line = []
            bracket_level = 0
            in_nested = False
            
            # Process body line by line
            for line in body.split(';'):
                line = line.strip()
                if not line:
                    continue
                    
                # Handle nested class definitions
                if 'class' in line and not line.startswith('//'):
                    in_nested = True
                    current_line = [line]
                    bracket_level = line.count('{')
                    continue
                        
                if in_nested:
                    current_line.append(line)
                    bracket_level += line.count('{') - line.count('}')
                    if bracket_level == 0:
                        nested_content = ';'.join(current_line)
                        nested_matches = self._class_pattern.finditer(nested_content)
                        for nested_match in nested_matches:
                            nested_name, nested_parent, nested_body = nested_match.groups()
                            if nested_name and not nested_name.isdigit():
                                nested_classes.extend(self._parse_class_content(nested_content, source))
                        in_nested = False
                        continue
                        
                # Handle properties
                if '=' in line and not in_nested:
                    key, value = line.split('=', 1)
                    properties[key.strip()] = value.strip()
            
            # Create the main class
            class_def = ClassDef(
                name=name,
                parent=parent.strip() if parent else None,
                properties=properties,
                source=source
            )
            classes.add(class_def)
            
            # Extract equipment references from properties
            self._extract_equipment_references(properties, classes, source)
            
            # Process nested classes
            for nested in nested_classes:
                if '.' not in nested.name:
                    nested.name = f"{name}.{nested.name}"
                classes.add(nested)

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
            fields = next(csv.reader([data.strip('"')]))  # Strip quotes from entire data
            if len(fields) < 8:
                return None
                
            name, mod, _, parent, inherits, is_simple, num_props, scope, *rest = fields
            model = rest[0] if rest else None
            display_name = rest[1] if len(rest) > 1 else None
            
            meta = InidbiClass(
                category=category,
                source_mod=mod,  # Store original mod name
                properties={},
                inherits_from=inherits if inherits else None,
                is_simple_object=is_simple.lower() == 'true',
                num_properties=int(num_props) if num_props.isdigit() else 0,
                scope=int(scope) if scope.isdigit() else 0,
                model=model,
                display_name=display_name
            )
            
            class_def = ClassDef(
                name=name,
                parent=parent if parent else None,
                source=mod,  # Use mod as source directly
                properties={},
                inidbi_meta=meta
            )
            
            # Add to class sources tracking
            self._class_sources[name].add(mod)
            
            return class_def
            
        except Exception as e:
            logger.error(f"Error parsing INIDBI line: {line} - {e}")
            return None

    def _extract_properties_and_nested(self, body: str) -> Tuple[Dict[str, str], str]:
        """Extract properties and nested content with improved array handling"""
        properties = {}
        nested_content = ""
        bracket_level = 0
        in_array = False
        current_array = []

        for line in body.split(";"):
            line = line.strip()
            if not line:
                continue

            # Handle arrays explicitly
            if line.endswith("[]=") or line.endswith("[] ="):
                in_array = True
                current_array = []
                continue

            if in_array:
                if line.startswith("{"):
                    current_array = []
                elif line.startswith("}"):
                    # Join array items and save property
                    array_key = next((k for k in properties if k.endswith("[]")), None)
                    if array_key:
                        properties[array_key] = "{" + ",".join(current_array) + "}"
                    in_array = False
                elif line:
                    # Clean and add array item
                    item = line.strip(",").strip()
                    if item:
                        current_array.append(item)
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

    def _extract_equipment_references(self, properties: Dict[str, str], classes: Set[ClassDef], source: str):
        """Extract equipment references with improved array handling"""
        def clean_item_name(item: str) -> Optional[str]:
            """Clean up item name by removing comment markers"""
            # Strip any comment markers and handle trailing comments
            item = item.strip()

            # Handle // comments first
            if '//' in item:
                item = item.split('//')[0].strip()

            # Handle /* */ comments
            if '/*' in item and '*/' in item:
                comment_start = item.find('/*')
                comment_end = item.find('*/') + 2
                item = (item[:comment_start] + item[comment_end:]).strip()
            elif item.startswith('/*'):
                item = item[2:].strip()
            elif item.endswith('*/'):
                item = item[:-2].strip()

            # Handle quote marks if present
            if item.startswith('"') and item.endswith('"'):
                item = item[1:-1].strip()
            
            # Skip empty or all-comment items
            if not item or item.startswith('//') or item.startswith('/*'):
                return None
                
            # Skip empty LIST macros
            if re.match(r'LIST_\d+\(""\)', item) or re.match(r'LIST_\d+\("")', item):
                return None
                
            # Skip .varInit suffixes
            if item.endswith('.varInit'):
                item = item[:-8]  # Remove .varInit suffix

            # Clean up array format that has numeric values after class names
            if ',' in item:
                parts = item.split(',')
                item = parts[0].strip()

            # Handle string literals with trailing values
            if '"' in item:
                item = item.split('"')[1]  # Get content between quotes

            # Skip pure numeric values
            if item.replace(".", "").isdigit():
                return None
                
            # Remove any trailing whitespace/commas
            item = item.rstrip(',').strip()
            
            return item

        def parse_array_content(content: str) -> List[str]:
            """Parse array content handling class name + value pairs"""
            items = []
            parts = content.split(',')
            i = 0
            while i < len(parts):
                part = parts[i].strip()
                # Skip empty parts
                if not part:
                    i += 1
                    continue
                    
                # If it's a quoted string, it's likely a class name
                if part.startswith('"'):
                    class_name = part.strip('"')
                    if class_name:
                        items.append(class_name)
                    # Skip the next part which should be the numeric value
                    i += 2
                else:
                    # Handle non-quoted items
                    if not part.replace(".", "").isdigit():
                        items.append(part)
                    i += 1
            return items

        for key, value in properties.items():
            key = key.strip('[]')
            if key not in self._equipment_arrays:
                continue

            # Clean up array value
            array_value = value.strip()
            if not array_value:
                continue

            # Handle both single-item and multi-item arrays
            items = []
            if array_value.startswith('{'):
                # Split array content by commas while preserving quoted strings and comments
                content = array_value.strip('{}')
                current = []
                in_quotes = False
                in_comment = False
                comment_type = None  # Could be '//' or '/*'
                
                for i, char in enumerate(content):
                    if not in_comment:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif not in_quotes and char == '/' and i + 1 < len(content) and content[i+1] == '/':
                            in_comment = True
                            comment_type = '//'
                            current.append(char)
                        elif not in_quotes and char == '/' and i + 1 < len(content) and content[i+1] == '*':
                            in_comment = True
                            comment_type = '/*'
                            current.append(char)
                        elif char == ',' and not in_quotes:
                            item = ''.join(current).strip()
                            if clean_name := clean_item_name(item):
                                items.append(clean_name)
                            current = []
                            continue
                        current.append(char)
                    else:
                        current.append(char)
                        if comment_type == '//' and char == '\n':
                            in_comment = False
                        elif comment_type == '/*' and char == '/' and current[-2] == '*':
                            in_comment = False
                
                # Add last item if present
                if current:
                    item = ''.join(current).strip()
                    if clean_name := clean_item_name(item):
                        items.append(clean_name)
            else:
                # Handle single item
                if clean_name := clean_item_name(array_value):
                    items.append(clean_name)

            # Process each item - modified to check for duplicates
            for item in items:
                # Handle LIST macro items
                if list_match := re.match(r'LIST_(\d+)\("([^"]+)"\)', item):
                    count = int(list_match.group(1))
                    class_name = list_match.group(2)
                    if class_name and class_name not in self._processed_classes:
                        self._processed_classes.add(class_name)
                        ref_class = ClassDef(
                            name=class_name,
                            parent=None,
                            source=source,
                            properties={"list_count": str(count)},
                            is_reference=True
                        )
                        classes.add(ref_class)
                else:
                    # Regular items are already cleaned by clean_item_name
                    if not item.isdigit() and item not in self._processed_classes:  # Skip pure number values
                        self._processed_classes.add(item)
                        ref_class = ClassDef(
                            name=item,
                            parent=None,
                            source=source,
                            properties={},
                            is_reference=True
                        )
                        classes.add(ref_class)

class InidbiParser(BaseParser):
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
                    current_category = line[13:-1]  # Remove brackets
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
                        data = data.strip().strip('"')  # Strip outer quotes
                        fields = next(csv.reader([data]))  # Use csv parser for field splitting
                        
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
