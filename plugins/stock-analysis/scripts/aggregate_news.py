#!/usr/bin/env python3
"""
Aggregate News Script
Aggregates and analyzes news from multiple sources using Tavily API and other sources.

Usage:
    python aggregate_news.py AAPL --days 30 --output news_AAPL.json
    python aggregate_news.py NVDA --tavily-api-key YOUR_KEY --sources tavily,google
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# Check for required dependencies
try:
    import requests
except ImportError:
    print("Error: 'requests' module not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


class NewsAggregator:
    """Aggregates news from multiple sources."""
    
    def __init__(self, tavily_api_key: Optional[str] = None):
        self.tavily_api_key = tavily_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Stock-Analysis-Agent/1.0'
        })
    
    def search_tavily(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search news using Tavily API."""
        if not self.tavily_api_key:
            return []
        
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "advanced",
                "include_answer": False,
                "include_images": False,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": ["bloomberg.com", "reuters.com", "wsj.com", "ft.com", 
                                   "cnbc.com", "marketwatch.com", "seekingalpha.com",
                                   "sec.gov", "yahoo.com"]
            }
            
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'published_date': item.get('published_date'),
                    'source': item.get('url', '').split('/')[2] if item.get('url') else '',
                    'relevance_score': item.get('score', 0)
                })
            
            return results
        except Exception as e:
            print(f"Tavily search error: {e}", file=sys.stderr)
            return []
    
    def search_google_news(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Google News (web scraping fallback)."""
        try:
            # Using Google News RSS feed
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse RSS (simplified - would need proper RSS parser)
            # This is a placeholder - actual implementation would parse RSS XML
            return []
        except Exception as e:
            print(f"Google News search error: {e}", file=sys.stderr)
            return []
    
    def categorize_news(self, news_items: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize news by type."""
        categories = {
            'earnings': [],
            'merger_acquisition': [],
            'product_launch': [],
            'regulatory': [],
            'management': [],
            'market_event': [],
            'other': []
        }
        
        keywords = {
            'earnings': ['earnings', 'quarterly', 'revenue', 'eps', 'guidance', 'beat', 'miss'],
            'merger_acquisition': ['merger', 'acquisition', 'm&a', 'buyout', 'deal', 'takeover'],
            'product_launch': ['launch', 'product', 'announcement', 'release', 'unveil'],
            'regulatory': ['fda', 'sec', 'approval', 'regulation', 'compliance', 'investigation'],
            'management': ['ceo', 'cfo', 'executive', 'resign', 'appoint', 'leadership'],
            'market_event': ['dividend', 'split', 'buyback', 'offering', 'ipo', 'spinoff']
        }
        
        for item in news_items:
            title_lower = item.get('title', '').lower()
            content_lower = item.get('content', '').lower()
            text = title_lower + ' ' + content_lower
            
            categorized = False
            for category, category_keywords in keywords.items():
                if any(keyword in text for keyword in category_keywords):
                    categories[category].append(item)
                    categorized = True
                    break
            
            if not categorized:
                categories['other'].append(item)
        
        return categories
    
    def analyze_sentiment(self, news_items: List[Dict]) -> Dict[str, int]:
        """Simple sentiment analysis based on keywords."""
        positive_keywords = ['beat', 'gain', 'rise', 'growth', 'profit', 'success', 'win', 'upgrade']
        negative_keywords = ['miss', 'fall', 'decline', 'loss', 'fail', 'downgrade', 'warning', 'cut']
        
        sentiment = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for item in news_items:
            text = (item.get('title', '') + ' ' + item.get('content', '')).lower()
            
            positive_count = sum(1 for kw in positive_keywords if kw in text)
            negative_count = sum(1 for kw in negative_keywords if kw in text)
            
            if positive_count > negative_count:
                sentiment['positive'] += 1
            elif negative_count > positive_count:
                sentiment['negative'] += 1
            else:
                sentiment['neutral'] += 1
        
        return sentiment
    
    def aggregate(self, ticker: str, company_name: str, days: int = 30, 
                  sources: List[str] = None) -> Dict:
        """Aggregate news from all sources."""
        if sources is None:
            sources = ['tavily']
        
        all_news = []
        
        # Build search queries
        queries = [
            f"{company_name} {ticker} stock news",
            f"{company_name} earnings",
            f"{company_name} {ticker} financial",
            f"{ticker} stock"
        ]
        
        # Search each source
        for source in sources:
            if source == 'tavily':
                for query in queries:
                    results = self.search_tavily(query, max_results=20)
                    all_news.extend(results)
            elif source == 'google':
                for query in queries:
                    results = self.search_google_news(query, max_results=10)
                    all_news.extend(results)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_news = []
        for item in all_news:
            url = item.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(item)
        
        # Sort by relevance score and date
        unique_news.sort(key=lambda x: (
            x.get('relevance_score', 0),
            x.get('published_date', '')
        ), reverse=True)
        
        # Limit to most recent news
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_news = [
            item for item in unique_news
            if not item.get('published_date') or 
            datetime.fromisoformat(item['published_date'].replace('Z', '+00:00')) >= cutoff_date
        ]
        
        # Categorize and analyze
        categorized = self.categorize_news(recent_news)
        sentiment = self.analyze_sentiment(recent_news)
        
        return {
            'ticker': ticker,
            'company_name': company_name,
            'timestamp': datetime.now().isoformat(),
            'period_days': days,
            'total_news_items': len(recent_news),
            'sources_used': sources,
            'sentiment': sentiment,
            'categories': {
                k: len(v) for k, v in categorized.items()
            },
            'news_items': recent_news[:50],  # Top 50 most relevant
            'categorized_news': {
                k: v[:10] for k, v in categorized.items()  # Top 10 per category
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate and analyze news for stock analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('ticker', help='Stock ticker symbol (e.g., AAPL)')
    parser.add_argument(
        '--company-name',
        help='Company name (default: same as ticker)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to look back (default: 30)'
    )
    parser.add_argument(
        '--tavily-api-key',
        help='Tavily API key (required for Tavily searches)'
    )
    parser.add_argument(
        '--sources',
        default='tavily',
        help='Comma-separated list of sources (tavily, google)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output JSON file path (default: stdout)'
    )
    
    args = parser.parse_args()
    
    aggregator = NewsAggregator(tavily_api_key=args.tavily_api_key)
    
    company_name = args.company_name or args.ticker
    sources_list = [s.strip() for s in args.sources.split(',')]
    
    result = aggregator.aggregate(
        args.ticker,
        company_name,
        days=args.days,
        sources=sources_list
    )
    
    output_json = json.dumps(result, indent=2, default=str)
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_json)
        print(f"News aggregation saved to {args.output}")
        print(f"Found {result['total_news_items']} news items")
        print(f"Sentiment: {result['sentiment']}")
    else:
        print(output_json)


if __name__ == '__main__':
    main()
