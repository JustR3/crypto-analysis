"""Trading signal generation functions."""

import pandas as pd
import numpy as np
from analysis.technical_indicators import (
    calculate_rsi,
    calculate_macd,
    calculate_sma
)


def simple_ma_crossover(df: pd.DataFrame, fast_period: int = 20, slow_period: int = 50) -> pd.Series:
    """
    Simple moving average crossover strategy.
    
    Buy when fast MA crosses above slow MA.
    Sell when fast MA crosses below slow MA.
    
    Returns:
        Series with signals: 1 (buy), -1 (sell), 0 (hold)
    """
    fast_ma = calculate_sma(df['close'], fast_period)
    slow_ma = calculate_sma(df['close'], slow_period)
    
    signals = pd.Series(0, index=df.index)
    
    # Buy signal: fast MA crosses above slow MA
    buy_signal = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
    signals[buy_signal] = 1
    
    # Sell signal: fast MA crosses below slow MA
    sell_signal = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))
    signals[sell_signal] = -1
    
    return signals


def rsi_strategy(df: pd.DataFrame, rsi_period: int = 14, oversold: int = 30, overbought: int = 70) -> pd.Series:
    """
    RSI-based strategy.
    
    Buy when RSI crosses above oversold level.
    Sell when RSI crosses below overbought level.
    
    Returns:
        Series with signals: 1 (buy), -1 (sell), 0 (hold)
    """
    rsi = calculate_rsi(df['close'], rsi_period)
    
    signals = pd.Series(0, index=df.index)
    
    # Buy signal: RSI crosses above oversold
    buy_signal = (rsi > oversold) & (rsi.shift(1) <= oversold)
    signals[buy_signal] = 1
    
    # Sell signal: RSI crosses below overbought
    sell_signal = (rsi < overbought) & (rsi.shift(1) >= overbought)
    signals[sell_signal] = -1
    
    return signals


def macd_strategy(df: pd.DataFrame) -> pd.Series:
    """
    MACD crossover strategy.
    
    Buy when MACD crosses above signal line.
    Sell when MACD crosses below signal line.
    
    Returns:
        Series with signals: 1 (buy), -1 (sell), 0 (hold)
    """
    from analysis.technical_indicators import calculate_macd
    
    macd_data = calculate_macd(df['close'])
    macd = macd_data['macd']
    signal = macd_data['signal']
    
    signals = pd.Series(0, index=df.index)
    
    # Buy signal: MACD crosses above signal
    buy_signal = (macd > signal) & (macd.shift(1) <= signal.shift(1))
    signals[buy_signal] = 1
    
    # Sell signal: MACD crosses below signal
    sell_signal = (macd < signal) & (macd.shift(1) >= signal.shift(1))
    signals[sell_signal] = -1
    
    return signals



