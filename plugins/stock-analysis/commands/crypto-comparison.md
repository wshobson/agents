---
name: crypto-comparison
description: Compare multiple cryptocurrencies side-by-side across technical, fundamental, tokenomics, and risk metrics. Provides relative ranking and helps identify best opportunity among digital asset candidates.
---

# Cryptocurrency Comparison Analysis

Compare multiple cryptocurrencies or blockchain projects side-by-side across key metrics to identify relative value, risk-adjusted returns, and best opportunities for investment.

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Overview

This command executes a comparative analysis workflow:
1. **Technical Comparison** - Price action, trend strength, setup quality
2. **Fundamental Comparison** - Project quality, adoption, competitive positioning
3. **Tokenomics Comparison** - Supply dynamics, FDV valuation, sustainability
4. **Risk Comparison** - Volatility, regulatory risk, drawdown potential
5. **Ranking & Recommendation** - Which asset offers best risk-adjusted opportunity

## Workflow

### Phase 1: Technical Comparison
**Led by**: Crypto Technical Analyst

Compare technical setups across assets:

**Output**:
```
TECHNICAL SCORECARD

                    BTC    ETH    SOL    AVA    XRP
Trend              Bull   Bull   Bull   Bull  Neutral
Momentum (0-10)      8      7      6      5      3
Entry Setup (0-10)   7      6      7      4      2
Risk-Reward         2.5:1  2.0:1  1.8:1  1.5:1 1.2:1
Signal Quality       High   High  Medium  Low  Weak
Time Frame          1D/1W  1D/1W  4H/1D  4H    4H

Best Setup: BTC (strongest confluence, best risk-reward)
Worst Setup: XRP (unclear trend, weak signals)
```

### Phase 2: Fundamental Comparison
**Led by**: Crypto Fundamental Analyst

Compare project quality and adoption:

**Output**:
```
FUNDAMENTAL SCORECARD

                           BTC     ETH      SOL      AVA
Network Maturity          10/10    9/10     7/10    6/10
Active Development         7/10    9/10     8/10    7/10
Ecosystem Strength         9/10   10/10     8/10    5/10
Market Position          Leader  Leader   Strong  Moderate
Technology Risk           Low     Low      Med     High
Adoption Growth          Mature  Growing  Growing  Stable

Strongest: Ethereum (mature + growing ecosystem)
Weakest: Avalanche (smaller ecosystem, lower adoption)
```

### Phase 3: Tokenomics Comparison
**Led by**: Crypto Fundamental Analyst

Compare token economics and valuation:

**Output**:
```
TOKENOMICS SCORECARD

                        BTC          ETH          SOL         AVA
Circulating Supply      21.0M        120.6M       410M        293M
Max Supply             21.0M        Unlimited    511M         720M
Current Price          $42,500      $2,300       $95         $8.50
Market Cap             $834B        $276B        $39B        $2.5B
FDV                    $834B        Unlimited    $48B        $6.1B
Inflation Rate         1.8%         0.5%         8%           2%

Holder Top 10          <5%          ~8%          12%          15%
Vesting Status         Complete     Ongoing      Mostly done  Ongoing
Token Utility          Essential    Essential    Essential    High

Best Tokenomics: BTC (capped supply, no dilution)
Concerning: ETH (unlimited supply, though deflationary)
Dilutive: SOL (8% annual inflation)
```

### Phase 4: Risk Comparison
**Led by**: Risk Management Specialist

Compare risk profiles across assets:

**Output**:
```
RISK COMPARISON

                    BTC    ETH    SOL    AVA    XRP
Volatility         60%    70%    85%    100%   110%
Beta to BTC        1.0    1.1    1.3    1.4    1.5
Max Drawdown      -75%   -80%   -90%   -95%   -98%
Regulatory Risk    Low    Med    Med    High   High
Technical Risk     Low    Low    Med    High   High
Correlation       N/A    0.85   0.80   0.75   0.70

Safest: BTC (proven security, lowest volatility)
Riskiest: XRP (highest volatility, regulatory uncertainty)
Best Risk/Return: ETH (good balance of risk/quality)
```

### Phase 5: Ranking & Recommendation
**Led by**: Crypto Technical Analyst + Fundamental Analyst

Synthesize comparison into ranked recommendation:

