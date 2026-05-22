# startup-financial-modeling — detailed sections

## Step-by-Step Process

### Step 1: Define Business Model

Clarify revenue model and pricing.

**SaaS Model:**

- Subscription pricing tiers
- Annual vs. monthly contracts
- Free trial or freemium approach
- Expansion revenue strategy

**Marketplace Model:**

- GMV projections
- Take rate (% of transactions)
- Buyer and seller economics
- Transaction frequency

**Transactional Model:**

- Transaction volume
- Revenue per transaction
- Frequency and seasonality

### Step 2: Build Revenue Projections

Use cohort-based methodology for accuracy.

**Monthly Customer Acquisition:**
Define new customers acquired each month.

**Retention Curve:**
Model customer retention over time.

**Typical SaaS Retention:**

- Month 1: 100%
- Month 3: 90%
- Month 6: 85%
- Month 12: 75%
- Month 24: 70%

**Revenue Calculation:**
For each cohort, calculate retained customers × ARPU for each month.

### Step 3: Model Cost Structure

Break down costs by category and behavior.

**Fixed vs. Variable:**

- Fixed: Salaries, software, rent
- Variable: Hosting, payment processing, support

**Scaling Assumptions:**

- COGS as % of revenue
- S&M as % of revenue (CAC payback)
- R&D growth rate
- G&A as % of total expenses

### Step 4: Create Hiring Plan

Model headcount growth by role and department.

**Inputs:**

- Starting headcount
- Hiring velocity by role
- Fully-loaded compensation by role
- Benefits and taxes (typically 1.3-1.4x salary)

**Example:**

```
Engineer: $150K salary × 1.35 = $202K fully-loaded
Sales Rep: $100K OTE × 1.30 = $130K fully-loaded
```

### Step 5: Project Cash Flow

Calculate monthly cash position and runway.

**Monthly Cash Flow:**

```
Beginning Cash
+ Revenue Collected (consider payment terms)
- Operating Expenses Paid
- CapEx
= Ending Cash
```

**Runway Calculation:**

```
If Ending Cash < 0:
  Funding Need = Negative Cash Balance
  Runway = 0
Else:
  Runway = Ending Cash / Average Monthly Burn
```

### Step 6: Calculate Key Metrics

Track metrics that matter for stage.

**Revenue Metrics:**

- MRR / ARR
- Growth rate (MoM, YoY)
- Revenue by segment or cohort

**Unit Economics:**

- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- CAC Payback Period
- LTV / CAC Ratio

**Efficiency Metrics:**

- Burn multiple (Net Burn / Net New ARR)
- Magic number (Net New ARR / S&M Spend)
- Rule of 40 (Growth % + Profit Margin %)

**Cash Metrics:**

- Monthly burn rate
- Runway (months)
- Cash efficiency

### Step 7: Scenario Analysis

Create three scenarios with different assumptions.

**Variable Assumptions:**

- Customer acquisition rate (±30%)
- Churn rate (±20%)
- Average contract value (±15%)
- CAC (±25%)

**Fixed Assumptions:**

- Pricing structure
- Core operating expenses
- Hiring plan (adjust timing, not roles)
