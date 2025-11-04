#!/usr/bin/env python3
"""
Compare Companies Script
Compares multiple companies across valuation, growth, quality, and risk metrics.

Usage:
    python compare_companies.py AAPL MSFT GOOGL --metrics valuation,growth,quality
    python compare_companies.py --tickers AAPL,MSFT,GOOGL --output comparison.json
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Check for required dependencies
try:
    import pandas as pd
except ImportError:
    print("Error: 'pandas' module not found. Install with: pip install pandas", file=sys.stderr)
    sys.exit(1)


class CompanyComparator:
    """Compare multiple companies across various metrics."""
    
    def __init__(self):
        self.metrics = {
            'valuation': ['pe_ratio', 'peg_ratio', 'pb_ratio', 'ev_ebitda', 'price_to_sales'],
            'growth': ['revenue_growth', 'eps_growth', 'fcf_growth', 'book_value_growth'],
            'profitability': ['gross_margin', 'operating_margin', 'net_margin', 'roe', 'roa', 'roic'],
            'financial_health': ['debt_to_equity', 'current_ratio', 'quick_ratio', 'interest_coverage'],
            'quality': ['quality_score', 'earnings_quality', 'cash_flow_quality'],
            'risk': ['beta', 'volatility', 'max_drawdown', 'var_95']
        }
    
    def compare_valuation(self, companies_data: Dict[str, Dict]) -> Dict:
        """Compare valuation metrics."""
        comparison = {
            'metric': 'Valuation',
            'companies': {}
        }
        
        for ticker, data in companies_data.items():
            valuation = data.get('valuation', {})
            comparison['companies'][ticker] = {
                'pe_ratio': valuation.get('pe_ratio'),
                'peg_ratio': valuation.get('peg_ratio'),
                'pb_ratio': valuation.get('pb_ratio'),
                'ev_ebitda': valuation.get('ev_ebitda'),
                'price_to_sales': valuation.get('price_to_sales'),
                'intrinsic_value': valuation.get('intrinsic_value'),
                'current_price': valuation.get('current_price'),
                'margin_of_safety': valuation.get('margin_of_safety')
            }
        
        # Find best/worst
        if all('pe_ratio' in comp and comp['pe_ratio'] for comp in comparison['companies'].values()):
            best_pe = min(
                (ticker, comp['pe_ratio']) 
                for ticker, comp in comparison['companies'].items() 
                if comp['pe_ratio']
            )
            comparison['best_value'] = best_pe[0]
        
        return comparison
    
    def compare_growth(self, companies_data: Dict[str, Dict]) -> Dict:
        """Compare growth metrics."""
        comparison = {
            'metric': 'Growth',
            'companies': {}
        }
        
        for ticker, data in companies_data.items():
            growth = data.get('growth', {})
            comparison['companies'][ticker] = {
                'revenue_growth': growth.get('revenue_growth'),
                'eps_growth': growth.get('eps_growth'),
                'fcf_growth': growth.get('fcf_growth'),
                'book_value_growth': growth.get('book_value_growth')
            }
        
        # Find fastest growing
        if all('revenue_growth' in comp and comp['revenue_growth'] for comp in comparison['companies'].values()):
            best_growth = max(
                (ticker, comp['revenue_growth']) 
                for ticker, comp in comparison['companies'].items() 
                if comp['revenue_growth']
            )
            comparison['fastest_growth'] = best_growth[0]
        
        return comparison
    
    def compare_profitability(self, companies_data: Dict[str, Dict]) -> Dict:
        """Compare profitability metrics."""
        comparison = {
            'metric': 'Profitability',
            'companies': {}
        }
        
        for ticker, data in companies_data.items():
            profitability = data.get('profitability', {})
            comparison['companies'][ticker] = {
                'gross_margin': profitability.get('gross_margin'),
                'operating_margin': profitability.get('operating_margin'),
                'net_margin': profitability.get('net_margin'),
                'roe': profitability.get('roe'),
                'roa': profitability.get('roa'),
                'roic': profitability.get('roic')
            }
        
        # Find most profitable
        if all('roe' in comp and comp['roe'] for comp in comparison['companies'].values()):
            best_roe = max(
                (ticker, comp['roe']) 
                for ticker, comp in comparison['companies'].items() 
                if comp['roe']
            )
            comparison['best_profitability'] = best_roe[0]
        
        return comparison
    
    def compare_quality(self, companies_data: Dict[str, Dict]) -> Dict:
        """Compare quality scores."""
        comparison = {
            'metric': 'Quality',
            'companies': {}
        }
        
        for ticker, data in companies_data.items():
            quality = data.get('quality', {})
            comparison['companies'][ticker] = {
                'quality_score': quality.get('quality_score'),
                'earnings_quality': quality.get('earnings_quality'),
                'cash_flow_quality': quality.get('cash_flow_quality'),
                'competitive_position': quality.get('competitive_position')
            }
        
        # Find highest quality
        if all('quality_score' in comp and comp['quality_score'] for comp in comparison['companies'].values()):
            best_quality = max(
                (ticker, comp['quality_score']) 
                for ticker, comp in comparison['companies'].items() 
                if comp['quality_score']
            )
            comparison['highest_quality'] = best_quality[0]
        
        return comparison
    
    def compare_risk(self, companies_data: Dict[str, Dict]) -> Dict:
        """Compare risk metrics."""
        comparison = {
            'metric': 'Risk',
            'companies': {}
        }
        
        for ticker, data in companies_data.items():
            risk = data.get('risk', {})
            comparison['companies'][ticker] = {
                'beta': risk.get('beta'),
                'volatility': risk.get('volatility'),
                'max_drawdown': risk.get('max_drawdown'),
                'var_95': risk.get('var_95')
            }
        
        # Find lowest risk
        if all('beta' in comp and comp['beta'] for comp in comparison['companies'].values()):
            lowest_beta = min(
                (ticker, comp['beta']) 
                for ticker, comp in comparison['companies'].items() 
                if comp['beta']
            )
            comparison['lowest_risk'] = lowest_beta[0]
        
        return comparison
    
    def create_comparison_table(self, companies_data: Dict[str, Dict], 
                               metrics: List[str]) -> pd.DataFrame:
        """Create comparison table DataFrame."""
        rows = []
        for ticker, data in companies_data.items():
            row = {'Ticker': ticker}
            
            for metric_group in metrics:
                if metric_group in self.metrics:
                    for metric_name in self.metrics[metric_group]:
                        if metric_group in data:
                            row[metric_name] = data[metric_group].get(metric_name)
                        elif metric_name in data:
                            row[metric_name] = data[metric_name]
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def compare_all(self, companies_data: Dict[str, Dict], 
                   metrics: List[str] = None) -> Dict:
        """Compare all companies across specified metrics."""
        if metrics is None:
            metrics = list(self.metrics.keys())
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tickers': list(companies_data.keys()),
            'comparisons': {}
        }
        
        for metric_group in metrics:
            if metric_group == 'valuation':
                results['comparisons']['valuation'] = self.compare_valuation(companies_data)
            elif metric_group == 'growth':
                results['comparisons']['growth'] = self.compare_growth(companies_data)
            elif metric_group == 'profitability':
                results['comparisons']['profitability'] = self.compare_profitability(companies_data)
            elif metric_group == 'quality':
                results['comparisons']['quality'] = self.compare_quality(companies_data)
            elif metric_group == 'risk':
                results['comparisons']['risk'] = self.compare_risk(companies_data)
        
        # Create summary
        results['summary'] = {
            'total_companies': len(companies_data),
            'metrics_compared': metrics
        }
        
        # Create comparison table
        df = self.create_comparison_table(companies_data, metrics)
        results['comparison_table'] = df.to_dict('records')
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Compare multiple companies across various metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'tickers',
        nargs='*',
        help='Stock ticker symbols to compare'
    )
    parser.add_argument(
        '--tickers',
        help='Comma-separated list of tickers (alternative to positional args)'
    )
    parser.add_argument(
        '--data-files',
        nargs='+',
        type=argparse.FileType('r'),
        help='JSON files with company analysis data (one per company)'
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        help='Directory containing JSON files with company data'
    )
    parser.add_argument(
        '--metrics',
        default='valuation,growth,profitability,quality,risk',
        help='Comma-separated list of metric groups to compare'
    )
    parser.add_argument(
        '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output JSON file (default: stdout)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'table'],
        default='json',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    # Get ticker list
    if args.tickers:
        ticker_list = [t.strip() for t in args.tickers.split(',')]
    elif args.tickers is None and args.tickers:
        ticker_list = list(args.tickers)
    else:
        ticker_list = []
    
    # Load company data
    companies_data = {}
    
    if args.data_files:
        for data_file in args.data_files:
            data = json.load(data_file)
            ticker = data.get('ticker', data_file.name.split('.')[0])
            companies_data[ticker] = data
    elif args.data_dir:
        for json_file in args.data_dir.glob('*.json'):
            with open(json_file) as f:
                data = json.load(f)
                ticker = data.get('ticker', json_file.stem)
                companies_data[ticker] = data
    else:
        # If no data provided, create placeholder data structure
        for ticker in ticker_list:
            companies_data[ticker] = {'ticker': ticker}
    
    if not companies_data:
        print("Error: No company data provided", file=sys.stderr)
        sys.exit(1)
    
    # Compare
    comparator = CompanyComparator()
    metrics_list = [m.strip() for m in args.metrics.split(',')]
    results = comparator.compare_all(companies_data, metrics_list)
    
    # Output
    if args.format == 'table':
        df = pd.DataFrame(results['comparison_table'])
        print(df.to_string(index=False))
    else:
        json.dump(results, args.output, indent=2, default=str)


if __name__ == '__main__':
    main()
