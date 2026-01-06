"""Main entry point for crypto analysis."""

import argparse
from data.fetch_data import CryptoDataFetcher
from analysis.exploratory import (
    load_crypto_data,
    plot_price_chart,
    plot_indicators,
    plot_correlation_matrix,
    plot_returns_analysis
)
from analysis.backtests import SimpleBacktester, plot_backtest_results
from strategies.signals import simple_ma_crossover, rsi_strategy, macd_strategy
from utils.helpers import get_cache_info, clear_cache


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(description='Cryptocurrency Analysis Tool')
    parser.add_argument('--symbol', default='BTC/USDT', help='Trading pair (default: BTC/USDT)')
    parser.add_argument('--timeframe', default='1d', help='Timeframe (default: 1d)')
    parser.add_argument('--days', type=int, default=365, help='Number of days of data (default: 365)')
    parser.add_argument('--exchange', default='binance', help='Exchange name (default: binance)')
    parser.add_argument('--action', choices=['fetch', 'plot', 'analyze', 'backtest', 'cache-info', 'clear-cache'],
                       default='plot', help='Action to perform')
    parser.add_argument('--strategy', choices=['ma', 'rsi', 'macd'], default='ma',
                       help='Strategy for backtesting (default: ma)')
    
    args = parser.parse_args()
    
    if args.action == 'cache-info':
        info = get_cache_info()
        print(f"Cache Info:")
        print(f"  Total files: {info['total_files']}")
        print(f"  Total size: {info['total_size_mb']} MB")
        print(f"  Directory: {info['cache_directory']}")
        return
    
    if args.action == 'clear-cache':
        deleted = clear_cache()
        print(f"Cleared {deleted} cache files")
        return
    
    # Load data
    print(f"Loading data for {args.symbol} from {args.exchange}...")
    df = load_crypto_data(args.symbol, args.timeframe, args.days)
    print(f"Loaded {len(df)} candles")
    print(f"\nData summary:")
    print(df.describe())
    
    if args.action == 'fetch':
        print("\nData fetched successfully!")
        print(df.head())
        return
    
    if args.action == 'plot':
        print("\nGenerating price chart...")
        plot_price_chart(df, args.symbol)
        import matplotlib.pyplot as plt
        plt.show()
        return
    
    if args.action == 'analyze':
        print("\nGenerating analysis charts...")
        plot_indicators(df, args.symbol)
        plot_correlation_matrix(df)
        plot_returns_analysis(df)
        import matplotlib.pyplot as plt
        plt.show()
        return
    
    if args.action == 'backtest':
        print(f"\nRunning backtest with {args.strategy} strategy...")
        
        # Select strategy
        if args.strategy == 'ma':
            signal_func = simple_ma_crossover
        elif args.strategy == 'rsi':
            signal_func = rsi_strategy
        elif args.strategy == 'macd':
            signal_func = macd_strategy
        
        # Run backtest
        backtester = SimpleBacktester(initial_balance=10000.0, commission=0.001)
        result = backtester.run_backtest(df, signal_func, position_size=1.0)
        
        # Print results
        backtester.print_results(result)
        
        # Plot results
        plot_backtest_results(df, result)
        import matplotlib.pyplot as plt
        plt.show()
        return


if __name__ == "__main__":
    main()
