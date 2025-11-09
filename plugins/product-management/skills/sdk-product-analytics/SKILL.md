---
name: sdk-product-analytics
description: Master Claude SDK for automated product analytics, user behavior analysis, A/B testing automation, and data-driven decision making. Covers SDK tools for metric tracking, cohort analysis, funnel optimization, and automated reporting. Use when analyzing product metrics, running experiments, building analytics dashboards, or automating product insights generation.
---

# Claude SDK Product Analytics Automation

Master the Claude SDK to build automated product analytics systems with real-time metric tracking, intelligent experimentation, and data-driven product decision making.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Automating product metrics tracking and reporting
- Building real-time analytics dashboards
- Orchestrating A/B testing and experimentation
- Creating automated cohort analysis pipelines
- Developing user behavior analysis systems
- Integrating product analytics APIs (Mixpanel, Amplitude, etc.)
- Building funnel optimization workflows
- Creating automated insight generation
- Developing retention analysis automation
- Building product health monitoring systems

## Core Concepts

### 1. Claude SDK Fundamentals for Product Analytics

**Available SDK Tools for Analytics**

The Claude SDK provides powerful tools for product analytics automation:

**WebFetch** - Fetch analytics data from external sources
```python
# Fetch user metrics from analytics API
WebFetch(
    url="https://api.analytics.com/metrics?metric=DAU&period=7d",
    prompt="Extract daily active users for last 7 days with trend"
)
```

**Task (Multi-Agent)** - Orchestrate specialized analysis
```python
# Delegate to specialized agents
Task(
    subagent_type="general-purpose",
    description="Analyze user retention",
    prompt="Analyze cohort retention data and identify drop-off points"
)
```

**Bash** - Execute analytics scripts
```bash
# Run Python analytics analysis
python analyze_user_behavior.py --cohort 2025-11 --output reports/
```

**Read/Write** - File operations for data and reports
```python
# Read analytics data
Read(file_path="/data/user_events.json")

# Write analysis report
Write(
    file_path="/reports/product_metrics_2025-11-09.md",
    content=analytics_report
)
```

**Key SDK Capabilities for Product Analytics:**

1. **Automated Metric Tracking** - Continuous monitoring of key product metrics
2. **Real-Time Data Access** - Fetch live analytics from APIs
3. **Multi-Agent Analysis** - Coordinate user research, data science, product insights
4. **Experiment Orchestration** - Manage A/B tests and feature flags
5. **Report Automation** - Generate weekly/monthly product reports
6. **Alert Systems** - Notify when metrics breach thresholds

### 2. Real-Time Product Metrics Tracking

**Core Product Metrics Collection**

Use WebFetch to retrieve product metrics from analytics platforms:

```markdown
## Example: Fetch DAU/MAU Metrics

**Task:** Get current user engagement metrics

**SDK Workflow:**
```python
# Fetch DAU
WebFetch(
    url="https://api.mixpanel.com/api/2.0/engage",
    prompt="Get daily active users for last 30 days"
)

# Fetch MAU
WebFetch(
    url="https://api.mixpanel.com/api/2.0/engage",
    prompt="Get monthly active users for current month"
)

# Calculate DAU/MAU ratio (stickiness)
Bash(command="python scripts/calculate_stickiness.py --dau data/dau.json --mau data/mau.json")
```

**Output:**
```
Product Engagement Metrics - 2025-11-09

DAU: 12,450 users (+3.2% vs yesterday)
MAU: 48,200 users (+5.1% vs last month)
DAU/MAU: 25.8% (Stickiness ratio)

Trend: ↑ Growing engagement
Benchmark: 25.8% vs industry avg 20% (Strong)
Insight: Product stickiness above industry average
```
```

**Funnel Analysis Automation**

Track conversion through product funnels:

```markdown
## Automated Funnel Analysis

**Signup Funnel:** Visit → Signup → Activate → Subscribe

**SDK Workflow:**
```python
# Fetch funnel data
WebFetch(
    url="https://api.amplitude.com/api/2/funnels",
    prompt="Get signup funnel conversion rates for last 7 days"
)

