# Project Structure and File Usage Guide

This document explains the structure and purpose of all files in the crypto-analysis project.

## Directory Structure

```
crypto-analysis/
├── data/                    # Data fetching and caching
│   ├── __init__.py
│   ├── fetch_data.py       # CCXT data fetching with caching
│   └── raw/                # Cached data storage (JSON files)
├── analysis/               # Analysis and visualization
│   ├── __init__.py
│   ├── crypto_analysis.ipynb  # Jupyter notebook for interactive analysis
│   ├── exploratory.py      # Plotting functions for analysis
│   ├── technical_indicators.py  # Technical indicator calculations
│   └── backtests.py        # Backtesting framework
├── strategies/             # Trading strategies
│   ├── __init__.py
│   └── signals.py          # Trading signal generators
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── helpers.py          # Caching and helper utilities
├── main.py                 # CLI entry point
├── pyproject.toml          # Project dependencies (managed by uv)
└── run.sh                  # Helper script to run with uv
```

---

## File Descriptions

### Core Application Files

#### `main.py`
**Purpose**: Command-line interface entry point for the application.

**Usage**:
```bash
uv run python main.py --symbol BTC/USDT --action analyze
```

**Features**:
- CLI interface for all analysis functions
- Actions: `fetch`, `plot`, `analyze`, `backtest`, `cache-info`, `clear-cache`
- Supports different exchanges, timeframes, and strategies
- Displays results in terminal and opens plots in separate windows

**Key Functions**:
- `main()`: Parses arguments and routes to appropriate analysis functions

---

### Data Module (`data/`)

#### `data/fetch_data.py`
**Purpose**: Fetch cryptocurrency data from exchanges using CCXT with local caching.

**Key Classes**:
- `CryptoDataFetcher`: Main class for fetching data with caching support

**Key Methods**:
- `fetch_ohlcv()`: Fetch OHLCV (Open, High, Low, Close, Volume) data
- `fetch_ticker()`: Get current ticker information
- `fetch_trades()`: Get recent trades
- `get_markets()`: List available markets on exchange

**Features**:
- Automatic local caching to `data/raw/` directory
- Cache keyed by symbol, timeframe, and parameters
- Optional cache expiration (max_age_hours)
- Supports multiple exchanges (Binance, Coinbase, Kraken, etc.)

**Example**:
```python
fetcher = CryptoDataFetcher(exchange_name='binance', use_cache=True)
df = fetcher.fetch_ohlcv('BTC/USDT', '1d', days=365)
```

**Convenience Function**:
- `fetch_ohlcv()`: Standalone function for quick data fetching

---

### Analysis Module (`analysis/`)

#### `analysis/crypto_analysis.ipynb`
**Purpose**: Jupyter notebook for interactive cryptocurrency analysis with inline visualizations.

**Usage**:
- Open in VS Code/Cursor or JupyterLab
- Run cells interactively to see plots inline
- Modify parameters (SYMBOL, TIMEFRAME, DAYS) to analyze different assets

**Sections**:
1. Data loading with caching
2. Price charts with volume
3. Technical indicators visualization
4. Correlation analysis
5. Returns and volatility analysis
6. Strategy backtesting
7. Custom analysis cells

**Best For**: Interactive exploration, experimentation, and visualization

---

#### `analysis/exploratory.py`
**Purpose**: Plotting functions for exploratory data analysis. Can be used in scripts or imported into notebooks.

**Key Functions**:
- `load_crypto_data()`: Load cryptocurrency data with date range
- `plot_price_chart()`: Basic price chart with volume
- `plot_indicators()`: Price with technical indicators (RSI, MACD, Bollinger Bands)
- `plot_correlation_matrix()`: Correlation heatmap of price and volume
- `plot_returns_analysis()`: Returns distribution, cumulative returns, volatility

**Features**:
- Jupyter-compatible with `# %%` cell markers
- Inline plotting support for notebooks
- Returns matplotlib figure objects for further customization

