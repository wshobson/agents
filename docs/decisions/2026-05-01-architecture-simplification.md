# ADR: Architecture Simplification — Remove Per-Plugin Files (Option C)

**Date:** 2026-05-01  
**Status:** Accepted  
**Deciders:** Project maintainers  
**Decider Notes:** Audit of ADRs revealed false power user benefit claim. This ADR documents the decision to simplify by removing per-plugin GEMINI.md files.

---

## Context

Initial ADR for Gemini CLI integration (ADR 1, Option 4) proposed including 79 per-plugin `GEMINI.md` files alongside slash commands. The rationale was that these files would enable a "power user" developer workflow:

> "Developers can `cd plugins/security-scanning/` and Gemini CLI auto-loads the scoped context."

A comprehensive audit of this claim (2026-05-01) revealed this is **false**.

---

## The False Claim

**Original claim:** Developers who clone the repository and `cd plugins/security-scanning/` will have Gemini CLI auto-load the scoped context from `plugins/security-scanning/GEMINI.md`.

**What was wrong:**
1. Gemini CLI's subdirectory scanning applies to the *user's project working directory*, not to cloned extension repositories
2. Extension context loading checks for `.gemini/GEMINI.md` (in a `.gemini/` subdirectory), not arbitrary `GEMINI.md` files at the repository root
3. Per-plugin files were placed at `plugins/<name>/GEMINI.md`, not `plugins/<name>/.gemini/GEMINI.md`
4. Therefore, files never auto-loaded, even in developer workflows

**Verification source:** [Gemini CLI Extension Reference](https://geminicli.com/docs/extensions/writing-extensions/) — *"If a `GEMINI.md` file is present in your extension directory, then that file will be loaded."* Extension directory = root, not subdirectories. Subdirectory scanning only applies to user project directories.

**Impact:** The entire power user justification for Option 4 was invalidated by this discovery. Option 4 was chosen partly because it appeared to offer better developer ergonomics. It didn't.

---

## Real Power User Feature

The actual power user feature is **slash commands** (115 TOML files), which:
- Do work reliably
- Provide fast discovery (`/security-scan` vs. searching text)
- Work identically for all users (developers and end-users)
- Enable quick context switching between plugins

This is a real feature with real value. Per-plugin files were fictional.

---

## Options Reconsidered

### Option A: Keep per-plugin files as-is (current state)

Ship the 79 per-plugin `GEMINI.md` files alongside the 115 TOML slash commands.

**Cons:**
- Files serve no real purpose (not auto-loaded, not referenced by TOML commands)
- 79 false claims in architecture about "power user discovery"
- Unnecessary repository complexity
- 142 KB of dead weight

### Option B: Move files to `.gemini/` subdirectory

Move all 79 files to `plugins/<name>/.gemini/GEMINI.md` so they would actually auto-load when developers `cd plugins/<name>/`.

**Cons:**
- Requires Gemini CLI configuration to point to correct directory (not automatic)
- Still doesn't help end-users (they don't clone the repo)
- Still justifying 79 files for niche developer workflow
- Adds a new directory layer for no clear gain

### Option C (Chosen): Remove per-plugin files entirely

Delete all 79 per-plugin `GEMINI.md` files. Keep only:
- Root `GEMINI.md` with comprehensive bootstrap context
- 115 TOML slash commands (`/plugin-name` shortcuts)
- Generator script for commands (kept; generator for per-plugin files deleted)

**Rationale:**
- Removes false architectural claims
- Simplifies repository structure (cleaner, more auditable)
- Preserves the real power user feature (slash commands)
- Reduces maintenance surface
- Users get all skills from single root context (context filtering works fine in modern LLMs)

---

## Decision

Implement Option C. Remove all 79 per-plugin `GEMINI.md` files and the `tools/generate_plugin_gemini_md.py` generator script.

Keep:
- Root `GEMINI.md` (comprehensive, all 79 plugins listed)
- 115 TOML slash commands (real discovery mechanism)
- `tools/generate_gemini_commands.py` (command generator)

---

## Consequences

**Architectural:**
- Extension is simpler: 1 context file + commands, not 80 context files + commands
- No false claims about power user benefits
- Easier to audit and understand the design

**User Experience:**
- Normal users: load extension once, use `/plugin-name` commands for quick access, get all 150 skills via auto-activation
- Power users: slash commands are the real fast-track (faster than searching a readme anyway)
- No functionality loss (all content still accessible, just organized differently)

**File Size:**
- Before: GEMINI.md (root) + 79 per-plugin files + 115 TOML = ~260 KB
- After: GEMINI.md (root, slightly larger) + 115 TOML = ~120 KB
- Reduction: ~54%

**Permanent gaps vs. Claude Code:**
- No per-plugin selective install (Gemini architectural limit)
- No per-agent model tier assignment (Gemini is session-level model only)
- No parallel subagent fan-out (Gemini executes sequentially)

---

## Lessons Learned

1. **Verify before justifying:** The initial Option 4 was justified by a feature that didn't actually exist. Verification should come before acceptance.
2. **Don't preserve "potential future value":** Files placed "in case Gemini CLI adds feature X later" create architectural cruft. Build only what's real.
3. **Real features vs. fictional ones:** Slash commands are real (tested, working). Per-plugin context was fictional (positioned as auto-loading but never did). Choose real features.

---

## References

- [ADR 1: Gemini CLI Integration Strategy](2026-04-30-gemini-cli-integration.md) — updated with Option C choice
- [ADR 3: Slash Commands](2026-05-01-gemini-slash-commands.md) — documents real power user mechanism
- [Audit Report](AUDIT_REPORT.md) — comprehensive findings
- [Skepticism Audit](SKEPTICISM_AUDIT.md) — detailed analysis of questionable claims
- Archived: [Previous ADR 2](archive/2026-05-01-per-plugin-gemini-md-distribution.md) (superseded by this decision)
