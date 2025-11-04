---
name: news-search
description: Search and analyze important company news, earnings announcements, regulatory changes, M&A activity, and market-moving events. Provides comprehensive news research with sentiment analysis and impact assessment.
---

# News Search & Analysis

Search for and analyze important company news, earnings announcements, regulatory changes, M&A activity, and other market-moving events. Provides comprehensive news research with sentiment analysis, materiality assessment, and timeline construction.

**Execution Method**: This command uses Task tool to delegate work to News Researcher agent with a focused prompt.

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Overview

This command performs comprehensive news research for a company:

1. **News Aggregation** - Search multiple sources for company news
2. **Categorization** - Organize news by type (earnings, M&A, products, regulatory)
3. **Sentiment Analysis** - Assess positive/negative/neutral impact
4. **Materiality Assessment** - Identify news that could meaningfully impact stock price
5. **Timeline Construction** - Build chronological news narrative
6. **Impact Evaluation** - Assess how news affects fundamentals and valuation

## Workflow

**IMPORTANT**: This command uses Task tool to delegate work to News Researcher agent. Execute using Task tool with subagent_type="stock-analysis:news-researcher".

### Phase 1: News Search & Aggregation
**Led by**: News Researcher

**How to execute**: Use Task tool with subagent_type="stock-analysis:news-researcher"

**Prompt for News Researcher**:
"Search and aggregate news for {TICKER} (last {DAYS} days) using Tavily API. Search for: (1) Earnings announcements and guidance updates, (2) M&A activity, partnerships, strategic deals, (3) Regulatory approvals, litigation, compliance issues, (4) Product launches, technology announcements, R&D milestones, (5) Management changes (CEO/CFO/board), (6) Market events (dividends, buybacks, offerings). Extract headlines, dates, sources, content snippets. Filter by date and source credibility. Aggregate results from multiple search queries. Provide: total news items found, material news items (price impact >5%), Tavily coverage percentage."

Search for company news using **Tavily Search API** as primary method:

**Primary Method: Tavily Search**
- **Tavily API** - Real-time news aggregation from multiple sources (tavily.com)
- **Search queries** - Use company name, ticker, and event types:
  - `"[Company Name] [Ticker] stock news last [X] days"`
  - `"[Company Name] earnings announcement"`
  - `"[Company Name] M&A acquisition"`
  - `"[Company Name] regulatory approval"`
  - `"[Company Name] product launch"`
- **Time filters** - Specify range in queries (last 7/30 days, quarter, year)
- **Source filtering** - Focus on credible financial sources (bloomberg.com, reuters.com, wsj.com, sec.gov)

**Additional Sources** (when Tavily results need verification):
- **Financial news platforms** - Bloomberg, Reuters, Financial Times, WSJ, CNBC, MarketWatch
- **Regulatory filings** - SEC filings (10-K, 10-Q, 8-K), press releases, investor relations
- **Earnings announcements** - Earnings releases, conference calls, guidance updates
- **Industry publications** - Sector-specific news, trade publications, analyst reports
- **News aggregators** - Google News, Yahoo Finance, Seeking Alpha, Reddit

**Search Criteria**:
- Company name and ticker symbol
- Time horizon (last 7 days, 30 days, quarter, or full year)
- News categories (earnings, M&A, products, regulatory, management, market events)

**Tavily Result Processing**:
- Extract headlines, dates, sources, and content snippets from Tavily results
- Filter by date, source credibility, and relevance
- Aggregate results from multiple Tavily search queries
- Cross-reference with official filings when available

**Output**:
```
Primary Search Method: Tavily API
Tavily Queries Executed: [X] queries
News Sources Searched: [List sources from Tavily results]
Time Period: Last [X] days
Total News Items Found: [X]
Material News Items: [X] (price impact >5%)
Tavily Coverage: [X]% of results from Tavily
```

### Phase 2: News Categorization & Prioritization
**Led by**: News Researcher

**How to execute**: Use Task tool with subagent_type="stock-analysis:news-researcher"