**Example**:
```python
from analysis.exploratory import plot_price_chart, load_crypto_data

df = load_crypto_data('ETH/USDT', '1d', days=180)
plot_price_chart(df, 'ETH/USDT')
```

---

#### `analysis/technical_indicators.py`
**Purpose**: Calculate technical indicators for cryptocurrency analysis.

**Key Functions**:
- `calculate_rsi()`: Relative Strength Index (default period: 14)
- `calculate_macd()`: Moving Average Convergence Divergence
- `calculate_bollinger_bands()`: Bollinger Bands with configurable std dev
- `calculate_sma()`: Simple Moving Average
- `calculate_ema()`: Exponential Moving Average
- `calculate_atr()`: Average True Range
- `calculate_stochastic()`: Stochastic Oscillator
- `add_indicators()`: Add all common indicators to a DataFrame

**Usage**:
```python
from analysis.technical_indicators import add_indicators, calculate_rsi

# Add all indicators at once
df_with_indicators = add_indicators(df)

# Or calculate individual indicators
rsi = calculate_rsi(df['close'], period=14)
```

**Returns**: Pandas Series or DataFrames with indicator values

---

#### `analysis/backtests.py`
**Purpose**: Backtesting framework for evaluating trading strategies on historical data.

**Key Classes**:
- `SimpleBacktester`: Backtesting engine
- `BacktestResult`: Dataclass containing backtest metrics

**Key Methods**:
- `run_backtest()`: Execute backtest with a signal function
- `print_results()`: Display formatted backtest results
- `plot_backtest_results()`: Visualize backtest performance

**Metrics Calculated**:
- Total return (%)
- Sharpe ratio (annualized)
- Maximum drawdown (%)
- Win rate (%)
- Total number of trades
- Equity curve over time

**Usage**:
```python
from analysis.backtests import SimpleBacktester
from strategies.signals import simple_ma_crossover

backtester = SimpleBacktester(initial_balance=10000.0, commission=0.001)
result = backtester.run_backtest(df, simple_ma_crossover, position_size=1.0)
backtester.print_results(result)
plot_backtest_results(df, result)
```

**Features**:
- Configurable initial balance and commission
- Position sizing control
- Trade-by-trade tracking
- Drawdown visualization

---

### Strategies Module (`strategies/`)

#### `strategies/signals.py`
**Purpose**: Generate trading signals based on technical indicators.

**Key Functions**:
- `simple_ma_crossover()`: Moving average crossover strategy
  - Buy when fast MA crosses above slow MA
  - Sell when fast MA crosses below slow MA
- `rsi_strategy()`: RSI-based mean reversion
  - Buy when RSI crosses above oversold (30)
  - Sell when RSI crosses below overbought (70)
- `macd_strategy()`: MACD crossover
  - Buy when MACD crosses above signal line
  - Sell when MACD crosses below signal line
- `bollinger_bands_strategy()`: Bollinger Bands mean reversion
  - Buy when price touches lower band
  - Sell when price touches upper band
- `combined_strategy()`: Multi-indicator strategy using majority vote

**Returns**: Pandas Series with signals:
- `1`: Buy signal
- `-1`: Sell signal
- `0`: Hold/no signal

**Usage**:
```python
from strategies.signals import simple_ma_crossover, rsi_strategy

# Generate signals
signals = simple_ma_crossover(df, fast_period=20, slow_period=50)
# Use with backtester
result = backtester.run_backtest(df, simple_ma_crossover)
```

**Customization**: All functions accept parameters to adjust indicator periods and thresholds

---

### Utils Module (`utils/`)

#### `utils/helpers.py`
**Purpose**: Utility functions for caching and data management.

**Key Functions**:
- `get_cache_dir()`: Get path to cache directory
- `generate_cache_key()`: Create unique cache key from request parameters
- `load_from_cache()`: Load cached data if available and not expired
- `save_to_cache()`: Save data to cache file
- `clear_cache()`: Delete cache files (optionally by exchange or age)
- `get_cache_info()`: Get statistics about cached files