# Analyze drop-off points
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze signup funnel:
    1. Identify highest drop-off stage
    2. Compare to previous week
    3. Segment by user source (organic, paid, referral)
    4. Recommend optimization experiments
    """
)
```

**Output:**
```
Signup Funnel Analysis - Week of 2025-11-03

Conversion Rates:
1. Visit → Signup: 15.2% (-1.3% vs last week) 🔴
2. Signup → Activate: 68.5% (+2.1% vs last week) ✅
3. Activate → Subscribe: 12.8% (+0.4% vs last week) ✅

Critical Issue: Visit → Signup conversion declining

Segment Analysis:
- Organic: 18.5% (above avg)
- Paid: 12.1% (below avg, worsening)
- Referral: 22.3% (above avg)

Root Cause Hypothesis:
- Paid traffic quality declining (wrong targeting?)
- Landing page changes affecting paid users

Recommended Experiments:
1. A/B test: Restore old landing page for paid traffic
2. Analyze: Review ad targeting parameters
3. Test: Personalized landing pages by source
```
```

**Cohort Retention Analysis**

Automate cohort retention tracking:

```markdown
## Cohort Retention Automation

**Goal:** Track user retention by signup cohort

**SDK Workflow:**
```python
# Fetch cohort retention data
WebFetch(
    url="https://api.mixpanel.com/api/2.0/cohorts",
    prompt="Get retention data for last 12 monthly cohorts (Month 0 through Month 6)"
)

# Process retention curves
Bash(command="python scripts/analyze_cohorts.py --data data/cohorts.json --output reports/retention.md")
```

**analyze_cohorts.py:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load cohort data
cohorts = pd.read_json("data/cohorts.json")

# Calculate retention by month
retention_table = cohorts.pivot_table(
    index='cohort',
    columns='month',
    values='retention_rate'
)

# Identify best/worst cohorts
best_cohort = retention_table.iloc[:, 3].idxmax()  # Month 3 retention
worst_cohort = retention_table.iloc[:, 3].idxmin()

# Analyze trends
improving = (retention_table.iloc[-3:, 3].mean() >
             retention_table.iloc[:3, 3].mean())

print(f"Best cohort: {best_cohort}")
print(f"Worst cohort: {worst_cohort}")
print(f"Trend: {'Improving' if improving else 'Declining'}")
```

**Output:**
```
Cohort Retention Analysis

Retention Rates by Cohort:
| Cohort    | M0   | M1   | M2   | M3   | M6   |
|-----------|------|------|------|------|------|
| 2025-05   | 100% | 45%  | 32%  | 28%  | 22%  |
| 2025-06   | 100% | 48%  | 35%  | 30%  | 24%  |
| 2025-07   | 100% | 52%  | 38%  | 33%  | 27%  | ← Best
| 2025-08   | 100% | 50%  | 36%  | 31%  | -    |
| 2025-09   | 100% | 46%  | 33%  | 27%  | -    | ← Worst
| 2025-10   | 100% | 51%  | 37%  | -    | -    |
| 2025-11   | 100% | 49%  | -    | -    | -    |

Key Insights:
✅ Retention improving over time (M3: 28% → 31% avg)
✅ July cohort significantly outperformed (new onboarding?)
🔴 September cohort underperformed (back-to-school distraction?)

Recommendations:
1. Analyze July cohort: What drove higher retention?
2. Replicate successful patterns from July
3. Investigate September drop-off causes
```
```

### 3. A/B Testing Automation with SDK

**Experiment Orchestration**

Automate A/B test analysis and decision making:

```markdown
## A/B Test Analysis Automation

**Experiment:** New onboarding flow vs. control

**SDK Workflow:**

**Step 1: Fetch Experiment Data**
```python
# Get experiment results
WebFetch(
    url="https://api.optimizely.com/v2/experiments/12345/results",
    prompt="Get A/B test results for onboarding experiment: conversion rates, sample sizes, statistical significance"
)
```

**Step 2: Statistical Analysis**
```bash
# Run statistical significance test
Bash(command="python scripts/ab_test_analysis.py --experiment data/experiment_12345.json")
```

**ab_test_analysis.py:**
```python
from scipy import stats
import numpy as np

# Load experiment data
control = {'conversions': 850, 'visitors': 5000}
variant = {'conversions': 975, 'visitors': 5000}

# Calculate conversion rates
control_rate = control['conversions'] / control['visitors']
variant_rate = variant['conversions'] / variant['visitors']

# Chi-square test
contingency = [[control['conversions'], control['visitors'] - control['conversions']],
               [variant['conversions'], variant['visitors'] - variant['conversions']]]
chi2, p_value = stats.chi2_contingency(contingency)[:2]

# Calculate lift
lift = (variant_rate - control_rate) / control_rate

# Statistical significance
significant = p_value < 0.05
confidence = (1 - p_value) * 100

print(f"Control: {control_rate:.2%}")
print(f"Variant: {variant_rate:.2%}")
print(f"Lift: {lift:+.2%}")
print(f"P-value: {p_value:.4f}")
print(f"Significant: {significant} ({confidence:.1f}% confidence)")
```

**Step 3: Decision Recommendation**
```python
# Generate recommendation
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze A/B test results:
    1. Evaluate statistical significance
    2. Calculate business impact (revenue, retention)
    3. Check for segment differences (mobile vs desktop)
    4. Recommend: Ship, Iterate, or Kill
    5. Draft rollout plan if shipping
    """
)
```

**Output:**
```
A/B Test Results - Onboarding Experiment

