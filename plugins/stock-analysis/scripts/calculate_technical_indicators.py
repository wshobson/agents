#!/usr/bin/env python3
"""
Calculate Technical Indicators Script
Calculates technical indicators for stock analysis: RSI, MACD, Bollinger Bands, etc.

Usage:
    python calculate_technical_indicators.py AAPL --period 30 --indicators RSI,MACD,BB
    python calculate_technical_indicators.py NVDA --data data/NVDA_prices.csv --output indicators.json
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Check for required dependencies
try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Error: Required module not found: {e}", file=sys.stderr)
    print("Install with: pip install pandas numpy", file=sys.stderr)
    sys.exit(1)


class TechnicalIndicators:
    """Calculate technical indicators for stock price data."""
    
    @staticmethod
    def rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index (RSI)."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)."""
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band,
            'bandwidth': (upper_band - lower_band) / sma * 100
        }
    
    @staticmethod
    def moving_averages(prices: pd.Series, periods: List[int]) -> Dict[str, pd.Series]:
        """Calculate multiple moving averages."""
        ma_dict = {}
        for period in periods:
            ma_dict[f'SMA_{period}'] = prices.rolling(window=period).mean()
            ma_dict[f'EMA_{period}'] = prices.ewm(span=period, adjust=False).mean()
        return ma_dict
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range (ATR)."""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    @staticmethod
    def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                   k_period: int = 14, d_period: int = 3) -> Dict[str, pd.Series]:
        """Calculate Stochastic Oscillator."""
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return {
            'k': k_percent,
            'd': d_percent
        }
    
    @staticmethod
    def support_resistance(prices: pd.Series, window: int = 20) -> Dict[str, float]:
        """Identify support and resistance levels."""
        recent_prices = prices.tail(window)
        resistance = recent_prices.max()
        support = recent_prices.min()
        
        # Find pivot points
        highs = recent_prices[recent_prices == recent_prices.rolling(window=5, center=True).max()]
        lows = recent_prices[recent_prices == recent_prices.rolling(window=5, center=True).min()]
        
        return {
            'resistance': float(resistance),
            'support': float(support),
            'pivot_highs': highs.tolist()[-3:] if len(highs) > 0 else [],
            'pivot_lows': lows.tolist()[-3:] if len(lows) > 0 else []
        }


def calculate_indicators(data: pd.DataFrame, indicators: List[str], periods: Dict) -> Dict:
    """Calculate all requested indicators."""
    calc = TechnicalIndicators()
    results = {
        'timestamp': datetime.now().isoformat(),
        'indicators': {}
    }
    
    if 'close' not in data.columns:
        raise ValueError("Data must contain 'close' column")
    
    close = data['close']
    
    if 'RSI' in indicators:
        period = periods.get('rsi', 14)
        results['indicators']['RSI'] = {
            'values': calc.rsi(close, period).tail(30).to_dict(),
            'current': float(calc.rsi(close, period).iloc[-1]) if not calc.rsi(close, period).isna().iloc[-1] else None,
            'signal': 'overbought' if calc.rsi(close, period).iloc[-1] > 70 else 'oversold' if calc.rsi(close, period).iloc[-1] < 30 else 'neutral'
        }
    
    if 'MACD' in indicators:
        results['indicators']['MACD'] = {
            'macd': calc.macd(close)['macd'].tail(30).to_dict(),
            'signal': calc.macd(close)['signal'].tail(30).to_dict(),
            'histogram': calc.macd(close)['histogram'].tail(30).to_dict(),
            'current': {
                'macd': float(calc.macd(close)['macd'].iloc[-1]),
                'signal': float(calc.macd(close)['signal'].iloc[-1]),
                'histogram': float(calc.macd(close)['histogram'].iloc[-1])
            }
        }
    
    if 'BB' in indicators or 'Bollinger' in indicators:
        period = periods.get('bb', 20)
        bb = calc.bollinger_bands(close, period)
        results['indicators']['Bollinger_Bands'] = {
            'upper': bb['upper'].tail(30).to_dict(),
            'middle': bb['middle'].tail(30).to_dict(),
            'lower': bb['lower'].tail(30).to_dict(),
            'bandwidth': bb['bandwidth'].tail(30).to_dict(),
            'current': {
                'upper': float(bb['upper'].iloc[-1]),
                'middle': float(bb['middle'].iloc[-1]),
                'lower': float(bb['lower'].iloc[-1]),
                'price': float(close.iloc[-1]),
                'position': 'above_upper' if close.iloc[-1] > bb['upper'].iloc[-1] else 'below_lower' if close.iloc[-1] < bb['lower'].iloc[-1] else 'middle'
            }
        }
    
    if 'MA' in indicators or 'Moving_Average' in indicators:
        ma_periods = periods.get('ma', [20, 50, 200])
        ma = calc.moving_averages(close, ma_periods)
        results['indicators']['Moving_Averages'] = {
            k: v.tail(30).to_dict() for k, v in ma.items()
        }
    
    if 'ATR' in indicators:
        if 'high' in data.columns and 'low' in data.columns:
            atr = calc.atr(data['high'], data['low'], close, periods.get('atr', 14))
            results['indicators']['ATR'] = {
                'values': atr.tail(30).to_dict(),
                'current': float(atr.iloc[-1]) if not atr.isna().iloc[-1] else None
            }
    
    if 'Stochastic' in indicators:
        if 'high' in data.columns and 'low' in data.columns:
            stoch = calc.stochastic(data['high'], data['low'], close)
            results['indicators']['Stochastic'] = {
                'k': stoch['k'].tail(30).to_dict(),
                'd': stoch['d'].tail(30).to_dict(),
                'current': {
                    'k': float(stoch['k'].iloc[-1]),
                    'd': float(stoch['d'].iloc[-1])
                }
            }
    
    if 'Support_Resistance' in indicators:
        sr = calc.support_resistance(close, periods.get('sr_window', 20))
        results['indicators']['Support_Resistance'] = sr
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Calculate technical indicators for stock analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('ticker', nargs='?', help='Stock ticker symbol (optional if --data provided)')
    parser.add_argument(
        '--data',
        type=argparse.FileType('r'),
        help='CSV file with price data (columns: date, open, high, low, close, volume)'
    )
    parser.add_argument(
        '--indicators',
        default='RSI,MACD,BB,MA',
        help='Comma-separated list of indicators (RSI, MACD, BB, MA, ATR, Stochastic, Support_Resistance)'
    )
    parser.add_argument(
        '--period',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    parser.add_argument(
        '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output JSON file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Load data
    if args.data:
        data = pd.read_csv(args.data)
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            data.set_index('date', inplace=True)
    elif args.ticker:
        try:
            import yfinance as yf
        except ImportError:
            print("Error: yfinance not installed. Install with: pip install yfinance", file=sys.stderr)
            print("Alternatively, provide price data via --data CSV file", file=sys.stderr)
            sys.exit(1)
        
        try:
            stock = yf.Ticker(args.ticker)
            data = stock.history(period=f'{args.period}d')
            data.columns = [col.lower() for col in data.columns]
        except Exception as e:
            print(f"Error fetching data: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: Must provide either ticker or --data file", file=sys.stderr)
        sys.exit(1)
    
    # Calculate indicators
    indicators_list = [ind.strip() for ind in args.indicators.split(',')]
    periods = {
        'rsi': 14,
        'bb': 20,
        'ma': [20, 50, 200],
        'atr': 14,
        'sr_window': 20
    }
    
    try:
        results = calculate_indicators(data, indicators_list, periods)
        results['ticker'] = args.ticker or 'unknown'
        results['period'] = args.period
        
        json.dump(results, args.output, indent=2, default=str)
    except Exception as e:
        print(f"Error calculating indicators: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
