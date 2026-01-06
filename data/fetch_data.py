"""Fetch cryptocurrency data using CCXT with local caching."""

import ccxt
from typing import Optional, Dict, Any
from datetime import datetime
import pandas as pd
from pathlib import Path

from utils.helpers import (
    generate_cache_key,
    load_from_cache,
    save_to_cache,
    get_cache_info
)


class CryptoDataFetcher:
    """Fetch crypto data from exchanges using CCXT with caching."""
    
    def __init__(self, exchange_name: str = 'binance', use_cache: bool = True, cache_max_age_hours: Optional[int] = None):
        """
        Initialize the data fetcher.
        
        Args:
            exchange_name: Name of the exchange (e.g., 'binance', 'coinbase', 'kraken')
            use_cache: Whether to use local caching
            cache_max_age_hours: Maximum age of cache in hours (None = no expiration)
        """
        self.exchange_name = exchange_name
        self.use_cache = use_cache
        self.cache_max_age_hours = cache_max_age_hours
        
        # Initialize CCXT exchange
        exchange_class = getattr(ccxt, exchange_name)
        self.exchange = exchange_class({
            'enableRateLimit': True,  # Respect rate limits
        })
    
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1d',
        since: Optional[int] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe (e.g., '1m', '5m', '1h', '1d')
            since: Timestamp in milliseconds (optional)
            limit: Number of candles to fetch (optional)
        
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        cache_key = generate_cache_key(symbol, timeframe, since, limit)
        
        # Try to load from cache
        if self.use_cache:
            cached_data = load_from_cache(cache_key, self.exchange_name, self.cache_max_age_hours)
            if cached_data is not None:
                df = pd.DataFrame(cached_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                return df
        
        # Fetch from exchange
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Save to cache
            if self.use_cache:
                save_to_cache(cache_key, self.exchange_name, ohlcv)
            
            return df
        
        except Exception as e:
            raise Exception(f"Error fetching data from {self.exchange_name}: {e}")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about cached data."""
        return get_cache_info()


def fetch_ohlcv(
    symbol: str,
    timeframe: str = '1d',
    exchange: str = 'binance',
    since: Optional[int] = None,
    limit: Optional[int] = None,
    use_cache: bool = True
) -> pd.DataFrame:
    """
    Convenience function to fetch OHLCV data.
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT')
        timeframe: Timeframe (e.g., '1d', '1h', '4h')
        exchange: Exchange name (default: 'binance')
        since: Timestamp in milliseconds (optional)
        limit: Number of candles (optional)
        use_cache: Whether to use caching
    
    Returns:
        DataFrame with OHLCV data
    """
    fetcher = CryptoDataFetcher(exchange_name=exchange, use_cache=use_cache)
    return fetcher.fetch_ohlcv(symbol, timeframe, since, limit)

