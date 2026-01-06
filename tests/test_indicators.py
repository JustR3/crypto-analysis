"""Tests for technical indicators."""

import pytest
import pandas as pd
import numpy as np
from analysis.technical_indicators import calculate_rsi, calculate_macd, calculate_sma


def test_calculate_sma():
    """Test simple moving average calculation."""
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    sma = calculate_sma(data, period=3)
    
    # First two values should be NaN
    assert pd.isna(sma.iloc[0])
    assert pd.isna(sma.iloc[1])
    
    # Third value should be average of first 3
    assert sma.iloc[2] == 2.0


# Add more tests as needed
