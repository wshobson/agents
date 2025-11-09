---
name: sdk-market-intelligence
description: Master Claude SDK for automated market intelligence gathering, news sentiment analysis, competitive monitoring, and alternative data integration. Covers real-time data aggregation, multi-source analysis, and intelligent insight generation. Use when gathering market intelligence, analyzing news sentiment, monitoring competitors, or integrating alternative data sources.
---

# Claude SDK Market Intelligence Automation

Master the Claude SDK to build comprehensive market intelligence systems with real-time news monitoring, sentiment analysis, competitive tracking, and alternative data integration.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Building real-time news monitoring and sentiment analysis
- Automating competitive intelligence gathering
- Integrating alternative data sources (social media, satellite, web scraping)
- Creating market event detection systems
- Developing economic indicator tracking
- Building insider trading monitoring
- Creating sector rotation analysis
- Developing earnings calendar automation
- Building regulatory filing analysis (SEC, 10-K, 10-Q)
- Creating market correlation and regime detection

## Core Concepts

### 1. Real-Time News Monitoring and Sentiment Analysis

**Automated News Aggregation**

Use SDK to monitor and analyze market-moving news:

```markdown
## News Monitoring System Architecture

**Data Sources:**
- Financial news (Bloomberg, Reuters, WSJ)
- Social media (Twitter/X, Reddit, StockTwits)
- Press releases (PR Newswire, Business Wire)
- Company filings (SEC EDGAR)
- Economic data (Fed, BLS, Census Bureau)

**SDK Workflow:**

**Step 1: Fetch News from Multiple Sources**
```python
# Fetch from news API
news_api = WebFetch(
    url="https://newsapi.org/v2/everything?q=AAPL&sortBy=publishedAt&apiKey=XXX",
    prompt="Get latest AAPL news from last 24 hours with title, source, description, url"
)

# Fetch from social media
reddit = WebFetch(
    url="https://www.reddit.com/r/wallstreetbets/search.json?q=AAPL&sort=top&t=day",
    prompt="Get top AAPL discussions from r/wallstreetbets today with sentiment indicators"
)

# Fetch from financial sites
seeking_alpha = WebFetch(
    url="https://seekingalpha.com/api/v3/news?filter[symbols]=AAPL",
    prompt="Get AAPL news from Seeking Alpha with analyst ratings and price targets"
)
```

**Step 2: Sentiment Analysis**
```bash
# Run sentiment analysis on collected news
Bash(command="python intelligence/news_sentiment.py --symbol AAPL --data data/news_24h.json")
```

**news_sentiment.py:**
```python
from transformers import pipeline
import pandas as pd
import json

# Load FinBERT for financial sentiment
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# Load news articles
with open("data/news_24h.json") as f:
    articles = json.load(f)

# Analyze sentiment for each article
results = []
for article in articles:
    text = f"{article['title']} {article['description']}"
    sentiment = sentiment_analyzer(text[:512])[0]  # Truncate to model limit

    results.append({
        'title': article['title'],
        'source': article['source'],
        'sentiment': sentiment['label'],  # positive/negative/neutral
        'score': sentiment['score'],  # confidence
        'published': article['publishedAt'],
        'url': article['url']
    })

# Aggregate sentiment
df = pd.DataFrame(results)

bullish = len(df[df['sentiment'] == 'positive'])
bearish = len(df[df['sentiment'] == 'negative'])
neutral = len(df[df['sentiment'] == 'neutral'])

# Calculate sentiment score
sentiment_score = (bullish - bearish) / len(df)  # Range: -1 to +1

output = {
    'total_articles': len(df),
    'bullish': bullish,
    'bearish': bearish,
    'neutral': neutral,
    'sentiment_score': sentiment_score,
    'top_bullish': df[df['sentiment'] == 'positive'].nlargest(3, 'score').to_dict('records'),
    'top_bearish': df[df['sentiment'] == 'negative'].nlargest(3, 'score').to_dict('records')
}

