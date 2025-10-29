# Stock Analysis Output Handler

**Purpose:** Automatically process agent outputs and save markdown reports

**Configuration:** This handler intercepts outputs from stock-analysis agents and saves them to markdown files.

---

## How It Works

### 1. Agent Output Format

When stock-analysis agents complete their analysis, they wrap their output with special markers:

```
---SAVE_MARKDOWN_START---
filename: {category}/{TICKER}_{DATE}_{category}.md
---CONTENT_START---
[Complete markdown report content]
---CONTENT_END---
---SAVE_MARKDOWN_END---
```

### 2. Output Processing

The handler:
1. Detects the `---SAVE_MARKDOWN_START---` marker
2. Extracts the filename from the `filename:` line
3. Captures all content between `---CONTENT_START---` and `---CONTENT_END---`
4. Saves the content to the specified file path
5. Also displays console output for immediate review

### 3. File Locations

Reports are automatically saved to:

```
/Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/reports/
├── technical/
│   └── {TICKER}_{DATE}_technical.md
├── fundamental/
│   └── {TICKER}_{DATE}_fundamental.md
├── risk/
│   └── {TICKER}_{DATE}_risk.md
├── competitive/
│   └── {TICKER}_{DATE}_competitive.md
└── synthesis/
    └── {TICKER}_{DATE}_recommendation.md
```

---

## Agent Configuration

All stock-analysis agents have been updated with output format instructions:

| Agent | Report Category | Output File Pattern |
|-------|---|---|
| **technical-analyst** | technical | technical/{TICKER}_{DATE}_technical.md |
| **fundamental-analyst** | fundamental | fundamental/{TICKER}_{DATE}_fundamental.md |
| **risk-management-specialist** | risk | risk/{TICKER}_{DATE}_risk.md |
| **patent-researcher** | competitive | competitive/{TICKER}_{DATE}_competitive.md |
| **equity-analyst** | synthesis | synthesis/{TICKER}_{DATE}_recommendation.md |

---

## Usage Examples

### Example 1: Run NVDA Analysis

```bash
/stock-analysis:ticker-analysis NVDA
```

**Result:**
- Runs 5-phase analysis
- Automatically creates:
  - `reports/technical/NVDA_2025-10-28_technical.md`
  - `reports/fundamental/NVDA_2025-10-28_fundamental.md`
  - `reports/risk/NVDA_2025-10-28_risk.md`
  - `reports/competitive/NVDA_2025-10-28_competitive.md`
  - `reports/synthesis/NVDA_2025-10-28_recommendation.md`

### Example 2: Analyze Different Stock

```bash
/stock-analysis:ticker-analysis TSLA
```

**Result:**
- Creates new reports for TSLA with today's date
- All saved automatically to same directory structure

### Example 3: Compare Multiple Analyses

```bash
/stock-analysis:ticker-analysis AMD
/stock-analysis:ticker-analysis NVDA
```

**Result:**
- Creates reports for both AMD and NVDA
- Can compare side-by-side from reports directory

---

## File Naming Convention

All reports follow consistent naming:

```
{CATEGORY}/{TICKER}_{YYYY-MM-DD}_{CATEGORY}.md
```

**Examples:**
- `technical/NVDA_2025-10-28_technical.md`
- `fundamental/TSLA_2025-10-28_fundamental.md`
- `risk/AMD_2025-10-28_risk.md`
- `competitive/GOOGL_2025-10-28_competitive.md`
- `synthesis/MSFT_2025-10-28_recommendation.md`

**Benefits:**
- ✅ Easy to identify report type
- ✅ Clear date for versioning
- ✅ Alphabetical sorting shows chronological order
- ✅ Can compare same stock across dates

---

## Integration Points

### In Your Claude Code Session

1. **View Reports:** `open reports/INDEX.md`
2. **Check Latest Analysis:** `open reports/synthesis/`
3. **Monitor Competitors:** `grep -r "threat" reports/competitive/`
4. **Track Updates:** `ls -lt reports/**/*.md | head -10`

### Git Integration

```bash
# Commit latest analysis
git add reports/
git commit -m "Add stock analysis for NVDA, TSLA, AMD - 2025-10-28"
git push
```

### Directory Monitoring

```bash
# Watch for new reports
watch -n 5 'ls -lt reports/**/*.md | head -5'
```

---

## How Agents Know to Save Output

Each agent has been updated with instructions in their system prompt:

**Technical Analyst:**
> When you complete your technical analysis, you MUST output the complete analysis in the following format with `---SAVE_MARKDOWN_START---` markers...

**Fundamental Analyst:**
> When you complete your fundamental analysis, you MUST output the complete analysis in the following format with `---SAVE_MARKDOWN_START---` markers...

(And so on for all agents)

---

## Data Flow

