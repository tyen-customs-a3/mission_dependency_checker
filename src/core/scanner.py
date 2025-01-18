from pathlib import Path
from typing import Set, Dict, Optional, Generator, List, Pattern
from datetime import datetime
import hashlib
import logging
import subprocess
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import re
from .models import Asset, ClassDef, ScanResult
from .cache import CacheManager  # Add this import

logger = logging.getLogger(__name__)

class AssetScanner:
    """
    Asset scanner for mission content.
    
    Scans directories for:
    - PBO archives
    - Direct asset files
    - Referenced content
    """
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_mgr = CacheManager(cache_dir)  # Initialize cache manager
        self._asset_cache = {}
    
    def scan_directory(self, path: Path, patterns: Optional[List[Pattern]] = None, max_files: Optional[int] = None) -> Set[Asset]:
        """Scan directory for assets with strict file limit enforcement"""
        if cached := self.cache_mgr.get_cached_scan(path.as_posix()):
            if max_files is None or len(cached) <= max_files:
                return cached
            return set(list(cached)[:max_files])

        patterns = patterns or [re.compile(".*")]
        all_assets = set()

        # First collect all candidate files
        pbo_files = []
        regular_files = []

        try:
            for f in path.rglob("*"):
                if f.is_file():
                    rel_path = str(f.relative_to(path))
                    if not any(p.match(rel_path) for p in patterns):
                        continue

                    if f.suffix.lower() == '.pbo':
                        pbo_files.append(f)
                    elif f.suffix.lower() in {'.paa', '.p3d', '.sqf'}:
                        regular_files.append(f)

                    # Early exit if we've found enough files
                    if max_files and (len(pbo_files) + len(regular_files)) >= max_files:
                        break

        except Exception as e:
            logger.error(f"Error collecting files: {e}")
            return set()

        # Process PBOs first
        if pbo_files:
            pbo_limit = max_files // 2 if max_files else len(pbo_files)
            processed_pbos = pbo_files[:pbo_limit]
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                pbo_futures = [executor.submit(self._scan_pbo, pbo) for pbo in processed_pbos]
                for future in as_completed(pbo_futures):
                    try:
                        all_assets.update(future.result())
                    except Exception as e:
                        logger.error(f"PBO scanning error: {e}")

        # Process regular files if we haven't hit the limit
        if not max_files or len(all_assets) < max_files:
            remaining = max_files - len(all_assets) if max_files else None
            file_subset = regular_files[:remaining] if remaining else regular_files
            try:
                all_assets.update(self._scan_regular_files(path, patterns, file_subset))
            except Exception as e:
                logger.error(f"Regular file scanning error: {e}")

        # Final size enforcement
        if max_files and len(all_assets) > max_files:
            all_assets = set(list(all_assets)[:max_files])

        # Cache results
        try:
            self.cache_mgr.cache_scan(str(path), all_assets)
        except Exception as e:
            logger.error(f"Cache write error: {e}")

        return all_assets

    def _normalize_asset_path(self, path: str) -> str:
        """
        Normalize asset paths consistently.
        
        Handles:
        - Case normalization
        - Path separator normalization
        - Double prefix removal
        - Trailing/leading slash removal
        - Common path prefixes
        """
        # Convert to lowercase and normalize separators
        norm_path = path.lower().replace('\\', '/')
        
        # Remove any double prefixes
        prefixes = ['a3/', 'arma3/', '@/', 'addons/']
        for prefix in prefixes:
            while f"{prefix}{prefix}" in norm_path:
                norm_path = norm_path.replace(f"{prefix}{prefix}", prefix)
                
        # Clean up slashes and spaces
        norm_path = norm_path.strip('/ ')
        
        # Remove any ./ or ../ components
        parts = [p for p in norm_path.split('/') 
                if p and p != '.' and p != '..']
        
        return '/'.join(parts)

    def _scan_pbo(self, pbo_path: Path) -> Set[Asset]:
        """List PBO contents efficiently with caching and error handling"""
        try:
            # Check cache first using file hash
            file_hash = self._get_file_hash(pbo_path)
            if cached := self.cache_mgr.get_cached_scan(f"pbo_{file_hash}"):
                return cached

            # Use extractpbo with -LBP flag for fast listing
            result = subprocess.run(
                ['extractpbo', '-LBP', str(pbo_path)],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                check=True
            )
            
            assets = set()
            prefix = None
            
            # Process output lines efficiently
            for line in result.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                    
                # Extract prefix from first non-empty line
                if prefix is None:
                    if line.startswith('prefix='):
                        prefix = line.split('=')[1].strip(';').strip()
                        continue
                    prefix = ''  # No prefix found
                    
                # Skip property section markers
                if line.startswith('//<'):
                    continue
                if line.startswith('//</'): 
                    continue
                    
                # Fast extension check
                if any(line.lower().endswith(ext) for ext in {'.paa', '.p3d', '.wss', '.ogg', '.sqf'}):
                    rel_path = self._normalize_asset_path(
                        f"{prefix}/{line}" if prefix else line
                    )
                    assets.add(Asset(
                        path=Path(rel_path),
                        checksum="list_only",
                        source=pbo_path.stem,
                        last_scan=datetime.now()
                    ))
                    
            # Cache the results
            self.cache_mgr.cache_scan(f"pbo_{file_hash}", assets)
            return assets
            
        except subprocess.TimeoutExpired:
            logger.warning(f"PBO list timeout: {pbo_path}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"PBO list failed: {pbo_path} - {e.stderr}")
        except Exception as e:
            logger.error(f"PBO list error: {pbo_path} - {e}")
            
        return set()

    def _scan_regular_files(self, path: Path, patterns: List[Pattern], max_files: Optional[int] = None) -> Set[Asset]:
        """Scan regular files matching patterns with optional limit"""
        assets = set()
        files_processed = 0
        
        try:
            for file_path in path.rglob('*'):
                if file_path.suffix.lower() in {'.paa', '.p3d', '.sqf'}:
                    try:
                        rel_path = str(file_path.relative_to(path))
                        if not any(p.match(rel_path) for p in patterns):
                            continue
                            
                        # Special simplified handling for SQF files
                        if file_path.suffix.lower() == '.sqf':
                            # For SQF files, just record that we found them without parsing
                            # This avoids the comparison issues
                            asset = Asset(
                                path=file_path.relative_to(path),
                                checksum="sqf_present",  # Simple presence marker
                                source=path.name,
                                last_scan=datetime.now()
                            )
                            assets.add(asset)
                            files_processed += 1
                            continue

                        # Normal handling for other file types
                        try:
                            checksum = self._get_file_hash(file_path)
                            asset = Asset(
                                path=file_path.relative_to(path),
                                checksum=checksum,
                                source=path.name,
                                last_scan=datetime.now()
                            )
                            assets.add(asset)
                            files_processed += 1
                        except Exception as e:
                            logger.error(f"Error scanning file {file_path}: {e}")
                            continue
                            
                        if max_files and files_processed >= max_files:
                            logger.info(f"Reached file limit of {max_files}")
                            break
                            
                    except Exception as e:
                        logger.debug(f"Error processing file {file_path}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error scanning directory: {e}")
            
        return assets

    def _get_file_hash(self, path: Path) -> str:
        """Generate MD5 hash of file"""
        hasher = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
        
    def _get_cache_key(self, path: Path) -> str:
        """Generate cache key for directory"""
        return f"scan_{path.name}_{path.stat().st_mtime}"
