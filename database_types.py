from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ClassEntry:
    """Represents an Arma 3 class entry"""
    class_name: str
    source: str
    category: str
    parent: Optional[str] = None

    def __hash__(self):
        return hash((self.class_name, self.source, self.category, self.parent))
    
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
