# ADR: Gemini CLI Slash Commands — Format and Context Strategy

**Date:** 2026-05-01  
**Status:** Accepted  
**Deciders:** Project maintainers  
**Sources Verified:** 2026-05-01 — Gemini CLI official documentation checked against https://geminicli.com/docs/

---

## Context

Claude Code exposes 100 commands across 50 plugins as slash commands (`/plugin:command`). Gemini CLI supports custom slash commands via TOML files. This ADR documents the decisions made when implementing the Gemini equivalent.

---

## Decision 1: TOML over Markdown for Gemini Commands

Claude Code commands are authored as `.md` files with YAML frontmatter. Gemini CLI's command system uses `.toml` files.

**Primary source:** [Gemini CLI Custom Commands](https://geminicli.com/docs/cli/custom-commands/) — "Custom commands are stored in TOML files."

**Schema confirmed:**
- `description` (optional) — displayed in help menu
- `prompt` (required) — instruction text sent to model
- Supports `{{args}}` for user input, `@{path}` for file inclusion, `!{shell}` for shell output

**Decision:** Generate `.toml` files from existing `.md` command files using `tools/generate_gemini_commands.py`. The generator reads frontmatter `description`, `argument-hint`, `keywords`, and the first context paragraph from the body.

---

## Decision 2: Directory Structure Mirrors Claude Code Namespace

Claude Code uses `/plugin-name:command-name`. Gemini CLI derives command names from directory structure: `commands/<plugin>/<cmd>.toml` → `/<plugin>:<cmd>`.

**Primary source:** [Gemini CLI Extension Reference](https://geminicli.com/docs/extensions/reference/) — "Nested: `commands/gcs/sync.toml` → `/gcs:sync` (colon-namespaced)."

**Decision:** Use `commands/<plugin-name>/<cmd-name>.toml` to preserve the identical namespace. Users familiar with Claude Code's `/security-scanning:security-sast` get the same command in Gemini CLI.

---

## Decision 3: Self-Contained Prompts — No Extension-Relative File Inclusion

This is the most consequential decision. The initial design intended to use `@{plugins/<name>/GEMINI.md}` in TOML prompts to load per-plugin context. This was rejected after research.

**What was investigated:**

The Gemini CLI `@{path}` syntax in TOML command prompts resolves paths **relative to the user's CWD** (their project directory), not relative to the extension's installation directory (`~/.gemini/extensions/<name>/`).

**Evidence:**
1. Official docs: "Paths are relative to the current directory or workspace directories." ([Custom Commands docs](https://geminicli.com/docs/cli/custom-commands/))
2. Real extension examples examined on GitHub (e.g., `gemini-cli-extensions/security`, `gemini-cli-extensions/conductor`) **do not use `@{}` file inclusion** — they embed all context in the prompt field directly. This is the established pattern because extension developers have hit the same wall.
3. The `@{}` resolver has no knowledge of `~/.gemini/extensions/` as a valid resolution root.

**Consequence:** `@{plugins/security-scanning/GEMINI.md}` in a TOML prompt would look for `<user-project>/plugins/security-scanning/GEMINI.md`, which does not exist.

**Decision:** All 100 TOML commands embed context directly in their `prompt` field:
- The command's description (from frontmatter or H1 fallback)
- Context paragraph from the command body (deduped against description)
- Available agents and skills for the plugin
- Argument hint
- `{{args}}` placeholder

This matches the established pattern used by real Gemini CLI extension authors and is verifiably safe.

---

## Decision 4: Commands Are Auto-Discovered — No Manifest Update Needed

Gemini CLI auto-discovers commands from a `commands/` directory within the extension. No `commands` field is required in `gemini-extension.json`.

**Primary source:** [Gemini CLI Extension Reference](https://geminicli.com/docs/extensions/reference/) — "Commands are auto-discovered from the `commands/` directory."

**Decision:** No change to `gemini-extension.json`.

---

## Consequences

**Gains:**
- 100 Gemini slash commands mirroring Claude Code's full command surface
- Identical `/<plugin>:<command>` namespace across both platforms
- Self-contained prompts work without CWD dependency or file system assumptions

**Limitations:**
- TOML prompts are summaries, not the full command content. Complex multi-phase orchestration commands (e.g., `feature-development`, `tdd-cycle`) lose their detailed step sequences in the Gemini version.
- If Gemini CLI later adds extension-relative `@{path}` resolution, prompts could be updated to reference per-plugin GEMINI.md files instead of embedding context inline.

**Future option:** If the `@./` GEMINI.md inclusion syntax (confirmed for `GEMINI.md` files, path resolution ambiguous for extensions) is verified to work extension-relative, the per-plugin GEMINI.md files from Phase B could be referenced from slash command prompts to provide richer context without prompt bloat.
