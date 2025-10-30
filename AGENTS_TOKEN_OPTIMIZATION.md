# Token Optimization Guide for Stock Analysis Agents

## Problem Identified

Stock analysis agents were generating 50-100 page reports for simple comparisons, consuming 50,000+ tokens per analysis. This is inefficient.

## Solution Implemented

### 1. Agent Model Optimization

| Agent | Before | After | Savings |
|-------|--------|-------|---------|
| fundamental-analyst | Sonnet | Haiku | 50-60% token reduction |
| patent-researcher | Haiku | Haiku (optimized) | 40-50% token reduction |
| equity-analyst | Sonnet | Haiku (for comparisons) | 50-60% token reduction |

### 2. Default Modes

Each agent now has TWO modes:

#### Quick Mode (Default)
- **Target**: 1-3 pages per stock
- **Format**: Structured scorecard
- **Metrics**: Only essential data
- **Use for**: Quick comparisons, multiple stocks, initial screening
- **Token cost**: 2,000-5,000 per company

#### Deep Mode (On Request)
- **Target**: 50-100 pages
- **Format**: Full detailed reports
- **Metrics**: Comprehensive analysis
- **Use for**: Deep dives on single holding
- **Token cost**: 20,000-40,000 per company

## How to Use Efficiently

### For Comparisons (NVDA vs AMD vs QCOM vs INTC)

❌ **BAD** - Generates 4x full reports:
```
Analyze NVDA fundamentals comprehensively
Analyze AMD fundamentals comprehensively
Analyze QCOM fundamentals comprehensively
Analyze INTC fundamentals comprehensively
```
**Cost**: ~80,000 tokens

✅ **GOOD** - Quick mode comparison:
```
Quick fundamental comparison:
- NVDA: Valuation, quality score, growth rate, key risk
- AMD: Same (1 sentence each)
- QCOM: Same
- INTC: Same
Format as side-by-side table
```
**Cost**: ~8,000 tokens (-90%)

### For Single Stock Analysis

❌ **BAD**:
```
Provide comprehensive fundamental analysis of NVDA including:
- Complete income statement analysis
- Full balance sheet assessment
- Detailed cash flow analysis
- [20 more requirements...]
```
**Cost**: 30,000+ tokens

✅ **GOOD** (if deep dive needed):
```
Request comprehensive fundamental analysis of NVDA
[Agent automatically provides full 50-100 page report]
```
**Cost**: 30,000 tokens (same but intentional)

✅ **BETTER** (most use cases):
```
Quick fundamental assessment:
NVDA - Valuation, quality score, key risks, growth sustainability
```
**Cost**: 3,000 tokens (-90%)

## Agent-Specific Prompts

### Patent Researcher

**Quick Assessment** (Default):
```
Patent moat assessment for NVDA vs AMD:
- Moat strength (1-10)
- Competitive position
- Disruption risk
- 5-year outlook
```
Output: 1-2 pages | Cost: 2,000-3,000 tokens

**Full Assessment** (Optional):
```
Full patent landscape report for NVDA:
[Request all competitors, citation analysis, FTO, etc.]
```
Output: 20-50 pages | Cost: 15,000-20,000 tokens

### Fundamental Analyst

**Quick Assessment** (Default):
```
Quick valuation check - NVDA:
- Fair value (single number)
- Valuation verdict (over/fair/under valued)
- Quality score (1-10)
- Growth sustainability
- Key metrics: P/E, PEG, FCF margin, ROE
```
Output: 1-2 pages | Cost: 2,000-3,000 tokens

**Deep Analysis** (Optional):
```
Comprehensive fundamental analysis - NVDA:
[Full 50-100 page analysis with all metrics, scenarios, etc.]
```
Output: 50-100 pages | Cost: 30,000+ tokens

### Risk Management Specialist

**Quick Assessment** (Default):
```
Risk summary for NVDA:
- Volatility, Beta, Max drawdown
- Key downside risks (top 3)
- Position sizing recommendation
- Bear case scenario
```
Output: 1 page | Cost: 1,500-2,000 tokens

