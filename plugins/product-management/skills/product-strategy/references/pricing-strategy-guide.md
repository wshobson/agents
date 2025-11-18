# Pricing Strategy Guide

## Pricing Models

### 1. Freemium

**Definition**: Free basic tier + paid premium features

**Examples**:
- Spotify: Free (ads) → Premium ($10/mo, ad-free)
- Slack: Free (90-day history) → Pro (unlimited)
- Notion: Free (personal) → Team ($10/user)

**When to Use**:
- High volume potential (millions of users)
- Viral growth mechanics
- Low marginal cost to serve

**Conversion Benchmarks**:
```
Industry        Free-to-Paid Conversion
─────────────────────────────────────────
B2C             2-5%
Productivity    10-15%
Dev Tools       5-10%
B2B SaaS        25-40% (teams)
```

---

### 2. Tiered Pricing

**Definition**: Multiple tiers with increasing features/limits

**Structure**:
```
Basic: $10/mo (core features)
Pro: $25/mo (advanced features)
Enterprise: $100/mo (custom, unlimited)
```

**Best Practices**:
- 3-4 tiers maximum (avoid choice paralysis)
- Anchor on middle tier (most popular)
- Clear differentiation between tiers

---

### 3. Usage-Based Pricing

**Definition**: Pay for what you use

**Examples**:
- AWS: Pay per compute hour, storage GB
- Twilio: Pay per SMS/call
- OpenAI: Pay per API token

**Benefits**:
- Aligns with customer value
- Scales automatically
- No overpaying/underpaying

**Challenges**:
- Unpredictable revenue
- Billing complexity
- Potential surprise bills

---

### 4. Per-User (Seat-Based)

**Definition**: Fixed price per active user

**Examples**:
- Slack: $8.75/user/month
- Salesforce: $25/user/month
- GitHub: $4/user/month

**Benefits**:
- Predictable revenue
- Scales with company growth
- Industry standard (familiar)

**Considerations**:
- Sharing accounts (limit enforcement)
- Inactive users (charge or not?)
- Minimum seats (prevent gaming)

---

## Pricing Psychology

### Anchoring

**Technique**: Show high price first to make others seem reasonable

**Example**:
```
Enterprise: $500/mo
Pro: $100/mo        ← Seems cheap vs Enterprise
Basic: $20/mo
```

---

### Decoy Pricing

**Technique**: Add option to make target tier more attractive

**Example**:
```
Monthly: $20/mo ($240/year)
Annual: $15/mo ($180/year)  ← Target tier
Annual + Support: $18/mo ($216/year) ← Decoy (makes annual better)
```

**Result**: Annual tier looks like best value

---

### Charm Pricing

**Technique**: Price ending in 9 or 7

**Example**: $99 instead of $100, $7 instead of $10

**Impact**: 5-10% higher conversion (perception of discount)

---

### Price Framing

**Instead of**: "$120/year"
**Use**: "$10/month (billed annually)"

**Perception**: Monthly price feels lower

---

## Pricing Strategy Frameworks

### Value-Based Pricing

**Process**:
1. Measure customer value delivered (ROI)
2. Capture 20-40% of value as price
3. Adjust for willingness to pay

**Example**:
```
SaaS saves customer $100K/year in labor costs
→ Price at $30K/year (30% of value)
→ Customer nets $70K savings (clear ROI)
```

---

### Competitive Pricing

**Positioning Options**:

**Premium (10-30% above competition)**:
- Superior features
- Better support
- Brand value

**Market Rate (match competition)**:
- Feature parity
- Compete on execution
- Market share focus

**Value (10-30% below competition)**:
- Good-enough features
- Volume strategy
- Cost leadership

---

### Cost-Plus Pricing

**Formula**: Cost + Margin = Price

**Example**:
```
COGS (hosting, support): $5/user/month
Target margin: 80%
Price: $5 / (1 - 0.80) = $25/user/month
```

**Limitations**:
- Ignores customer value
- Ignores competition
- Leaves money on table

---

## Pricing Experiments

### A/B Testing Price

**Setup**:
- Variant A: $20/mo
- Variant B: $25/mo

**Measure**:
- Conversion rate
- Revenue per visitor
- Customer LTV

**Decision**:
```
        Conv%   ARPU    LTV     Decision
─────────────────────────────────────────────
$20/mo  15%     $3.00   $240    Baseline
$25/mo  12%     $3.00   $300    ✓ Choose (higher LTV)
```

---

### Price Elasticity

**Measure**: How demand changes with price

**Formula**:
```
Elasticity = (% Change in Demand) / (% Change in Price)
```

**Interpretation**:
- > 1: Elastic (price-sensitive)
- < 1: Inelastic (not price-sensitive)

**Example**:
```
Price: $10 → $12 (+20%)
Demand: 100 → 90 (-10%)
Elasticity = -10% / +20% = -0.5 (inelastic)

→ Increase price (demand doesn't drop much)
```

---

## Pricing for Different Segments

### B2C Consumer

**Characteristics**:
- Price-sensitive
- Self-serve
- Credit card payment

**Pricing**:
- $5-50/month
- Simple tiers (1-3 options)
- Annual discount (2-3 months free)

---

### SMB (Small Business)

**Characteristics**:
- Value-conscious
- Self-serve or light touch sales
- ROI-focused

**Pricing**:
- $50-500/month
- Per-user or usage-based
- Free trial (14-30 days)

---

### Enterprise

**Characteristics**:
- Feature and support requirements
- Complex procurement
- Multi-year contracts

**Pricing**:
- $5K-$500K+/year
- Custom quotes
- Volume discounts
- Negotiated terms

---

## Pricing Mistakes to Avoid

### 1. Pricing Too Low

**Problem**: Can't raise prices later (anchoring)
**Solution**: Start higher, discount if needed

### 2. Too Many Tiers

**Problem**: Choice paralysis
**Solution**: 3-4 tiers maximum

### 3. Unclear Differentiation

**Problem**: Can't decide between tiers
**Solution**: Clear feature comparison table

### 4. No Pricing Page

**Problem**: Friction in buying process
**Solution**: Public pricing (or "Contact Sales" for enterprise)

### 5. Ignoring Competitors

**Problem**: Priced out of market
**Solution**: Regular competitive pricing analysis

---

## Pricing Metrics

### Key Metrics

```
Metric                  Formula                         Target
───────────────────────────────────────────────────────────────
ARPU                    Revenue / Customers             Up/right
LTV                     ARPU * Avg Lifetime             3-5x CAC
CAC Payback             CAC / (ARPU * Margin)           <12 mo
Price Realization       Actual $ / List Price           >80%
Discount %              (List - Actual) / List          <20%
```

---

## References

- "Monetizing Innovation" - Madhavan Ramanujam
- "The 1-Page Marketing Plan" - Allan Dib
- ProfitWell pricing research
- Price Intelligently blog
