# Stock Analysis Auto-Save Quick Start

**Status:** ✅ Phase 3 Complete - Session-Based Organization
**Date:** October 29, 2025

---

## What's New (Phase 3 Update)

Your stock-analysis agents have been upgraded with **session-based folder organization**! Each analysis request now creates a self-contained folder with all 5 reports.

## Quick Summary

| Before (Phase 1-2) | After (Phase 3) |
|--------|-------|
| Reports in category folders | ✅ Reports in session folders |
| Hard to track by analysis date | ✅ Easy to compare same stock over time |
| `category/TICKER_DATE_type.md` | ✅ `TICKER_DATE/DATE_type.md` |
| Mixed dates in same folder | ✅ Self-contained analysis packages |

---

## How to Use (Simple)

```bash
# Just run analysis as normal
/stock-analysis:ticker-analysis NVDA

# Session folder is automatically created:
# reports/NVDA_2025-10-29/
#   ├── README.md (session overview)
#   ├── metadata.json (session metadata)
#   ├── 2025-10-29_technical.md
#   ├── 2025-10-29_fundamental.md
#   ├── 2025-10-29_risk.md
#   ├── 2025-10-29_competitive.md
#   └── 2025-10-29_recommendation.md
```

That's it! No special commands needed. Works automatically.

---

## Where Reports Are Saved

```
reports/
├── NVDA_2025-10-28/        # Session folder (TICKER_DATE)
│   ├── README.md           # Session overview
│   ├── metadata.json       # Session metadata
│   ├── 2025-10-28_technical.md
│   ├── 2025-10-28_fundamental.md
│   ├── 2025-10-28_risk.md
│   ├── 2025-10-28_competitive.md
│   └── 2025-10-28_recommendation.md
├── NVDA_2025-10-29/        # Later analysis (same stock, different date)
│   └── ... (all 5 reports with updated date)
├── TSLA_2025-10-28/        # Different stock analysis
│   └── ... (all 5 reports)
├── INDEX.md                # Quick reference
└── README.md               # Detailed guide
```

---

## Quick Access

```bash
# View all reports
open reports/

# View INDEX (recommended)
open reports/INDEX.md

# View latest NVDA session
open reports/NVDA_2025-10-29/

# View specific analysis
open reports/NVDA_2025-10-29/2025-10-29_recommendation.md

# List all sessions by date
ls -td reports/*/
```

---

## What Changed in Agents

Each agent was updated with an "Output Format" section telling it to:

1. Produce complete markdown analysis ✓
2. Wrap output with save markers ✓
3. Include filename in output ✓
4. Save to appropriate category folder ✓

**Example from Technical Analyst:**
```markdown
## Output Format

When you complete your technical analysis, you MUST output in format:

---SAVE_MARKDOWN_START---
filename: {TICKER}_{DATE}/{DATE}_technical.md
---CONTENT_START---
[complete analysis]
---CONTENT_END---
---SAVE_MARKDOWN_END---
```

**Note:** Session-based organization - all 5 reports in one folder!

Same approach for all 5 agents:
- ✅ technical-analyst.md
- ✅ fundamental-analyst.md
- ✅ risk-management-specialist.md
- ✅ patent-researcher.md
- ✅ equity-analyst.md

---

## File Organization

### By Session

Each analysis creates a session folder with all 5 reports:

```
NVDA_2025-10-28/                        # Oct 28 analysis
├── 2025-10-28_technical.md             # Chart analysis
├── 2025-10-28_fundamental.md           # Valuation analysis
├── 2025-10-28_risk.md                  # Risk assessment
├── 2025-10-28_competitive.md           # Competitive analysis
├── 2025-10-28_recommendation.md        # Investment decision
├── README.md                           # Session overview
└── metadata.json                       # Machine-readable metadata

NVDA_2025-10-29/                        # Oct 29 analysis (same stock, different date)
└── ... (all files with updated date)
```

### Reports in Session

**Technical Analysis** - `{DATE}_technical.md`
- Chart patterns, entry/exit prices, technical signals
- Size: ~5 KB
- For: Traders, tactical entries

**Fundamental Analysis** - `{DATE}_fundamental.md`
- Valuation, profitability, growth, financials
- Size: ~9 KB
- For: Long-term investors, value analysis

**Risk Analysis** - `{DATE}_risk.md`
- Position sizing, VaR, drawdowns, volatility
- Size: ~11 KB
- For: Portfolio managers, risk assessment

