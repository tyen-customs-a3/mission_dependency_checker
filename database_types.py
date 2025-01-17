from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ClassEntry:
    """Represents an Arma 3 class entry with all available information"""
    class_name: str
    source: str
    category: str
    parent: Optional[str] = None
    inherits_from: Optional[str] = None  # Can be different from parent in some cases
    is_simple_object: bool = False
    num_properties: int = 0
    scope: int = 0
    model: Optional[str] = None
    display_name: Optional[str] = None

    def __hash__(self):
        return hash((
            self.class_name, 
            self.source, 
            self.category, 
            self.parent,
            self.inherits_from
        ))
    
    def __lt__(self, other):
        if not isinstance(other, ClassEntry):
            return NotImplemented
        return (self.source, self.class_name) < (other.source, other.class_name)

    def __eq__(self, other):
        if not isinstance(other, ClassEntry):
            return NotImplemented
        return (self.class_name == other.class_name and 
                self.source == other.source and 
                self.category == other.category and 
                self.parent == other.parent)