Test Details:
- Experiment: New onboarding flow
- Duration: 14 days
- Sample: 10,000 users (5,000 per variant)

Results:
Control: 17.0% activation rate
Variant: 19.5% activation rate
Lift: +14.7% ✅
P-value: 0.0023 (99.8% confidence) ✅

Statistical Significance: YES

Business Impact:
- +2.5pp activation rate
- Expected +125 activations per month
- Revenue impact: +$37,500/month (at $300 LTV)
- Implementation cost: $15,000 one-time

ROI: 2.5x in first month, 25x annually

Segment Analysis:
- Mobile: +18.2% lift (p=0.003) ✅
- Desktop: +11.5% lift (p=0.041) ✅
- Both segments significant

Recommendation: SHIP
- High statistical confidence
- Strong business impact
- Works across segments
- Positive user feedback

Rollout Plan:
1. Week 1: Ship to 25% of users (monitor)
2. Week 2: Ship to 50% of users
3. Week 3: Ship to 100% (full rollout)
```
```

### 4. Automated Product Health Monitoring

**Product Health Dashboard Automation**

Build real-time product health monitoring:

```markdown
## Product Health Monitoring System

**Key Metrics to Monitor:**
- DAU, MAU, Stickiness
- Signup conversion rate
- Activation rate
- Retention (D1, D7, D30)
- Churn rate
- NPS score

**SDK Implementation:**
```python
# monitor_product_health.py
import time
import json

# Define thresholds
THRESHOLDS = {
    'dau_drop': -0.05,  # -5% DAU change
    'conversion_drop': -0.02,  # -2pp conversion
    'activation_drop': -0.03,  # -3pp activation
}

while True:
    # Fetch latest metrics
    metrics = {}

    metrics['dau'] = WebFetch(
        url="https://api.analytics.com/metrics/dau",
        prompt="Get today's DAU vs yesterday"
    )

    metrics['conversion'] = WebFetch(
        url="https://api.analytics.com/funnels/signup",
        prompt="Get signup conversion rate today vs 7-day avg"
    )

    # Check for alerts
    alerts = []

    if metrics['dau']['change'] < THRESHOLDS['dau_drop']:
        alerts.append({
            'severity': 'HIGH',
            'metric': 'DAU',
            'change': metrics['dau']['change'],
            'message': f"DAU dropped {metrics['dau']['change']:.1%}"
        })

    # If alerts, analyze and notify
    if alerts:
        # Deep dive analysis
        Task(
            subagent_type="general-purpose",
            prompt=f"Product health alert triggered: {alerts}. Analyze root causes and recommend immediate actions."
        )

        # Send notification
        Bash(command="python scripts/send_alert.py --alerts '{json.dumps(alerts)}'")

    time.sleep(3600)  # Check every hour
```

**Alert Example:**
```
🚨 Product Health Alert - 2025-11-09 10:00

Metric: DAU
Current: 11,850 users
Yesterday: 12,450 users
Change: -4.8% 🔴

Severity: HIGH (approaching -5% threshold)

Potential Causes:
1. Weekend effect (today is Saturday)
2. Recent app update causing crashes?
3. Outage in key market/region?

