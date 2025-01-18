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
        # Updated regex to better handle nested braces and parentheses
        self._class_pattern = re.compile(
            r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*({[^{}]*(?:{[^{}]*}[^{}]*)*})',
            re.MULTILINE | re.DOTALL
        )
        self._config_pattern = re.compile(r'#include\s+"([^"]+)"')
        
        # INIDBI2 patterns
        self._category_pattern = re.compile(r'\[CategoryData_(\w+)\]')
        self._header_pattern = re.compile(r'header\s*=\\s*(.+)')

        # Add tracking for class relationships
        self._inheritance_graph: DefaultDict[str, Set[str]] = defaultdict(set)
        self._class_sources: Dict[str, Set[str]] = defaultdict(set)

        # Loadout-specific patterns
        self._list_macro_pattern = re.compile(r'LIST_(\d+)\s*\(\s*(["\']?)([^"\'\)]*)\2\s*\)')
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
        # Updated regex to better handle array definitions
        self._array_pattern = re.compile(r'(\w+)\[\]\s*=\\s*({[^}]*}|\[[^\]]*\]|"[^"]*")')
        self._list_macro_pattern = re.compile(r'LIST_(\d+)\s*\(\s*(["\']?)([^"\'\)]*)\2\s*\)')
        # Improve class pattern to handle more formats
        self._class_pattern = re.compile(
            r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*({(?:[^{}]|(?:\{[^{}]*\}))*})',
            re.MULTILINE | re.DOTALL
        )
        # Improved nested class regex
        self._nested_class_pattern = re.compile(
            r'\bclass\s+(\w+)\s*({[^{}]*(?:{[^{}]*}[^{}]*)*})',
            re.MULTILINE | re.DOTALL
        )
        
        # Add mission-specific patterns
        self.mission_parser = MissionParser()
        self.ignore_mission_files = False  # Add control flag
        self.treat_as_mission = True  # Add control flag for mission file parsing

    def _find_included_files(self, content: str, base_path: Path) -> Generator[Path, None, None]:
        """Find and resolve #include statements"""
        for match in self._config_pattern.finditer(content):
            include_path = match.group(1)
            resolved_path = base_path.parent / include_path
            if resolved_path.exists():
                yield resolved_path

    def parse_file(self, path: Path, treat_as_mission: bool = True) -> Set[ClassDef]:
        """
        Parse class file with control over mission parsing
        
        Args:
            path: Path to file to parse
            treat_as_mission: If True, use mission-specific parsing when appropriate
        """
        classes = set()
        
        try:
            content = path.read_text(encoding='utf-8')
            source = path.stem
            
            # Only use mission parsing if enabled and file matches mission patterns
            if treat_as_mission and self.mission_parser.is_mission_file(path):
                classes.update(self.mission_parser.parse_file(path))
            else:
                classes.update(self._parse_content(content, source))
                
            # Validate inheritance for non-mission classes
            available = classes | set(self._get_existing_classes())
            for class_def in classes:
                if not class_def.is_mission_local:
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
        """Parse class definitions with improved error handling"""
        classes = set()
        
        # First verify brace balance
        if not self._verify_balanced_braces(content):
            logger.error(f"Failed to parse {source} due to unbalanced braces")
            # Try to recover by finding complete class definitions
            return self._parse_with_recovery(content, source)

        # Continue with normal parsing
        for match in self._class_pattern.finditer(content):
            try:
                name, parent, body = match.groups()
                name = name.strip()
                
                if not name or name.isdigit():
                    continue
                    
                # Extract properties and nested classes
                properties = {}
                nested_classes = set()
                
                # Clean up body by removing comments and normalizing whitespace
                clean_body = self._clean_class_body(body.strip('{}'))
                
                # Parse nested classes first
                nested_matches = list(self._nested_class_pattern.finditer(clean_body))
                nested_content = clean_body
                
                for nested_match in nested_matches:
                    nested_name, nested_body = nested_match.groups()
                    if nested_name and not nested_name.isdigit():
                        # Create full nested class name
                        full_nested_name = f"{name}.{nested_name}"
                        nested_props = self._extract_properties(nested_body.strip('{}'))
                        
                        nested_class = ClassDef(
                            name=full_nested_name,
                            parent=None,
                            properties=nested_props,
                            source=source
                        )
                        nested_classes.add(nested_class)
                        # Remove nested class content to avoid parsing its properties again
                        nested_content = nested_content.replace(nested_match.group(0), '')
                
                # Parse remaining properties
                properties = self._extract_properties(nested_content)
                
                # Extract equipment references from properties
                self._extract_equipment_references(properties, classes, source)
                
                # Create main class
                class_def = ClassDef(
                    name=name,
                    parent=parent.strip() if parent else None,
                    properties=properties,
                    source=source,
                    nested_classes=nested_classes
                )
                classes.add(class_def)
                classes.update(nested_classes)
                
            except Exception as e:
                logger.error(f"Error parsing class {name} in {source}: {e}")
                continue

        return classes

    def _parse_with_recovery(self, content: str, source: str) -> Set[ClassDef]:
        """Attempt to recover and parse valid class definitions from malformed content"""
        classes = set()
        lines = content.splitlines()
        current_class = []
        brace_count = 0
        in_class = False
        
        for line in lines:
            try:
                stripped = line.strip()
                
                # Skip comments
                if stripped.startswith('//') or stripped.startswith('/*'):
                    continue
                    
                # Track class start
                if stripped.startswith('class ') and not in_class:
                    current_class = [line]
                    brace_count = line.count('{') - line.count('}')
                    in_class = True
                    continue
                    
                if in_class:
                    current_class.append(line)
                    brace_count += line.count('{') - line.count('}')
                    
                    # Check if we've found a complete class definition
                    if brace_count == 0:
                        class_content = '\n'.join(current_class)
                        if match := self._class_pattern.search(class_content):
                            name, parent, body = match.groups()
                            if self._verify_balanced_braces(body):
                                classes.add(ClassDef(
                                    name=name.strip(),
                                    parent=parent.strip() if parent else None,
                                    properties=self._extract_properties(body.strip('{}'))
                                ))
                        current_class = []
                        in_class = False
                        
            except Exception as e:
                logger.debug(f"Recovery parsing error on line: {line}: {e}")
                continue
                
        return classes

    def _verify_balanced_braces(self, content: str) -> bool:
        """Comprehensive brace balance checker with error reporting"""
        stack = []
        in_string = False
        in_comment = False
        comment_type = None
        line_num = 1
        col_num = 0
        
        for i, char in enumerate(content):
            col_num += 1
            if char == '\n':
                line_num += 1
                col_num = 0

            # Handle string literals
            if char == '"' and not in_comment:
                if not in_string or content[i-1] != '\\':
                    in_string = not in_string
                    
            # Handle comments
            elif not in_string:
                if char == '/' and i + 1 < len(content):
                    next_char = content[i + 1]
                    if next_char == '/' and not in_comment:
                        in_comment = True
                        comment_type = '//'
                        i += 2
                        continue
                    elif next_char == '*' and not in_comment:
                        in_comment = True
                        comment_type = '/*'
                        i += 2
                        continue
                        
                elif in_comment:
                    if comment_type == '//' and char == '\n':
                        in_comment = False
                    elif comment_type == '/*' and char == '*' and i + 1 < len(content) and content[i + 1] == '/':
                        in_comment = False
                        i += 2
                        continue
                        
            # Track braces outside strings and comments
            if not in_string and not in_comment:
                if char in '{(':
                    stack.append((char, line_num, col_num))
                elif char in '})':
                    if not stack:
                        logger.error(f"Unexpected closing '{char}' at line {line_num}, column {col_num}")
                        return False
                    opening, open_line, open_col = stack.pop()
                    if (opening == '{' and char != '}') or (opening == '(' and char != ')'):
                        msg = f"Mismatched braces: found '{char}' at line {line_num}, column {col_num} "
                        msg += f"for opening '{opening}' at line {open_line}, column {open_col}"
                        logger.error(msg)
                        return False

        if stack:
            opening, line_num, col_num = stack[-1]
            logger.error(f"Unclosed '{opening}' from line {line_num}, column {col_num}")
            return False
            
        return True

    def _clean_class_body(self, body: str) -> str:
        """Clean class body by removing comments and normalizing whitespace"""
        # Remove /* */ style comments
        body = re.sub(r'/\*.*?\*/', '', body, flags=re.DOTALL)
        
        # Remove // style comments
        body = re.sub(r'//[^\n]*', '', body)
        
        # Normalize whitespace
        body = re.sub(r'\s+', ' ', body)
        
        return body.strip()

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

    def _extract_equipment_references(self, properties: Dict[str, str], 
                                   classes: Set[ClassDef], source: str, 
                                   mission_mode: bool = False):
        """Extract equipment references with mission-aware handling"""
        for key, value in properties.items():
            key = key.strip('[]')
            if key not in self._equipment_arrays:
                continue
                
            # Handle array and single value formats
            if value.startswith('{'):
                content = value.strip('{}')
                items = self._parse_array_items(content)
            else:
                items = [value.strip()]
                
            for item in items:
                item = item.strip().strip('"')
                
                # Handle LIST macro with improved empty detection
                if list_match := self._list_macro_pattern.match(item):
                    count = int(list_match.group(1))
                    content = list_match.group(3)
                    
                    # Skip if content is empty or just whitespace
                    if not content or content.isspace():
                        continue
                        
                    # Skip mission local classes if in mission mode
                    if mission_mode and self._is_mission_local_class(content):
                        continue
                        
                    if content not in self._processed_classes:
                        self._processed_classes.add(content)
                        ref_class = ClassDef(
                            name=content,
                            parent=None,
                            source=source,
                            properties={"list_count": str(count)},
                            is_reference=True,
                            is_mission_local=False
                        )
                        classes.add(ref_class)
                        
                # Handle regular item references
                elif item and not item.isdigit():
                    # Skip local classes in mission mode
                    if mission_mode and self._is_mission_local_class(item):
                        continue
                        
                    if item not in self._processed_classes:
                        self._processed_classes.add(item)
                        ref_class = ClassDef(
                            name=item,
                            parent=None,
                            source=source,
                            properties={},
                            is_reference=True,
                            is_mission_local=False
                        )
                        classes.add(ref_class)

    def _parse_array_items(self, content: str) -> List[str]:
        """Parse array content with improved comma handling"""
        items = []
        current = []
        in_quotes = False
        in_comment = False
        brace_level = 0
        
        i = 0
        while i < len(content):
            char = content[i]
            
            # Handle comments
            if not in_quotes and char == '/' and i + 1 < len(content):
                if content[i + 1] == '/':
                    while i < len(content) and content[i] != '\n':
                        i += 1
                    continue
                elif content[i + 1] == '*':
                    i += 2
                    while i < len(content) and not (content[i-1:i+1] == '*/'):
                        i += 1
                    i += 1
                    continue
            
            # Handle quotes
            if char == '"' and (i == 0 or content[i-1] != '\\'):
                in_quotes = not in_quotes
            
            # Handle braces and commas
            elif not in_quotes:
                if char == '{':
                    brace_level += 1
                elif char == '}':
                    brace_level -= 1
                # Split on comma at top level, ignoring trailing commas
                elif char == ',' and brace_level == 0:
                    item = ''.join(current).strip()
                    # Only add non-empty items
                    if item and not item.isspace():
                        items.append(item)
                    current = []
                    i += 1
                    continue
            
            current.append(char)
            i += 1
            
        # Handle final item, avoiding empty trailing items
        if current:
            item = ''.join(current).strip()
            if item and not item.isspace() and not item.endswith(','):
                items.append(item)
        
        # Clean up items - remove trailing commas and whitespace
        return [item.rstrip(',').strip() for item in items if item.rstrip(',').strip()]

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

