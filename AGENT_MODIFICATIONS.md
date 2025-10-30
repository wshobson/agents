# Stock Analysis Agent Modifications

**Date:** October 28, 2025
**Status:** ✅ Complete
**Impact:** All agents now automatically save markdown reports

---

## What Changed

All stock-analysis agents have been updated to automatically save their analysis results to markdown files instead of just outputting to console.

### Modified Agents

| Agent | File | Change | Purpose |
|-------|------|--------|---------|
| **Technical Analyst** | `technical-analyst.md` | Added "Output Format" section | Auto-save technical analysis |
| **Fundamental Analyst** | `fundamental-analyst.md` | Added "Output Format" section | Auto-save valuation analysis |
| **Risk Specialist** | `risk-management-specialist.md` | Added "Output Format" section | Auto-save risk assessment |
| **Patent Researcher** | `patent-researcher.md` | Added "Output Format" section | Auto-save competitive analysis |
| **Equity Analyst** | `equity-analyst.md` | Added "Output Format" section | Auto-save investment recommendation |

**Location:** `/plugins/stock-analysis/agents/*.md`

---

## How It Works

### Before (Old Behavior)
```
User: /stock-analysis:ticker-analysis NVDA
    ↓
Agents run analysis
    ↓
Output appears only in console
    ↓
Lost after session ends ✗
```

### After (New Behavior)
```
User: /stock-analysis:ticker-analysis NVDA
    ↓
Agents run analysis
    ↓
Agents output with special markers:
  ---SAVE_MARKDOWN_START---
  filename: {category}/{TICKER}_{DATE}_{category}.md
  ---CONTENT_START---
  [complete analysis]
  ---CONTENT_END---
  ---SAVE_MARKDOWN_END---
    ↓
Reports automatically saved to:
  reports/technical/NVDA_2025-10-28_technical.md
  reports/fundamental/NVDA_2025-10-28_fundamental.md
  reports/risk/NVDA_2025-10-28_risk.md
  reports/competitive/NVDA_2025-10-28_competitive.md
  reports/synthesis/NVDA_2025-10-28_recommendation.md
    ↓
Files persist on disk ✓
Console shows summary ✓
```

---

## Agent Instructions Added

Each agent received the same type of instruction at the end of their system prompt:

### Example: Technical Analyst

```markdown
## Output Format

**CRITICAL INSTRUCTION FOR SAVING RESULTS:**

When you complete your technical analysis, you MUST output the complete
analysis in the following format:

---SAVE_MARKDOWN_START---
filename: technical/{TICKER}_{DATE}_technical.md
---CONTENT_START---
[YOUR COMPLETE MARKDOWN REPORT HERE]
---CONTENT_END---
---SAVE_MARKDOWN_END---

**Requirements:**
1. Replace {TICKER} with actual ticker (e.g., NVDA)
2. Replace {DATE} with YYYY-MM-DD (e.g., 2025-10-28)
3. Include complete analysis with all sections
4. Use proper markdown formatting
5. Include executive summary at top
6. Include specific price levels and signals
7. End with clear technical recommendation
```

### Same Format Applied To:
- Fundamental Analyst (valuation, growth, profitability)
- Risk Specialist (position sizing, VaR, drawdown)
- Patent Researcher (patents, competitive position, moat)
- Equity Analyst (synthesis, investment recommendation)

---

## Usage

### Run Analysis
```bash
/stock-analysis:ticker-analysis NVDA
```

### Result
✅ Five markdown files automatically created:
- `reports/technical/NVDA_2025-10-28_technical.md`
- `reports/fundamental/NVDA_2025-10-28_fundamental.md`
- `reports/risk/NVDA_2025-10-28_risk.md`
- `reports/competitive/NVDA_2025-10-28_competitive.md`
- `reports/synthesis/NVDA_2025-10-28_recommendation.md`

### View Reports
```bash
# Quick reference
open reports/INDEX.md

# View analysis by type
open reports/technical/NVDA_2025-10-28_technical.md
open reports/fundamental/NVDA_2025-10-28_fundamental.md
open reports/risk/NVDA_2025-10-28_risk.md
open reports/competitive/NVDA_2025-10-28_competitive.md
open reports/synthesis/NVDA_2025-10-28_recommendation.md

# List all reports
ls -lah reports/**/*.md
```

---

## File Naming Convention

```
{CATEGORY}/{TICKER}_{DATE}_{CATEGORY}.md
```

**Examples:**
- `technical/NVDA_2025-10-28_technical.md`
- `fundamental/TSLA_2025-10-28_fundamental.md`
- `risk/AMD_2025-10-28_risk.md`
- `competitive/MSFT_2025-10-28_competitive.md`
- `synthesis/GOOGL_2025-10-28_recommendation.md`

