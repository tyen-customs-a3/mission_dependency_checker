import sqlite3
import logging
from typing import Dict, Set, Optional, List, Tuple
from database_types import ClassEntry
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class ClassDatabase:
    def __init__(self, db_path: str = ':memory:'):
        self.db_path = db_path
        # Store a single connection for in-memory databases
        if db_path == ':memory:':
            self._connection = sqlite3.connect(db_path)
            self._connection.row_factory = sqlite3.Row
        else:
            self._connection = None
        self.init_database()

    def __del__(self):
        if self._connection:
            self._connection.close()

    def init_database(self):
        """Initialize the database schema"""
        sql = '''
            CREATE TABLE IF NOT EXISTS classes (
                class_name TEXT NOT NULL,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                parent TEXT,
                PRIMARY KEY (class_name, source)
            );
            CREATE INDEX IF NOT EXISTS idx_class_name ON classes(class_name);
            CREATE INDEX IF NOT EXISTS idx_source ON classes(source);
            CREATE INDEX IF NOT EXISTS idx_parent ON classes(parent);
        '''
        with self.get_connection() as conn:
            conn.executescript(sql)
            # Verify table creation
            if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classes'").fetchone():
                raise RuntimeError("Failed to create database tables")

    @contextmanager
    def get_connection(self):
        """Get database connection - reuse for in-memory, create new for file"""
        if self._connection:
            yield self._connection
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            finally:
                conn.close()

    def add_class_entries(self, entries: List[ClassEntry], batch_size: int = 1000):
        """Efficiently insert multiple class entries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            batch = []
            
            for entry in entries:
                batch.append((
                    entry.class_name,
                    entry.source,
                    entry.category,
                    entry.parent
                ))
                
                if len(batch) >= batch_size:
                    cursor.executemany(
                        'INSERT OR REPLACE INTO classes VALUES (?, ?, ?, ?)',
                        batch
                    )
                    batch = []
            
            if batch:  # Insert any remaining entries
                cursor.executemany(
                    'INSERT OR REPLACE INTO classes VALUES (?, ?, ?, ?)',
                    batch
                )

    def get_class_entries(self) -> Dict[str, Set[ClassEntry]]:
        """Retrieve all class entries grouped by source"""
        result: Dict[str, Set[ClassEntry]] = {}
        
        with self.get_connection() as conn:
            # First group by source
            cursor = conn.execute('SELECT class_name, source, category, parent FROM classes')
            
            for row in cursor:
                entry = ClassEntry(
                    class_name=row[0],
                    source=row[1],
                    category=row[2],
                    parent=row[3]
                )
                
                if entry.source not in result:
                    result[entry.source] = set()
                result[entry.source].add(entry)
        
        return result

    def find_class(self, class_name: str) -> List[ClassEntry]:
        """Find all entries for a specific class name"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT class_name, source, category, parent FROM classes WHERE class_name = ?',
                (class_name,)
            )
            return [ClassEntry(row[0], row[1], row[2], row[3]) for row in cursor]

    def find_similar_classes(self, partial_name: str, limit: int = 5) -> List[ClassEntry]:
        """Find classes with similar names"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT class_name, source, category, parent FROM classes WHERE class_name LIKE ? LIMIT ?',
                (f'%{partial_name}%', limit)
            )
            return [ClassEntry(row[0], row[1], row[2], row[3]) for row in cursor]

    def clear_database(self):
        """Clear all data from the database"""
        with self.get_connection() as conn:
            conn.execute('DELETE FROM classes')

    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            stats = {
                'total_classes': cursor.execute('SELECT COUNT(*) FROM classes').fetchone()[0],
                'unique_sources': cursor.execute('SELECT COUNT(DISTINCT source) FROM classes').fetchone()[0],
                'unique_categories': cursor.execute('SELECT COUNT(DISTINCT category) FROM classes').fetchone()[0]
            }
        return stats

    def get_inheritance_tree(self, class_name: str) -> List[Tuple[ClassEntry, int]]:
        """Get complete inheritance tree for a class with depth levels"""
        results = []
        visited = set()

        def traverse_parents(current_class: str, depth: int = 0):
            if current_class in visited:
                return
            visited.add(current_class)
            
            # Get current class entry
            entries = self.find_class(current_class)
            if not entries:
                return
            
            # Add current class with its depth
            results.append((entries[0], depth))
            
            # Recursively process parent
            if entries[0].parent:
                traverse_parents(entries[0].parent, depth + 1)

        traverse_parents(class_name)
        return results

    def get_derived_classes(self, base_class: str) -> List[Tuple[ClassEntry, int]]:
        """Get all classes that inherit from the given base class"""
        results = []
        visited = set()

        def traverse_children(current_class: str, depth: int = 0):
            if current_class in visited:
                return
            visited.add(current_class)
            
            # Find all classes that have this as parent
            with self.get_connection() as conn:
                cursor = conn.execute(
                    'SELECT class_name, source, category, parent FROM classes WHERE parent = ?',
                    (current_class,)
                )
                children = [ClassEntry(row[0], row[1], row[2], row[3]) for row in cursor]
            
            # Add children with their depth
            for child in children:
                results.append((child, depth))
                traverse_children(child.class_name, depth + 1)

        # Add base class itself at depth 0
        base_entries = self.find_class(base_class)
        if base_entries:
            results.append((base_entries[0], 0))
            traverse_children(base_class)

        return results

    def print_inheritance_tree(self, class_name: str, show_derived: bool = False):
        """Print complete inheritance tree for a class"""
        if show_derived:
            tree = self.get_derived_classes(class_name)
        else:
            tree = self.get_inheritance_tree(class_name)
        
        if not tree:
            print(f"No inheritance information found for {class_name}")
            return

        print(f"\nInheritance {'Tree' if not show_derived else 'Hierarchy'} for {class_name}:")
        print("=" * 50)
        
        for entry, depth in tree:
            indent = "  " * depth
            prefix = "└─" if depth > 0 else ""
            print(f"{indent}{prefix}{entry.class_name} [{entry.source}]")
            
        print(f"\nTotal related classes: {len(tree)}")