**Competitive Analysis** - `{DATE}_competitive.md`
- Patents, competitive position, moat, threats
- Size: ~15 KB
- For: Strategists, competitive intelligence

**Investment Recommendation** - `{DATE}_recommendation.md`
- Buy/Hold/Sell rating, thesis, targets, actions
- Size: ~15 KB
- For: Decision-makers, investment decisions

**Benefit:** Self-contained sessions, easy to compare same stock over time

---

## Example Workflow

### Day 1: Analyze NVDA

```bash
/stock-analysis:ticker-analysis NVDA
```

**Result:** Session folder `NVDA_2025-10-28/` created with 5 reports + metadata + README

### Day 2: Analyze Multiple Stocks

```bash
/stock-analysis:ticker-analysis TSLA
/stock-analysis:ticker-analysis AMD
/stock-analysis:ticker-analysis MSFT
```

**Result:** 3 new session folders created:
- `TSLA_2025-10-29/`
- `AMD_2025-10-29/`
- `MSFT_2025-10-29/`

### Day 3: Re-analyze NVDA

```bash
/stock-analysis:ticker-analysis NVDA
```

**Result:** New session folder `NVDA_2025-10-29/` with updated analysis
**Old reports:** Still in `NVDA_2025-10-28/` for comparison

### Compare NVDA Over Time

```bash
# See both analyses side-by-side
open reports/NVDA_2025-10-28/2025-10-28_recommendation.md  # Oct 28
open reports/NVDA_2025-10-29/2025-10-29_recommendation.md  # Oct 29

# Compare differences
diff reports/NVDA_2025-10-28/ reports/NVDA_2025-10-29/

# Check what changed
diff reports/NVDA_2025-10-28/2025-10-28_fundamental.md reports/NVDA_2025-10-29/2025-10-29_fundamental.md
```

---

## Key Features

✅ **Automatic** - No manual saving needed
✅ **Organized** - Reports grouped by type
✅ **Versioned** - Date-stamped for tracking changes
✅ **Persistent** - Stored on disk, not lost
✅ **Shareable** - Easy to share markdown files
✅ **Searchable** - Can grep/search across all reports
✅ **Git-friendly** - Can commit to version control
✅ **Professional** - Institutional-quality formatting

---

## Things to Know

### Automatic, Not Manual

You don't have to do anything special. Just run:
```bash
/stock-analysis:ticker-analysis NVDA
```

Files are created automatically in the background.

### Session Organization

**Same stock, same day:** Reports overwrite
```
NVDA_2025-10-28/2025-10-28_technical.md (created 09:00 AM)
NVDA_2025-10-28/2025-10-28_technical.md (overwritten at 03:00 PM)
```

**Same stock, different days:** Sessions are separate
```
NVDA_2025-10-28/  (Oct 28 analysis - kept for history)
NVDA_2025-10-29/  (Oct 29 analysis - new session)
```

**Easy comparison:** Just compare the session folders!

### File Naming Pattern

Session-based organization with date-stamped reports:

```
{TICKER}_{DATE}/{DATE}_{REPORT_TYPE}.md

Examples:
NVDA_2025-10-28/2025-10-28_technical.md
TSLA_2025-10-28/2025-10-28_fundamental.md
AMD_2025-10-28/2025-10-28_risk.md
MSFT_2025-10-28/2025-10-28_competitive.md
GOOGL_2025-10-28/2025-10-28_recommendation.md
```

### Console Output

Console output still shows the full analysis:
- ✅ Everything still appears in console
- ✅ Plus it's now also saved to files
- ✅ No changes to user experience

---

## Documentation

### Start Here
- **QUICK_START.md** ← You are here
- **INDEX.md** - Full report catalog with links
- **README.md** - Detailed usage guide

### Technical Docs
- **AGENT_MODIFICATIONS.md** - What changed in agents
- **.claude-agents/stock-analysis-output-handler.md** - System architecture

### Example Reports
- Already created for NVDA (Oct 28, 2025)
- Review these to understand the format and content

---

## Troubleshooting

### Reports not being created?

1. **Check reports directory exists:**
   ```bash
   ls -la reports/
   ```
   Should show session folders like: NVDA_2025-10-28/, TSLA_2025-10-28/

2. **Create if missing:**
   ```bash
   mkdir -p reports/
   ```