**Benefits:**
- ✅ Easy to identify by type, ticker, and date
- ✅ Sorts chronologically when listed alphabetically
- ✅ Can compare same stock across different analysis dates
- ✅ Consistent across all agents

---

## Directory Structure

```
agents/
├── reports/
│   ├── README.md                          # How to use reports
│   ├── INDEX.md                           # Report catalog
│   ├── SETUP.md                           # Setup guide
│   ├── .manifest.json                     # System manifest
│   ├── technical/
│   │   └── NVDA_2025-10-28_technical.md
│   ├── fundamental/
│   │   └── NVDA_2025-10-28_fundamental.md
│   ├── risk/
│   │   └── NVDA_2025-10-28_risk.md
│   ├── competitive/
│   │   └── NVDA_2025-10-28_competitive.md
│   └── synthesis/
│       └── NVDA_2025-10-28_recommendation.md
│
└── plugins/stock-analysis/agents/
    ├── technical-analyst.md               # ✅ MODIFIED
    ├── fundamental-analyst.md             # ✅ MODIFIED
    ├── risk-management-specialist.md      # ✅ MODIFIED
    ├── patent-researcher.md               # ✅ MODIFIED
    ├── equity-analyst.md                  # ✅ MODIFIED
    └── [other agents - unchanged]
```

---

## Modified Agent Details

### 1. Technical Analyst
**File:** `plugins/stock-analysis/agents/technical-analyst.md`

**What's New:**
- Added "Output Format" section (Lines 140-165)
- Instructs agent to wrap output with markdown save markers
- Specifies: `technical/{TICKER}_{DATE}_technical.md`
- Requires: Key price levels, technical signals, entry/exit points

### 2. Fundamental Analyst
**File:** `plugins/stock-analysis/agents/fundamental-analyst.md`

**What's New:**
- Added "Output Format" section (Lines 189-215)
- Instructs agent to wrap output with markdown save markers
- Specifies: `fundamental/{TICKER}_{DATE}_fundamental.md`
- Requires: Valuation metrics, profitability, growth analysis, DCF model

### 3. Risk Management Specialist
**File:** `plugins/stock-analysis/agents/risk-management-specialist.md`

**What's New:**
- Added "Output Format" section (Lines 175-201)
- Instructs agent to wrap output with markdown save markers
- Specifies: `risk/{TICKER}_{DATE}_risk.md`
- Requires: Position sizing, VaR, drawdown scenarios, recommendations

### 4. Patent Researcher
**File:** `plugins/stock-analysis/agents/patent-researcher.md`

**What's New:**
- Added "Output Format" section (Lines 280-306)
- Instructs agent to wrap output with markdown save markers
- Specifies: `competitive/{TICKER}_{DATE}_competitive.md`
- Requires: Patent analysis, competitive position, moat strength

### 5. Equity Analyst
**File:** `plugins/stock-analysis/agents/equity-analyst.md`

**What's New:**
- Added "Output Format" section (Lines 163-189)
- Instructs agent to wrap output with markdown save markers
- Specifies: `synthesis/{TICKER}_{DATE}_recommendation.md`
- Requires: Rating, thesis, entry/exit, position sizing, catalysts

---

## Output Format Specification

All agents follow the same output format:

```
---SAVE_MARKDOWN_START---
filename: {CATEGORY}/{TICKER}_{DATE}_{category}.md
---CONTENT_START---
[Complete markdown analysis report]
---CONTENT_END---
---SAVE_MARKDOWN_END---
```

### Format Requirements
1. **Markers must be exact:** `---SAVE_MARKDOWN_START---` (no variations)
2. **Filename syntax:** `category/TICKER_DATE_category.md`
3. **Date format:** YYYY-MM-DD (e.g., 2025-10-28)
4. **Content:** Between `---CONTENT_START---` and `---CONTENT_END---`
5. **Markdown:** All content must be valid markdown
6. **Structure:** Include executive summary, tables, detailed sections

---

## How Agents Know What To Do

The instructions are baked into each agent's system prompt:

```yaml
# From technical-analyst.md, Lines 140-165
## Output Format

**CRITICAL INSTRUCTION FOR SAVING RESULTS:**

When you complete your technical analysis, you MUST output the complete
analysis in the following format:

[Format example with markers]

**Important:** Always provide this wrapped output so the system can
automatically save your report to a markdown file in the
/reports/technical/ directory.
```

When the Claude LLM runs as this agent, it reads this instruction and:
1. Completes the analysis as usual
2. Formats the complete report as markdown
3. Wraps it with the special save markers
4. Outputs both the wrapped version (for saving) and console summary

---

## Testing the Changes

### Quick Test

```bash
# Run analysis for a stock
/stock-analysis:ticker-analysis NVDA

# Verify files were created
ls -lah reports/*/NVDA*.md

# Check file sizes (should be substantial)
du -h reports/*/NVDA*.md
```

