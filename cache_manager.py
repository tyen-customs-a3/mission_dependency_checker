import os
import pickle
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Set, Optional, Tuple
from database_types import ClassEntry
import hashlib

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize cache manager with optional custom cache directory"""
        if cache_dir is not None:
            self.cache_dir = Path(cache_dir)
        else:
            # Default to .cache in the application directory
            self.cache_dir = Path(__file__).parent / '.cache'
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = str(self.cache_dir / 'scanner_cache.db')  # Convert Path to string for sqlite3
        self.temp_dir = self.cache_dir / 'temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            # Create folder cache table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS folder_cache (
                    folder_hash TEXT NOT NULL,
                    folder_path TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    cache_type TEXT NOT NULL,
                    data BLOB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (folder_hash, cache_type)
                )
            ''')
            
            # Create PBO cache table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pbo_cache (
                    pbo_path TEXT,
                    pbo_hash TEXT,
                    prefix TEXT,
                    assets TEXT,
                    task_name TEXT,
                    PRIMARY KEY (pbo_path, task_name)
                )
            ''')
            
            # Create asset cache table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS asset_cache (
                    task_name TEXT PRIMARY KEY,
                    task_hash TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Add vanilla assets table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS vanilla_assets (
                    asset_path TEXT PRIMARY KEY,
                    arma_path TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def check_pbo_cache(self, pbo_path: str, pbo_hash: str, task_name: str) -> Optional[Tuple[str, Set[str]]]:
        """Check if PBO exists in cache and hash matches"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    'SELECT prefix, assets FROM pbo_cache WHERE pbo_path = ? AND pbo_hash = ? AND task_name = ?',
                    (pbo_path, pbo_hash, task_name)
                )
                result = cursor.fetchone()
                if result:
                    prefix, assets_str = result
                    return prefix, set(assets_str.split('|')) if assets_str else set()
        except sqlite3.Error as e:
            logger.error(f"Database error checking PBO cache: {e}")
        return None
    
    def update_pbo_cache(self, pbo_path: str, pbo_hash: str, prefix: str, assets: Set[str], task_name: str):
        """Update or insert PBO cache entry"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO pbo_cache (pbo_path, pbo_hash, prefix, assets, task_name)
                    VALUES (?, ?, ?, ?, ?)
                ''', (pbo_path, pbo_hash, prefix, '|'.join(assets), task_name))
        except sqlite3.Error as e:
            logger.error(f"Database error updating PBO cache: {e}")
    
    def check_asset_cache_valid(self, task_name: str, task_hash: str) -> bool:
        """Check if asset cache for task is valid"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    'SELECT task_hash FROM asset_cache WHERE task_name = ?',
                    (task_name,)
                )
                result = cursor.fetchone()
                return result is not None and result[0] == task_hash
        except sqlite3.Error as e:
            logger.error(f"Database error checking asset cache: {e}")
            return False
    
    def initialize_asset_cache(self, task_name: str, task_hash: str):
        """Initialize or reset asset cache for task"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Clear existing cache for this task
                conn.execute('DELETE FROM pbo_cache WHERE task_name = ?', (task_name,))
                conn.execute('''
                    INSERT OR REPLACE INTO asset_cache (task_name, task_hash)
                    VALUES (?, ?)
                ''', (task_name, task_hash))
        except sqlite3.Error as e:
            logger.error(f"Database error initializing asset cache: {e}")

    def clear_cache(self):
        """Clear all cache data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM pbo_cache')
                conn.execute('DELETE FROM asset_cache')
        except sqlite3.Error as e:
            logger.error(f"Database error clearing cache: {e}")

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

    def get_vanilla_assets(self) -> Optional[Set[str]]:
        """Retrieve cached vanilla assets"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT asset_path FROM vanilla_assets')
                results = cursor.fetchall()
                if results:
                    return {row[0] for row in results}
        except sqlite3.Error as e:
            logger.error(f"Database error retrieving vanilla assets: {e}")
        return None

    def update_vanilla_assets(self, assets: Set[str], arma_path: str):
        """Update cached vanilla assets"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Clear existing assets
                conn.execute('DELETE FROM vanilla_assets')
                # Insert new assets
                conn.executemany(
                    'INSERT INTO vanilla_assets (asset_path, arma_path) VALUES (?, ?)',
                    [(asset, arma_path) for asset in assets]
                )
        except sqlite3.Error as e:
            logger.error(f"Database error updating vanilla assets: {e}")
