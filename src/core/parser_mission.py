from pathlib import Path
from typing import Set, Dict, List, Optional, DefaultDict
import re
import csv
import logging
from .models import ClassDef
from .base_parser import BaseParser

logger = logging.getLogger(__name__)

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
            self._process_defines(content, path)
            source = path.stem
            return self._parse_mission_content(content, source)
        except Exception as e:
            logger.error(f"Failed to parse mission file {path}: {e}")
            return set()

    def _process_defines(self, content: str, file_path: Path):
        """Process #define directives and store them"""
        self._defines.clear()  # Clear existing defines
        if not self._verify_balanced_braces(content, file_path):
            logger.error(f"Failed to parse defines in {file_path} due to unbalanced braces")
            return
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
