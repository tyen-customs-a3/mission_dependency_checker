import os
import pickle
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Set, Optional, Tuple
from database_class import ClassEntry
import hashlib

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.cache_dir / "cache.db"
        self.temp_dir = Path(__file__).parent / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database schema"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Create scan cache table
            c.execute("""
                CREATE TABLE IF NOT EXISTS folder_cache (
                    folder_hash TEXT PRIMARY KEY,
                    folder_path TEXT,
                    signature TEXT,
                    cache_type TEXT,
                    data BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def get_asset_db_path(self, task_name: str) -> Path:
        """Get asset cache database path for task"""
        return self.temp_dir / f"asset_cache_{task_name}.db"

    def create_asset_cache_db(self, task_name: str) -> None:
        """Create or reset asset cache database"""
        db_path = self.get_asset_db_path(task_name)
        
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_meta (
                    task_hash TEXT PRIMARY KEY,
                    creation_time INTEGER
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pbo_assets (
                    pbo_path TEXT,
                    pbo_hash TEXT,
                    prefix TEXT,
                    last_modified INTEGER,
                    PRIMARY KEY (pbo_path)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    pbo_path TEXT,
                    asset_path TEXT,
                    PRIMARY KEY (pbo_path, asset_path),
                    FOREIGN KEY (pbo_path) REFERENCES pbo_assets(pbo_path)
                )
            """)
            conn.commit()

    def check_asset_cache_valid(self, task_name: str, task_hash: str) -> bool:
        """Check if asset cache is valid for given task"""
        db_path = self.get_asset_db_path(task_name)
        if not db_path.exists():
            return False
            
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute("SELECT task_hash FROM cache_meta LIMIT 1")
                result = cursor.fetchone()
                return result is not None and result[0] == task_hash
        except sqlite3.Error:
            return False

    def initialize_asset_cache(self, task_name: str, task_hash: str) -> None:
        """Initialize or reset asset cache for task"""
        db_path = self.get_asset_db_path(task_name)
        
        # Delete existing database if it exists
        if db_path.exists():
            try:
                db_path.unlink()
            except OSError as e:
                logger.error(f"Failed to delete old cache: {e}")
        
        # Create new database
        self.create_asset_cache_db(task_name)
        
        # Store task hash
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO cache_meta (task_hash, creation_time) VALUES (?, ?)",
                (task_hash, int(os.path.getmtime(__file__)))
            )
            conn.commit()

    def _get_folder_hash(self, folder_path: str) -> str:
        """Generate a unique hash for the folder path"""
        return hashlib.sha256(folder_path.encode()).hexdigest()
    
    def _get_folder_signature(self, folder_path: str) -> str:
        """Get a signature of folder contents based on modification times"""
        signature = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.hpp', '.cpp', '.paa', '.sqf', '.json')):
                    file_path = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(file_path)
                        size = os.path.getsize(file_path)
                        signature.append(f"{file_path}:{mtime}:{size}")
                    except OSError:
                        continue
        return hashlib.sha256('|'.join(sorted(signature)).encode()).hexdigest()

    def _get_cached_data(self, folder_path: str, cache_type: str) -> Optional[bytes]:
        """Get cached data if signature matches"""
        folder_hash = self._get_folder_hash(folder_path)
        current_sig = self._get_folder_signature(folder_path)
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT signature, data FROM folder_cache 
                WHERE folder_hash = ? AND cache_type = ?
            """, (folder_hash, cache_type))
            result = c.fetchone()
            
            if result and result[0] == current_sig:
                return result[1]
        return None

    def _save_cached_data(self, folder_path: str, cache_type: str, data: bytes):
        """Save cached data with current signature"""
        folder_hash = self._get_folder_hash(folder_path)
        current_sig = self._get_folder_signature(folder_path)
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO folder_cache 
                (folder_hash, folder_path, signature, cache_type, data, timestamp)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (folder_hash, folder_path, current_sig, cache_type, data))
            conn.commit()

    def get_cached_scan(self, folder_path: str) -> Optional[Tuple[Dict[str, Set[ClassEntry]], Set[str]]]:
        """Get cached scan results if valid"""
        cached_data = self._get_cached_data(folder_path, "scan")
        if cached_data:
            try:
                return pickle.loads(cached_data)
            except:
                return None
        return None

    def cache_scan(self, folder_path: str, scan_results: Tuple[Dict[str, Set[ClassEntry]], Set[str]]):
        """Cache scan results"""
        try:
            data = pickle.dumps(scan_results)
            self._save_cached_data(folder_path, "scan", data)
        except:
            pass  # Silently fail if caching fails

    def get_cached_mission(self, mission_path: str) -> Optional[Tuple[Set[str], Set[str]]]:
        """Get cached mission scan results if valid"""
        cached_data = self._get_cached_data(mission_path, "mission")
        if cached_data:
            try:
                return pickle.loads(cached_data)
            except:
                return None
        return None

    def cache_mission(self, mission_path: str, scan_results: Tuple[Set[str], Set[str]]):
        """Cache mission scan results"""
        try:
            data = pickle.dumps(scan_results)
            self._save_cached_data(mission_path, "mission", data)
        except:
            pass  # Silently fail if caching fails

    def check_pbo_cache(self, pbo_path: str, pbo_hash: str, task_name: str) -> Optional[Tuple[str, Set[str]]]:
        """Check if PBO is in cache and return its prefix and assets if valid"""
        db_path = self.get_asset_db_path(task_name)
        if not db_path.exists():
            return None
            
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute(
                    "SELECT prefix FROM pbo_assets WHERE pbo_path = ? AND pbo_hash = ?", 
                    (pbo_path, pbo_hash)
                )
                result = cursor.fetchone()
                
                if result:
                    prefix = result[0]
                    cursor = conn.execute(
                        "SELECT asset_path FROM assets WHERE pbo_path = ?",
                        (pbo_path,)
                    )
                    assets = {f"{prefix}/{path}" for (path,) in cursor.fetchall()}
                    return prefix, assets
                    
        except sqlite3.Error as e:
            logger.error(f"Database error checking PBO cache: {e}")
            
        return None

    def update_pbo_cache(self, pbo_path: str, pbo_hash: str, prefix: str, 
                        assets: Set[str], task_name: str) -> None:
        """Update cache with new PBO data"""
        db_path = self.get_asset_db_path(task_name)
        
        with sqlite3.connect(db_path) as conn:
            # Update PBO entry
            conn.execute(
                """INSERT OR REPLACE INTO pbo_assets 
                   (pbo_path, pbo_hash, prefix, last_modified) 
                   VALUES (?, ?, ?, ?)""",
                (pbo_path, pbo_hash, prefix, int(os.path.getmtime(pbo_path)))
            )
            
            # Remove old assets
            conn.execute("DELETE FROM assets WHERE pbo_path = ?", (pbo_path,))
            
            # Add new assets
            assets_data = [(pbo_path, asset.split('/', 1)[1]) for asset in assets]
            conn.executemany(
                "INSERT INTO assets (pbo_path, asset_path) VALUES (?, ?)",
                assets_data
            )
            conn.commit()

    def cleanup_old_caches(self, days: int = 30):
        """Remove cache entries older than specified days"""
        # Clean up scan cache
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                DELETE FROM folder_cache 
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            """, (days,))
            conn.commit()
            
        # Clean up asset cache files
        current_time = os.time()
        for file in self.temp_dir.glob("asset_cache_*.db"):
            if (current_time - file.stat().st_mtime) > (days * 86400):
                try:
                    file.unlink()
                except OSError:
                    pass
