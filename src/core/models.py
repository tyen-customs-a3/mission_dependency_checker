from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Optional, Dict, Set, List, Any
from datetime import datetime

@dataclass(frozen=True)  # Make Asset immutable for hashing
class Asset:
    path: Path
    checksum: str
    source: str
    last_scan: datetime

    def __hash__(self):
        return hash((str(self.path), self.checksum, self.source))

    def __eq__(self, other):
        if not isinstance(other, Asset):
            return False
        return (str(self.path) == str(other.path) and 
                self.checksum == other.checksum and 
                self.source == other.source)

@dataclass
class InidbiProperty:
    """Property definition from INIDBI2"""
    name: str
    value: Any
    source_file: str
    line_number: int
    inherited: bool = False

@dataclass
class InidbiClass:
    """INIDBI2 specific class metadata"""
    category: str
    source_mod: str
    properties: Dict[str, InidbiProperty]
    inherits_from: Optional[str] = None
    is_simple_object: bool = False
    num_properties: int = 0
    scope: int = 0
    model: Optional[str] = None
    display_name: Optional[str] = None
    config_path: Optional[str] = None
    config_line: Optional[int] = None

@dataclass
class ClassDef:
    """Class definition model"""
    name: str
    parent: Optional[str] = None
    source: str = "unknown"
    properties: Dict[str, str] = field(default_factory=dict)
    scope: str = "private"
    is_reference: bool = False  # Add flag for referenced classes
    is_mission_local: bool = False  # Add flag for mission-local classes
    inidbi_meta: Optional[InidbiClass] = None
    nested_classes: Set['ClassDef'] = field(default_factory=set)
    
    def __post_init__(self):
        if self.nested_classes is None:
            self.nested_classes = set()

    def __hash__(self):
        return hash((self.name, self.source))

    def __eq__(self, other):
        if not isinstance(other, ClassDef):
            return False
        return self.name == other.name and self.source == other.source

@dataclass
class ScanResult:
    """Result of scanning a mission folder"""
    assets: Set[Asset]
    classes: Set[ClassDef]
    timestamp: datetime
    missing_assets: Set[str] = None
    invalid_classes: Set[str] = None
    warnings: Set[str] = None

@dataclass
class ScanConfig:
    """Configuration for test runs"""
    include_patterns: List[str] = field(default_factory=lambda: [".*"])
    exclude_patterns: List[str] = field(default_factory=list)
    max_files: Optional[int] = None
    arma3_path: Optional[Path] = None
    modpack_path: Optional[Path] = None
    ini_file: Optional[Path] = None

    def matches_path(self, path: str) -> bool:
        """Check if path matches include/exclude patterns"""
        if any(re.match(p, path) for p in self.exclude_patterns):
            return False
        return any(re.match(p, path) for p in self.include_patterns)