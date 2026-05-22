---
name: kpi-dashboard-design
description: Design effective KPI dashboards with metrics selection, visualization best practices, and real-time monitoring patterns. Use this skill when building an executive SaaS metrics dashboard tracking MRR, churn, and LTV/CAC ratios; designing an operations center with live service health and request throughput; creating a cohort retention analysis view for a product team; or debugging a dashboard where metrics contradict each other due to inconsistent calculation methodology.
---

# KPI Dashboard Design

Comprehensive patterns for designing effective Key Performance Indicator (KPI) dashboards that drive business decisions.

## When to Use This Skill

- Designing executive dashboards
- Selecting meaningful KPIs
- Building real-time monitoring displays
- Creating department-specific metrics views
- Improving existing dashboard layouts
- Establishing metric governance

## Core Concepts

### 1. KPI Framework

| Level           | Focus            | Update Frequency  | Audience   |
| --------------- | ---------------- | ----------------- | ---------- |
| **Strategic**   | Long-term goals  | Monthly/Quarterly | Executives |
| **Tactical**    | Department goals | Weekly/Monthly    | Managers   |
| **Operational** | Day-to-day       | Real-time/Daily   | Teams      |

### 2. SMART KPIs

```
Specific: Clear definition
Measurable: Quantifiable
Achievable: Realistic targets
Relevant: Aligned to goals
Time-bound: Defined period
```

### 3. Dashboard Hierarchy

```
├── Executive Summary (1 page)
│   ├── 4-6 headline KPIs
│   ├── Trend indicators
│   └── Key alerts
├── Department Views
│   ├── Sales Dashboard
│   ├── Marketing Dashboard
│   ├── Operations Dashboard
│   └── Finance Dashboard
└── Detailed Drilldowns
    ├── Individual metrics
    └── Root cause analysis
```

## Detailed worked examples and patterns

Detailed sections (starting with `## Common KPIs by Department`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Best Practices

### Do's

- **Limit to 5-7 KPIs** - Focus on what matters
- **Show context** - Comparisons, trends, targets
- **Use consistent colors** - Red=bad, green=good
- **Enable drilldown** - From summary to detail
- **Update appropriately** - Match metric frequency

### Don'ts

- **Don't show vanity metrics** - Focus on actionable data
- **Don't overcrowd** - White space aids comprehension
- **Don't use 3D charts** - They distort perception
- **Don't hide methodology** - Document calculations
- **Don't ignore mobile** - Ensure responsive design

## Troubleshooting

### MRR shown on dashboard contradicts finance's number

The most common cause is inconsistent treatment of annual plans. Finance may prorate to a daily rate while the dashboard normalizes to monthly. Align on a single formula and document it directly on the dashboard card:

```sql
-- Explicit formula shown in tooltip / data dictionary
-- Annual plans: divide total contract value by 12
-- Quarterly plans: divide by 3
-- Monthly plans: use as-is
CASE subscription_interval
    WHEN 'monthly'   THEN amount
    WHEN 'quarterly' THEN amount / 3.0
    WHEN 'yearly'    THEN amount / 12.0
END AS normalized_mrr
```

### Dashboard shows green but product team reports users complaining

The dashboard likely tracks system uptime (a lagging indicator) but not user-facing quality metrics. Add customer-perceived metrics alongside infrastructure metrics:

| Infrastructure (green) | User-perceived (add these) |
|---|---|
| API uptime 99.9% | P95 page load time |
| Error rate 0.1% | Task completion rate |
| Queue depth normal | Support ticket volume |

### Retention cohort looks flat — no variation between cohorts

Check whether the cohort query is partitioning by signup month correctly. A common bug is using `created_at::date` instead of `DATE_TRUNC('month', created_at)`, which groups by day and produces cohorts too small to show trends:

```sql
-- Wrong: too granular, cohorts are too small
DATE_TRUNC('day', created_at) AS cohort_date

-- Correct: monthly cohorts
DATE_TRUNC('month', created_at) AS cohort_month
```

### Real-time dashboard hammers the database

A live dashboard refreshing every 10 seconds with complex cohort SQL will degrade production query performance. Separate OLAP workloads from OLTP by writing pre-aggregated metrics to a summary table via a scheduled job, and have the dashboard read from that:

```python
# Scheduled every 5 minutes via cron/Celery
def refresh_mrr_summary():
    conn.execute("""
        INSERT INTO kpi_snapshot (metric, value, snapshot_at)
        SELECT 'mrr', SUM(...), NOW()
        FROM subscriptions WHERE status = 'active'
        ON CONFLICT (metric) DO UPDATE SET value = EXCLUDED.value
    """)
```

### Alert thresholds fire constantly, team ignores them

Static thresholds set once and never reviewed cause alert fatigue. Use dynamic thresholds based on rolling averages so alerts fire only when the metric deviates significantly from its own baseline:

```python
# Alert if current value is > 2 standard deviations from 30-day rolling mean
def is_anomalous(current: float, history: list[float]) -> bool:
    mean = statistics.mean(history)
    stdev = statistics.stdev(history)
    return abs(current - mean) > 2 * stdev
```

## Related Skills

- `data-storytelling` - Turn dashboard findings into narratives that drive executive decisions
