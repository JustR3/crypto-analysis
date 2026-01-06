# Cryptocurrency Analysis

A Python project for cryptocurrency data analysis, technical indicators, and backtesting using CCXT, matplotlib, and seaborn.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 📊 **Data Fetching**: Fetch cryptocurrency data from multiple exchanges via CCXT
- 💾 **Local Caching**: Automatic caching to avoid repeated API calls
- 📈 **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages, ATR, Stochastic
- 📉 **Visualizations**: Price charts, indicators, correlation matrices, returns analysis
- 🔄 **Backtesting**: Test trading strategies on historical data
- 📓 **Jupyter Notebooks**: Interactive analysis with inline visualizations

## Quick Start

### 1. Install Dependencies

The project uses `uv` for dependency management. Dependencies are already defined in `pyproject.toml`.

```bash
# Dependencies are automatically managed by uv
```

### 2. Setup Jupyter Kernel (First Time)

To use the Jupyter notebook with the uv-managed virtual environment:

```bash
./scripts/setup_kernel.sh
```

Or manually:
```bash
uv run python -m ipykernel install --user --name crypto-analysis --display-name "Python (crypto-analysis)"
```

### 3. Run Analysis

**Option A: Interactive Jupyter Notebook (Recommended)**
```bash
# Open analysis/crypto_analysis.ipynb in your IDE
# Select kernel: "Python (crypto-analysis)"
# Run cells to see inline visualizations
```

**Option B: Command Line**
```bash
# Plot price chart
uv run python main.py --symbol BTC/USDT --action plot

# Full analysis
uv run python main.py --symbol ETH/USDT --action analyze

# Backtest strategy
uv run python main.py --symbol BTC/USDT --action backtest --strategy ma
```

## Project Structure

```
crypto-analysis/
├── analysis/               # Analysis and visualization modules
│   ├── backtests.py       # Backtesting framework
│   ├── crypto_analysis.ipynb  # Interactive Jupyter notebook
│   ├── exploratory.py     # Plotting and visualization functions
│   └── technical_indicators.py  # Technical indicator calculations
├── config/                # Configuration files
│   └── __init__.py        # Default settings and constants
├── data/                  # Data fetching and storage
│   ├── fetch_data.py      # CCXT data fetching with caching
│   └── raw/               # Cached data (JSON files, gitignored)
├── docs/                  # Documentation
│   ├── FUNCTION_REFERENCE.md  # Function documentation
│   ├── KERNEL_SETUP.md    # Kernel setup guide
│   └── PROJECT_STRUCTURE.md   # Detailed project structure
├── scripts/               # Shell scripts
│   └── setup_kernel.sh    # Jupyter kernel setup
├── strategies/            # Trading strategies
│   └── signals.py         # Trading signal generators
├── tests/                 # Unit tests
│   ├── test_fetch_data.py
│   ├── test_indicators.py
│   └── test_strategies.py
├── utils/                 # Utility functions
│   └── helpers.py         # Caching and helper utilities
├── main.py                # CLI entry point
├── pyproject.toml         # Project dependencies (uv)
├── requirements.txt       # Pip-compatible requirements
├── LICENSE                # MIT License
└── .gitignore             # Git ignore rules
```

For detailed documentation, see [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

## Usage Examples

### Interactive Notebook

1. Open `analysis/crypto_analysis.ipynb` in VS Code/Cursor
2. Select kernel: **"Python (crypto-analysis)"** (uses uv venv)
3. Modify variables in the first cell:
   - `SYMBOL`: Trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
   - `TIMEFRAME`: '1m', '5m', '15m', '1h', '4h', '1d', '1w'
   - `DAYS`: Number of days of historical data
4. Run cells sequentially to see inline plots

### Python Script

```python
from data.fetch_data import CryptoDataFetcher
from analysis.exploratory import plot_price_chart

fetcher = CryptoDataFetcher('binance', use_cache=True)
df = fetcher.fetch_ohlcv('BTC/USDT', '1d', days=365)
plot_price_chart(df, 'BTC/USDT')
```

## Dependencies

Managed by `uv` in `pyproject.toml`:
- `ccxt`: Exchange API integration
- `pandas`, `numpy`: Data manipulation
- `matplotlib`, `seaborn`: Visualization
- `jupyterlab`, `ipykernel`: Jupyter notebook support

For pip users, see [requirements.txt](requirements.txt).

## Testing

Run tests with pytest:

```bash
uv run pytest tests/
```

## Configuration

Default settings are in [config/__init__.py](config/__init__.py). For environment-specific settings, copy [.env.example](.env.example) to `.env` and customize.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on how to contribute to this project.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.

## Notes

- Data is cached in `data/raw/` to avoid rate limits
- Use `uv run` to execute scripts (ensures correct Python version)
- The Jupyter kernel uses the uv-managed virtual environment automatically

