---
name: deal-structuring
description: Enterprise deal structuring frameworks including pricing models, contract terms, payment structures, and multi-year agreements. Use when structuring deals, negotiating contracts, or designing pricing proposals.
---

# Deal Structuring

## When to Use This Skill

- Structuring enterprise pricing proposals
- Designing multi-year agreements
- Negotiating payment terms
- Creating volume discount structures
- Balancing risk and reward in contracts
- Optimizing deal economics

## Pricing Models

### 1. Subscription (SaaS Model)

**Annual Subscription**:
- Fixed annual fee for defined usage tier
- Predictable revenue for vendor, predictable cost for customer
- Typical discount: 10-15% vs. monthly

**Example**:
```
Tier 1: 0-100 users @ $50/user/month = $5K/month or $51K/year (15% discount)
Tier 2: 101-500 users @ $40/user/month
Tier 3: 500+ users @ $30/user/month
```

**Pros**: Predictable revenue, easier forecasting
**Cons**: Doesn't scale with usage

### 2. Consumption-Based (Utility Model)

**Pay-As-You-Go**:
- Usage-based pricing (compute hours, storage GB, API calls)
- Scales with customer growth
- Aligns cost with value

**Example**:
```
VK Kubernetes:
- Control Plane: Free
- Worker Nodes: $0.05/hour per vCPU
- Storage: $0.10/GB/month

Monthly usage: 100 vCPUs × 730 hours × $0.05 = $3,650/month
```

**Pros**: Low barrier to entry, scales with usage
**Cons**: Unpredictable costs for customer, revenue volatility

### 3. Committed Spend

**Annual Commit with Drawdown**:
- Customer commits to $X annually
- Draws down from credit pool as they consume
- Discounts based on commit level

**Example**:
```
Commit $500K annually → 20% discount on all services
Unused credits: Rollover 25% to next year or lose
Overage: Pay at standard rates
```

**Pros**: Predictable revenue, encourages deeper usage
**Cons**: Requires customer budget commitment

### 4. Enterprise License Agreement (ELA)

**Unlimited Usage for Fixed Fee**:
- Flat fee for unlimited use of product portfolio
- Typical for large strategic accounts
- 3-5 year terms

**Example**:
```
$2M/year for unlimited use of VK Cloud products
- All compute, storage, managed services included
- Support and training included
- Excludes: Professional services, premium support
```

**Pros**: Simple, predictable, encourages broad adoption
**Cons**: Risk of underutilization or overuse

### 5. Hybrid Models

**Base + Overage**:
- Base subscription + usage-based overage
- Combines predictability with flexibility

**Example**:
```
Base: $10K/month for 10TB storage + 100 vCPUs
Overage: $0.15/GB over 10TB, $0.06/vCPU-hour over 100 vCPUs
```

**Ramp Deal**:
- Lower Year 1 pricing, higher Year 2-3
- Eases budget constraints, locks in multi-year

**Example**:
```
Year 1: $300K (50% discount)
Year 2: $500K (standard pricing)
Year 3: $600K (20% growth)
Total: $1.4M over 3 years
```

## Volume Discounting

### Tiered Discounts

**Usage Tiers**:
```
Tier 1: $0-$100K ARR → 0% discount (list price)
Tier 2: $100K-$500K ARR → 10% discount
Tier 3: $500K-$1M ARR → 20% discount
Tier 4: $1M+ ARR → 25-30% discount (negotiated)
```

### Multi-Year Discounts

**Term-Based Pricing**:
```
1-year: $500K/year (list price)
2-year: $450K/year (10% discount) = $900K total
3-year: $425K/year (15% discount) = $1,275K total
```

**Calculation**: Longer commitment = lower annual cost

### Prepayment Discounts

**Payment Terms Impact**:
```
Monthly arrears: $50K/month = $600K/year (list)
Quarterly prepay: $145K/quarter = $580K/year (3% discount)
Annual prepay: $510K/year (15% discount)
```

## Payment Terms

### Standard Terms

**Net 30**: Payment due 30 days after invoice
**Net 60**: Payment due 60 days (for larger enterprises)
**Net 90**: Payment due 90 days (strategic accounts only)

### Prepayment Options

**Annual Prepay**: Full year upfront (10-15% discount)
**Quarterly Prepay**: Quarterly in advance (5% discount)
**Monthly Arrears**: Pay at end of month (no discount)

### Payment Structure Examples

**Option 1 - Annual Prepay**:
- $510K upfront on Jan 1
- 15% discount vs. monthly
- Customer gets budget certainty

**Option 2 - Quarterly Prepay**:
- $145K per quarter (Jan, Apr, Jul, Oct)
- 3% discount vs. monthly
- Balance between cash flow and discount

**Option 3 - Monthly Arrears**:
- $50K at end of each month
- No discount
- Pay-as-you-go flexibility

## Contract Terms

### Contract Duration

**1-Year**: Standard, least commitment risk
**2-Year**: 10% discount, moderate commitment
**3-Year**: 15% discount, strong commitment
**5-Year**: 20%+ discount, strategic partnership

### Auto-Renewal Clauses

**Standard**:
"Agreement auto-renews for successive 1-year terms unless either party provides 60-day written notice prior to renewal date."