```
User Command
    ↓
/stock-analysis:ticker-analysis NVDA
    ↓
Agent 1: Technical Analyst
    └→ Analyzes charts
    └→ Outputs: ---SAVE_MARKDOWN_START--- ... ---SAVE_MARKDOWN_END---
    └→ File saved: technical/NVDA_2025-10-28_technical.md
    ↓
Agent 2: Fundamental Analyst
    └→ Analyzes financials
    └→ Outputs: ---SAVE_MARKDOWN_START--- ... ---SAVE_MARKDOWN_END---
    └→ File saved: fundamental/NVDA_2025-10-28_fundamental.md
    ↓
Agent 3: Risk Specialist
    └→ Analyzes risk
    └→ Outputs: ---SAVE_MARKDOWN_START--- ... ---SAVE_MARKDOWN_END---
    └→ File saved: risk/NVDA_2025-10-28_risk.md
    ↓
Agent 4: Patent Researcher
    └→ Analyzes competitive
    └→ Outputs: ---SAVE_MARKDOWN_START--- ... ---SAVE_MARKDOWN_END---
    └→ File saved: competitive/NVDA_2025-10-28_competitive.md
    ↓
Agent 5: Equity Analyst
    └→ Synthesizes recommendation
    └→ Outputs: ---SAVE_MARKDOWN_START--- ... ---SAVE_MARKDOWN_END---
    └→ File saved: synthesis/NVDA_2025-10-28_recommendation.md
    ↓
User
    └→ Console summary + 5 markdown files saved
```

---

## Troubleshooting

### Reports Not Being Saved?

1. **Check file permissions:**
   ```bash
   ls -la /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/reports/
   chmod -R 755 reports/
   ```

2. **Verify directory exists:**
   ```bash
   mkdir -p reports/{technical,fundamental,risk,competitive,synthesis}
   ```

3. **Check agent prompt updates:**
   - Verify agents have "Output Format" section
   - Ensure markers are exactly: `---SAVE_MARKDOWN_START---`, etc.

### Files Saved to Wrong Location?

- Check the `filename:` line in agent output
- Should be: `filename: technical/NVDA_2025-10-28_technical.md`
- Not: `filename: /full/path/...`

### Content Missing from Files?

- Agents must include content between `---CONTENT_START---` and `---CONTENT_END---`
- Nothing outside these markers will be saved
- Empty lines will be preserved

---

## Advanced Usage

### Extract Specific Data from Reports

```bash
# Get all price targets
grep -h "Price Target\|Target:" reports/synthesis/*.md

# Find all buy ratings
grep -h "RATING\|BUY" reports/synthesis/*.md

# Monitor risk assessment changes
diff reports/risk/NVDA_2025-10-27_risk.md reports/risk/NVDA_2025-10-28_risk.md
```

### Generate Report Index

```bash
# Create index of all reports
echo "# Stock Analysis Reports" > reports/ALL_REPORTS.md
echo "" >> reports/ALL_REPORTS.md
find reports -type f -name "*.md" | sort | while read f; do
  echo "- [$(basename $f)]($f)" >> reports/ALL_REPORTS.md
done
```

### Automated Report Updates

```bash
# Run analysis for multiple stocks
for ticker in NVDA TSLA AMD MSFT GOOGL; do
  echo "Analyzing $ticker..."
  /stock-analysis:ticker-analysis $ticker
  sleep 5  # Rate limiting
done
```

---

## Requirements & Dependencies

### Directory Structure
```
agents/
└── reports/
    ├── technical/       (auto-created)
    ├── fundamental/     (auto-created)
    ├── risk/           (auto-created)
    ├── competitive/    (auto-created)
    └── synthesis/      (auto-created)
```

### Agent Updates
- ✅ technical-analyst.md - Output Format section added
- ✅ fundamental-analyst.md - Output Format section added
- ✅ risk-management-specialist.md - Output Format section added
- ✅ patent-researcher.md - Output Format section added
- ✅ equity-analyst.md - Output Format section added

---

## Configuration Files

- **Agent prompts:** `plugins/stock-analysis/agents/*.md`
- **Output handler:** This file
- **Output processor:** `process_agent_output.sh` (optional helper script)
- **Reports directory:** `reports/` (auto-created on first run)

---

## Future Enhancements

Potential additions:
- [ ] Automatic INDEX.md generation
- [ ] Report comparison across dates
- [ ] Summary statistics extraction
- [ ] Email notifications on new reports
- [ ] Database integration (SQLite)
- [ ] Web dashboard for viewing reports
- [ ] Automated archival of old reports
- [ ] Report quality scoring

---

## Support

For issues or enhancements:
1. Check this documentation
2. Verify agent prompt updates
3. Test output format manually
4. Review console output for errors

---

**Last Updated:** October 28, 2025
**Status:** Fully Operational
**Version:** 1.0