**Prompt for News Researcher**:
"Categorize and prioritize news items for {TICKER}. Organize by categories: Earnings & Financials, M&A Activity, Regulatory & Legal, Product & Innovation, Management Changes, Market Events, Competitive Dynamics, Macro Impact. Prioritize by: (1) Recency (most recent first), (2) Materiality (price impact >5%), (3) Source credibility (official filings, major outlets), (4) Confirmation (multiple sources), (5) Impact scope (company-wide). Provide: news categories found with counts, top 10 most important news items with materiality assessment."

Organize and prioritize news:

**News Categories**:
- **Earnings & Financials** - Earnings releases, guidance changes, financial results
- **M&A Activity** - Mergers, acquisitions, divestitures, joint ventures, partnerships
- **Regulatory & Legal** - FDA approvals, regulatory changes, litigation, compliance
- **Product & Innovation** - Product launches, technology announcements, R&D milestones
- **Management Changes** - CEO/CFO changes, board changes, executive departures
- **Market Events** - Stock splits, dividends, buybacks, secondary offerings, debt issuance
- **Competitive Dynamics** - Market share changes, competitive threats, industry disruption
- **Macro Impact** - Economic events, sector trends, geopolitical events affecting company

**Prioritization Criteria**:
- **Recency** - Most recent news prioritized (last 7 days, 30 days, quarter)
- **Materiality** - Events that could impact stock price by >5% prioritized
- **Source credibility** - Official filings, major news outlets prioritized
- **Confirmation** - News confirmed by multiple sources prioritized
- **Impact scope** - Company-wide impact prioritized over minor division news

**Output**:
```
News Categories Found:
- Earnings: [X] items
- M&A: [X] items
- Products: [X] items
- Regulatory: [X] items
- Management: [X] items
- Market Events: [X] items

Top 10 Most Important News Items:
1. [Date] [Category] [Headline] - [Materiality: HIGH/MEDIUM/LOW]
2. [Date] [Category] [Headline] - [Materiality: HIGH/MEDIUM/LOW]
...
```

### Phase 3: Sentiment Analysis & Impact Assessment
**Led by**: News Researcher

**How to execute**: Use Task tool with subagent_type="stock-analysis:news-researcher"

**Prompt for News Researcher**:
"Analyze sentiment and impact for {TICKER} news. Assess: (1) Overall sentiment (positive/negative/neutral), (2) Positive signals (earnings beats, guidance raises, product launches), (3) Negative signals (earnings misses, guidance cuts, regulatory issues), (4) Fundamental impact (how news affects revenue, earnings, growth, competitive position), (5) Valuation impact (does news change intrinsic value?), (6) Timing impact (near-term vs long-term), (7) Risk impact (does news increase/decrease risk?), (8) Catalyst identification (is this a price catalyst?), (9) Market reaction (how did stock price react?). Provide: sentiment breakdown, material news impact analysis, key catalysts identified."

Analyze news sentiment and impact:

**Sentiment Analysis**:
- **Positive signals** - Earnings beats, guidance raises, product launches, M&A premium
- **Negative signals** - Earnings misses, guidance cuts, regulatory issues, management departures
- **Neutral/Informational** - Factual updates, routine announcements, status updates
- **Controversy detection** - Mixed reactions, conflicting analyst views, uncertainty

**Impact Assessment**:
- **Fundamental impact** - How news affects revenue, earnings, growth, competitive position
- **Valuation impact** - Does news change intrinsic value or multiple expansion/contraction?
- **Timing impact** - Near-term vs long-term implications
- **Risk impact** - Does news increase or decrease risk profile?
- **Catalyst identification** - Is this news a price catalyst or just informational?
- **Market reaction** - How did stock price react to news?

