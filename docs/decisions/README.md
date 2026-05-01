# ADR Audit & Architecture Simplification

Complete audit of three Gemini CLI integration Architecture Decision Records, including critical findings, skepticism analysis, and the final decision to simplify architecture by removing per-plugin files (Option C).

## Final Decision: Option C (Architecture Simplification)

**Status:** IMPLEMENTED (2026-05-01)

Per-plugin GEMINI.md files have been removed. The power user workflow claim was false (files were never auto-loaded). The real power user feature — slash commands — is kept.

### What Changed

- ✂️ **Deleted:** 79 per-plugin GEMINI.md files
- ✂️ **Deleted:** `tools/generate_plugin_gemini_md.py` (per-plugin file generator)
- ✓ **Kept:** Root GEMINI.md (comprehensive bootstrap context)
- ✓ **Kept:** 115 TOML slash commands (`/plugin-name` shortcuts)
- ✓ **Kept:** `tools/generate_gemini_commands.py` (command generator)

### Why

1. **Power user benefit was false** — Files positioned to auto-load when developers `cd plugins/<name>/`. This never worked. Gemini CLI only reads `.gemini/GEMINI.md` (in a subdirectory), not `plugins/*/GEMINI.md` (at root).

2. **Real feature is slash commands** — Users get fast plugin discovery via `/` menu. Works the same for developers and end-users. No false claims.

3. **Simpler architecture** — 1 root context file + commands instead of 80 context files + commands. Easier to audit, maintain, and understand.

---

## ADRs: Original + Revised

1. **2026-04-30-gemini-cli-integration.md**
   - Main integration strategy for Gemini CLI
   - Status: REVISED to document Option C choice
   - Updated: Explains why Option 4 (with per-plugin files) was rejected after audit

2. **2026-05-01-per-plugin-gemini-md-distribution.md**
   - ARCHIVED (replaced by simplification ADR below)
   - See: `archive/2026-05-01-per-plugin-gemini-md-distribution.md`

3. **2026-05-01-gemini-slash-commands.md**
   - Format and context strategy for Gemini slash commands
   - Status: REVISED to clarify slash commands are the primary (and now only) power user feature

4. **2026-05-01-architecture-simplification.md** ⭐ NEW
   - Documents the decision to remove per-plugin files (Option C)
   - Explains the false power user claim and why it was rejected
   - Rationale for simplified architecture
   - Lessons learned from the audit

---

## Audit Reports & Analysis

### AUDIT_REPORT.md
Comprehensive audit with:
- Methodology and scope
- Claim-by-claim verification matrix
- Critical flaw: Power user auto-loading claim (INVALID)
- Minor issue: Line count discrepancy (CORRECTED)
- Recommendations for next steps

### SKEPTICISM_AUDIT.md
Deep analysis of 7 other questionable claims:
- 🔴 **Critical (1)**: Option 3 rejection uses circular logic
- 🔴 **High (3)**: Option 2 weak rejection, ADR 3 unnamed examples, overstated "permanent" gaps
- ⚠️ **Medium (3)**: Option 1 lacks data, .geminiignore untested, orchestration loss undemonstrated

Pattern identified: ADRs are **narrative-driven, not data-driven**
- Good logical reasoning and structure
- Weak on metrics, citations, and demonstrations

### DECISION_POINT_power_user_files.md
Strategic decision framework for per-plugin files (SUPERSEDED):
- **Option A**: Keep as-is (future-proofing hedge) — NOT chosen
- **Option B**: Move to `.gemini/` subdirectories (makes power user benefit real) — NOT chosen
- **Option C**: Remove entirely (clean implementation) — ✓ CHOSEN (2026-05-01)

## Archived Documents

- **archive/2026-05-01-per-plugin-gemini-md-distribution.md** — Previous ADR 2 (superseded by simplification decision)

### Corrections Applied
✅ ADR 2: Removed false "developer workflow" power user claim  
✅ ADR 2: Fixed line count (2,632 → 2,389)  
✅ ADR 1: Added command distribution clarification (100 → 115 TOML files)  
✅ All ADRs: Added source verification metadata (2026-05-01)  

### Critical Findings
❌ Per-plugin GEMINI.md files do NOT auto-load for power users  
❌ Files are placed at `plugins/<name>/GEMINI.md`, but Gemini CLI looks for `.gemini/GEMINI.md`  
⚠️ Option 3 rejection logic contradicts Option 4 choice  

## Key Insights

The ADRs are **sound architectural reasoning** but need:

| Category | Status | Notes |
|----------|--------|-------|
| Architecture Quality | ★★★★☆ | Solid despite logic gaps |
| Documentation | ★★★★☆ | Good (now improved) |
| Verification Rigor | ★★★☆☆ | Needs empirical testing |
| Option Analysis | ★★★★☆ | Well-explored but some gaps |

## Recommendations

### Immediate
1. Decide on per-plugin files strategy (A/B/C from DECISION_POINT_power_user_files.md)
2. Re-articulate Option 3 rejection if needed
3. Update "permanent gaps" language with caveats

### Medium-term
4. Test Gemini CLI `.gitignore` behavior
5. Verify extension-relative `@{path}` with actual testing
6. Measure token costs (monolithic vs. scoped context)
7. Demonstrate TOML command limitations empirically

### Nice-to-have
8. Add GitHub example citations
9. Document Option 2 monorepo alternative
10. Clarify distinction between Options 3 and 4

## Usage

- **Start here**: AUDIT_REPORT.md (overview) → SKEPTICISM_AUDIT.md (details)
- **Decision needed**: DECISION_POINT_power_user_files.md
- **Deep dive**: Original ADRs (now with corrections)

## Verification Status

| Claim Category | Verified | Notes |
|---|---|---|
| Gemini CLI extension reference | ✅ | Direct documentation match |
| TOML command format | ✅ | Verified in official docs |
| @{path} CWD resolution | ✅ | Documented behavior confirmed |
| Commands auto-discovery | ✅ | Official docs verified |
| Power user auto-loading | ❌ | **FALSE** — files in wrong location |
| Line count (79 files) | ✅ | 2,389 lines (not 2,632) |

## Questions & Decisions

**What about Option 3?** Why was it rejected if power users clone anyway?
→ See SKEPTICISM_AUDIT.md section 3 (Circular Logic)

**What about the per-plugin files?** Do we keep them?
→ See DECISION_POINT_power_user_files.md (three options provided)

**Are the ADRs approved?** 
→ Yes, with caveats noted in SKEPTICISM_AUDIT.md. Architecture is sound but needs empirical validation.

---

**Audit Date:** 2026-05-01  
**Auditor:** Copilot CLI  
**Status:** Complete with corrections applied
