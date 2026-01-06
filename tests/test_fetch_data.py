"""Tests for data fetching module."""

import pytest
from data.fetch_data import CryptoDataFetcher


def test_crypto_data_fetcher_init():
    """Test initialization of CryptoDataFetcher."""
    fetcher = CryptoDataFetcher('binance', use_cache=False)
    assert fetcher.exchange_name == 'binance'
    assert fetcher.use_cache == False


# Add more tests as needed