Investigation Steps:
1. Check error logs for spike in crashes ✓
2. Review app store ratings for complaints ✓
3. Analyze by region (is one market down?) ✓

Findings:
- Error rate spiked 10x in last 6 hours
- Android app version 2.5.1 has critical bug
- 85% of errors from Android users

Immediate Actions:
1. Roll back Android app to 2.5.0
2. Notify affected users via push notification
3. Fast-track bug fix for 2.5.2
4. Monitor DAU recovery over next 24h
```
```

### 5. User Segmentation and Behavior Analysis

**Automated Segmentation Analysis**

Use SDK to identify and analyze user segments:

```markdown
## User Segmentation Automation

**Goal:** Identify distinct user behavior segments

**SDK Workflow:**

**Step 1: Collect User Behavior Data**
```python
# Fetch user event data
WebFetch(
    url="https://api.amplitude.com/api/2/events",
    prompt="Get user event data for last 30 days: login frequency, feature usage, session duration"
)

# Save for analysis
Write(
    file_path="data/user_events.json",
    content=user_events
)
```

**Step 2: Clustering Analysis**
```bash
# Run K-means clustering
Bash(command="python scripts/user_segmentation.py --data data/user_events.json --clusters 4")
```

**user_segmentation.py:**
```python
from sklearn.cluster import KMeans
import pandas as pd

# Load user data
users = pd.read_json("data/user_events.json")

# Feature engineering
features = pd.DataFrame({
    'login_frequency': users.groupby('user_id')['login'].sum(),
    'session_duration': users.groupby('user_id')['session_time'].mean(),
    'feature_usage': users.groupby('user_id')['features_used'].nunique(),
})

# K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
features['segment'] = kmeans.fit_predict(features)

# Analyze segments
segment_profiles = features.groupby('segment').agg({
    'login_frequency': 'mean',
    'session_duration': 'mean',
    'feature_usage': 'mean',
}).round(2)

print(segment_profiles)

# Save results
features.to_json("data/user_segments.json")
```

**Step 3: Segment Profiling**
```python
# Profile each segment
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze user segments:
    1. Name each segment based on behavior
    2. Calculate segment sizes and revenue
    3. Identify growth opportunities per segment
    4. Recommend targeted strategies
    """
)
```

**Output:**
```
User Segmentation Analysis

Segment 1: Power Users (12% of users, 45% of revenue)
- Login frequency: 24x/month
- Session duration: 18 minutes
- Feature usage: 15 features/month
- Characteristics: High engagement, use advanced features
- Strategy: Upsell premium tier, beta test new features

Segment 2: Regular Users (35% of users, 38% of revenue)
- Login frequency: 12x/month
- Session duration: 8 minutes
- Feature usage: 7 features/month
- Characteristics: Consistent usage, core feature focus
- Strategy: Increase feature adoption, prevent churn

Segment 3: Casual Users (41% of users, 15% of revenue)
- Login frequency: 3x/month
- Session duration: 4 minutes
- Feature usage: 3 features/month
- Characteristics: Infrequent, basic usage only
- Strategy: Activation campaigns, habit building

Segment 4: At-Risk Users (12% of users, 2% of revenue)
- Login frequency: 0.5x/month
- Session duration: 2 minutes
- Feature usage: 1 feature/month
- Characteristics: Barely active, high churn risk
- Strategy: Win-back campaigns, identify pain points

Recommended Actions:
1. Power Users: Launch premium tier ($99/month)
2. Regular Users: Email campaign showcasing underused features
3. Casual Users: In-app nudges to build daily habits
4. At-Risk: Survey + special offer to re-engage
```
```

### 6. Feature Adoption and Usage Analysis

**Feature Performance Tracking**

Automate feature adoption analysis:

```markdown
## Feature Adoption Automation

**New Feature:** Collaborative workspaces (launched 30 days ago)

**SDK Workflow:**

**Step 1: Fetch Adoption Data**
```python
# Get feature usage data
WebFetch(
    url="https://api.mixpanel.com/api/2.0/events",
    prompt="Get usage of 'collaborative_workspace' feature: users, frequency, retention"
)
```

**Step 2: Calculate Adoption Metrics**
```bash
# Analyze feature adoption
Bash(command="python scripts/feature_adoption.py --feature collaborative_workspace --launch-date 2025-10-10")
```

**feature_adoption.py:**
```python
import pandas as pd
from datetime import datetime, timedelta

# Load feature usage data
usage = pd.read_json("data/feature_usage.json")

# Calculate adoption rate
total_users = 48200  # MAU
feature_users = usage['user_id'].nunique()
adoption_rate = feature_users / total_users

# Calculate retention
day_1_users = usage[usage['day'] == 1]['user_id'].nunique()
day_7_users = len(set(usage[usage['day'] == 1]['user_id']) &
                   set(usage[usage['day'] >= 7]['user_id']))
day_7_retention = day_7_users / day_1_users if day_1_users > 0 else 0

# Calculate frequency
avg_uses_per_user = usage.groupby('user_id')['event'].count().mean()

# Growth trajectory
daily_new_users = usage.groupby('date')['user_id'].nunique()
growth_rate = (daily_new_users.iloc[-7:].mean() /
               daily_new_users.iloc[:7].mean()) - 1

print(f"Adoption rate: {adoption_rate:.1%}")
print(f"Day 7 retention: {day_7_retention:.1%}")
print(f"Avg uses per user: {avg_uses_per_user:.1f}")
print(f"Growth rate: {growth_rate:+.1%}")
```

**Step 3: Insights and Recommendations**
```python
# Analyze adoption patterns
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze feature adoption:
    1. Compare to historical feature launches
    2. Identify user segments with highest/lowest adoption
    3. Find blockers preventing adoption
    4. Recommend growth tactics
    """
)
```

**Output:**
```
Feature Adoption Analysis - Collaborative Workspaces

