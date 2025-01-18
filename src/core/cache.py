from pathlib import Path
from typing import Optional, Set, Dict
import pickle
import sqlite3
import logging
from datetime import datetime
import hashlib
import threading

logger = logging.getLogger(__name__)

class CacheManager:
    """Thread-safe cache manager using SQLite"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self._local = threading.local()
        self._lock = threading.RLock()
        self._init_schema = """
            CREATE TABLE IF NOT EXISTS scan_cache (
                path_hash TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                data BLOB,
                timestamp TEXT,
                invalidated BOOLEAN DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS pbo_cache (
                pbo_hash TEXT PRIMARY KEY,
                pbo_path TEXT NOT NULL,
                prefix TEXT,
                data BLOB,
                timestamp TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_timestamp ON scan_cache(timestamp);
            CREATE INDEX IF NOT EXISTS idx_pbo_path ON pbo_cache(pbo_path);
        """

    def _get_connection(self):
        """Get thread-local connection with locking"""
        with self._lock:
            if not hasattr(self._local, 'conn'):
                self._local.conn = sqlite3.connect(":memory:",
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
                sqlite3.register_adapter(datetime, lambda dt: dt.isoformat())
                sqlite3.register_converter('timestamp', lambda b: datetime.fromisoformat(b.decode()))
                self._local.conn.executescript(self._init_schema)
            return self._local.conn

    def _get_path_hash(self, path: str) -> str:
        return hashlib.sha256(path.encode()).hexdigest()
        
    def get_cached_scan(self, path: str) -> Optional[Set]:
        try:
            path_hash = self._get_path_hash(path)
            cursor = self._get_connection().execute(
                "SELECT data FROM scan_cache WHERE path_hash = ?",
                (path_hash,)
            )
            if row := cursor.fetchone():
                return pickle.loads(row[0])
        except Exception as e:
            logger.error(f"Cache read error: {e}")
        return None
        
    def cache_scan(self, path: str, scan_result) -> None:
        """Cache scan results, handling SQF files specially"""
        try:
            path_hash = self._get_path_hash(path)
            
            # Filter out SQF files with "sqf_present" checksum before caching
            filtered_result = {
                asset for asset in scan_result
                if not (asset.checksum == "sqf_present" and 
                       str(asset.path).lower().endswith('.sqf'))
            }
            
            self._get_connection().execute(
                """INSERT OR REPLACE INTO scan_cache 
                   (path_hash, path, data, timestamp, invalidated)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    path_hash,
                    path,
                    pickle.dumps(filtered_result),
                    datetime.now(),
                    False
                )
            )
            self._get_connection().commit()
        except Exception as e:
            logger.error(f"Cache write error: {e}")

    def __del__(self):
        """Ensure connection is closed on deletion"""
        self.close()

    def get_cached_pbo(self, pbo_path: str, file_hash: str) -> Optional[Set]:
        """Get cached PBO content if valid"""
        try:
            cursor = self._get_connection().execute(
                "SELECT data FROM pbo_cache WHERE pbo_hash = ?",
                (file_hash,)
            )
            if row := cursor.fetchone():
                return pickle.loads(row[0])
        except Exception as e:
            logger.error(f"PBO cache read error: {e}")
        return None

    def cache_pbo(self, pbo_path: str, file_hash: str, data, prefix: str = None) -> None:
        """Cache PBO content in memory"""
        try:
            self._get_connection().execute(
                """INSERT OR REPLACE INTO pbo_cache 
                   (pbo_hash, pbo_path, prefix, data, timestamp)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    file_hash, 
                    pbo_path,
                    prefix,
                    pickle.dumps(data),
                    datetime.now()
                )
            )
            self._get_connection().commit()
        except Exception as e:
            logger.error(f"PBO cache write error: {e}")

    def invalidate_old_entries(self, max_age_days: int = 30) -> None:
        """Invalidate cache entries older than specified days"""
        try:
            self._get_connection().execute("""
                UPDATE scan_cache 
                SET invalidated = 1
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            """, (max_age_days,))
                
            # Optionally remove invalidated entries
            self._get_connection().execute("DELETE FROM scan_cache WHERE invalidated = 1")
        except Exception as e:
            logger.error(f"Cache invalidation error: {e}")

    def __enter__(self):
        """Context manager enter"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure connection is closed"""
        self.close()

    def close(self):
        """Close thread-local connection if it exists"""
        if hasattr(self._local, 'conn'):
            try:
                self._local.conn.close()
            except Exception as e:
                logger.error(f"Error closing database: {e}")
            finally:
                self._local.conn = None