**Cache Storage**:
- Location: `data/raw/`
- Format: JSON files
- Naming: `{exchange}_{cache_key}.json`
- Cache keys: MD5 hash of symbol, timeframe, and parameters

**Usage**:
```python
from utils.helpers import get_cache_info, clear_cache

# Check cache status
info = get_cache_info()
print(f"Total cached files: {info['total_files']}")

# Clear old cache (older than 7 days)
deleted = clear_cache(older_than_days=7)
```

---

### Configuration Files

#### `pyproject.toml`
**Purpose**: Project configuration and dependencies managed by uv.

**Key Sections**:
- `[project]`: Project metadata and dependencies
- `[dependency-groups]`: Development dependencies (ipykernel for Jupyter)

**Dependencies Include**:
- `ccxt`: Exchange API integration
- `pandas`, `numpy`: Data manipulation
- `matplotlib`, `seaborn`: Visualization
- `jupyterlab`: Jupyter notebook support
- `ta-lib`: Technical analysis library (optional)

**Management**: Use `uv` commands to manage dependencies

---

#### `run.sh`
**Purpose**: Convenience script to run the application with uv.

**Usage**:
```bash
./run.sh --symbol BTC/USDT --action analyze
```

**Why**: Simplifies running commands when system Python differs from project Python

---

## Workflow Examples

### 1. Interactive Analysis (Recommended)
```bash
# Open Jupyter notebook in IDE
# Edit and run cells in analysis/crypto_analysis.ipynb
```

### 2. Quick CLI Analysis
```bash
uv run python main.py --symbol ETH/USDT --action analyze
```

### 3. Custom Script
```python
from data.fetch_data import CryptoDataFetcher
from analysis.technical_indicators import add_indicators
from analysis.exploratory import plot_price_chart

fetcher = CryptoDataFetcher('binance', use_cache=True)
df = fetcher.fetch_ohlcv('BTC/USDT', '1d', days=365)
df = add_indicators(df)
plot_price_chart(df, 'BTC/USDT')
```

### 4. Backtesting
```python
from data.fetch_data import CryptoDataFetcher
from analysis.backtests import SimpleBacktester
from strategies.signals import simple_ma_crossover

fetcher = CryptoDataFetcher('binance')
df = fetcher.fetch_ohlcv('BTC/USDT', '1d', days=365)

backtester = SimpleBacktester(initial_balance=10000.0)
result = backtester.run_backtest(df, simple_ma_crossover)
backtester.print_results(result)
```

---

## Best Practices

1. **Use Caching**: Always enable caching (`use_cache=True`) to avoid rate limits
2. **Notebooks for Exploration**: Use `crypto_analysis.ipynb` for interactive analysis
3. **Scripts for Automation**: Use `main.py` or custom scripts for automated analysis
4. **Cache Management**: Periodically clear old cache files to save disk space
5. **Error Handling**: Exchange APIs may have rate limits; caching helps mitigate this

---

## File Relationships

```
main.py
  └─> data/fetch_data.py
      └─> utils/helpers.py (caching)
  └─> analysis/exploratory.py
      └─> analysis/technical_indicators.py
  └─> analysis/backtests.py
      └─> strategies/signals.py
          └─> analysis/technical_indicators.py

crypto_analysis.ipynb
  └─> (imports all modules above)
```

---

## Summary

- **Data Layer**: `data/fetch_data.py` + `utils/helpers.py` handle fetching and caching
- **Analysis Layer**: `analysis/` contains visualization and backtesting tools
- **Strategy Layer**: `strategies/signals.py` generates trading signals
- **Interface**: `main.py` (CLI) and `crypto_analysis.ipynb` (interactive)

All modules are designed to work together while remaining independent and reusable.