print(json.dumps(output))
```

**Step 3: Generate Trading Insights**
```python
# Analyze sentiment for trading signals
Task(
    subagent_type="general-purpose",
    prompt="""
    News sentiment analysis for AAPL:

    Sentiment Score: +0.42 (moderately bullish)
    Articles: 87 total (52 bullish, 18 bearish, 17 neutral)

    Top Bullish Themes:
    - iPhone 16 sales exceeding expectations (15 articles)
    - AI feature rollout successful (12 articles)
    - Strong earnings guidance (8 articles)

    Top Bearish Themes:
    - China regulatory concerns (10 articles)
    - Valuation stretched (5 articles)

    Provide:
    1. Overall sentiment interpretation
    2. Catalysts driving sentiment
    3. Trading recommendation (buy/hold/sell)
    4. Key risks to monitor
    """
)
```

**Output:**
```
📰 News Sentiment Analysis - AAPL - 2025-11-09

Analysis Period: Last 24 hours
Articles Analyzed: 87

Sentiment Breakdown:
- Bullish: 52 articles (59.8%) 📈
- Neutral: 17 articles (19.5%)
- Bearish: 18 articles (20.7%) 📉

Sentiment Score: +0.42 (Moderately Bullish)
Trend: ↑ +0.15 vs yesterday

Key Themes:

✅ Bullish Catalysts (High Conviction):
1. iPhone 16 Sales Beat (15 articles, avg confidence: 0.89)
   - "iPhone 16 demand surpasses expectations in China"
   - "Supply chain data suggests strong Q4 iPhone sales"

2. AI Features Success (12 articles, avg confidence: 0.82)
   - "Apple Intelligence driving user engagement"
   - "AI features may accelerate upgrade cycle"

3. Earnings Guidance Raised (8 articles, avg confidence: 0.91)
   - "Apple raises Q4 revenue guidance"
   - "Analyst upgrades following guidance increase"

🔴 Bearish Risks (Monitor Closely):
1. China Regulatory Concerns (10 articles, avg confidence: 0.78)
   - "China considering iPhone restrictions for govt employees"
   - "Geopolitical tensions could impact sales"

2. Valuation Concerns (5 articles, avg confidence: 0.65)
   - "AAPL P/E ratio above historical average"
   - "Some analysts see limited upside at current levels"

Trading Recommendation: BUY (Moderate Conviction)

Rationale:
- Strong positive sentiment driven by fundamental catalysts
- iPhone sales data is concrete (not speculation)
- Sentiment improving vs yesterday
- Bearish themes largely speculative

Risk Management:
- Monitor China news closely (potential quick reversal)
- Consider taking profits if P/E reaches 35x
- Watch for earnings report confirmation (Nov 15)

Position Sizing: Standard (not oversized due to China risk)
```
```

### 2. Social Media Intelligence

**Reddit/Twitter Sentiment Tracking**

Monitor retail investor sentiment on social platforms:

```markdown
## Social Media Monitoring System

**Target Platforms:**
- Reddit: r/wallstreetbets, r/stocks, r/investing
- Twitter/X: $AAPL hashtag, finance influencers
- StockTwits: Real-time stock discussions

**SDK Workflow:**

**Step 1: Scrape Social Discussions**
```python
# Reddit wallstreetbets mentions
reddit_data = WebFetch(
    url="https://www.reddit.com/r/wallstreetbets/search.json?q=AAPL&sort=hot&t=day&limit=100",
    prompt="Get AAPL discussions: title, score, comments count, sentiment words"
)

# Twitter/X mentions
twitter_data = WebFetch(
    url="https://api.twitter.com/2/tweets/search/recent?query=$AAPL",
    prompt="Get tweets mentioning $AAPL with engagement metrics"
)

# StockTwits stream
stocktwits_data = WebFetch(
    url="https://api.stocktwits.com/api/2/streams/symbol/AAPL.json",
    prompt="Get AAPL StockTwits messages with bullish/bearish labels"
)
```

**Step 2: Analyze Social Sentiment**
```bash
# Process social media data
Bash(command="python intelligence/social_sentiment.py --symbol AAPL --sources reddit,twitter,stocktwits")
```

**social_sentiment.py:**
```python
import pandas as pd
import json
from collections import Counter
import re

# Load social media data
with open("data/social_media.json") as f:
    data = json.load(f)

