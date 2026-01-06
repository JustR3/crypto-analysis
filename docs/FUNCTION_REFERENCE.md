# Function Reference and Modification Guide

This document explains all functions in the crypto-analysis project. **Edit this file to request changes** - add your instructions in the "MODIFICATION REQUESTS" section at the bottom.

---

## Table of Contents

1. [Data Fetching Module](#data-fetching-module)
2. [Caching Utilities](#caching-utilities)
3. [Technical Indicators](#technical-indicators)
4. [Exploratory Analysis](#exploratory-analysis)
5. [Trading Strategies](#trading-strategies)
6. [Backtesting](#backtesting)
7. [Modification Requests](#modification-requests)

---

## Data Fetching Module

**File:** `data/fetch_data.py`

### Class: `CryptoDataFetcher`

#### `__init__(exchange_name='binance', use_cache=True, cache_max_age_hours=None)`

**What it does:** Initializes a data fetcher for a specific exchange.

**How it works:**
- Takes exchange name (e.g., 'binance', 'coinbase', 'kraken')
- Uses CCXT library to create exchange instance
- Sets up rate limiting to respect API limits
- Configures caching behavior

**Parameters:**
- `exchange_name` (str): Exchange identifier
- `use_cache` (bool): Enable/disable local caching
- `cache_max_age_hours` (int, optional): Cache expiration in hours (None = never expire)

**Returns:** None (constructor)

**Usage:**
```python
fetcher = CryptoDataFetcher('binance', use_cache=True)
```

---

#### `fetch_ohlcv(symbol, timeframe='1d', since=None, limit=None)`

**What it does:** Fetches OHLCV (Open, High, Low, Close, Volume) candle data from exchange.

**How it works:**
1. Generates cache key from parameters
2. Checks cache first (if enabled)
3. If cache hit and valid, returns cached data
4. If cache miss, fetches from exchange API
5. Converts to pandas DataFrame with timestamp index
6. Saves to cache for future use

**Parameters:**
- `symbol` (str): Trading pair like 'BTC/USDT'
- `timeframe` (str): '1m', '5m', '15m', '1h', '4h', '1d', '1w'
- `since` (int, optional): Start timestamp in milliseconds
- `limit` (int, optional): Max number of candles

**Returns:** `pd.DataFrame` with columns: open, high, low, close, volume (indexed by timestamp)

**Usage:**
```python
df = fetcher.fetch_ohlcv('BTC/USDT', '1d', since=timestamp)
```

---

#### `get_cache_info()`

**What it does:** Returns information about cached data files.

**How it works:** Calls utility function to get cache statistics.

**Returns:** `Dict[str, Any]` with keys: total_files, total_size_mb, cache_directory

---

### Function: `fetch_ohlcv(symbol, timeframe='1d', exchange='binance', since=None, limit=None, use_cache=True)`

**What it does:** Convenience wrapper function for quick data fetching.

**How it works:** Creates a `CryptoDataFetcher` instance and calls its `fetch_ohlcv` method.

**Parameters:** Same as class method, plus `exchange` parameter

**Returns:** `pd.DataFrame` with OHLCV data

**Usage:**
```python
df = fetch_ohlcv('BTC/USDT', '1d', exchange='binance')
```

---

## Caching Utilities

**File:** `utils/helpers.py`

### `get_cache_dir() -> Path`

**What it does:** Returns the path to the cache directory.

**How it works:** 
- Calculates path relative to utils module: `project_root/data/raw/`
- Creates directory if it doesn't exist
- Returns Path object

**Returns:** `Path` object pointing to cache directory

---

### `generate_cache_key(symbol, timeframe, since=None, limit=None) -> str`

**What it does:** Creates a unique MD5 hash key for caching requests.

**How it works:**
1. Combines symbol, timeframe, since, limit into string
2. Joins with underscores
3. Creates MD5 hash
4. Returns hex digest

**Parameters:**
- `symbol` (str): Trading pair
- `timeframe` (str): Timeframe string
- `since` (int, optional): Timestamp
- `limit` (int, optional): Limit value

**Returns:** `str` - MD5 hash (32 character hex string)

**Example:** `"BTC/USDT_1d_1234567890"` → `"a8bfec32ff89462c9675d3736917cb02"`

---

### `get_cache_path(cache_key, exchange) -> Path`

**What it does:** Constructs full file path for a cache file.

**How it works:** Combines cache directory + exchange name + cache key + `.json`

**Returns:** `Path` object

**Example:** `data/raw/binance_a8bfec32ff89462c9675d3736917cb02.json`

---

### `load_from_cache(cache_key, exchange, max_age_hours=None) -> Optional[list]`

**What it does:** Loads cached data if it exists and hasn't expired.

**How it works:**
1. Gets cache file path
2. Checks if file exists
3. If `max_age_hours` set, checks file modification time
4. Reads JSON file
5. Returns data list or None if expired/missing

**Parameters:**
- `cache_key` (str): MD5 hash key
- `exchange` (str): Exchange name
- `max_age_hours` (int, optional): Maximum age in hours

**Returns:** `Optional[list]` - Cached OHLCV data or None

---

### `save_to_cache(cache_key, exchange, data) -> None`

**What it does:** Saves data to cache file as JSON.

**How it works:**
1. Gets cache file path
2. Writes data as formatted JSON (indent=2)
3. Handles IO errors gracefully

**Parameters:**
- `cache_key` (str): MD5 hash key
- `exchange` (str): Exchange name
- `data` (list): OHLCV data to cache

**Returns:** None

---

### `clear_cache(exchange=None, older_than_days=None) -> int`

**What it does:** Deletes cache files, optionally filtered by exchange or age.

**How it works:**
1. Scans cache directory for `.json` files
2. Filters by exchange name (if provided)
3. Filters by age (if provided) - deletes files older than X days
4. Deletes matching files
5. Returns count of deleted files

**Parameters:**
- `exchange` (str, optional): Only delete files for this exchange
- `older_than_days` (int, optional): Only delete files older than this

**Returns:** `int` - Number of files deleted

---

### `get_cache_info() -> Dict[str, Any]`

**What it does:** Returns statistics about cached files.

**How it works:**
1. Lists all `.json` files in cache directory
2. Calculates total file count
3. Sums total file sizes
4. Converts to MB

**Returns:** `Dict` with keys: `total_files`, `total_size_mb`, `cache_directory`

---

## Technical Indicators

**File:** `analysis/technical_indicators.py`

### `calculate_rsi(prices, period=14) -> pd.Series`

**What it does:** Calculates Relative Strength Index (RSI) - momentum oscillator.

**How it works:**
1. Calculates price changes (delta)
2. Separates gains (positive) and losses (negative)
3. Calculates average gain and average loss over period
4. Computes RS = avg_gain / avg_loss
5. RSI = 100 - (100 / (1 + RS))
6. Values range 0-100 (70+ overbought, 30- oversold)

**Parameters:**
- `prices` (pd.Series): Closing prices
- `period` (int): Lookback period (default 14)

**Returns:** `pd.Series` with RSI values

---

### `calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9) -> pd.DataFrame`

**What it does:** Calculates MACD (Moving Average Convergence Divergence).

**How it works:**
1. Calculates fast EMA (12 periods) and slow EMA (26 periods)
2. MACD line = fast EMA - slow EMA
3. Signal line = EMA of MACD (9 periods)
4. Histogram = MACD - Signal

**Parameters:**
- `prices` (pd.Series): Closing prices
- `fast_period` (int): Fast EMA period (default 12)
- `slow_period` (int): Slow EMA period (default 26)
- `signal_period` (int): Signal line period (default 9)

**Returns:** `pd.DataFrame` with columns: `macd`, `signal`, `histogram`

---

### `calculate_bollinger_bands(prices, period=20, std_dev=2.0) -> pd.DataFrame`

**What it does:** Calculates Bollinger Bands - volatility bands around price.

**How it works:**
1. Calculates SMA over period (default 20)
2. Calculates standard deviation over same period
3. Upper band = SMA + (std_dev × std)
4. Lower band = SMA - (std_dev × std)
5. Middle band = SMA

**Parameters:**
- `prices` (pd.Series): Closing prices
- `period` (int): Moving average period (default 20)
- `std_dev` (float): Standard deviation multiplier (default 2.0)

**Returns:** `pd.DataFrame` with columns: `upper`, `middle`, `lower`

---

### `calculate_sma(prices, period) -> pd.Series`

**What it does:** Calculates Simple Moving Average.

**How it works:** Rolling window mean over specified period.

**Parameters:**
- `prices` (pd.Series): Price series
- `period` (int): Window size

**Returns:** `pd.Series` with SMA values

---

### `calculate_ema(prices, period) -> pd.Series`

**What it does:** Calculates Exponential Moving Average (gives more weight to recent prices).

**How it works:** Uses pandas `ewm()` with specified span, no adjustment.

**Parameters:**
- `prices` (pd.Series): Price series
- `period` (int): EMA span

**Returns:** `pd.Series` with EMA values

---

### `calculate_atr(high, low, close, period=14) -> pd.Series`

**What it does:** Calculates Average True Range - measures volatility.

**How it works:**
1. True Range = max of:
   - High - Low
   - |High - Previous Close|
   - |Low - Previous Close|
2. ATR = rolling mean of True Range over period

**Parameters:**
- `high` (pd.Series): High prices
- `low` (pd.Series): Low prices
- `close` (pd.Series): Closing prices
- `period` (int): ATR period (default 14)

**Returns:** `pd.Series` with ATR values

---

### `calculate_stochastic(high, low, close, k_period=14, d_period=3) -> pd.DataFrame`

**What it does:** Calculates Stochastic Oscillator - momentum indicator.

**How it works:**
1. Finds lowest low and highest high over k_period
2. %K = 100 × ((Close - Lowest Low) / (Highest High - Lowest Low))
3. %D = Moving average of %K over d_period

**Parameters:**
- `high` (pd.Series): High prices
- `low` (pd.Series): Low prices
- `close` (pd.Series): Closing prices
- `k_period` (int): %K period (default 14)
- `d_period` (int): %D period (default 3)

**Returns:** `pd.DataFrame` with columns: `k`, `d`

---

### `add_indicators(df) -> pd.DataFrame`

**What it does:** Adds all common technical indicators to a DataFrame at once.

**How it works:**
1. Copies input DataFrame
2. Calculates and adds: SMA 20, SMA 50, EMA 12, EMA 26
3. Adds RSI
4. Adds MACD (macd, signal, histogram)
5. Adds Bollinger Bands (upper, middle, lower)
6. Adds ATR
7. Adds Stochastic (k, d)

**Parameters:**
- `df` (pd.DataFrame): DataFrame with columns: open, high, low, close, volume

**Returns:** `pd.DataFrame` with all indicator columns added

---

## Exploratory Analysis

**File:** `analysis/exploratory.py`

### `load_crypto_data(symbol='BTC/USDT', timeframe='1d', days=365) -> pd.DataFrame`

**What it does:** Convenience function to load crypto data for specified number of days.

**How it works:**
1. Creates CryptoDataFetcher with binance exchange
2. Calculates timestamp for N days ago
3. Fetches OHLCV data from that timestamp to now
4. Returns DataFrame

**Parameters:**
- `symbol` (str): Trading pair
- `timeframe` (str): Candle timeframe
- `days` (int): Number of days of history

**Returns:** `pd.DataFrame` with OHLCV data

---

### `plot_price_chart(df, symbol='BTC/USDT) -> matplotlib.figure.Figure`

**What it does:** Creates a 2-panel chart showing price and volume.

**How it works:**
1. Creates 2 subplots (price on top, volume on bottom)
2. Plots close price line with high-low fill
3. Plots volume bars
4. Adds labels, legends, grid

**Parameters:**
- `df` (pd.DataFrame): OHLCV data
- `symbol` (str): Trading pair name for title

**Returns:** `matplotlib.figure.Figure` object

---

### `plot_indicators(df, symbol='BTC/USDT') -> matplotlib.figure.Figure`

**What it does:** Creates 4-panel chart with price, RSI, MACD, and volume.

**How it works:**
1. Adds all indicators to DataFrame
2. Creates 4 subplots
3. Panel 1: Price with SMA 20, SMA 50, Bollinger Bands
4. Panel 2: RSI with overbought/oversold lines (70/30)
5. Panel 3: MACD line, signal line, histogram
6. Panel 4: Volume bars

**Parameters:**
- `df` (pd.DataFrame): OHLCV data
- `symbol` (str): Trading pair name

**Returns:** `matplotlib.figure.Figure` object

---

### `plot_correlation_matrix(df) -> matplotlib.figure.Figure`

**What it does:** Creates heatmap showing correlation between price columns and volume.

**How it works:**
1. Calculates correlation matrix for: open, high, low, close, volume
2. Creates seaborn heatmap with annotations
3. Uses coolwarm colormap centered at 0

**Parameters:**
- `df` (pd.DataFrame): OHLCV data

**Returns:** `matplotlib.figure.Figure` object

---

### `plot_returns_analysis(df) -> matplotlib.figure.Figure`

**What it does:** Creates 4-panel analysis of returns and volatility.

**How it works:**
1. Calculates returns (pct_change) and log returns
2. Panel 1: Histogram of returns distribution
3. Panel 2: Cumulative returns over time
4. Panel 3: Returns time series
5. Panel 4: 30-day rolling volatility (annualized)

**Parameters:**
- `df` (pd.DataFrame): OHLCV data

**Returns:** `matplotlib.figure.Figure` object

---

## Trading Strategies

**File:** `strategies/signals.py`

### `simple_ma_crossover(df, fast_period=20, slow_period=50) -> pd.Series`

**What it does:** Generates buy/sell signals based on moving average crossover.

**How it works:**
1. Calculates fast SMA and slow SMA
2. Buy signal: When fast MA crosses above slow MA (golden cross)
3. Sell signal: When fast MA crosses below slow MA (death cross)
4. Uses previous period comparison to detect crossovers

**Parameters:**
- `df` (pd.DataFrame): OHLCV data
- `fast_period` (int): Fast MA period (default 20)
- `slow_period` (int): Slow MA period (default 50)

**Returns:** `pd.Series` with values: 1 (buy), -1 (sell), 0 (hold)

---

### `rsi_strategy(df, rsi_period=14, oversold=30, overbought=70) -> pd.Series`

**What it does:** Generates signals based on RSI crossing oversold/overbought levels.

**How it works:**
1. Calculates RSI
2. Buy signal: When RSI crosses above oversold level (30)
3. Sell signal: When RSI crosses below overbought level (70)
4. Uses previous period to detect crossings

**Parameters:**
- `df` (pd.DataFrame): OHLCV data
- `rsi_period` (int): RSI calculation period (default 14)
- `oversold` (int): Oversold threshold (default 30)
- `overbought` (int): Overbought threshold (default 70)

**Returns:** `pd.Series` with values: 1 (buy), -1 (sell), 0 (hold)

---

### `macd_strategy(df) -> pd.Series`

**What it does:** Generates signals based on MACD line crossing signal line.

**How it works:**
1. Calculates MACD and signal line
2. Buy signal: When MACD crosses above signal line
3. Sell signal: When MACD crosses below signal line
4. Uses previous period comparison

**Parameters:**
- `df` (pd.DataFrame): OHLCV data

**Returns:** `pd.Series` with values: 1 (buy), -1 (sell), 0 (hold)

---

## Backtesting

**File:** `analysis/backtests.py`

### Class: `SimpleBacktester`

#### `__init__(initial_balance=10000.0, commission=0.001)`

**What it does:** Initializes backtesting engine.

**Parameters:**
- `initial_balance` (float): Starting capital
- `commission` (float): Commission rate (0.001 = 0.1%)

---

#### `run_backtest(data, signal_func, position_size=1.0) -> BacktestResult`

**What it does:** Runs a backtest simulation on historical data.

**How it works:**
1. Generates signals using signal function
2. Iterates through data chronologically
3. Executes trades when signals change:
   - Buy: Uses position_size fraction of balance, deducts commission
   - Sell: Closes position, deducts commission
4. Tracks balance, position, equity over time
5. Calculates metrics:
   - Total return %
   - Sharpe ratio (annualized, assumes daily data)
   - Max drawdown %
   - Win rate % (from completed trades)
   - Total trades count

**Parameters:**
- `data` (pd.DataFrame): OHLCV historical data
- `signal_func` (Callable): Function that takes DataFrame, returns Series of signals
- `position_size` (float): Fraction of capital per trade (0.0 to 1.0)

**Returns:** `BacktestResult` dataclass with all metrics

---

#### `print_results(result) -> None`

**What it does:** Prints formatted backtest results to console.

**Parameters:**
- `result` (BacktestResult): Results from run_backtest()

**Returns:** None

---

### Function: `plot_backtest_results(data, result) -> matplotlib.figure.Figure`

**What it does:** Creates visualization of backtest performance.

**How it works:**
1. Creates 2 subplots
2. Top panel: Price line + Equity curve (dual y-axis) + Buy/Sell markers
3. Bottom panel: Drawdown chart (shows equity drops from peak)

**Parameters:**
- `data` (pd.DataFrame): Original OHLCV data
- `result` (BacktestResult): Backtest results

**Returns:** `matplotlib.figure.Figure` object

---

## Modification Requests

**Instructions:** Add your change requests below. Use clear descriptions of what you want changed, which functions, and how they should behave differently.

### Example Format:

```markdown
### Request 1: [Date/Description]

**Function:** `calculate_rsi()` in `analysis/technical_indicators.py`

**Current behavior:** Uses default period of 14

**Requested change:** 
- Add option to use Wilder's smoothing method
- Add parameter `smoothing_method` with options: 'standard' (current) or 'wilder'

**Priority:** Medium
```

---

### Your Requests:

_Add your modification requests here..._

---

## Notes

- All functions that return DataFrames preserve the original index (usually timestamps)
- Caching is automatic when `use_cache=True` - no manual cache management needed
- Signal functions return Series with same index as input DataFrame
- All plotting functions return Figure objects so you can save them: `fig.savefig('output.png')`
- Backtesting assumes daily data for Sharpe ratio calculation (252 trading days/year)