**Output**:
```
OVERALL RANKING & RECOMMENDATION

╔═══════════════════════════════════════════════════════════╗
║ RANK │ ASSET │ SCORE │ RATING │ CONVICTION │ POSITION   ║
╠═══════════════════════════════════════════════════════════╣
║ 1    │ BTC   │ 8.5   │ BUY    │ HIGH       │ Core 60%   ║
║ 2    │ ETH   │ 8.0   │ BUY    │ HIGH       │ Core 25%   ║
║ 3    │ SOL   │ 6.5   │ HOLD   │ MEDIUM     │ Growth 10% ║
║ 4    │ AVA   │ 4.5   │ PASS   │ LOW        │ Skip       ║
║ 5    │ XRP   │ 3.0   │ SELL   │ HIGH       │ Avoid      ║
╚═══════════════════════════════════════════════════════════╝

BTC Recommendation:
═══════════════════
Thesis: Strongest fundamentals, best risk-reward, proven security
Entry: $40,500-42,000 (accumulate on dips)
Stop: $35,000
Target: $50,000+ (medium term)
Position: 60% core allocation (conservative/growth portfolios)
Conviction: HIGH

ETH Recommendation:
═══════════════════
Thesis: Growing ecosystem, deflationary mechanics, smart contract platform
Entry: $2,200-2,300
Stop: $1,900
Target: $3,500+ (medium term)
Position: 25% core allocation (growth portfolios)
Conviction: HIGH

SOL Recommendation:
═══════════════════
Thesis: Strong technology, but higher risk; only for growth portfolios
Entry: $90-95 (accumulate gradually)
Stop: $70
Target: $150+ (long term, uncertain)
Position: 10% allocation (growth portfolios only)
Conviction: MEDIUM

AVA & XRP:
═══════════════════
Recommendation: PASS/AVOID
Reason: Weaker fundamentals, higher risk than top alternatives
Better opportunities available in leading projects
```

## Input Requirements

To run crypto comparison analysis, provide:

```yaml
Assets:
  - BTC
  - ETH
  - SOL
  - AVA
Current_Prices: Optional (will look up current if not provided)
Comparison_Focus: technical|fundamental|tokenomics|all
Your_Goal: Best growth, Safest option, Income generation, Risk-reward
Portfolio_Context: Your portfolio type and constraints
```

## Example Comparison

### Input
```
Assets: Bitcoin, Ethereum, Solana, Cardano, Polygon
Your Goal: Find best growth opportunity for 12-month horizon
Portfolio: Growth-focused, moderate-aggressive risk tolerance
```

