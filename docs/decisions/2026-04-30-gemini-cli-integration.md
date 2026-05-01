# ADR: Gemini CLI Integration Strategy

**Date:** 2026-04-30  
**Status:** Accepted  
**Deciders:** Project maintainers  
**Sources Verified:** 2026-05-01 — Gemini CLI official documentation checked against https://geminicli.com/docs/

---

## Context

The `claude-agents` repository is a plugin marketplace built for Claude Code — 79 plugins bundling 184 agents, 150 skills, and 98 commands. Users wanted to access the same skill library from Gemini CLI without maintaining a separate ecosystem.

The core challenge: Claude Code and Gemini CLI have different extension architectures, and the gap is not symmetrical.

---

## Decision Drivers

- Reuse existing skill content without duplication
- Match Claude Code's user experience as closely as the platform allows
- Be honest about hard architectural limits rather than working around them poorly
- Keep the extension maintainable as the plugin count grows

---

## Options Considered

### Option 1: Single flat extension (GEMINI.md only)

Install the whole repo as one Gemini extension with a single root `GEMINI.md` that lists all plugins.

**Pros:** Minimal files, simple to maintain.  
**Rejected because:** No per-plugin scoping. A user working on Python gets the same context as one working on Kubernetes. Skills auto-activate against the full catalog with no way to narrow focus.

### Option 2: Separate extension per plugin (79 repos)

Break each of the 79 plugins into its own GitHub repo, each installable as an independent Gemini extension.

**Pros:** True per-plugin selective install — mirrors Claude Code's `/plugin install` model exactly.  
**Rejected because:** 79 separate repos to maintain, 79 separate `gemini extensions install` calls for users, no central catalog, and ongoing sync burden when plugins are added or changed. The maintenance cost is prohibitive.

### Option 3: Hierarchical GEMINI.md via subdirectory scanning

Place `plugins/<name>/GEMINI.md` files and rely on Gemini CLI's subdirectory scanning feature to load them contextually.

**Investigated and rejected:** Gemini CLI's subdirectory scanning applies to the *user's project working directory*, not to extension installation directories (`~/.gemini/extensions/<name>/`). Extensions load a single file from their root only. Subdirectory scanning would only work for users who clone the repo and run `gemini` from inside it — a developer workflow, not an end-user one.

**Source:** Official Gemini CLI extension reference: *"If this property [contextFileName] is not used but a GEMINI.md file is present in your extension directory, then that file will be loaded."* — no mention of subdirectory scanning within the extension.

### Option 4 (Initial): Single extension + per-plugin GEMINI.md + slash commands

One extension install (`gemini extensions install <url>`), with:

1. **`gemini-extension.json`** — manifest pointing to root `GEMINI.md`
2. **Root `GEMINI.md`** — bootstrap context listing all 79 plugins with trigger examples
3. **`plugins/<name>/GEMINI.md`** — per-plugin scoped context (agents + commands + skills) for each of the 79 plugins, loadable via `@{...}` inclusion
4. **`commands/<plugin>/<cmd>.toml`** — Gemini slash commands mapping Claude Code's `/plugin:command` pattern to Gemini's `.toml` command format

**Pros:** Single install, all skills matchable, per-plugin context available on demand, slash commands close the invocation gap.

**Status:** REJECTED after audit (see "Critical Finding" below).

---

### Option C (Chosen): Single extension + slash commands (simplified)

One extension install (`gemini extensions install <url>`), with:

1. **`gemini-extension.json`** — manifest pointing to root `GEMINI.md`
2. **Root `GEMINI.md`** — comprehensive bootstrap context listing all 79 plugins with full agent/skill/command details
3. **`commands/plugin-name.toml`** — Gemini slash commands for quick plugin access (`/security-scan`, `/conductor-orchestrate`, etc.)
4. **NO per-plugin GEMINI.md files** — removed after audit revealed false power user claim

**Rationale:** Per-plugin files were positioned to support a "power user" workflow where developers would `cd plugins/security-scanning/` and Gemini CLI would auto-load the scoped context. This claim was verified to be **false**: Gemini CLI only reads `GEMINI.md` from the extension root (or `.gemini/GEMINI.md`), not from `plugins/*/GEMINI.md`. The files were never going to auto-load. The real power user feature is **slash commands**, which do work reliably and provide fast discovery (`/security-scan` vs. typing the full context path).