class MissionParser(BaseParser):
    """Parser specifically for mission files like loadouts and configs"""
    
    def __init__(self):
        super().__init__()
        # Add patterns needed for parsing
        self._class_pattern = re.compile(
            r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*({[^{}]*(?:{[^{}]*}[^{}]*)*})',
            re.MULTILINE | re.DOTALL
        )
        # Add pattern for #define directives
        self._define_pattern = re.compile(r'#define\s+(\w+)\s+(.+)$', re.MULTILINE)
        
        self._mission_patterns = {
            r'.*loadout\.hpp$',
            r'.*description\.ext$',
            r'.*cfgFunctions\.hpp$',
            r'.*funcs\.hpp$'  # Add pattern for funcs.hpp
        }
        self._mission_patterns = [re.compile(p) for p in self._mission_patterns]
        
        self._known_local_bases = {
            'baseMan',       # Common loadout base class
            'CfgFunctions',  # Functions config
            'CfgSounds',     # Sounds config
            'CfgMusic',      # Music config
            'functions',     # Function category class
        }
        
        self._mission_local_classes = set()
        self._equipment_arrays = {
            'primaryWeapon', 'secondaryWeapon', 'handgunWeapon',
            'uniform', 'vest', 'backpack', 'magazines', 'items',
            'linkedItems', 'sidearmWeapon', 'attachment', 'scope',
            'silencer', 'bipod', 'backpackItems'
        }
        self._list_macro_pattern = re.compile(r'LIST_(\d+)\s*\(\s*(["\']?)([^"\'\)]*)\2\s*\)')
        self._processed_classes = set()
        # Add dictionary to store defines
        self._defines: Dict[str, str] = {}

    def is_mission_file(self, path: Path) -> bool:
        """Check if file is a mission-specific config"""
        return any(p.match(str(path)) for p in self._mission_patterns)

    def parse_file(self, path: Path) -> Set[ClassDef]:
        """Parse mission file and extract only external class references"""
        try:
            content = path.read_text(encoding='utf-8')
            # First process any #define directives
            self._process_defines(content)
            source = path.stem
            return self._parse_mission_content(content, source)
        except Exception as e:
            logger.error(f"Failed to parse mission file {path}: {e}")
            return set()

    def _process_defines(self, content: str):
        """Process #define directives and store them"""
        self._defines.clear()  # Clear existing defines
        for match in self._define_pattern.finditer(content):
            name, value = match.groups()
            # Store the define, stripping any trailing comments
            value = value.split('//')[0].strip()
            self._defines[name] = value

    def _is_local_class(self, name: str, parent: Optional[str] = None) -> bool:
        """Check if class is mission-local rather than external reference"""
        # Also check if this is a functions class member
        is_function_member = '.' in name and name.split('.')[0] == 'functions'
        return (name in self._known_local_bases or
                name in self._mission_local_classes or 
                parent in self._known_local_bases or
                is_function_member)

    def _parse_mission_content(self, content: str, source: str) -> Set[ClassDef]:
        """Parse content extracting only external class references"""
        referenced_classes = set()
        current_class_properties = {}
        
        for match in self._class_pattern.finditer(content):
            name, parent, body = match.groups()
            name = name.strip() if name else ""
            if not name or name.isdigit():
                continue
                
            # Skip local mission classes, only collect their references    
            if self._is_local_class(name, parent):
                self._mission_local_classes.add(name)
                clean_body = self._clean_class_body(body.strip('{}'))
                # Parse array properties properly
                properties = self._extract_properties(clean_body)
                # Process array properties and extract equipment
                self._extract_equipment_references(properties, referenced_classes, source)
                
        return referenced_classes

    def _clean_class_body(self, body: str) -> str:
        """Clean class body by removing comments and normalizing whitespace"""
        # Remove /* */ style comments
        body = re.sub(r'/\*.*?\*/', '', body, flags=re.DOTALL)
        # Remove // style comments
        body = re.sub(r'//[^\n]*', '', body)
        return body.strip()

    def _extract_properties(self, body: str) -> Dict[str, str]:
        """Extract properties from class body"""
        properties = {}
        lines = [l.strip() for l in body.split(';') if l.strip()]
        
        for line in lines:
            if '=' in line and not line.strip().startswith('class'):
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value:
                        properties[key] = value
                except Exception:
                    continue
                    
        return properties

    def _extract_equipment_references(self, properties: Dict[str, str], 
                                   classes: Set[ClassDef], source: str):
        """Extract equipment references with improved comma handling"""
        for key, value in properties.items():
            key = key.strip('[]')
            if key not in self._equipment_arrays:
                continue

            if value.startswith('{'):
                # Handle array format
                content = value.strip('{}')
                items = []
                # Split by commas but preserve quoted strings
                current = []
                in_quotes = False
                
                for char in content:
                    if char == '"':
                        in_quotes = not in_quotes
                    if char == ',' and not in_quotes:
                        item = ''.join(current).strip().strip('"')
                        if item and not item.startswith('//'):
                            items.append(item)
                        current = []
                    else:
                        current.append(char)
                
                # Handle last item
                if current:
                    item = ''.join(current).strip().strip('"')
                    if item and not item.startswith('//'):
                        items.append(item)
            else:
                items = [value.strip()]

            # Process items...
            for item in items:
                # Handle LIST macro with improved empty detection
                if list_match := self._list_macro_pattern.match(item):
                    count = int(list_match.group(1))
                    content = list_match.group(3)
                    
                    # Skip if content is empty or just whitespace
                    if not content or content.isspace():
                        continue
                        
                    if content and not self._is_local_class(content):
                        # Simplified class reference creation
                        ref_class = ClassDef(
                            name=content,
                            is_reference=True,
                            properties={"list_count": str(count)} if count > 1 else {}
                        )
                        classes.add(ref_class)
                # Handle regular items        
                elif item and not item.isdigit() and not self._is_local_class(item):
                    # Simplified class reference creation - only needs name
                    ref_class = ClassDef(
                        name=item,
                        is_reference=True
                    )
                    classes.add(ref_class)
