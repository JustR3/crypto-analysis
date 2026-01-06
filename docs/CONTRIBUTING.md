# Contributing to Crypto Analysis

Thank you for your interest in contributing to this project!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crypto-analysis
   ```

2. **Install dependencies with uv**
   ```bash
   # uv will automatically manage the virtual environment
   uv sync
   ```

3. **Setup Jupyter kernel** (if using notebooks)
   ```bash
   ./scripts/setup_kernel.sh
   ```

## Code Structure

- **data/**: Data fetching and caching logic
- **analysis/**: Analysis, indicators, and backtesting
- **strategies/**: Trading signal generation
- **utils/**: Helper functions
- **config/**: Configuration and settings
- **tests/**: Unit tests

## Running Tests

```bash
uv run pytest tests/
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular

## Adding New Features

### Adding a New Technical Indicator

1. Add the calculation function to `analysis/technical_indicators.py`
2. Add tests to `tests/test_indicators.py`
3. Document the function with a clear docstring
4. Update `docs/FUNCTION_REFERENCE.md`

### Adding a New Trading Strategy

1. Add the signal function to `strategies/signals.py`
2. Add tests to `tests/test_strategies.py`
3. Document parameters and return values
4. Test with backtesting framework

### Adding a New Data Source

1. Extend `data/fetch_data.py` or create a new module
2. Ensure caching works properly
3. Add error handling for API failures
4. Add tests

## Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused on a single change

## Pull Request Process

1. Create a new branch for your feature
2. Make your changes and add tests
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request with a clear description

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Documentation improvements
- Questions about the codebase
