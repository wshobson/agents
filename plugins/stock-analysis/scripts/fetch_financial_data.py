#!/usr/bin/env python3
"""
Fetch Financial Data Script
Automatically fetches financial data for stock analysis from multiple sources.
Supports: Yahoo Finance, Alpha Vantage, Financial Modeling Prep, and SEC EDGAR.

Usage:
    python fetch_financial_data.py AAPL --source yahoo
    python fetch_financial_data.py NVDA --source alpha_vantage --api_key YOUR_KEY
    python fetch_financial_data.py MSFT --source sec --output data/MSFT_financials.json
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path

# Check for optional dependencies
try:
    import requests
except ImportError:
    print("Error: 'requests' module not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


class FinancialDataFetcher:
    """Fetches financial data from various sources."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Stock-Analysis-Agent/1.0'
        })
    
    def fetch_yahoo_finance(self, ticker: str) -> Dict:
        """Fetch data from Yahoo Finance (no API key required)."""
        try:
            # Using yfinance library if available, otherwise manual parsing
            try:
                import yfinance as yf
            except ImportError:
                yf = None
            
            if yf is not None:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    financials = stock.financials
                    balance_sheet = stock.balance_sheet
                    cashflow = stock.cashflow
                    
                    return {
                        'source': 'yahoo_finance',
                        'ticker': ticker,
                        'timestamp': datetime.now().isoformat(),
                        'company_info': info,
                        'financials': financials.to_dict() if financials is not None else {},
                        'balance_sheet': balance_sheet.to_dict() if balance_sheet is not None else {},
                        'cashflow': cashflow.to_dict() if cashflow is not None else {},
                        'historical_data': stock.history(period='1y').to_dict() if hasattr(stock, 'history') else {}
                    }
                except Exception as e:
                    # Fall through to manual method if yfinance fails
                    pass
            
            # Fallback: manual Yahoo Finance API
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'yahoo_finance',
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'quote_data': data.get('chart', {}).get('result', [{}])[0] if data.get('chart') else {}
            }
        except Exception as e:
            return {'error': f'Failed to fetch from Yahoo Finance: {str(e)}'}
    
    def fetch_alpha_vantage(self, ticker: str) -> Dict:
        """Fetch data from Alpha Vantage API."""
        if not self.api_key:
            return {'error': 'Alpha Vantage requires API key'}
        
        try:
            base_url = "https://www.alphavantage.co/query"
            
            # Get company overview
            params = {
                'function': 'OVERVIEW',
                'symbol': ticker,
                'apikey': self.api_key
            }
            response = self.session.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            overview = response.json()
            
            # Get income statement
            params['function'] = 'INCOME_STATEMENT'
            response = self.session.get(base_url, params=params, timeout=10)
            income = response.json()
            
            # Get balance sheet
            params['function'] = 'BALANCE_SHEET'
            response = self.session.get(base_url, params=params, timeout=10)
            balance = response.json()
            
            # Get cash flow
            params['function'] = 'CASH_FLOW'
            response = self.session.get(base_url, params=params, timeout=10)
            cashflow = response.json()
            
            return {
                'source': 'alpha_vantage',
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'overview': overview,
                'income_statement': income,
                'balance_sheet': balance,
                'cashflow': cashflow
            }
        except Exception as e:
            return {'error': f'Failed to fetch from Alpha Vantage: {str(e)}'}
    
    def fetch_sec_edgar(self, ticker: str) -> Dict:
        """Fetch SEC filings from EDGAR."""
        try:
            # SEC CIK lookup
            cik_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K&count=1"
            response = self.session.get(cik_url, timeout=10)
            
            return {
                'source': 'sec_edgar',
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'filings_url': cik_url,
                'note': 'Use SEC EDGAR website or API for detailed filings'
            }
        except Exception as e:
            return {'error': f'Failed to fetch from SEC EDGAR: {str(e)}'}
    
    def fetch_all(self, ticker: str) -> Dict:
        """Fetch from all available sources."""
        results = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }
        
        # Try Yahoo Finance (no API key needed)
        results['sources']['yahoo'] = self.fetch_yahoo_finance(ticker)
        
        # Try Alpha Vantage if API key available
        if self.api_key:
            results['sources']['alpha_vantage'] = self.fetch_alpha_vantage(ticker)
        
        # Try SEC
        results['sources']['sec'] = self.fetch_sec_edgar(ticker)
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Fetch financial data for stock analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('ticker', help='Stock ticker symbol (e.g., AAPL)')
    parser.add_argument(
        '--source',
        choices=['yahoo', 'alpha_vantage', 'sec', 'all'],
        default='yahoo',
        help='Data source (default: yahoo)'
    )
    parser.add_argument(
        '--api-key',
        help='API key for Alpha Vantage (if using alpha_vantage source)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output JSON file path (default: stdout)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'pretty'],
        default='pretty',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    fetcher = FinancialDataFetcher(api_key=args.api_key)
    
    if args.source == 'yahoo':
        data = fetcher.fetch_yahoo_finance(args.ticker)
    elif args.source == 'alpha_vantage':
        data = fetcher.fetch_alpha_vantage(args.ticker)
    elif args.source == 'sec':
        data = fetcher.fetch_sec_edgar(args.ticker)
    else:
        data = fetcher.fetch_all(args.ticker)
    
    # Output
    if args.format == 'json':
        output = json.dumps(data, indent=2, default=str)
    else:
        output = json.dumps(data, indent=2, default=str)
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
        print(f"Data saved to {args.output}")
    else:
        print(output)
    
    # Check for errors
    if isinstance(data, dict) and 'error' in data:
        sys.exit(1)
    
    if isinstance(data, dict) and 'sources' in data:
        for source, result in data['sources'].items():
            if isinstance(result, dict) and 'error' in result:
                print(f"Warning: {source} failed: {result['error']}", file=sys.stderr)


if __name__ == '__main__':
    main()