### Output Structure
```
=== QUICK SCORECARD ===

Asset      Technical  Fundamental  Tokenomics  Risk  Overall  Rating
────────────────────────────────────────────────────────────────────
Bitcoin       8.5       8.0         9.0       8.0    8.5    BUY (High)
Ethereum      7.5       9.0         8.0       7.0    8.0    BUY (High)
Solana        6.5       7.5         7.0       5.0    6.5    HOLD (Med)
Cardano       5.0       6.5         7.5       6.0    6.0    HOLD (Med)
Polygon       5.5       7.0         6.5       5.5    6.0    HOLD (Low)

=== DETAILED COMPARISON ===

TECHNICAL ANALYSIS
─────────────────
Bitcoin:    Strong uptrend, highest quality signals, best entry/exit clarity
Ethereum:   Uptrend, good signals, minor consolidation
Solana:     Uptrend but weaker momentum, higher risk entry
Cardano:    Consolidating, unclear direction, risky entry now
Polygon:    Underperforming, no clear signals

Verdict: BTC and ETH have best technical setups

FUNDAMENTAL ANALYSIS
────────────────────
Bitcoin:    Proven security, digital gold narrative, institutional adoption
Ethereum:   Smart contract leader, growing ecosystem, DeFi dominance
Solana:     Fast, low fees, but smaller ecosystem, post-FTX recovery ongoing
Cardano:    Sound technology, but slower adoption vs ETH, smaller developer base
Polygon:    Growing L2 solution, but not as mature as Arbitrum/Optimism

Verdict: ETH strongest fundamentals, BTC proven resilience

TOKENOMICS ANALYSIS
───────────────────
Bitcoin:    Perfect (21M max, minimal new issuance)
Ethereum:   Good (capped EIP-1559 burns, but unlimited theoretical supply)
Solana:     Fair (8% annual inflation, relatively high)
Cardano:    Fair (declining inflation over time)
Polygon:    Concerning (large circulating supply, ongoing vesting)

Verdict: BTC best token economics

RISK COMPARISON
───────────────
Bitcoin:    Most stable of crypto (lowest volatility, lowest beta)
Ethereum:   Slightly higher volatility but acceptable
Solana:     High volatility, concentration risk (labs founder important)
Cardano:    Medium volatility, execution risk on upgrades
Polygon:    Medium volatility, competition from better L2s

Verdict: BTC lowest risk, ETH best risk-adjusted return

=== PORTFOLIO ALLOCATION RECOMMENDATION ===

For Growth Portfolio (12-month horizon):

Tier 1 (Core, 85%):
- Bitcoin: 50% - Stable core, best risk-reward, proven resilience
- Ethereum: 35% - Growth story + ecosystem, smart contract dominance

Tier 2 (Opportunistic, 15%):
- Solana: 10% - Growth potential but higher risk
- Polygon: 5% - Emerging L2 play but competition stronger

Not Recommended:
- Cardano: Better opportunities in Ethereum ecosystem

=== KEY CATALYSTS TO MONITOR ===

Bitcoin:
✓ ETF approvals (institutional adoption)
✓ Halving event (supply reduction)
✓ Fed policy (macro environment)

Ethereum:
✓ Shanghai upgrade (staking improvements)
✓ Dencun upgrade (L2 cost reduction)
✓ DeFi ecosystem growth

Solana:
✓ Firedancer upgrade (network speed)
✓ Ecosystem recovery post-FTX
✓ TVL growth and adoption

=== REBALANCING TRIGGERS ===

Rebalance if:
✓ Any asset moves >30% from target allocation
✓ Major catalyst occurs (upgrade, exploit, regulation)
✓ Risk profile changes significantly
✓ New information invalidates thesis
✓ Quarterly regardless of conditions

=== RISK MANAGEMENT RULES ===

✓ Never >10% in single altcoin
✓ Always use stop losses (crypto is 24/7)
✓ Minimum 2:1 risk-reward on new positions
✓ Adjust position size for volatility (SOL smaller than BTC)
✓ Maintain 10-20% stablecoin reserve for rebalancing
```

## Comparison Dimensions

### Technical Dimensions
- Trend strength and direction
- Entry/exit setup quality
- Risk-reward ratio
- Signal confidence
- Timeframe alignment

### Fundamental Dimensions
- Project maturity and proven track record
- Ecosystem health and adoption
- Development team quality
- Competitive positioning
- Regulatory environment

### Tokenomics Dimensions
- Supply structure and inflation
- Holder distribution
- Token utility and value capture
- Vesting schedules
- Dilution risk assessment

### Risk Dimensions
- Volatility and beta
- Maximum drawdown history
- Regulatory risk
- Technical risk (smart contract)
- Concentration/centralization risk

## Best Practices

### For Comparisons
1. **Use consistent metrics** - Compare apples to apples
2. **Weight appropriately** - Technical for trading, fundamentals for investing
3. **Consider your goals** - Different assets for different objectives
4. **Avoid recency bias** - Don't overweight recent performance
5. **Recheck assumptions** - Update analysis as facts change

### For Portfolio Building
1. **Tier your allocation** - Core/satellite model with different weights
2. **Diversify risk** - Don't concentrate in single asset/narrative
3. **Balance profiles** - Mix stable (BTC/ETH) with growth (quality alts)
4. **Plan exits** - Know your profit targets before entering
5. **Monitor holdings** - Track key metrics and catalyst timeline

## Common Pitfalls

❌ Comparing market caps without FDV adjustment
❌ Chasing recent winners (recency bias)
❌ Underweighting risk in bull markets
❌ Overweighting single technical indicator
❌ Ignoring fundamental changes
❌ Staying in underperformers too long
❌ Not diversifying across risk profiles

## Disclaimers

- **Educational Only**: Not financial advice
- **Point-in-Time**: Analysis current as of analysis date
- **Market Changes**: Crypto conditions change rapidly; re-analyze regularly
- **Risk of Loss**: All crypto investments carry risk of significant loss
- **Speculative**: Cryptocurrencies are highly speculative assets
- **Past Performance**: Historical performance does not guarantee future results