**Consequences of simplification:**
- Users get all 150 skills from single root context (minimal UX impact — LLMs handle context filtering well)
- Slash commands provide the real discovery mechanism (faster than searching 79+ plugins in text)
- 79 fewer files to maintain, cleaner repository structure
- Generator script simplified (one less generator to run)

**Pros:** Single install, all skills matchable, slash commands provide real (not fictional) power user feature, simpler architecture.

---

## Critical Finding (Audit 2026-05-01)

**False Claim Identified:** ADR initially justified per-plugin GEMINI.md files as enabling a "power user" developer workflow:

> "Developers can `cd plugins/security-scanning/` and Gemini CLI auto-loads the scoped context."

**Verification Result:** INVALID

Gemini CLI extension architecture loads a single context file at extension root only:
- Checks for `gemini-extension.json` with `contextFileName` property
- If absent, looks for `.gemini/GEMINI.md` in extension root
- Does NOT recursively scan subdirectories

Per-plugin files were at `plugins/security-scanning/GEMINI.md` (root level), not `.gemini/GEMINI.md` (required subdirectory). This means:
1. Files were never going to auto-load
2. Power user benefit was fictional
3. Option 4 was justified by false reasoning

**Decision:** Remove per-plugin files (Option C). Keep slash commands (real feature). Acknowledge circular reasoning in option analysis.

---

## Key Findings During Investigation

### Gemini slash commands ARE supported

Initial documentation (and the tool mapping guide) incorrectly stated that slash commands are "Claude Code only." Gemini CLI supports custom slash commands via `.toml` files in a `commands/` directory:

```
commands/security-scanning/scan.toml  →  /security-scanning:scan
```

This means the invocation gap is fully closeable. `docs/gemini-tool-mapping.md` requires correction (pending).

### Command file distribution: 100 → 115 TOML files

The 100 Claude Code commands map to 115 Gemini `.toml` files due to a mix of nested and flat-root commands:
- **Nested**: `commands/backend-development/feature-development.toml` → `/backend-development:feature-development`
- **Flat**: `commands/c4-architecture.toml` → `/c4-architecture` (also has nested variants)

This creates plugin-level shortcuts that weren't present in Claude Code, providing better discoverability. Both variants are intentional and beneficial.

### Gemini slash commands ARE supported

### Install granularity is a hard architectural limit

Verified against official docs: `gemini extensions install <URL>` installs the entire extension as one unit. There is no `--plugin` flag or sub-unit selection. This is the one gap that cannot be closed without splitting into 79 separate repos (Option 2, rejected above).

Claude Code's selective install (`/plugin install security-scanning@claude-code-workflows`) remains a unique advantage.

### Per-plugin GEMINI.md files are generated, not hand-authored

79 per-plugin `GEMINI.md` files are generated by `tools/generate_plugin_gemini_md.py`, which reads each plugin's agent/command/skill frontmatter and produces a consistent scoped context file. This keeps the files maintainable — when a plugin gains a new agent or skill, re-running the generator updates the GEMINI.md.

---

## Decision

Implement Option C (chosen 2026-05-01 after audit).

The initial Option 4 was justified by a false power user workflow claim. After verification, per-plugin GEMINI.md files do not auto-load as envisioned. The real power user feature is slash commands. Option C removes the fictional per-plugin files and keeps the real discovery mechanism (commands).

---

## Consequences

**Gains (Option C):**
- All 150 skills accessible in Gemini CLI via natural language auto-activation
- Slash commands provide real, reliable discovery mechanism (`/security-scan` etc.)
- Single install, low friction for end users
- Simpler architecture — no generator script for per-plugin files
- Cleaner repository structure (79 fewer files)

**Trade-offs:**
- No per-plugin context files (but root context includes all plugin details)
- All plugins loaded in single context (modern LLMs handle context filtering well)

**Permanent gaps vs. Claude Code:**
- No per-plugin selective install (Gemini architectural limit)
- No per-agent model tier assignment (Gemini is session-level model only)
- No parallel subagent fan-out (Gemini executes sequentially)

**Completed work:**
- Phase A: `commands/*.toml` files for all 115 commands (slash commands fully functional)