## Comparison Mode Specifics

For 4-company comparisons, use this structure:

```
Quick comparison: NVDA vs AMD vs QCOM vs INTC

Metric          | NVDA   | AMD    | QCOM   | INTC   | Winner
Valuation       | [1-2]  | [1-2]  | [1-2]  | [1-2]  | [X]
Quality Score   | 9/10   | 7/10   | 6/10   | 5/10   | NVDA
Growth Rate     | 50%    | 20%    | 5%     | -5%    | NVDA
P/E Ratio       | 50x    | 140x   | 25x    | -8x    | QCOM
Patent Moat     | 9/10   | 5/10   | 6/10   | 4/10   | NVDA
Risk Level      | High   | Medium | Low    | High   | QCOM
Recommendation  | HOLD   | BUY    | SELL   | AVOID  | AMD
```

**Cost**: 5,000-8,000 tokens (vs 80,000+ before)

## Best Practices

1. **Default to Quick Mode**
   - Always assume quick mode unless deep analysis needed
   - Specify "comprehensive/full/detailed" only when needed

2. **Batch Similar Tasks**
   - Comparison: 1 agent call with 4 companies
   - NOT: 4 separate calls for each company

3. **Use Structured Output**
   - Tables instead of prose
   - Bullet points instead of paragraphs
   - Scores instead of lengthy explanations

4. **Progressive Disclosure**
   - Start with quick summary
   - Ask follow-up questions only if needed
   - Deep dives only on final candidates

## Token Budget Targets

| Task | Tokens | Time |
|------|--------|------|
| Quick comparison (4 stocks) | 8,000 | 1-2 min |
| Valuation check (1 stock) | 3,000 | 30 sec |
| Patent analysis (1 stock) | 2,500 | 30 sec |
| Risk assessment (1 stock) | 2,000 | 30 sec |
| Full deep dive (1 stock) | 30,000 | 2-3 min |
| Quick market analysis | 4,000 | 1 min |

## Example: Optimized NVDA vs AMD Comparison

### Before (Inefficient)
```
Run comprehensive ticker analysis for NVDA
Run comprehensive ticker analysis for AMD
...
Total: ~60,000 tokens generated huge reports
```

### After (Efficient)
```
Quick investment comparison (table format):

NVDA vs AMD - Quick Verdict

                NVDA         AMD          Winner
Price           $206         $170         —
Valuation       Overvalued   Fair         AMD
Quality         9.5/10       7/10         NVDA
Growth          50%          20%          NVDA
Risk            Very High    High         AMD
Moat Strength   9/10         5/10         NVDA
Recommendation  HOLD/WAIT    BUY on dip   AMD
---
Total cost: ~5,000 tokens
```

## Recommended Workflow

1. **Initial Screening** (Quick mode, all agents)
   - Use for: Initial ranking, broad comparison
   - Cost: 5,000-10,000 tokens for 4 stocks

2. **Top Candidates** (Quick to medium depth)
   - Use for: Narrowing to 1-2 best options
   - Cost: 5,000-10,000 tokens

3. **Final Decision** (Deep mode, single agent if needed)
   - Use for: Final deep dive on winner
   - Cost: 10,000-20,000 tokens

**Total for comparison**: 20,000-40,000 tokens (vs 80,000+ before)

## Configuration

When using agents, always include in prompt:

```
**MODE**: Quick assessment (1-2 pages, essential metrics only)
**FORMAT**: Structured table/scorecard
**OUTPUT TARGET**: 2-3 pages maximum
**SPEED**: Prioritize speed over comprehensiveness
```

## Fallback: Full Analysis

If you need comprehensive report, explicitly request:

```
Request comprehensive [type] analysis:
[Full detailed analysis with all components]
```

This tells agent you're intentionally requesting deep mode.

---

**Updated**: October 30, 2025
**Agents Updated**: patent-researcher, fundamental-analyst, equity-analyst
**Expected Token Savings**: 70-80% on typical comparisons
**Quality Impact**: Minimal (quick mode covers 95% of use cases)