**Customer-Friendly**:
"Agreement auto-renews unless Customer provides 30-day notice. No penalty for non-renewal."

**Vendor-Friendly**:
"Agreement auto-renews for 2-year term unless Customer provides 90-day notice and pays early termination fee of 25% remaining contract value."

### Price Escalation

**CPI-Based**: Adjust pricing annually by CPI (Consumer Price Index)
**Fixed Escalator**: 3-5% annual increase
**No Escalation**: Lock pricing for contract term (negotiate higher base)

**Example**:
```
Year 1: $500K
Year 2: $515K (3% escalator)
Year 3: $530K (3% escalator)
```

### Termination Rights

**For Cause**: Either party may terminate for material breach
**For Convenience**: Customer can terminate with X days notice (+ penalty)
**No Termination**: Contract is binding for full term

### True-Up Mechanisms

**Quarterly True-Up**:
"Customer will be invoiced quarterly for actual usage exceeding committed amount at standard rates."

**Annual True-Up**:
"At year-end, Customer pays for actual usage exceeding annual commit at agreed-upon rate."

## Advanced Deal Structures

### Land-and-Expand Agreement

**Phase 1 - Land** (Pilot):
- Small initial commitment ($50K-$100K)
- 3-6 month pilot period
- Success criteria defined

**Phase 2 - Expand** (Production):
- Convert to multi-year agreement
- Volume commitments with discounts
- Enterprise-wide rollout

**Example**:
```
Pilot (Q1-Q2): $100K for development environment
Production (Year 1): $500K for enterprise rollout
Year 2-3: $750K/year with expansion to new business units
Total 3-year value: $2M
```

### Ramp Deal Structure

**Gradual Increase**:
```
Year 1: $300K (pilot + initial rollout)
Year 2: $600K (2x growth as adoption scales)
Year 3: $900K (1.5x growth as maturity reaches)
Total: $1.8M
```

**Why Use**: Eases Year 1 budget constraints, secures multi-year commitment

### Co-Terminus Agreements

**Align Renewal Dates**:
- All products renew on same date
- Simplifies negotiations and budgeting
- Enables portfolio-level discounting

**Example**:
```
Product A: $200K, renews June 30
Product B: $300K, renews Sept 30
Product C: $500K, renews Dec 31

→ Co-term all to Dec 31, negotiate combined $1M/year agreement
```

### Success-Based Pricing

**Performance Tiers**:
```
Tier 1: Customer achieves <20% cost reduction → $400K/year
Tier 2: Customer achieves 20-40% cost reduction → $500K/year
Tier 3: Customer achieves >40% cost reduction → $600K/year
```

**Why Use**: Aligns vendor success with customer success, reduces customer risk

### Partnership Agreements

**Strategic Partnership**:
- Multi-year (3-5 years)
- Volume commitments ($5M+)
- Co-marketing, case studies, joint innovation
- Executive sponsorship on both sides
- Preferred vendor status

**Value-Adds**:
- Dedicated account team
- Product roadmap influence
- Early access to beta features
- Custom integrations or features
- Executive business reviews (quarterly)

## Deal Structuring Checklist

**Pricing**:
- [ ] Pricing model selected (subscription, consumption, hybrid)
- [ ] Volume discounts applied
- [ ] Multi-year discounts calculated
- [ ] Prepayment discounts offered
- [ ] Competitive pricing validated

**Terms**:
- [ ] Contract duration defined (1-3 years)
- [ ] Payment terms agreed (Net 30/60/90, prepay)
- [ ] Auto-renewal clause included
- [ ] Price escalation defined (CPI, fixed, none)
- [ ] Termination rights specified

**Scope**:
- [ ] Products/services included listed
- [ ] Usage limits or tiers defined
- [ ] Exclusions clearly stated
- [ ] Professional services scoped
- [ ] Support level defined

**Legal**:
- [ ] SLA commitments documented
- [ ] Data protection and security terms
- [ ] Liability limitations
- [ ] Indemnification clauses
- [ ] Audit rights

## Negotiation Tactics

### Anchoring

**Start High**:
Present list price first, then offer discounts conditionally

"Our standard pricing is $600K/year. For a 3-year commitment, we can offer $425K/year."

### Bundling

**Better Together**:
Combine multiple products for portfolio discount

"VK Kubernetes alone is $300K. Add VK Data Platform and VK Object Storage for $500K total (17% bundle discount)."

### Conditional Discounts

**If-Then Statements**:
"If you commit to $1M over 3 years, we can offer 25% discount."
"If you prepay annually, we include $50K in professional services."

### Walk-Away Power

**Know Your Reservation Price**:
Minimum acceptable deal = $400K/year
Below that, better to walk away

## Key Principles

1. **Value-Based**: Price based on value delivered, not cost
2. **Predictable Revenue**: Favor models that ensure predictable ARR
3. **Customer Success**: Align pricing with customer outcomes
4. **Flexibility**: Offer multiple options (annual, consumption, hybrid)
5. **Multi-Year**: Push for 2-3 year terms (with discounts)
6. **Trade, Don't Cave**: Exchange concessions for value
7. **Document Clearly**: No ambiguity in contract terms
8. **Win-Win**: Structure deals for long-term partnership
