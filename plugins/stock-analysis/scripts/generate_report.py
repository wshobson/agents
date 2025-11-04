#!/usr/bin/env python3
"""
Generate Report Script
Generates markdown reports from analysis data using templates.

Usage:
    python generate_report.py --template technical --data indicators.json --output report.md
    python generate_report.py --template comprehensive --ticker AAPL --data-dir reports/
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Check for required dependencies
try:
    import jinja2
except ImportError:
    print("Error: 'jinja2' module not found. Install with: pip install jinja2", file=sys.stderr)
    sys.exit(1)


class ReportGenerator:
    """Generate markdown reports from analysis data."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent / 'templates'
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(exist_ok=True)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=False
        )
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default report templates if they don't exist."""
        templates = {
            'technical.md': """# Technical Analysis Report: {{ ticker }}

**Date**: {{ date }}
**Analysis Period**: {{ period }} days

## Executive Summary

{{ summary }}

## Technical Indicators

### RSI (Relative Strength Index)
- **Current**: {{ rsi.current }}
- **Signal**: {{ rsi.signal }}
- **Interpretation**: {{ rsi.interpretation }}

### MACD
- **MACD Line**: {{ macd.macd }}
- **Signal Line**: {{ macd.signal }}
- **Histogram**: {{ macd.histogram }}
- **Signal**: {{ macd.signal_type }}

### Bollinger Bands
- **Upper Band**: {{ bb.upper }}
- **Middle (SMA)**: {{ bb.middle }}
- **Lower Band**: {{ bb.lower }}
- **Current Price**: {{ bb.price }}
- **Position**: {{ bb.position }}

## Moving Averages

{% for period, value in ma.items() %}
- **{{ period }}**: {{ value }}
{% endfor %}

## Support and Resistance

- **Resistance**: {{ support_resistance.resistance }}
- **Support**: {{ support_resistance.support }}

## Trading Signals

### Entry Signals
{{ entry_signals }}

### Exit Signals
{{ exit_signals }}

## Risk Assessment

- **Stop Loss**: {{ stop_loss }}
- **Profit Target**: {{ profit_target }}
- **Risk-Reward Ratio**: {{ risk_reward }}

## Recommendation

**Rating**: {{ rating }}
**Time Horizon**: {{ time_horizon }}

{{ recommendation }}
""",
            
            'fundamental.md': """# Fundamental Analysis Report: {{ ticker }}

**Date**: {{ date }}

## Executive Summary

{{ summary }}

## Valuation Metrics

- **P/E Ratio**: {{ valuation.pe }}
- **PEG Ratio**: {{ valuation.peg }}
- **Price-to-Book**: {{ valuation.pb }}
- **EV/EBITDA**: {{ valuation.ev_ebitda }}
- **Intrinsic Value**: {{ valuation.intrinsic_value }}
- **Current Price**: {{ valuation.current_price }}
- **Margin of Safety**: {{ valuation.margin_of_safety }}

## Profitability

- **Gross Margin**: {{ profitability.gross_margin }}
- **Operating Margin**: {{ profitability.operating_margin }}
- **Net Margin**: {{ profitability.net_margin }}
- **ROE**: {{ profitability.roe }}
- **ROA**: {{ profitability.roa }}
- **ROIC**: {{ profitability.roic }}

## Growth Metrics

- **Revenue Growth**: {{ growth.revenue_growth }}
- **EPS Growth**: {{ growth.eps_growth }}
- **FCF Growth**: {{ growth.fcf_growth }}

## Financial Health

- **Debt-to-Equity**: {{ financial_health.debt_equity }}
- **Current Ratio**: {{ financial_health.current_ratio }}
- **Interest Coverage**: {{ financial_health.interest_coverage }}

## Recommendation

**Rating**: {{ rating }}
**Quality Score**: {{ quality_score }}/10

{{ recommendation }}
""",
            
            'comprehensive.md': """# Comprehensive Stock Analysis: {{ ticker }}

**Date**: {{ date }}
**Company**: {{ company_name }}

## Executive Summary

{{ executive_summary }}

## Technical Analysis

{{ technical_analysis }}

## Fundamental Analysis

{{ fundamental_analysis }}

## News & Catalysts

{{ news_analysis }}

## Risk Assessment

{{ risk_analysis }}

## Investment Recommendation

**Rating**: {{ rating }}
**Conviction**: {{ conviction }}
**Time Horizon**: {{ time_horizon }}

{{ recommendation }}

## Action Items

{{ action_items }}
"""
        }
        
        for name, content in templates.items():
            template_path = self.templates_dir / name
            if not template_path.exists():
                template_path.write_text(content)
    
    def generate_technical_report(self, data: Dict, ticker: str) -> str:
        """Generate technical analysis report."""
        template = self.env.get_template('technical.md')
        return template.render(
            ticker=ticker,
            date=datetime.now().strftime('%Y-%m-%d'),
            **data
        )
    
    def generate_fundamental_report(self, data: Dict, ticker: str) -> str:
        """Generate fundamental analysis report."""
        template = self.env.get_template('fundamental.md')
        return template.render(
            ticker=ticker,
            date=datetime.now().strftime('%Y-%m-%d'),
            **data
        )
    
    def generate_comprehensive_report(self, data: Dict, ticker: str) -> str:
        """Generate comprehensive analysis report."""
        template = self.env.get_env().get_template('comprehensive.md')
        return template.render(
            ticker=ticker,
            date=datetime.now().strftime('%Y-%m-%d'),
            **data
        )


def main():
    parser = argparse.ArgumentParser(
        description='Generate markdown reports from analysis data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--template',
        choices=['technical', 'fundamental', 'comprehensive'],
        required=True,
        help='Report template type'
    )
    parser.add_argument(
        '--ticker',
        help='Stock ticker symbol'
    )
    parser.add_argument(
        '--data',
        type=argparse.FileType('r'),
        help='JSON file with analysis data'
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        help='Directory with multiple analysis JSON files'
    )
    parser.add_argument(
        '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output markdown file (default: stdout)'
    )
    parser.add_argument(
        '--templates-dir',
        type=Path,
        help='Directory with custom templates (default: scripts/templates/)'
    )
    
    args = parser.parse_args()
    
    generator = ReportGenerator(templates_dir=args.templates_dir)
    
    # Load data
    if args.data:
        data = json.load(args.data)
    elif args.data_dir:
        # Load all JSON files from directory
        data = {}
        for json_file in args.data_dir.glob('*.json'):
            with open(json_file) as f:
                file_data = json.load(f)
                data[json_file.stem] = file_data
    else:
        print("Error: Must provide either --data or --data-dir", file=sys.stderr)
        sys.exit(1)
    
    ticker = args.ticker or data.get('ticker', 'UNKNOWN')
    
    # Generate report
    if args.template == 'technical':
        report = generator.generate_technical_report(data, ticker)
    elif args.template == 'fundamental':
        report = generator.generate_fundamental_report(data, ticker)
    else:
        report = generator.generate_comprehensive_report(data, ticker)
    
    args.output.write(report)


if __name__ == '__main__':
    main()
