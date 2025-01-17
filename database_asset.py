import os
import subprocess
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Set, Optional, List, Tuple
from dataclasses import dataclass
import hashlib
from multiprocessing import Pool, cpu_count
from functools import partial

logger = logging.getLogger(__name__)

@dataclass
class AssetEntry:
    path: str
    source: str

# Remove load_class_database function as it's not used anymore

def scan_for_assets(folder_path: str) -> Set[str]:
    """Scan folder for asset files"""
    assets = set()
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.paa', '.p3d', '.wss', '.ogg', '.wav', '.jpg', '.png')):
                rel_path = os.path.relpath(os.path.join(root, file), folder_path)
                # Normalize path
                norm_path = rel_path.replace('\\', '/').lower()
                assets.add(norm_path)
                
    return assets


def get_pbo_contents(pbo_path: str) -> List[str]:
    """Use extractpbo to list contents of a PBO file"""
    try:
        # Run extractpbo with -LB for brief listing format
        result = subprocess.run(['extractpbo', '-LBP', pbo_path], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            # Get all lines and return non-empty ones
            lines = result.stdout.splitlines()
            return [line.strip() for line in lines if line.strip()]
        return []
    except subprocess.SubProcessError:
        logger.error(f"Failed to read PBO: {pbo_path}")
        return []

def get_pbo_hash(pbo_path: str) -> str:
    """Get hash of PBO file using size and modification time for quick comparison"""
    stat = os.stat(pbo_path)
    return hashlib.md5(f"{stat.st_size}_{stat.st_mtime}".encode()).hexdigest()

def process_pbo(pbo_path: str, task_name: str, cache_mgr) -> Tuple[Optional[str], Set[str]]:
    """Process a single PBO file and return its prefix and assets"""
    try:
        # Check cache first
        pbo_hash = get_pbo_hash(pbo_path)
        cache_result = cache_mgr.check_pbo_cache(pbo_path, pbo_hash, task_name)
        if cache_result:
            return cache_result
        
        # Process PBO normally if not in cache
        assets = set()
        prefix = None
        
        # Get list of files in PBO
        pbo_contents = get_pbo_contents(pbo_path)
        
        # Extract prefix
        for line in pbo_contents:
            if 'prefix=' in line:
                prefix = line.split('=')[1].strip()
                break
        
        if not prefix:
            return None, set()
        
        for line in pbo_contents:
            if line.lower().endswith(('.paa', '.p3d', '.wss', '.ogg', '.wav')):
                norm_path = f"{prefix}/{line}".replace('\\', '/').lower()
                assets.add(norm_path)
        
        # Update cache
        cache_mgr.update_pbo_cache(pbo_path, pbo_hash, prefix, assets, task_name)
        
        return prefix, assets
    
    except sqlite3.OperationalError as e:
        logger.error(f"Database error processing PBO {pbo_path}: {e}")
        return None, set()
    except Exception as e:
        logger.error(f"Error processing PBO {pbo_path}: {e}")
        return None, set()

def _process_pbo_worker(args: Tuple[str, str, object]) -> Tuple[str, Optional[str], Set[str]]:
    """Worker function for parallel PBO processing"""
    pbo_path, task_name, cache_mgr = args
    prefix, assets = process_pbo(pbo_path, task_name, cache_mgr)
    return pbo_path, prefix, assets

def scan_folder(folder_path: str, task_name: str, task_hash: str, cache_mgr, max_workers: int = None) -> Set[str]:
    """Scan folder for PBO files and process them in parallel"""
    # Check if we need to initialize/reset cache
    if not cache_mgr.check_asset_cache_valid(task_name, task_hash):
        cache_mgr.initialize_asset_cache(task_name, task_hash)
    
    # Collect all PBO files first
    pbo_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pbo'):
                pbo_files.append(os.path.join(root, file))
    
    if not pbo_files:
        return set()
    
    # Set number of workers
    if max_workers is None:
        max_workers = max(1, cpu_count() - 1)
    
    # Process PBOs in parallel
    assets = set()
    with Pool(max_workers) as pool:
        worker_args = [(pbo, task_name, cache_mgr) for pbo in pbo_files]
        results = pool.map(_process_pbo_worker, worker_args)
        
        # Collect results
        for _, _, pbo_assets in results:
            assets.update(pbo_assets)
    
    return assets