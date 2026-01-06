"""Configuration settings for the crypto-analysis project."""

# Exchange settings
DEFAULT_EXCHANGE = 'binance'
AVAILABLE_EXCHANGES = ['binance', 'coinbase', 'kraken', 'kucoin']

# Data settings
DEFAULT_TIMEFRAME = '1d'
DEFAULT_DAYS = 365
CACHE_MAX_AGE_HOURS = None  # None = never expire

# Technical indicator settings
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

BB_PERIOD = 20
BB_STD_DEV = 2.0

MA_FAST_PERIOD = 20
MA_SLOW_PERIOD = 50

# Backtesting settings
INITIAL_BALANCE = 10000.0
COMMISSION_RATE = 0.001  # 0.1%
POSITION_SIZE = 1.0  # 100% of capital

# Plotting settings
FIGURE_DPI = 100
FIGURE_WIDTH = 14
FIGURE_HEIGHT = 10
