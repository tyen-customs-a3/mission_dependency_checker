import os
import json
import pickle
from typing import Dict, Set, Optional, Tuple
from database import ClassEntry, AssetEntry
from datetime import datetime

class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
    def _get_cache_path(self, folder_path: str, cache_type: str) -> str:
        """Get cache file path for a given folder"""
        folder_hash = str(hash(folder_path))
        return os.path.join(self.cache_dir, f"{cache_type}_{folder_hash}.pickle")
        
    def _get_folder_signature(self, folder_path: str) -> str:
        """Get a signature of folder contents based on modification times"""
        signature = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.hpp', '.cpp', '.paa')):
                    file_path = os.path.join(root, file)
                    mtime = os.path.getmtime(file_path)
                    signature.append(f"{file_path}:{mtime}")
        return "|".join(sorted(signature))

    def get_cached_scan(self, folder_path: str) -> Optional[Tuple[Dict[str, Set[ClassEntry]], Set[str]]]:
        """Get cached scan results if valid"""
        cache_path = self._get_cache_path(folder_path, "scan")
        sig_path = cache_path + ".sig"
        
        if not (os.path.exists(cache_path) and os.path.exists(sig_path)):
            return None
            
        # Check if signature matches
        current_sig = self._get_folder_signature(folder_path)
        with open(sig_path, 'r') as f:
            cached_sig = f.read()
            
        if current_sig != cached_sig:
            return None
            
        # Load cached data
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except:
            return None
            
    def cache_scan(self, folder_path: str, scan_results: Tuple[Dict[str, Set[ClassEntry]], Set[str]]):
        """Cache scan results"""
        cache_path = self._get_cache_path(folder_path, "scan")
        sig_path = cache_path + ".sig"
        
        # Save signature
        current_sig = self._get_folder_signature(folder_path)
        with open(sig_path, 'w') as f:
            f.write(current_sig)
            
        # Save scan results
        with open(cache_path, 'wb') as f:
            pickle.dump(scan_results, f)

    def get_cached_mission(self, mission_path: str) -> Optional[Tuple[Set[str], Set[str]]]:
        """Get cached mission scan results if valid"""
        cache_path = self._get_cache_path(mission_path, "mission")
        sig_path = cache_path + ".sig"
        
        if not (os.path.exists(cache_path) and os.path.exists(sig_path)):
            return None
            
        # Check if signature matches
        current_sig = self._get_folder_signature(mission_path)
        with open(sig_path, 'r') as f:
            cached_sig = f.read()
            
        if current_sig != cached_sig:
            return None
            
        # Load cached data
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except:
            return None

    def cache_mission(self, mission_path: str, scan_results: Tuple[Set[str], Set[str]]):
        """Cache mission scan results"""
        cache_path = self._get_cache_path(mission_path, "mission")
        sig_path = cache_path + ".sig"
        
        # Save signature
        current_sig = self._get_folder_signature(mission_path)
        with open(sig_path, 'w') as f:
            f.write(current_sig)
            
        # Save scan results
        with open(cache_path, 'wb') as f:
            pickle.dump(scan_results, f)