3. **Verify agents updated:**
   ```bash
   grep "filename: {TICKER}_{DATE}/{DATE}" plugins/stock-analysis/agents/*.md
   ```
   Should show 5 matches (new session-based format)

### Files incomplete?

1. **Check file size:**
   ```bash
   du -h reports/*/2025-*.md | sort -rh
   ```
   Should be 5-15 KB per file

2. **Check metadata:**
   ```bash
   head -20 reports/NVDA_2025-10-28/metadata.json
   ```
   Should show valid JSON structure

3. **Check session structure:**
   ```bash
   ls -la reports/NVDA_2025-10-28/
   ```
   Should show: 2 support files (README.md, metadata.json) + 5 reports

### Wrong location?

Reports always go to relative `reports/` directory from script location.
Session folders are created automatically as: `{TICKER}_{DATE}/`

---

## Advanced Usage

### Search Across All Reports

```bash
# Find all buy signals
grep -r "BUY\|POSITIVE" reports/*/2025-*_recommendation.md

# Get all price targets
grep -r "Price Target\|Target:" reports/*/2025-*_recommendation.md

# Find risk warnings
grep -r "VERY HIGH\|Risk:" reports/*/2025-*_risk.md
```

### Compare Stocks (Same Date)

```bash
# Compare technical setups
diff reports/NVDA_2025-10-28/2025-10-28_technical.md reports/TSLA_2025-10-28/2025-10-28_technical.md

# Compare valuations
diff reports/NVDA_2025-10-28/2025-10-28_fundamental.md reports/TSLA_2025-10-28/2025-10-28_fundamental.md
```

### Track Changes Over Time (Same Stock)

```bash
# See how NVDA rating changed
grep "Rating\|BUY\|SELL\|HOLD" reports/NVDA_*/2025-*_recommendation.md

# Track price target changes
grep "Price Target\|$[0-9]" reports/NVDA_*/2025-*_recommendation.md

# Compare full sessions
diff -r reports/NVDA_2025-10-28/ reports/NVDA_2025-10-29/
```

### Git Integration

```bash
# Commit latest analysis
git add reports/
git commit -m "Stock analysis: NVDA, TSLA, AMD - 2025-10-28"
git push

# Track report history
git log --oneline reports/

# See what changed
git diff HEAD~1 reports/synthesis/NVDA*.md
```

---

## Next Steps

1. **View existing reports:**
   ```bash
   open reports/INDEX.md
   ```

2. **Read an analysis:**
   ```bash
   open reports/synthesis/NVDA_2025-10-28_recommendation.md
   ```

3. **Run new analysis:**
   ```bash
   /stock-analysis:ticker-analysis [TICKER]
   ```

4. **Compare reports:**
   ```bash
   # Run analysis on different stocks
   /stock-analysis:ticker-analysis TSLA
   /stock-analysis:ticker-analysis AMD

   # Compare in reports directory
   ```

---

## Support Resources

| Need | File |
|------|------|
| How to use reports | `reports/README.md` |
| Quick reference | `reports/INDEX.md` |
| Implementation details | `PHASE_3_IMPLEMENTATION.md` |
| Completion summary | `PHASE_3_COMPLETION_SUMMARY.md` |
| Processing script | `process_agent_output.sh` |
| This quick start | `QUICK_START.md` |

---

## Questions?

Check these files in order:
1. **QUICK_START.md** (this file) - Overview and examples
2. **reports/README.md** - Report system guide
3. **reports/INDEX.md** - Report catalog
4. **reports/NVDA_2025-10-28/README.md** - Session-level documentation
5. **PHASE_3_IMPLEMENTATION.md** - Technical implementation details
6. **PHASE_3_COMPLETION_SUMMARY.md** - What was completed

---

## Summary

✅ **Phase 3 Complete** - Session-based report organization
✅ **Automatic saving** - All reports saved with special markers
✅ **Self-contained sessions** - Each analysis is a complete package
✅ **Easy comparison** - Compare same stock across different dates
✅ **Production ready** - Ready for immediate use

---

**Congratulations!** Your stock analysis system is now fully automated with session-based markdown reports. 🎉

**Ready to go?** Just run:
```bash
/stock-analysis:ticker-analysis [TICKER]
```

Reports will be automatically created in the `reports/{TICKER}_{DATE}/` session folder.

