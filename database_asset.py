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

def normalize_path(path: str, is_arma3: bool = False) -> str:
    """Normalize asset path consistently"""
    # 1. Convert backslashes to forward slashes
    norm_path = path.replace('\\', '/').lower()
    
    # 2. Remove any double a3 prefixes
    while 'a3/a3/' in norm_path:
        norm_path = norm_path.replace('a3/a3/', 'a3/')
    
    # 3. Clean up slashes
    norm_path = norm_path.strip('/').replace('//', '/')
    
    # 4. Ensure a3 prefix for Arma assets if missing
    if is_arma3 and not norm_path.startswith('a3/'):
        norm_path = f"a3/{norm_path}"
    
    return norm_path

def scan_for_assets(folder_path: str) -> Set[str]:
    """Scan folder for asset files"""
    assets = set()
    is_arma3 = 'arma 3' in folder_path.lower()
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.paa', '.p3d', '.wss', '.ogg', '.wav', '.jpg', '.png')):
                # Get full path and make it relative to folder_path
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                
                # Normalize the path
                norm_path = normalize_path(rel_path, is_arma3)
                logger.debug(f"Found asset: {norm_path} (original: {rel_path})")
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
        
        # Extract prefix from properties section
        for line in pbo_contents:
            if line.startswith('prefix='):
                prefix = line.split('=')[1].strip(';').strip()
                break
        
        if not prefix:
            logger.warning(f"No prefix found in PBO: {pbo_path}")
            return None, set()
        
        # Process each file in the PBO
        in_properties = False
        for line in pbo_contents:
            # Skip properties section
            if line.startswith('//<'):
                in_properties = True
                continue
            if line.startswith('//</'):
                in_properties = False
                continue
            if in_properties or line.startswith('//'):
                continue
                
            # Check if file has an asset extension
            if line.lower().endswith(('.paa', '.p3d', '.wss', '.ogg', '.wav')):
                # Apply consistent path normalization
                norm_path = normalize_path(
                    f"{prefix}/{line}", 
                    is_arma3='arma 3' in pbo_path.lower()
                )
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

def scan_folder(folder_path: str, task_name: str, task_hash: str, cache_mgr: 'CacheManager', max_workers: int = None) -> Set[str]:
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

def find_arma3_install() -> Optional[str]:
    """Find Arma 3 installation directory"""
    common_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Arma 3",
        r"C:\Program Files\Steam\steamapps\common\Arma 3",
        # Add more common paths if needed
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

def scan_arma3_base(arma_path: str, task_name: str, cache_mgr) -> Set[str]:
    """Recursively scan entire Arma 3 installation for assets"""
    logger.info("Recursively scanning Arma 3 installation for assets...")
    
    task_hash = hashlib.md5(arma_path.encode()).hexdigest()
    try:
        # Direct scan for vanilla assets first
        vanilla_assets = scan_for_assets(arma_path)
        logger.info(f"Direct scan found {len(vanilla_assets)} vanilla assets")
        
        # Now scan PBOs as well
        pbo_assets = scan_folder(arma_path, f"{task_name}_base", task_hash, cache_mgr)
        logger.info(f"PBO scan found {len(pbo_assets)} additional assets")
        
        # Combine both sets
        all_assets = vanilla_assets | pbo_assets
        logger.info(f"Total unique assets found: {len(all_assets)}")
        
        return all_assets
        
    except Exception as e:
        logger.error(f"Error scanning Arma 3 installation: {e}")
        return set()