# Process Reddit
reddit_posts = data['reddit']
reddit_sentiment = sum([1 if post['score'] > 50 else -1 if post['score'] < 0 else 0
                        for post in reddit_posts]) / len(reddit_posts)

# Extract trending phrases
all_text = " ".join([post['title'] for post in reddit_posts])
words = re.findall(r'\b\w+\b', all_text.lower())
trending = Counter(words).most_common(10)

# Process Twitter engagement
twitter_posts = data['twitter']
twitter_engagement = sum([post['likes'] + post['retweets'] for post in twitter_posts])

# Process StockTwits explicit sentiment
stocktwits = data['stocktwits']
st_bullish = len([m for m in stocktwits if m['sentiment'] == 'bullish'])
st_bearish = len([m for m in stocktwits if m['sentiment'] == 'bearish'])

# Calculate overall social sentiment score
social_score = (
    (reddit_sentiment * 0.3) +  # Reddit weight
    ((st_bullish - st_bearish) / len(stocktwits) * 0.4) +  # StockTwits weight
    (min(twitter_engagement / 10000, 1) * 0.3)  # Twitter weight (capped)
)

output = {
    'social_score': social_score,  # -1 to +1
    'reddit_sentiment': reddit_sentiment,
    'reddit_mentions': len(reddit_posts),
    'reddit_trending': trending,
    'twitter_engagement': twitter_engagement,
    'stocktwits_bullish': st_bullish,
    'stocktwits_bearish': st_bearish,
    'stocktwits_total': len(stocktwits)
}

print(json.dumps(output))
```

**Step 3: Contrarian Signal Detection**
```python
# Detect extreme sentiment (contrarian indicator)
Task(
    subagent_type="general-purpose",
    prompt="""
    Social media sentiment analysis for AAPL:

    Social Score: +0.78 (Very Bullish)
    Reddit: 248 mentions (highest in 6 months)
    Reddit Trending: "moon", "calls", "yolo", "ATH"
    StockTwits: 85% bullish (extreme)

    Analyze:
    1. Is sentiment at extreme level (contrarian signal)?
    2. Compare to historical sentiment levels
    3. Correlation with price movements
    4. Trading recommendation considering crowd psychology
    """
)
```

**Output:**
```
📱 Social Media Intelligence - AAPL

Period: Last 24 hours

Aggregate Social Score: +0.78 (Very Bullish) ⚠️

Platform Breakdown:

Reddit (r/wallstreetbets):
- Mentions: 248 (6-month high) 🔴
- Sentiment: +0.65 (bullish)
- Trending Words: "moon", "calls", "yolo", "ATH", "buy"
- Top Post: "AAPL to $200 next week 🚀" (1.2K upvotes)

Twitter/X:
- Engagement: 125K interactions
- Mentions: 3,400 tweets
- Influencer Sentiment: Mixed (50/50)

StockTwits:
- Messages: 1,850
- Bullish: 85% 🔴 (extreme)
- Bearish: 15%
- Sentiment Trend: ↑ Rapidly increasing

⚠️ CONTRARIAN ALERT

Extreme Sentiment Indicators:
1. Reddit mentions at 6-month high (euphoria signal)
2. "YOLO" and "moon" trending (retail FOMO)
3. StockTwits 85% bullish (extreme reading)
4. Sentiment +0.78 is in top 5% historically

Historical Pattern:
When social sentiment exceeds +0.70:
- Next 5 days: -2.3% average return
- Win rate: 35%
- Correlation: Negative (contrarian indicator works)

Current Price: $189.25
Recent Move: +4.8% in 2 days (rapid)

Contrarian Interpretation: SELL SIGNAL

Rationale:
- Extreme bullish sentiment often marks short-term tops
- Retail FOMO suggests late-stage rally
- Smart money may fade retail enthusiasm
- Risk/reward unfavorable at current sentiment extreme

