---
name: performance-metrics
description: Master KPI and OKR design, performance measurement, and operational analytics. Use when defining business metrics, building dashboards, tracking organizational performance, or measuring improvement initiatives.
---

# Performance Metrics & KPIs Skill

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Defining Key Performance Indicators (KPIs) for departments or company
- Designing Objectives and Key Results (OKRs) for strategy execution
- Creating performance dashboards and reporting systems
- Establishing baseline metrics and improvement targets
- Analyzing operational performance data and trends
- Building measurement frameworks for new initiatives
- Designing performance management systems
- Translating strategy into measurable outcomes

## Core Concepts

### KPI vs OKR

**Key Performance Indicators (KPIs)**:
- Operational metrics that measure current performance
- Ongoing metrics tracked continuously
- Establish baselines and targets
- Used for operational management and control
- Example: Customer satisfaction score, on-time delivery %, revenue per employee

**Objectives and Key Results (OKRs)**:
- Strategic goals with measurable results
- Time-bound (typically quarterly)
- Ambitious but achievable targets
- Link individual/team goals to company strategy
- Example: Objective: "Become the #1 choice for enterprise customers"
  - Key Result 1: Win 10 enterprise accounts
  - Key Result 2: Achieve 95%+ customer retention
  - Key Result 3: NPS score of 70+

**Key Differences**:
| Aspect | KPI | OKR |
|--------|-----|-----|
| **Duration** | Ongoing/continuous | Time-bound (quarterly) |
| **Purpose** | Measure current state | Drive strategic change |
| **Ambition** | Realistic/achievable | Stretch goals (70% success is good) |
| **Frequency** | Constant monitoring | Quarterly review |
| **Scope** | Often individual/team | Organization-wide alignment |

### Characteristics of Good Metrics

**SMART Framework**:
- **Specific**: What exactly are we measuring? (not "improve service" but "reduce response time")
- **Measurable**: Can we quantify it? (yes: "5 days" / no: "improve satisfaction")
- **Achievable**: Is it realistic given resources and constraints?
- **Relevant**: Does it matter to business objectives?
- **Time-bound**: By when should we achieve it?

**Additional Qualities**:
- **Actionable**: Can team influence it? (not: "industry growth rate")
- **Leading vs Lagging**:
  - Leading: Predict future outcomes (effort invested, meetings held)
  - Lagging: Measure results (revenue, customer satisfaction)
- **Balanced**: Mix of financial and non-financial metrics
- **Comparable**: Benchmark against competitors or past performance

### Common Operational Metrics

**Efficiency Metrics**:
- **Cycle Time**: How long does a process take? (days)
- **Throughput**: How much can we produce/deliver? (units per month)
- **Labor Productivity**: Output per person (revenue per FTE, items per hour)
- **Cost Per Unit**: What's the cost to deliver? (COGS, cost per transaction)
- **Utilization**: % of capacity being used (85% is often optimal, <70% is waste)
- **First Pass Yield**: % of work completed without rework

**Quality Metrics**:
- **Defect Rate**: % of output with errors or issues
- **Customer Satisfaction (CSAT)**: Survey-based satisfaction score (1-5 or 1-10)
- **Net Promoter Score (NPS)**: "How likely to recommend?" Score: -100 to +100
  - >0 is good, >30 is healthy, >70 is world-class
- **Customer Effort Score (CES)**: "How easy was it?" (1-5 scale)
- **Resolution Time**: How quickly do we resolve customer issues?
- **Rework/Return Rate**: % of deliverables requiring redo

**Financial Metrics**:
- **Revenue Growth**: % increase year-over-year
- **Gross Margin**: (Revenue - COGS) / Revenue (%)
- **Operating Margin**: Operating Income / Revenue (%)
- **Customer Lifetime Value (CLV)**: Total profit from a customer over time
- **Cost Per Acquisition (CAC)**: Cost to acquire one customer
- **CLV/CAC Ratio**: Should be 3:1 or higher for healthy business
- **Cash Runway**: Months of cash remaining at current burn rate

**People Metrics**:
- **Employee Engagement Score**: Annual survey (scale 1-10)
- **Turnover Rate**: % of employees who leave per year (high = problem)
- **Time to Hire**: Days to fill open position
- **Training Hours Per Employee**: Professional development investment
- **Promotion From Within %**: % of leadership filled internally vs. external
- **Absenteeism Rate**: % of days missed due to absence

