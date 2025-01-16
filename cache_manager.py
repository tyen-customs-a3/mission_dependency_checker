import os
import pickle
import sqlite3
from typing import Dict, Set, Optional, Tuple
from database import ClassEntry, AssetEntry
from datetime import datetime
import hashlib

class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        self.db_path = os.path.join(cache_dir, "cache.db")
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database schema"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Create tables if they don't exist
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

    def cleanup_old_caches(self, days: int = 30):
        """Remove cache entries older than specified days"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                DELETE FROM folder_cache 
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            """, (days,))
            conn.commit()