Launch Date: 2025-10-10 (30 days ago)

Adoption Metrics:
- Adoption rate: 18.5% (8,917 / 48,200 MAU)
- Day 7 retention: 45.2%
- Avg uses per user: 12.3 times/month
- Growth: +15.2% week-over-week

vs Historical Feature Launches:
- Adoption: 18.5% vs 22.1% avg (Below avg) 🟡
- Retention: 45.2% vs 38.5% avg (Above avg) ✅
- Frequency: 12.3 vs 8.7 avg (Above avg) ✅

Insights:
✅ Users who try it love it (high retention & frequency)
🔴 Adoption lower than expected (discovery issue?)

Segment Analysis:
- Team accounts: 42% adoption (strong)
- Individual accounts: 8% adoption (weak)
- Paid users: 35% adoption
- Free users: 12% adoption

Blockers:
1. Feature buried in settings (low discoverability)
2. No onboarding tutorial (unclear value prop)
3. Free tier limits (only 2 collaborators)

Recommendations:
1. Move to main navigation (increase visibility)
2. Add onboarding flow with use cases
3. Increase free tier to 5 collaborators
4. In-app promotion campaign

Projected Impact:
- Adoption: 18.5% → 32% (+13.5pp)
- Additional users: +6,500
- Revenue impact: +$195K/month (premium conversions)
```
```

### 7. NPS and User Feedback Analysis

**Automated NPS Tracking and Analysis**

Monitor and analyze user satisfaction:

```markdown
## NPS Automation and Sentiment Analysis

**SDK Workflow:**

**Step 1: Fetch NPS Survey Responses**
```python
# Get NPS data
WebFetch(
    url="https://api.delighted.com/v1/survey_responses.json",
    prompt="Get NPS survey responses from last 30 days: scores, comments, user segments"
)
```

**Step 2: Calculate NPS Score**
```bash
# Calculate NPS
Bash(command="python scripts/calculate_nps.py --data data/nps_responses.json")
```

**calculate_nps.py:**
```python
import pandas as pd

# Load NPS responses
responses = pd.read_json("data/nps_responses.json")

# Categorize respondents
responses['category'] = responses['score'].apply(lambda x:
    'Promoter' if x >= 9 else ('Passive' if x >= 7 else 'Detractor'))

# Calculate NPS
promoters = (responses['category'] == 'Promoter').sum()
detractors = (responses['category'] == 'Detractor').sum()
total = len(responses)

nps = ((promoters - detractors) / total) * 100

