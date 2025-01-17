from typing import Dict, Set, List, Optional, Generator
from pathlib import Path
import sqlite3
from datetime import datetime
from .models import ClassDef  # Remove ClassVersion, ClassOverride imports
import logging

logger = logging.getLogger(__name__)

class ClassDatabase:
    """Manages persistence and querying of class definitions"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Always use in-memory database"""
        self._conn = sqlite3.connect(":memory:", 
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self._conn.row_factory = sqlite3.Row
        # Add datetime adapter
        sqlite3.register_adapter(datetime, lambda dt: dt.isoformat())
        sqlite3.register_converter('timestamp', lambda b: datetime.fromisoformat(b.decode()))
        self._initialize_db()
        self._required_classes = set()
        self._conn.create_function("LOWER", 1, lambda x: x.lower() if x else None)
    
    def _initialize_db(self):
        """Initialize SQLite database schema"""
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                parent TEXT,
                source TEXT NOT NULL,
                scope TEXT DEFAULT 'private',
                UNIQUE(name, source)
            );
            
            CREATE TABLE IF NOT EXISTS properties (
                class_id INTEGER,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                FOREIGN KEY(class_id) REFERENCES classes(id)
            );

            CREATE TABLE IF NOT EXISTS required_classes (
                name TEXT PRIMARY KEY,
                category TEXT,
                reason TEXT
            );

            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
        """)
    
    def add_class(self, class_def) -> None:
        """Add or update a class definition preserving original case"""
        cursor = self._conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO classes (name, parent, source, scope)
                VALUES (?, ?, ?, ?)
            """, (class_def.name, class_def.parent, class_def.source, class_def.scope))
            
            class_id = cursor.lastrowid
            
            if class_def.properties:
                cursor.executemany("""
                    INSERT INTO properties (class_id, key, value)
                    VALUES (?, ?, ?)
                """, [(class_id, k, v) for k, v in class_def.properties.items()])
            
            self._conn.commit()
        finally:
            cursor.close()

        # Handle nested classes
        if class_def.nested_classes:
            for nested in class_def.nested_classes:
                nested.parent = class_def.name
                self.add_class(nested)

    def get_class_history(self, class_name: str) -> List[ClassDef]:
        """Get version history for a class preserving original case"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT c.name, c.parent, c.source, c.scope,
                       GROUP_CONCAT(p.key || '=' || p.value) as props
                FROM classes c
                LEFT JOIN properties p ON c.id = p.class_id
                WHERE LOWER(c.name) = LOWER(?)
                GROUP BY c.id, c.name, c.parent, c.source, c.scope
            """, (class_name,))
            
            results = []
            for row in cursor:
                props = {}
                if row['props']:
                    for prop in row['props'].split(','):
                        if '=' in prop:
                            key, value = prop.split('=', 1)
                            props[key] = value
                            
                class_def = ClassDef(
                    name=row['name'],
                    parent=row['parent'],  # Parent case is now preserved
                    source=row['source'],
                    scope=row['scope'],
                    properties=props
                )
                results.append(class_def)
                
            return results

    def get_inheritance_chain(self, class_name: str) -> List[ClassDef]:
        """Get complete inheritance chain for a class"""
        chain = []
        visited = set()
        
        def _get_parent_recursive(name: str):
            if name in visited:
                logger.warning(f"Circular inheritance detected for {name}")
                return
            visited.add(name)
            
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT c.*, GROUP_CONCAT(p.key || '=' || p.value) as props
                    FROM classes c
                    LEFT JOIN properties p ON c.id = p.class_id
                    WHERE c.name = ?
                    GROUP BY c.id
                """, (name,))
                
                row = cursor.fetchone()
                if row:
                    # Safely parse properties
                    props = {}
                    if row['props']:
                        try:
                            for prop in row['props'].split(','):
                                if '=' in prop:
                                    key, value = prop.split('=', 1)
                                    props[key] = value
                        except Exception as e:
                            logger.warning(f"Error parsing properties: {e}")
                    
                    class_def = ClassDef(
                        name=row['name'],
                        parent=row['parent'],
                        source=row['source'],
                        properties=props
                    )
                    chain.append(class_def)
                    
                    if class_def.parent:
                        _get_parent_recursive(class_def.parent)
        
        _get_parent_recursive(class_name)
        return chain

    def get_class(self, class_name: str) -> bool:
        """Check if class exists in database using case-insensitive lookup"""
        if not class_name:
            return False
            
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT EXISTS(SELECT 1 FROM classes WHERE LOWER(name) = LOWER(?) LIMIT 1)", 
                (class_name,)
            )
            return bool(cursor.fetchone()[0])

    def add_required_class(self, name: str, category: str = None, reason: str = None) -> None:
        """Mark a class as required"""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO required_classes (name, category, reason) VALUES (?, ?, ?)",
                (name, category, reason)
            )
        self._required_classes.add(name)

    def get_required_classes(self) -> Set[str]:
        """Get all required class names"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT name FROM required_classes")
            return {row[0] for row in cursor}

    def get_class_requirements(self, class_name: str) -> Dict[str, str]:
        """Get requirement details for a class"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT category, reason FROM required_classes WHERE name = ?",
                (class_name,)
            )
            if row := cursor.fetchone():
                return {"category": row[0], "reason": row[1]}
        return {}

    def _get_connection(self):
        """Return existing connection"""
        return self._conn

    def close(self):
        """Ensure connection is properly closed"""
        if self._conn:
            try:
                self._conn.close()
            finally:
                self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """Cleanup database connection"""
        self.close()