**Delivery & Execution**:
- **On-Time Delivery %**: % of projects/deliverables completed by deadline
- **Budget Performance**: Actual spend vs. planned (% variance)
- **Sprint Velocity**: # of story points completed per sprint (agile teams)
- **Schedule Adherence**: Actual schedule vs. baseline
- **Critical Bugs**: Number of priority bugs in production

**Customer Metrics**:
- **Customer Acquisition Rate**: New customers per month/quarter
- **Customer Retention/Churn**: % staying vs. leaving
- **Market Share**: % of total addressable market
- **Customer Concentration**: % of revenue from top 10/20 customers (concentration risk)

### OKR Design

**Writing Strong Objectives**:
- Inspirational and motivating
- Qualitative and directional
- Short and memorable
- Time-bound (quarterly or annual)
- Examples:
  - "Become the easiest SaaS platform to implement"
  - "Achieve industry-leading customer loyalty"
  - "Dominate the mid-market segment"

**Writing Key Results**:
- Measurable outcome (quantified)
- 2-4 key results per objective (3 is typical)
- Ambitious (60-70% success rate is target)
- Realistic (achievable with significant effort)
- Examples for "Become #1 in customer experience":
  - KR1: Achieve NPS of 75+ (currently 55)
  - KR2: Reduce support response time to <2 hours (currently 8 hours)
  - KR3: Launch 3 new self-service features

**OKR Cascading**:
- Company-level OKRs set direction
- Department/team OKRs align with company goals
- Individual OKRs support team goals
- Each level contributes to level above
- Balance top-down direction with bottom-up input

### Performance Dashboard Design

**Dashboard Components**:
1. **High-Level Overview** (top of page)
   - 3-5 most critical metrics
   - Current status vs. target
   - Trend (up/down/flat)
   - Year-to-date or quarter-to-date

2. **Detailed Metrics** (by functional area)
   - Revenue metrics (sales, pipeline, forecasts)
   - Operational metrics (efficiency, quality)
   - Customer metrics (satisfaction, retention)
   - People metrics (engagement, retention)

3. **Benchmarks & Context**
   - Target vs. actual
   - Previous period comparison
   - Industry benchmarks or competitor data
   - Alerts for metrics out of range

4. **Drill-Down Capability**
   - Click to see underlying data
   - Segment by product, region, customer, team
   - Root cause analysis capability

**Dashboard Best Practices**:
- Update frequency aligned with decision frequency (real-time for critical, weekly for others)
- Color coding: Green (on target), Yellow (caution), Red (needs action)
- Data quality and validation
- Owner assigned for each metric
- Clear definitions and calculation methods
- Mobile-friendly or accessible format

### Measurement Systems & Data Collection

**Data Sources**:
- **Systems**: Billing, CRM, ERP, HR, product analytics
- **Manual Collection**: Surveys, feedback, observations
- **External**: Market data, competitor information, industry benchmarks
- **Calculated**: Ratios, indices, aggregations

**Data Quality**:
- **Accuracy**: Is the data correct?
- **Completeness**: Is all data captured?
- **Timeliness**: Is it current?
- **Consistency**: Same methodology over time
- **Validation**: Regular audits and reconciliation

**Reporting Cadence**:
- **Daily**: Real-time dashboards for critical metrics
- **Weekly**: Management team reviews
- **Monthly**: Full business reviews and analysis
- **Quarterly**: OKR reviews and strategic planning
- **Annual**: Board reporting and planning

### Analyzing & Acting on Metrics

**Performance Analysis Framework**:
1. **Status Check**: Where are we vs. target?
2. **Trend Analysis**: Are we improving or worsening?
3. **Root Cause**: Why is performance at this level?
4. **Benchmarking**: How do we compare to competitors/industry?
5. **Action Planning**: What will we do to improve?
6. **Accountability**: Who is responsible for improvement?

**Common Analysis Mistakes**:
- **Chasing the wrong metrics** (vanity metrics that don't matter)
- **Too many metrics** (dilutes focus; ideal: 5-10 key metrics)
- **Metrics without context** (numbers without understanding drivers)
- **Lack of ownership** (metrics are nobody's responsibility)
- **Reactive vs. proactive** (responding to results instead of preventing issues)

## References

- Balanced Scorecard methodology
- OKR framework by John Doerr
- Six Sigma and Lean metrics
- Kaplan-Norton Strategy Maps
- Data-driven decision making frameworks
- Agile metrics and velocity tracking
- Industry-specific benchmarking databases
