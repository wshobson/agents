#!/usr/bin/env python3
"""
Calculate Portfolio Risk Metrics Script
Calculates risk metrics for portfolios: VaR, Sharpe ratio, correlation, beta, etc.

Usage:
    python calculate_portfolio_risk.py --holdings AAPL:100,MSFT:50 --prices data/prices.json
    python calculate_portfolio_risk.py --portfolio-file portfolio.json --output risk_report.json
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


class PortfolioRiskCalculator:
    """Calculate portfolio risk metrics."""
    
    @staticmethod
    def calculate_returns(prices: pd.Series) -> pd.Series:
        """Calculate daily returns."""
        return prices.pct_change().dropna()
    
    @staticmethod
    def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
        """Calculate Value at Risk (VaR)."""
        return float(np.percentile(returns, (1 - confidence) * 100))
    
    @staticmethod
    def calculate_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
        """Calculate Conditional Value at Risk (CVaR)."""
        var = PortfolioRiskCalculator.calculate_var(returns, confidence)
        return float(returns[returns <= var].mean())
    
    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        excess_returns = returns.mean() * 252 - risk_free_rate  # Annualized
        volatility = returns.std() * np.sqrt(252)  # Annualized
        if volatility == 0:
            return 0.0
        return float(excess_returns / volatility)
    
    @staticmethod
    def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio (uses downside deviation)."""
        excess_returns = returns.mean() * 252 - risk_free_rate
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        if downside_std == 0:
            return 0.0
        return float(excess_returns / downside_std)
    
    @staticmethod
    def calculate_max_drawdown(returns: pd.Series) -> Dict[str, float]:
        """Calculate maximum drawdown."""
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_dd = drawdown.min()
        max_dd_idx = drawdown.idxmin()
        
        return {
            'max_drawdown': float(max_dd),
            'max_drawdown_date': str(max_dd_idx),
            'recovery_days': None  # Could calculate if needed
        }
    
    @staticmethod
    def calculate_beta(portfolio_returns: pd.Series, market_returns: pd.Series) -> float:
        """Calculate portfolio beta vs market."""
        covariance = np.cov(portfolio_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        if market_variance == 0:
            return 0.0
        return float(covariance / market_variance)
    
    @staticmethod
    def calculate_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix between holdings."""
        return returns_df.corr()
    
    @staticmethod
    def calculate_concentration_risk(weights: Dict[str, float]) -> Dict[str, float]:
        """Calculate concentration risk metrics."""
        weight_values = list(weights.values())
        
        # Herfindahl-Hirschman Index (HHI)
        hhi = sum(w ** 2 for w in weight_values)
        
        # Largest position
        max_weight = max(weight_values) if weight_values else 0
        
        # Top 5 concentration
        sorted_weights = sorted(weight_values, reverse=True)
        top5_concentration = sum(sorted_weights[:5])
        
        return {
            'hhi': float(hhi),
            'hhi_normalized': float(hhi * 10000),  # Scale to 0-10000
            'max_position_weight': float(max_weight),
            'top5_concentration': float(top5_concentration),
            'concentration_risk': 'high' if hhi > 0.25 else 'medium' if hhi > 0.15 else 'low'
        }
    
    def calculate_portfolio_risk(self, holdings: Dict[str, Dict], 
                               market_returns: Optional[pd.Series] = None) -> Dict:
        """Calculate comprehensive portfolio risk metrics."""
        # Prepare data
        tickers = list(holdings.keys())
        weights = {ticker: holdings[ticker].get('weight', 0) for ticker in tickers}
        
        # Calculate individual stock returns
        returns_dict = {}
        for ticker, data in holdings.items():
            if 'prices' in data:
                prices = pd.Series(data['prices'])
                returns = self.calculate_returns(prices)
                returns_dict[ticker] = returns
        
        if not returns_dict:
            return {'error': 'No price data provided'}
        
        returns_df = pd.DataFrame(returns_dict)
        
        # Portfolio returns (weighted average)
        portfolio_returns = pd.Series(0.0, index=returns_df.index)
        for ticker, weight in weights.items():
            if ticker in returns_df.columns:
                portfolio_returns += returns_df[ticker] * weight
        
        # Calculate metrics
        results = {
            'timestamp': datetime.now().isoformat(),
            'portfolio_composition': {
                'tickers': tickers,
                'weights': weights,
                'total_positions': len(tickers)
            },
            'risk_metrics': {
                'volatility_annualized': float(portfolio_returns.std() * np.sqrt(252)),
                'var_95': self.calculate_var(portfolio_returns, 0.95),
                'var_99': self.calculate_var(portfolio_returns, 0.99),
                'cvar_95': self.calculate_cvar(portfolio_returns, 0.95),
                'sharpe_ratio': self.calculate_sharpe_ratio(portfolio_returns),
                'sortino_ratio': self.calculate_sortino_ratio(portfolio_returns),
                'max_drawdown': self.calculate_max_drawdown(portfolio_returns)
            },
            'concentration_risk': self.calculate_concentration_risk(weights),
            'correlation_matrix': self.calculate_correlation_matrix(returns_df).to_dict()
        }
        
        # Beta if market returns provided
        if market_returns is not None:
            # Align dates
            aligned_returns = portfolio_returns.align(market_returns, join='inner')[0]
            aligned_market = portfolio_returns.align(market_returns, join='inner')[1]
            if len(aligned_returns) > 0:
                results['risk_metrics']['beta'] = self.calculate_beta(aligned_returns, aligned_market)
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Calculate portfolio risk metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--holdings',
        help='Comma-separated holdings: TICKER:WEIGHT (e.g., AAPL:0.4,MSFT:0.6)'
    )
    parser.add_argument(
        '--portfolio-file',
        type=argparse.FileType('r'),
        help='JSON file with portfolio data'
    )
    parser.add_argument(
        '--prices-file',
        type=argparse.FileType('r'),
        help='JSON file with price data for holdings'
    )
    parser.add_argument(
        '--market-returns-file',
        type=argparse.FileType('r'),
        help='JSON file with market returns (e.g., S&P 500) for beta calculation'
    )
    parser.add_argument(
        '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output JSON file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Load portfolio data
    if args.portfolio_file:
        portfolio_data = json.load(args.portfolio_file)
        holdings = portfolio_data.get('holdings', {})
    elif args.holdings:
        holdings_dict = {}
        for item in args.holdings.split(','):
            ticker, weight = item.split(':')
            holdings_dict[ticker.strip()] = {'weight': float(weight.strip())}
        holdings = holdings_dict
    else:
        print("Error: Must provide either --holdings or --portfolio-file", file=sys.stderr)
        sys.exit(1)
    
    # Load price data
    if args.prices_file:
        prices_data = json.load(args.prices_file)
        for ticker in holdings:
            if ticker in prices_data:
                holdings[ticker]['prices'] = prices_data[ticker]
    
    # Load market returns
    market_returns = None
    if args.market_returns_file:
        market_data = json.load(args.market_returns_file)
        if 'returns' in market_data:
            market_returns = pd.Series(market_data['returns'])
        elif 'prices' in market_data:
            prices = pd.Series(market_data['prices'])
            market_returns = PortfolioRiskCalculator.calculate_returns(prices)
    
    # Calculate risk
    calculator = PortfolioRiskCalculator()
    results = calculator.calculate_portfolio_risk(holdings, market_returns)
    
    # Output
    json.dump(results, args.output, indent=2, default=str)
    
    if 'error' in results:
        sys.exit(1)


if __name__ == '__main__':
    main()
