"""Basic backtesting framework for trading strategies."""

import pandas as pd
import numpy as np
from typing import Callable
from dataclasses import dataclass


@dataclass
class BacktestResult:
    """Results from a backtest."""
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    final_balance: float
    equity_curve: pd.Series
    trades: pd.DataFrame


class SimpleBacktester:
    """Simple backtesting engine."""
    
    def __init__(self, initial_balance: float = 10000.0, commission: float = 0.001):
        """
        Initialize backtester.
        
        Args:
            initial_balance: Starting capital
            commission: Commission rate (e.g., 0.001 = 0.1%)
        """
        self.initial_balance = initial_balance
        self.commission = commission
    
    def run_backtest(
        self,
        data: pd.DataFrame,
        signal_func: Callable[[pd.DataFrame], pd.Series],
        position_size: float = 1.0
    ) -> BacktestResult:
        """
        Run a backtest on historical data.
        
        Args:
            data: DataFrame with OHLCV data
            signal_func: Function that takes DataFrame and returns Series of signals
                         (1 = buy, -1 = sell, 0 = hold)
            position_size: Fraction of capital to use per trade (0.0 to 1.0)
        
        Returns:
            BacktestResult object
        """
        df = data.copy()
        
        # Generate signals
        signals = signal_func(df)
        df['signal'] = signals
        
        # Initialize tracking variables
        balance = self.initial_balance
        position = 0  # Number of coins held
        trades = []
        equity_curve = [balance]
        
        for i in range(1, len(df)):
            current_price = df.iloc[i]['close']
            prev_signal = df.iloc[i-1]['signal']
            
            # Execute trades
            if prev_signal == 1 and position == 0:  # Buy signal
                trade_amount = balance * position_size
                position = trade_amount / current_price
                commission_cost = trade_amount * self.commission
                balance -= (trade_amount + commission_cost)
                
                trades.append({
                    'timestamp': df.index[i],
                    'type': 'BUY',
                    'price': current_price,
                    'quantity': position,
                    'balance': balance
                })
            
            elif prev_signal == -1 and position > 0:  # Sell signal
                trade_value = position * current_price
                commission_cost = trade_value * self.commission
                balance += (trade_value - commission_cost)
                
                trades.append({
                    'timestamp': df.index[i],
                    'type': 'SELL',
                    'price': current_price,
                    'quantity': position,
                    'balance': balance
                })
                
                position = 0
            
            # Calculate current equity
            current_equity = balance + (position * current_price if position > 0 else 0)
            equity_curve.append(current_equity)
        
        # Close any open position at the end
        if position > 0:
            final_price = df.iloc[-1]['close']
            trade_value = position * final_price
            commission_cost = trade_value * self.commission
            balance += (trade_value - commission_cost)
            equity_curve[-1] = balance
        
        # Calculate metrics
        equity_series = pd.Series(equity_curve, index=df.index)
        returns = equity_series.pct_change().dropna()
        
        total_return = (balance / self.initial_balance - 1) * 100
        
        # Sharpe ratio (annualized)
        if len(returns) > 0 and returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # Assuming daily data
        else:
            sharpe_ratio = 0.0
        
        # Max drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = abs(drawdown.min()) * 100
        
        # Win rate
        trades_df = pd.DataFrame(trades)
        if len(trades_df) > 0:
            # Pair buy and sell trades
            buy_trades = trades_df[trades_df['type'] == 'BUY']
            sell_trades = trades_df[trades_df['type'] == 'SELL']
            
            if len(buy_trades) > 0 and len(sell_trades) > 0:
                # Calculate P&L for completed trades
                profits = []
                for _, buy in buy_trades.iterrows():
                    matching_sells = sell_trades[sell_trades['timestamp'] > buy['timestamp']]
                    if len(matching_sells) > 0:
                        sell = matching_sells.iloc[0]
                        profit = (sell['price'] - buy['price']) / buy['price']
                        profits.append(profit)
                
                if profits:
                    win_rate = len([p for p in profits if p > 0]) / len(profits) * 100
                else:
                    win_rate = 0.0
            else:
                win_rate = 0.0
        else:
            win_rate = 0.0
        
        return BacktestResult(
            total_return=total_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=len(trades),
            final_balance=balance,
            equity_curve=equity_series,
            trades=pd.DataFrame(trades) if trades else pd.DataFrame()
        )
    
    def print_results(self, result: BacktestResult):
        """Print backtest results in a readable format."""
        print("=" * 50)
        print("BACKTEST RESULTS")
        print("=" * 50)
        print(f"Initial Balance: ${self.initial_balance:,.2f}")
        print(f"Final Balance: ${result.final_balance:,.2f}")
        print(f"Total Return: {result.total_return:.2f}%")
        print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
        print(f"Max Drawdown: {result.max_drawdown:.2f}%")
        print(f"Win Rate: {result.win_rate:.2f}%")
        print(f"Total Trades: {result.total_trades}")
        print("=" * 50)


def plot_backtest_results(data: pd.DataFrame, result: BacktestResult):
    """Plot backtest results."""
    import matplotlib.pyplot as plt
    
    # Ensure inline plotting for notebooks
    try:
        get_ipython().run_line_magic('matplotlib', 'inline')  # type: ignore
    except NameError:
        pass
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])
    
    # Price and equity curve
    ax1 = axes[0]
    ax1_twin = ax1.twinx()
    
    ax1.plot(data.index, data['close'], label='Price', color='blue', alpha=0.5)
    ax1_twin.plot(result.equity_curve.index, result.equity_curve, 
                  label='Equity Curve', color='green', linewidth=2)
    
    # Mark trades
    if len(result.trades) > 0:
        buy_trades = result.trades[result.trades['type'] == 'BUY']
        sell_trades = result.trades[result.trades['type'] == 'SELL']
        
        for _, trade in buy_trades.iterrows():
            if trade['timestamp'] in data.index:
                ax1.scatter(trade['timestamp'], trade['price'], 
                           color='green', marker='^', s=100, zorder=5, label='Buy' if trade.name == buy_trades.index[0] else '')
        
        for _, trade in sell_trades.iterrows():
            if trade['timestamp'] in data.index:
                ax1.scatter(trade['timestamp'], trade['price'], 
                           color='red', marker='v', s=100, zorder=5, label='Sell' if trade.name == sell_trades.index[0] else '')
    
    ax1.set_title('Backtest Results', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price', fontsize=12, color='blue')
    ax1_twin.set_ylabel('Equity', fontsize=12, color='green')
    ax1.legend(loc='upper left')
    ax1_twin.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Drawdown
    ax2 = axes[1]
    returns = result.equity_curve.pct_change().dropna()
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    
    ax2.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
    ax2.plot(drawdown.index, drawdown, color='red', linewidth=1)
    ax2.set_title('Drawdown', fontsize=14)
    ax2.set_ylabel('Drawdown (%)', fontsize=10)
    ax2.set_xlabel('Date', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