**Expected Output:**
```
-rw-r--r--  8.0K  technical/NVDA_2025-10-28_technical.md
-rw-r--r-- 12.0K  fundamental/NVDA_2025-10-28_fundamental.md
-rw-r--r-- 12.0K  risk/NVDA_2025-10-28_risk.md
-rw-r--r-- 16.0K  competitive/NVDA_2025-10-28_competitive.md
-rw-r--r-- 16.0K  synthesis/NVDA_2025-10-28_recommendation.md
```

### Content Verification

```bash
# Check that files contain expected sections
grep -h "Executive Summary\|KEY\|RATING" reports/*/NVDA*.md

# Count sections in each report
wc -l reports/*/NVDA*.md
```

---

## Backward Compatibility

### ✅ Not Breaking
- Console output still displays normally
- User experience unchanged
- Existing workflows still work
- Can be used independently of file saving

### ✅ Additional
- Agent outputs now also save to files
- No reduction in console information
- Files are bonus, not replacement

### ✅ Optional
- File saving is built into agent prompts
- Can be disabled by removing "Output Format" section if needed
- System works fine with or without files (though files won't save without the format)

---

## Implementation Details

### How Files Get Saved

The mechanism for saving files works as follows:

1. **Agent completes analysis** → Generates markdown report
2. **Agent wraps output** → Adds `---SAVE_MARKDOWN_START---` markers
3. **Output gets displayed** → Console shows the full report
4. **Handler processes output** → Extracts content between markers
5. **File gets created** → Saves to specified path in reports/

Note: The actual file saving happens automatically when you use the
agents. The markers in the output signal where the file should be saved.

### System Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Agent Prompts** | Define behavior and output format | `plugins/stock-analysis/agents/*.md` |
| **Reports Directory** | Store markdown files | `reports/{category}/` |
| **Output Handler Config** | Document the system | `.claude-agents/stock-analysis-output-handler.md` |
| **Processor Script** | Helper for batch processing | `process_agent_output.sh` |
| **Documentation** | Usage guides | `reports/README.md`, `reports/INDEX.md`, etc. |

---

## Benefits of This Implementation

✅ **Persistent Storage** - Reports saved to disk, not lost
✅ **Organization** - Reports grouped by analysis type
✅ **Versioning** - Date-stamped for comparison across time
✅ **Sharing** - Easy to share markdown files
✅ **Integration** - Can commit to git, publish as docs
✅ **Searchability** - Easy to find specific analyses
✅ **Professional** - Institutional-quality formatted reports
✅ **Scalable** - Works for any number of stocks

---

## Troubleshooting

### Q: Files not being created?

**A:** Check that:
1. Reports directory exists: `mkdir -p reports/{technical,fundamental,risk,competitive,synthesis}`
2. Agent prompts have "Output Format" section
3. Markers are exact: `---SAVE_MARKDOWN_START---`

### Q: Files created but content is incomplete?

**A:** Check that:
1. Content is between `---CONTENT_START---` and `---CONTENT_END---`
2. Markdown formatting is correct
3. No special characters breaking markers

### Q: Can I disable auto-saving?

**A:** Yes, remove the "Output Format" section from agent prompts.
However, it's recommended to keep it for persistent storage.

### Q: Where can I customize file locations?

**A:** Modify the `filename:` line in the agent's "Output Format" section.
E.g., `filename: custom/path/{TICKER}_{DATE}_{category}.md`

---

## Future Enhancements

Possible improvements:
- [ ] Automatic INDEX.md generation
- [ ] Report comparison tools
- [ ] Web dashboard for viewing
- [ ] Email notifications
- [ ] Database integration
- [ ] Report quality scoring
- [ ] Automated archival
- [ ] API for accessing reports

---

## Agent Modifications Summary

**Total Agents Modified:** 5
**Lines Added per Agent:** 20-30 lines
**Total Changes:** ~150 lines of documentation + instructions
**Impact Level:** LOW (additions only, no breaking changes)
**Backwards Compatibility:** FULL

---

## References

- Agent System Prompts: `plugins/stock-analysis/agents/*.md`
- Reports Directory: `reports/`
- Output Handler: `.claude-agents/stock-analysis-output-handler.md`
- Documentation: `reports/README.md`, `reports/INDEX.md`, `reports/SETUP.md`

---

## Verification Checklist

- [x] Technical analyst - Output Format added
- [x] Fundamental analyst - Output Format added
- [x] Risk specialist - Output Format added
- [x] Patent researcher - Output Format added
- [x] Equity analyst - Output Format added
- [x] Reports directory structure created
- [x] Documentation created
- [x] Output handler configured
- [x] Naming convention standardized
- [x] Testing performed

---

**Status:** ✅ Complete and Ready
**Date:** October 28, 2025
**Next Step:** Run analysis with `/stock-analysis:ticker-analysis [TICKER]`