**Output**:
```
Overall News Sentiment: [POSITIVE/NEGATIVE/NEUTRAL]
Positive News Count: [X]
Negative News Count: [X]
Neutral News Count: [X]

Material News Impact:
- [News Item 1]: [POSITIVE/NEGATIVE] - [Fundamental Impact] - [Market Reaction]
- [News Item 2]: [POSITIVE/NEGATIVE] - [Fundamental Impact] - [Market Reaction]
- [News Item 3]: [POSITIVE/NEGATIVE] - [Fundamental Impact] - [Market Reaction]

Key Catalysts Identified:
- [Upcoming Event 1]: [Date] - [Expected Impact]
- [Upcoming Event 2]: [Date] - [Expected Impact]
- [Upcoming Event 3]: [Date] - [Expected Impact]
```

### Phase 4: News Timeline & Narrative
**Led by**: News Researcher

**How to execute**: Use Task tool with subagent_type="stock-analysis:news-researcher"

**Prompt for News Researcher**:
"Build news timeline and narrative for {TICKER}. Create: (1) Chronological news timeline (most recent first), (2) Group related news into themes (earnings, M&A, products, etc.), (3) Identify patterns and trends, (4) Connect dots between different news items, (5) Highlight most material events, (6) Synthesize overall news story (2-3 paragraphs), (7) Identify what news might be missing or expected, (8) Forward-looking implications. Save complete news analysis as markdown report."

Build chronological timeline and narrative:

**Timeline Construction**:
- Chronological ordering by date (most recent first)
- Group related news items into themes
- Identify patterns and trends
- Connect dots between different news items
- Highlight most material events

**Narrative Synthesis**:
- Overall news story for the company
- Key themes and patterns
- Recent developments and their significance
- What news might be missing or expected
- Forward-looking implications

**Output**:
```
News Timeline (Last 30 Days):
[Date 1] - [Category] - [Headline] - [Impact: POSITIVE/NEGATIVE/NEUTRAL]
[Date 2] - [Category] - [Headline] - [Impact: POSITIVE/NEGATIVE/NEUTRAL]
[Date 3] - [Category] - [Headline] - [Impact: POSITIVE/NEGATIVE/NEUTRAL]
...

Key Themes:
- Theme 1: [Description] - [Significance]
- Theme 2: [Description] - [Significance]
- Theme 3: [Description] - [Significance]

News Narrative:
[2-3 paragraph summary of overall news story and implications]
```

## Input Requirements

To run news search, provide:

```yaml
Company: AAPL (or company name)
Ticker: AAPL
Time Horizon: Last 30 days (or 7 days, quarter, full year)
Focus Areas: Optional (earnings, M&A, products, regulatory, all)
```

## Example Analysis

### Input
```
/stock-analysis:news-search AAPL --time-horizon=30-days
```

### Output Structure
```
=== NEWS SEARCH RESULTS ===
Company: Apple Inc. (AAPL)
Time Period: Last 30 days
Sources Searched: SEC filings, Bloomberg, Reuters, WSJ, CNBC, MarketWatch
Total News Items: 45
Material News Items: 12 (price impact >5%)

=== TOP 10 MOST IMPORTANT NEWS ===
1. [2025-01-15] Earnings - Q1 2025 Earnings Beat Expectations (+5% EPS, +8% revenue)
   Impact: POSITIVE - Materiality: HIGH
   Market Reaction: Stock +4.2% on earnings day
   
2. [2025-01-10] Product - New iPhone 16 Pro Launch Announced
   Impact: POSITIVE - Materiality: MEDIUM
   Market Reaction: Stock +1.5% on announcement
   
3. [2025-01-05] Regulatory - EU Approves Apple Pay Expansion
   Impact: POSITIVE - Materiality: MEDIUM
   Market Reaction: Stock +0.8% on approval

=== NEWS SENTIMENT ===
Overall Sentiment: POSITIVE
Positive News: 8 items
Negative News: 2 items
Neutral News: 35 items

=== KEY CATALYSTS ===
- Q2 2025 Earnings (3 weeks) - Expected positive
- Product Launch Event (next month) - Expected positive
- Regulatory Decision (6 weeks) - Uncertainty

=== NEWS TIMELINE ===
[Chronological list of all material news items]
```

## Usage Examples

### Quick News Search (Last 7 Days)
```
/stock-analysis:news-search NVDA --time-horizon=7-days
```

