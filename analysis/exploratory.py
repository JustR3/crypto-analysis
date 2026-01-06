"""
Exploratory data analysis with Jupyter-style cells.
Use # %% to create cells for interactive analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from data.fetch_data import CryptoDataFetcher
from analysis.technical_indicators import add_indicators

# Set inline plotting for Jupyter/IDE compatibility
try:
    # Try to set inline backend (works in Jupyter notebooks and some IDEs)
    get_ipython().run_line_magic('matplotlib', 'inline')  # type: ignore
except NameError:
    # If not in IPython/Jupyter, use default backend
    plt.ioff()  # Non-interactive mode for scripts

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100


# %% Fetch data
def load_crypto_data(symbol: str = 'BTC/USDT', timeframe: str = '1d', days: int = 365):
    """Load cryptocurrency data."""
    fetcher = CryptoDataFetcher(exchange_name='binance', use_cache=True)
    
    # Calculate since timestamp (days ago)
    from datetime import datetime, timedelta
    since_date = datetime.now() - timedelta(days=days)
    since_timestamp = int(since_date.timestamp() * 1000)
    
    df = fetcher.fetch_ohlcv(symbol, timeframe, since=since_timestamp)
    return df


# %% Basic price chart
def plot_price_chart(df: pd.DataFrame, symbol: str = 'BTC/USDT'):
    """Plot basic price chart with volume."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])
    
    # Price chart
    ax1.plot(df.index, df['close'], label='Close Price', linewidth=1.5)
    ax1.fill_between(df.index, df['low'], df['high'], alpha=0.3, label='High-Low Range')
    ax1.set_title(f'{symbol} Price Chart', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price (USDT)', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Volume chart
    ax2.bar(df.index, df['volume'], alpha=0.6, color='steelblue')
    ax2.set_title('Volume', fontsize=14)
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# %% Technical indicators chart
def plot_indicators(df: pd.DataFrame, symbol: str = 'BTC/USDT'):
    """Plot price with technical indicators."""
    df_with_indicators = add_indicators(df)
    
    fig, axes = plt.subplots(4, 1, figsize=(14, 14))
    
    # Price with moving averages and Bollinger Bands
    ax1 = axes[0]
    ax1.plot(df_with_indicators.index, df_with_indicators['close'], label='Close', linewidth=1.5)
    ax1.plot(df_with_indicators.index, df_with_indicators['sma_20'], label='SMA 20', alpha=0.7)
    ax1.plot(df_with_indicators.index, df_with_indicators['sma_50'], label='SMA 50', alpha=0.7)
    ax1.fill_between(df_with_indicators.index, df_with_indicators['bb_upper'], 
                     df_with_indicators['bb_lower'], alpha=0.2, label='Bollinger Bands')
    ax1.set_title(f'{symbol} Price with Indicators', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Price', fontsize=10)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # RSI
    ax2 = axes[1]
    ax2.plot(df_with_indicators.index, df_with_indicators['rsi'], label='RSI', color='purple')
    ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Overbought (70)')
    ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Oversold (30)')
    ax2.set_ylabel('RSI', fontsize=10)
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # MACD
    ax3 = axes[2]
    ax3.plot(df_with_indicators.index, df_with_indicators['macd'], label='MACD', color='blue')
    ax3.plot(df_with_indicators.index, df_with_indicators['macd_signal'], label='Signal', color='red')
    ax3.bar(df_with_indicators.index, df_with_indicators['macd_histogram'], 
            label='Histogram', alpha=0.3, color='gray')
    ax3.set_ylabel('MACD', fontsize=10)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Volume
    ax4 = axes[3]
    ax4.bar(df_with_indicators.index, df_with_indicators['volume'], alpha=0.6, color='steelblue')
    ax4.set_ylabel('Volume', fontsize=10)
    ax4.set_xlabel('Date', fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# %% Correlation analysis
def plot_correlation_matrix(df: pd.DataFrame):
    """Plot correlation matrix of price and volume."""
    correlation_df = df[['open', 'high', 'low', 'close', 'volume']].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_df, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Price and Volume Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return plt.gcf()


# %% Returns analysis
def plot_returns_analysis(df: pd.DataFrame):
    """Analyze and plot returns."""
    df = df.copy()
    df['returns'] = df['close'].pct_change()
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Returns distribution
    axes[0, 0].hist(df['returns'].dropna(), bins=50, alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('Returns Distribution', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Returns')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Cumulative returns
    axes[0, 1].plot(df.index, (1 + df['returns']).cumprod(), linewidth=1.5)
    axes[0, 1].set_title('Cumulative Returns', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Cumulative Returns')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Returns over time
    axes[1, 0].plot(df.index, df['returns'], alpha=0.6, linewidth=0.5)
    axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    axes[1, 0].set_title('Returns Over Time', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Returns')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Volatility (rolling std)
    df['volatility'] = df['returns'].rolling(window=30).std() * np.sqrt(365)  # Annualized
    axes[1, 1].plot(df.index, df['volatility'], linewidth=1.5, color='orange')
    axes[1, 1].set_title('30-Day Rolling Volatility (Annualized)', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Volatility')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# %% Example usage
if __name__ == "__main__":
    # Load data
    df = load_crypto_data('BTC/USDT', '1d', days=365)
    print(f"Loaded {len(df)} candles")
    print(df.head())
    
    # Plot price chart
    plot_price_chart(df, 'BTC/USDT')
    plt.show()
    
    # Plot indicators
    plot_indicators(df, 'BTC/USDT')
    plt.show()

    # Returns analysis
    plot_returns_analysis(df)
    plt.show()

