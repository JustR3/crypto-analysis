"""Utility functions for caching and data management."""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib


def get_cache_dir() -> Path:
    """Get the cache directory path."""
    cache_dir = Path(__file__).parent.parent / "data" / "raw"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def generate_cache_key(symbol: str, timeframe: str, since: Optional[int] = None, limit: Optional[int] = None) -> str:
    """Generate a unique cache key for the request."""
    key_parts = [symbol, timeframe]
    if since:
        key_parts.append(str(since))
    if limit:
        key_parts.append(str(limit))
    
    key_string = "_".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def get_cache_path(cache_key: str, exchange: str) -> Path:
    """Get the full path for a cache file."""
    cache_dir = get_cache_dir()
    filename = f"{exchange}_{cache_key}.json"
    return cache_dir / filename


def load_from_cache(cache_key: str, exchange: str, max_age_hours: Optional[int] = None) -> Optional[list]:
    """Load data from cache if it exists and is not expired."""
    cache_path = get_cache_path(cache_key, exchange)
    
    if not cache_path.exists():
        return None
    
    if max_age_hours:
        file_age = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if datetime.now() - file_age > timedelta(hours=max_age_hours):
            return None
    
    try:
        with open(cache_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_to_cache(cache_key: str, exchange: str, data: list) -> None:
    """Save data to cache."""
    cache_path = get_cache_path(cache_key, exchange)
    
    try:
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Warning: Failed to save cache: {e}")


def clear_cache(exchange: Optional[str] = None, older_than_days: Optional[int] = None) -> int:
    """Clear cache files. Optionally filter by exchange or age."""
    cache_dir = get_cache_dir()
    deleted_count = 0
    
    for cache_file in cache_dir.glob("*.json"):
        if exchange and exchange not in cache_file.name:
            continue
        
        if older_than_days:
            file_age = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - file_age < timedelta(days=older_than_days):
                continue
        
        try:
            cache_file.unlink()
            deleted_count += 1
        except OSError:
            pass
    
    return deleted_count


def get_cache_info() -> Dict[str, Any]:
    """Get information about cached files."""
    cache_dir = get_cache_dir()
    cache_files = list(cache_dir.glob("*.json"))
    
    total_size = sum(f.stat().st_size for f in cache_files)
    
    return {
        "total_files": len(cache_files),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "cache_directory": str(cache_dir)
    }

