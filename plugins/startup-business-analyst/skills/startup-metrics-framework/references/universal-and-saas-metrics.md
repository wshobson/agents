## Universal Startup Metrics

### Revenue Metrics

**MRR (Monthly Recurring Revenue)**

```
MRR = Σ (Active Subscriptions × Monthly Price)
```

**ARR (Annual Recurring Revenue)**

```
ARR = MRR × 12
```

**Growth Rate**

```
MoM Growth = (This Month MRR - Last Month MRR) / Last Month MRR
YoY Growth = (This Year ARR - Last Year ARR) / Last Year ARR
```

**Target Benchmarks:**

- Seed stage: 15-20% MoM growth
- Series A: 10-15% MoM growth, 3-5x YoY
- Series B+: 100%+ YoY (Rule of 40)

### Unit Economics

**CAC (Customer Acquisition Cost)**

```
CAC = Total S&M Spend / New Customers Acquired
```

Include: Sales salaries, marketing spend, tools, overhead

**LTV (Lifetime Value)**

```
LTV = ARPU × Gross Margin% × (1 / Churn Rate)
```

Simplified:

```
LTV = ARPU × Average Customer Lifetime × Gross Margin%
```

**LTV:CAC Ratio**

```
LTV:CAC = LTV / CAC
```

**Benchmarks:**

- LTV:CAC > 3.0 = Healthy
- LTV:CAC 1.0-3.0 = Needs improvement
- LTV:CAC < 1.0 = Unsustainable

**CAC Payback Period**

```
CAC Payback = CAC / (ARPU × Gross Margin%)
```

**Benchmarks:**

- < 12 months = Excellent
- 12-18 months = Good
- > 24 months = Concerning

### Cash Efficiency Metrics

**Burn Rate**

```
Monthly Net Burn = Monthly Expenses - Monthly Revenue
```

Positive net burn means the business is losing cash (typical early-stage).

**Runway**

```
Runway (months) = Cash Balance / Positive Monthly Net Burn
```

**Target:** Always maintain 12-18 months runway

When net burn is zero or negative, this formula has no finite burn-based runway; report break-even or cash generation instead of dividing by zero or reporting negative months.

**Burn Multiple**

```
Quarterly Burn Multiple = Total Net Burn During Quarter / Net New ARR Added During Quarter
```

Sum the three monthly net-burn amounts for the numerator. The denominator is the change in annual recurring revenue over that same quarter (ending ARR minus starting ARR); do not substitute monthly revenue or annualize the quarterly burn again. Report the ratio only when net new ARR is positive. See [Craft Ventures' quarterly example](https://www.craftventures.com/articles/the-burn-multiple).

**Benchmarks:**

- < 1.0 = Exceptional efficiency
- 1.0-1.5 = Good
- 1.5-2.0 = Acceptable
- > 2.0 = Inefficient

Lower is better (spending less to generate ARR)

## SaaS Metrics

### Revenue Composition

**New MRR**
New customers × ARPU

**Expansion MRR**
Upsells and cross-sells from existing customers

**Contraction MRR**
Downgrades from existing customers

**Churned MRR**
Lost customers

**Net New MRR Formula:**

```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

### Retention Metrics

**Logo Retention**

```
Logo Retention = (Customers End - New Customers) / Customers Start
```

**Dollar Retention (NDR - Net Dollar Retention)**

```
NDR = (ARR Start + Expansion - Contraction - Churn) / ARR Start
```

**Benchmarks:**

- NDR > 120% = Best-in-class
- NDR 100-120% = Good
- NDR < 100% = Needs work

**Gross Retention**

```
Gross Retention = (ARR Start - Churn - Contraction) / ARR Start
```

**Benchmarks:**

- > 90% = Excellent
- 85-90% = Good
- < 85% = Concerning

### SaaS-Specific Metrics

**Magic Number**

```
Magic Number = Net New ARR (quarter) / S&M Spend (prior quarter)
```

**Benchmarks:**

- > 0.75 = Efficient, ready to scale
- 0.5-0.75 = Moderate efficiency
- < 0.5 = Inefficient, don't scale yet

**Rule of 40**

```
Rule of 40 = Revenue Growth Rate% + Profit Margin%
```

**Benchmarks:**

- > 40% = Excellent
- 20-40% = Acceptable
- < 20% = Needs improvement

**Example:**
50% growth + (10%) margin = 40% ✓

**Quick Ratio**

```
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
```

**Benchmarks:**

- > 4.0 = Healthy growth
- 2.0-4.0 = Moderate
- < 2.0 = Churn problem
