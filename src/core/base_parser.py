from pathlib import Path
from typing import Dict, Set, List
from .models import ClassDef
import logging
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseParser:
    """Base class for parsing class definitions"""
    
    def __init__(self):
        self._class_registry: Dict[str, Set[ClassDef]] = {}
        self._base_classes = {"Object", "Vehicle", "Man", "Static", "Item"}

    def _parse_content(self, content: str, source: str) -> Set[ClassDef]:
        """Parse raw content into class definitions"""
        pass

    def parse_file(self, path: Path) -> Set[ClassDef]:
        """Parse file and extract class definitions"""
        try:
            content = path.read_text(encoding='utf-8')
            classes = self._parse_content(content, path.stem)
            self._process_classes(classes)
            return classes
        except Exception as e:
            logger.error(f"Failed to parse {path}: {e}")
            return set()

    def _process_classes(self, classes: Set[ClassDef]):
        """Process class definitions"""
        for class_def in classes:
            self._register_version(class_def)

    def _register_version(self, class_def: ClassDef):
        """Register a new version of a class definition"""
        version = ClassDef(
            source=class_def.source or "unknown",
            timestamp=datetime.now(),
            hash=self._get_content_hash(class_def.content)
        )
        
        if class_def.name not in self._class_registry:
            self._class_registry[class_def.name] = set()
            
        self._class_registry[class_def.name].add(version)
        class_def.version_info = version

    def validate_inheritance(self, class_def: ClassDef, available_classes: Set[ClassDef]) -> List[str]:
        """Validate class inheritance"""
        warnings = []
        
        if class_def.parent:
            parent_found = any(c.name == class_def.parent for c in available_classes)
            if not parent_found:
                warnings.append(f"Missing parent class '{class_def.parent}' for '{class_def.name}'")
                
        return warnings

    def _get_existing_classes(self) -> Set[ClassDef]:
        """Get known class definitions - override if needed"""
        return set()

    def _get_content_hash(self, content: str) -> str:
        """Generate hash for version tracking"""
        return hashlib.md5(content.encode()).hexdigest()