print(f"NPS: {nps:.0f}")
print(f"Promoters: {promoters / total:.1%}")
print(f"Passives: {((total - promoters - detractors) / total):.1%}")
print(f"Detractors: {detractors / total:.1%}")
```

**Step 3: Sentiment Analysis of Comments**
```python
# Analyze qualitative feedback
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze NPS comments:
    1. Categorize feedback themes (features, support, pricing, UX)
    2. Identify top praise points (what users love)
    3. Identify top pain points (what users hate)
    4. Extract actionable product improvements
    5. Segment by user type (promoter vs detractor themes)
    """
)
```

**Output:**
```
NPS Analysis - October 2025

Overall NPS: 42 (Good range: 30-50)

Distribution:
- Promoters (9-10): 55% (↑ from 52% last month)
- Passives (7-8): 32%
- Detractors (0-6): 13% (↓ from 16% last month)

Trend: ↑ Improving (+3 points vs last month)

Promoter Themes (What Users Love):
1. "Easy to use" (mentioned 142 times)
2. "Great collaboration features" (mentioned 89 times)
3. "Responsive support team" (mentioned 76 times)
4. "Time-saving automation" (mentioned 68 times)

Detractor Themes (Pain Points):
1. "Mobile app bugs" (mentioned 45 times) 🔴
2. "Expensive pricing" (mentioned 38 times)
3. "Missing integrations" (mentioned 32 times)
4. "Slow loading times" (mentioned 28 times)

Actionable Insights:

Critical Issues:
1. Mobile bugs: 35% of detractors mention mobile issues
   → Priority: Fix top 5 mobile bugs this sprint

2. Pricing concerns: 29% of detractors cite cost
   → Consider: Entry-level tier at $29/month

3. Integration gaps: Slack, Salesforce top requests
   → Roadmap: Add in Q1 2026

Growth Opportunities:
1. Collaboration features driving promoters
   → Double down: Enhance team features
   → Marketing: Feature in campaigns

2. Support quality differentiator
   → Maintain: Don't cut support team
   → Promote: Highlight in sales conversations
```
```

## References

### SDK Tools for Product Analytics

| Tool | Purpose | Analytics Use Cases |
|------|---------|---------------------|
| **WebFetch** | Fetch external data | Mixpanel/Amplitude API, user feedback, market data |
| **Task** | Multi-agent coordination | Complex analysis, experiment evaluation, segmentation |
| **Bash** | Execute scripts | Python/R analysis, ML models, data processing |
| **Read** | Read files | User data, event logs, experiment configs |
| **Write** | Write files | Reports, dashboards, analysis results |
| **Grep** | Search code/data | Find events, search logs, query data |

### Analytics Integration Patterns

**Pattern 1: Real-Time Metric Monitoring**
```
WebFetch (analytics API) → Compare (thresholds) → Task (analyze) → Bash (alert)
```

**Pattern 2: Automated A/B Testing**
```
WebFetch (experiment data) → Bash (statistics) → Task (recommendation) → Write (report)
```

**Pattern 3: Weekly Product Report**
```
WebFetch (metrics) → Bash (calculate) → Task (insights) → Write (report) → Bash (email)
```

**Pattern 4: User Segmentation**
```
WebFetch (user data) → Bash (clustering) → Task (profiling) → Write (segments)
```

### Best Practices

✅ **Automate recurring reports** - Weekly/monthly product reports on autopilot
✅ **Set up alerts** - Monitor critical metrics, alert on anomalies
✅ **Combine quantitative + qualitative** - Metrics + user feedback = complete picture
✅ **Segment everything** - Aggregate metrics hide important segment differences
✅ **Track trends over time** - Single data points misleading, trends reveal truth
✅ **Statistical rigor** - Use proper statistical tests for A/B testing
✅ **Act on insights** - Analysis without action is wasted effort

### Common Pitfalls to Avoid

❌ **Vanity metrics** - Track actionable metrics (retention) not vanity (signups)
❌ **Cherry-picking data** - Look at full picture, not just favorable segments
❌ **Ignoring statistical significance** - Don't ship experiments without significance
❌ **Over-segmentation** - Too many segments = small sample sizes, noise
❌ **Analysis paralysis** - Perfect data doesn't exist, make decisions with what you have
❌ **No context** - Compare to benchmarks, historical data, competitors