### Comprehensive News Search (Last Quarter)
```
/stock-analysis:news-search MSFT --time-horizon=quarter
```

### Focused Search (Earnings Only)
```
/stock-analysis:news-search AAPL --focus=earnings
```

### Full Year News Search
```
/stock-analysis:news-search TSLA --time-horizon=full-year
```

## Best Practices

### For Users
1. **Provide ticker/company name** - Clear identification of company to research
2. **Specify time horizon** - Recent news (7 days) or longer period (30 days, quarter)?
3. **Tavily integration** - Agent automatically uses Tavily for news search when available
4. **Share known news** - If you already know about specific news, share it for context
5. **Clarify focus** - Earnings, M&A, products, or all news?
6. **Combine with analysis** - Use news findings with technical/fundamental analysis

### For News Researcher
1. **Use Tavily first** - Start with Tavily API search for comprehensive news aggregation
2. **Multi-source verification** - Cross-check Tavily results across multiple sources
3. **Prioritize official sources** - SEC filings, company press releases prioritized over aggregated news
4. **Assess materiality** - Focus on news that could meaningfully impact stock price
5. **Verify timestamps** - Ensure news dates from Tavily results are accurate
6. **Check market reaction** - How did stock price react to news found via Tavily?
7. **Identify patterns** - Look for themes and trends across Tavily search results
8. **Tavily query optimization** - Use specific, targeted queries for better Tavily results

## Outputs & Deliverables

### Primary Output
- **News Timeline** - Chronological list of important news items
- **Sentiment Analysis** - Overall positive/negative/neutral assessment
- **Material News** - News items that could impact stock price >5%
- **Key Catalysts** - Upcoming events that could move stock price

### Secondary Output
- **News Categories** - Breakdown by type (earnings, M&A, products, etc.)
- **Impact Assessment** - How news affects fundamentals and valuation
- **Market Reaction** - How stock price reacted to news
- **Source Verification** - Cross-checked information from multiple sources

### Documentation
- **News Report** - Saved to `reports/{TICKER}_{DATE}/{DATE}_news.md`
- **News Timeline** - Chronological narrative
- **Sentiment Summary** - Overall news sentiment and key themes
- **Catalyst Calendar** - Upcoming events to watch

## Integration with Other Commands

Use `news-search` with:
- **ticker-analysis** - News search is automatically included in comprehensive analysis
- **stock-comparison** - Compare news sentiment across multiple stocks
- **portfolio-analysis** - Review news for all portfolio holdings

## Common Questions

**Q: How does news search work?**
A: Uses Tavily Search API as primary method to search across multiple news sources in real-time. Tavily aggregates results from Bloomberg, Reuters, WSJ, SEC filings, and other credible sources.

**Q: Do I need to configure Tavily API?**
A: The agent will use Tavily when available. If you have Tavily API access, the agent can use it directly. Otherwise, agent will use web search capabilities or you can provide news manually.

**Q: How far back does news search go?**
A: Default is last 30 days, but can be customized (7 days, quarter, full year). Tavily searches can filter by specific time ranges.

**Q: What sources are used?**
A: Primary: Tavily API aggregates from Bloomberg, Reuters, WSJ, CNBC, MarketWatch, SEC filings, Yahoo Finance, and more. Additional: Official company press releases, investor relations pages.

**Q: How do you determine materiality?**
A: News that could impact stock price by >5% is considered material. Tavily results are filtered and prioritized by materiality.

**Q: Can I search for specific news types?**
A: Yes, use --focus parameter (earnings, M&A, products, regulatory, etc.). Tavily can execute targeted searches for specific event types.

**Q: How often should I run news search?**
A: Before making investment decisions, after earnings, or when stock moves unexpectedly. Tavily enables real-time search for latest news.

## Disclaimers

- **Educational Only**: Not financial advice
- **Source Verification**: Always verify information from official sources
- **Timing**: News may be outdated; check for latest developments
- **Market Impact**: News impact on stock prices is unpredictable
- **Past Performance**: Historical news patterns don't guarantee future results