Recommendation:
- Action: Take profits or reduce exposure
- Timing: Now (don't wait for reversal)
- Alternative: Buy puts for downside protection
- Re-entry: Wait for sentiment to cool (<+0.40)

Risk: Momentum can continue (sentiment can stay extreme longer than expected)
```
```

### 3. Insider Trading Monitoring

**SEC Form 4 Tracking Automation**

Monitor insider buying/selling activity:

```markdown
## Insider Trading Intelligence

**Data Source:** SEC EDGAR (Form 4 filings)

**SDK Workflow:**

**Step 1: Fetch Insider Filings**
```python
# Get recent Form 4 filings for AAPL
insider_filings = WebFetch(
    url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=4&dateb=&owner=only&count=40",
    prompt="Extract insider trading filings for AAPL: name, title, transaction type, shares, price, date"
)
```

**Step 2: Parse and Analyze Transactions**
```bash
# Process insider transactions
Bash(command="python intelligence/insider_analysis.py --symbol AAPL --data data/insider_filings.xml")
```

**insider_analysis.py:**
```python
import pandas as pd
from datetime import datetime, timedelta

# Parse Form 4 filings
filings = pd.read_xml("data/insider_filings.xml")

# Calculate metrics
recent_30d = filings[filings['date'] > datetime.now() - timedelta(days=30)]

# Aggregate by transaction type
buys = recent_30d[recent_30d['transaction'] == 'P']  # P = Purchase
sells = recent_30d[recent_30d['transaction'] == 'S']  # S = Sale

# Calculate dollar volumes
buy_volume = (buys['shares'] * buys['price']).sum()
sell_volume = (sells['shares'] * sells['price']).sum()

# Insider sentiment score
insider_score = (buy_volume - sell_volume) / (buy_volume + sell_volume) if (buy_volume + sell_volume) > 0 else 0

# Identify key insiders
executives = recent_30d[recent_30d['title'].str.contains('CEO|CFO|President|Director')]

output = {
    'period': '30 days',
    'total_transactions': len(recent_30d),
    'buys': len(buys),
    'sells': len(sells),
    'buy_volume': buy_volume,
    'sell_volume': sell_volume,
    'insider_score': insider_score,  # -1 (selling) to +1 (buying)
    'top_buyers': buys.nlargest(3, 'shares').to_dict('records'),
    'top_sellers': sells.nlargest(3, 'shares').to_dict('records'),
    'executive_activity': executives.to_dict('records')
}

print(json.dumps(output))
```

**Step 3: Generate Insights**
```python
# Interpret insider activity
Task(
    subagent_type="general-purpose",
    prompt="""
    Insider trading analysis for AAPL:

    Last 30 days:
    - Buys: 3 transactions, $2.1M volume
    - Sells: 12 transactions, $45.8M volume
    - Insider Score: -0.91 (heavy selling)

    Key Activity:
    - CFO sold $18M (largest transaction)
    - 3 Board members sold $12M combined
    - Only 1 VP bought $2M

    Analyze:
    1. Significance of insider selling pattern
    2. Potential reasons (diversification vs bearish)
    3. Historical patterns for AAPL insiders
    4. Trading signal strength
    """
)
```

**Output:**
```
🔍 Insider Trading Intelligence - AAPL

Period: Last 30 days

Activity Summary:
- Total Transactions: 15
- Buys: 3 ($2.1M volume)
- Sells: 12 ($45.8M volume)

Insider Sentiment Score: -0.91 (Heavy Selling) 🔴

Key Transactions:

Sellers:
1. CFO - Sold 95,000 shares at $192.50 ($18.3M)
   - Date: 2025-11-05
   - Type: 10b5-1 Plan (pre-scheduled)

2. Board Member A - Sold 32,000 shares at $190.00 ($6.1M)
   - Date: 2025-11-03
   - Type: Discretionary

3. Board Member B - Sold 28,000 shares at $188.50 ($5.3M)
   - Date: 2025-11-01
   - Type: Discretionary

Buyers:
1. VP Engineering - Bought 11,000 shares at $185.00 ($2.0M)
   - Date: 2025-10-28
   - Type: Open market purchase

Analysis:

⚠️ Moderate Bearish Signal

Interpretation:
1. Heavy selling (21x more sold than bought)
2. CFO sale is largest, BUT pre-scheduled (10b5-1 plan)
3. Board members selling discretionary (more significant)
4. Only 1 insider buying (limited conviction)

Context:
- AAPL insiders historically sell >buy (diversification)
- Current selling is 2.5x normal rate (elevated)
- No pattern of buying before rallies

Potential Reasons:
✅ Diversification (CFO has >$200M in stock)
✅ Tax planning (year-end approaching)
🔴 Valuation concerns (stock near all-time highs)
🔴 Internal view on upcoming earnings?

Trading Signal: Mild Bearish

Recommendation:
- Not strong enough alone to sell
- Use as confirming factor with other signals
- Watch for additional discretionary selling
- Monitor CFO/CEO activity especially

Weight in decision: 15% (supporting indicator, not primary)
```
```

### 4. Earnings Calendar and Event Tracking

**Automated Earnings Intelligence**

Track and analyze earnings events systematically:

```markdown
## Earnings Event Automation

**SDK Workflow:**

**Step 1: Fetch Earnings Calendar**
```python
# Get upcoming earnings
earnings_cal = WebFetch(
    url="https://api.earningswhispers.com/calendar?symbol=AAPL",
    prompt="Get AAPL earnings date, time, consensus EPS estimate, whisper number"
)

# Get historical earnings surprises
history = WebFetch(
    url="https://api.earningswhispers.com/historical?symbol=AAPL&periods=8",
    prompt="Get last 8 quarters: reported EPS, estimate, surprise %, stock reaction"
)
```

**Step 2: Pre-Earnings Analysis**
```bash
# Analyze earnings setup
Bash(command="python intelligence/earnings_preview.py --symbol AAPL --data data/earnings_data.json")
```

**earnings_preview.py:**
```python
import pandas as pd
import statistics

# Load historical earnings data
history = pd.read_json("data/earnings_history.json")

# Calculate surprise rate
surprises = history['surprise_pct']
beat_rate = len(surprises[surprises > 0]) / len(surprises)

# Average price reaction
reactions = history['price_change_1d']
avg_reaction = reactions.mean()
volatility = reactions.std()

# Recent trend
recent_4q = surprises.tail(4)
improving = recent_4q.is_monotonic_increasing

# Options implied move
# (fetch from options API)
implied_move = 0.045  # 4.5% (from ATM straddle)

output = {
    'earnings_date': '2025-11-15',
    'consensus_eps': 1.54,
    'whisper_number': 1.58,
    'beat_rate': beat_rate,
    'avg_surprise': surprises.mean(),
    'avg_reaction': avg_reaction,
    'reaction_volatility': volatility,
    'implied_move': implied_move,
    'trend': 'improving' if improving else 'declining'
}

print(json.dumps(output))
```

**Step 3: Generate Earnings Strategy**
```python
# Develop earnings trading strategy
Task(
    subagent_type="general-purpose",
    prompt="""
    Earnings preview for AAPL (Nov 15, 2025):

    Historical Performance:
    - Beat rate: 87.5% (7 of 8 quarters)
    - Avg surprise: +3.2%
    - Avg reaction: +2.1% (day after)
    - Volatility: ±4.8%

    Current Setup:
    - Consensus EPS: $1.54
    - Whisper number: $1.58 (higher)
    - Implied move: 4.5% (options pricing)

    Sentiment:
    - News: Bullish (+0.42)
    - Social: Very bullish (+0.78, extreme)
    - Analysts: 78% Buy ratings

    Develop:
    1. Earnings beat probability
    2. Expected price reaction scenarios
    3. Pre-earnings positioning strategy
    4. Post-earnings trade plan
    """
)
```

**Output:**
```
📊 Earnings Intelligence - AAPL - Nov 15, 2025

Earnings Release: Nov 15, 2025 (After market close)

Consensus vs Whisper:
- Consensus EPS: $1.54
- Whisper Number: $1.58 (+2.6% above consensus)
- Revenue Estimate: $89.5B

Historical Beat Rate: 87.5% (Strong track record)

Price Reaction History:
- Average move after earnings: +2.1%
- Positive reactions: 75% of time
- Largest beat: +6.2% (Q1 2024)
- Largest miss: -3.8% (Q3 2023)

Current Implied Move: 4.5% (Options market pricing)
- Upside scenario: $198.00 (+4.5%)
- Downside scenario: $181.00 (-4.5%)

Probability Analysis:

Beat Scenario (70% probability):
- EPS: $1.58+ (beat by 2-3%)
- Expected reaction: +3% to +5%
- Target: $195 - $199
- Drivers: Strong iPhone sales, services growth

Meet Scenario (20% probability):
- EPS: $1.53 - $1.55 (in-line)
- Expected reaction: -1% to +1%
- Target: $188 - $192
- Drivers: Mixed iPhone sales, guidance matters

Miss Scenario (10% probability):
- EPS: <$1.52 (miss by 1-2%)
- Expected reaction: -5% to -7%
- Target: $176 - $181
- Drivers: Weak China sales, margin pressure

⚠️ Risk Factors:
- Very bullish sentiment (social +0.78) = high expectations
- Stock up 12% since last earnings (already pricing in beat?)
- Insider selling elevated (-0.91 score)
- Valuation at premium (P/E 32x)

Pre-Earnings Strategy:

Conservative Approach: WAIT
- Sentiment too bullish (crowded trade)
- Risk/reward unfavorable before event
- Better entry after volatility subsides

Aggressive Approach: Small Long Position
- Enter 25% position at current levels
- Add 50% more if beats and guides up
- Stop loss at $185 (-2.4%)

Options Strategy: Sell Put Spread
- Sell $180 put / Buy $175 put (collect premium)
- Assumes stock stays above $180 post-earnings
- Max profit: $200 per spread
- Max loss: $300 per spread
- Win if: stock flat, up, or down <4.5%

Post-Earnings Plan:
- If beats + guides up: BUY (target $210)
- If beats + flat guidance: HOLD
- If meets expectations: NEUTRAL (wait)
- If misses: SELL / SHORT (target $175)
```
```

### 5. Alternative Data Integration

**Satellite Imagery and Alternative Data**

Integrate unconventional data sources:

```markdown
## Alternative Data Intelligence

**Data Sources:**
- Satellite imagery (parking lot traffic, shipping activity)
- Credit card transaction data (consumer spending)
- Web traffic (app downloads, website visits)
- Job postings (hiring trends)
- Supply chain data (component orders)

**Example: Retail Traffic Analysis**

**Step 1: Fetch Satellite Data**
```python
# Get retail parking lot traffic data
satellite_data = WebFetch(
    url="https://api.satellitedata.com/retail-traffic?ticker=AAPL&locations=apple-stores",
    prompt="Get Apple Store parking lot traffic for last 30 days compared to previous year"
)
```

**Step 2: Analyze Traffic Trends**
```bash
# Process alternative data
Bash(command="python intelligence/alternative_data.py --source satellite --symbol AAPL")
```

**alternative_data.py:**
```python
import pandas as pd

# Load satellite traffic data
traffic = pd.read_json("data/satellite_traffic.json")

# Calculate year-over-year change
traffic['yoy_change'] = (traffic['current_count'] - traffic['prior_year_count']) / traffic['prior_year_count']

# Aggregate by region
regional = traffic.groupby('region')['yoy_change'].mean()

# Overall trend
overall_change = traffic['yoy_change'].mean()

# Recent trend (last 7 days)
recent_change = traffic.tail(7)['yoy_change'].mean()

output = {
    'overall_traffic_change': overall_change,
    'recent_trend': recent_change,
    'regional_breakdown': regional.to_dict(),
    'interpretation': 'increasing' if overall_change > 0.05 else 'flat' if overall_change > -0.05 else 'decreasing'
}

print(json.dumps(output))
```

**Step 3: Generate Trading Signal**
```python
# Interpret alternative data
Task(
    subagent_type="general-purpose",
    prompt="""
    Alternative data analysis for AAPL:

    Apple Store traffic (satellite data):
    - Overall YoY change: +8.2%
    - Recent 7-day trend: +12.5%
    - Regional: US +6%, China +15%, Europe +7%

    Credit card data:
    - Apple product spending: +11% vs last year

    Web traffic:
    - Apple.com visits: +9%
    - App Store downloads: +14%

    Analyze:
    1. Correlation with iPhone sales
    2. Predictive value for earnings
    3. Geographic insights (China strength)
    4. Trading signal from alternative data
    """
)
```

**Output:**
```
🛰️ Alternative Data Intelligence - AAPL

Data Period: Last 30 days

Satellite Traffic Analysis:
- Apple Store foot traffic: +8.2% YoY ✅
- Recent acceleration: +12.5% (last 7 days)
- Regional breakdown:
  * US: +6% (steady)
  * China: +15% (strong) 🔥
  * Europe: +7% (solid)

Credit Card Spending:
- Apple product purchases: +11% YoY ✅
- iPhone category: +14%
- Mac category: +8%
- Services: +6%

Digital Engagement:
- Apple.com traffic: +9% YoY
- App Store downloads: +14%
- Product page views: +18%

Supply Chain Data:
- Component orders: +12% vs last quarter
- iPhone assembly: Accelerating in October

Interpretation:

🎯 Strong Bullish Signal

Key Insights:
1. China traffic +15% contradicts "China weakness" narrative
   - Suggests strong iPhone 16 demand in critical market
   - Could drive earnings beat

2. All data sources aligned (high confidence)
   - Traffic, spending, web, supply chain all positive
   - Confluence increases signal reliability

3. Recent acceleration (last 7 days +12.5%)
   - Momentum building into earnings
   - Suggests strong Q4 trajectory

Historical Correlation:
- Traffic growth >8% historically predicts:
  - Earnings beat: 85% of time
  - Average beat magnitude: +3.4%
  - Stock reaction: +4.2% average

Earnings Implication:
- EPS estimate: $1.54
- Implied beat based on traffic: $1.58 - $1.60
- Confidence: HIGH (multiple data sources confirm)

Trading Signal: BUY before earnings

Position:
- Entry: Current price ($189)
- Target: $202 (post-earnings if beats)
- Stop: $185 (if data proves wrong)
- R/R: 1:3.25 (favorable)

Risk:
- Alternative data can be noisy
- Correlation not causation
- Supply chain data backward-looking
```
```

## References

### SDK Tools for Market Intelligence

| Tool | Purpose | Intelligence Use Cases |
|------|---------|------------------------|
| **WebFetch** | Fetch external data | News, social media, filings, economic data |
| **Task** | Multi-agent coordination | News analysis, sentiment synthesis, event interpretation |
| **Bash** | Execute scripts | NLP sentiment, data processing, ML models |
| **Read** | Read files | Historical data, event logs, watchlists |
| **Write** | Write files | Intelligence reports, alerts, trade signals |
| **Grep** | Search code/data | Find patterns in logs, search filings |

### Intelligence Gathering Patterns

**Pattern 1: Real-Time News Monitoring**
```
WebFetch (news API) → Bash (sentiment NLP) → Task (analyze) → Write (alert)
```

**Pattern 2: Social Sentiment Tracking**
```
WebFetch (Reddit/Twitter) → Bash (aggregate) → Task (contrarian analysis) → Write (signal)
```

**Pattern 3: Multi-Source Intelligence**
```
[WebFetch (news) + WebFetch (social) + WebFetch (filings)] → Bash (combine) → Task (synthesize)
```

**Pattern 4: Event-Driven Workflow**
```
WebFetch (earnings calendar) → Bash (historical analysis) → Task (strategy) → Write (plan)
```

### Best Practices

✅ **Multiple sources** - Don't rely on single data source
✅ **Cross-validate** - Confirm signals across different data types
✅ **Track accuracy** - Measure predictive value of each source
✅ **Automate monitoring** - Set up continuous feeds, not manual checks
✅ **Context matters** - Same news can be bullish or bearish depending on context
✅ **Timeliness** - Speed matters, automate for real-time processing
✅ **Historical baseline** - Compare current data to historical norms

### Common Pitfalls to Avoid

❌ **False causation** - Correlation ≠ causation in alternative data
❌ **Confirmation bias** - Don't only seek data confirming your view
❌ **Noise trading** - Not every news item is actionable
❌ **Overfitting** - Historical patterns may not repeat
❌ **Ignoring context** - Earnings beat during recession ≠ bullish
❌ **Stale data** - Real-time edge disappears if data is delayed
❌ **Single source dependency** - Diversify intelligence sources
