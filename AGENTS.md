# claude-agents — multi-harness agentic plugin marketplace

Production-ready agentic-workflow building blocks: **92 plugins** (91 local + 1 external), **202 agents**, **181 skills**, **105 commands**. Native source-of-truth for Claude Code; also consumed by OpenAI Codex CLI, Cursor, OpenCode, and the Google Antigravity CLI (`agy`) from a single Markdown source.

This file is the canonical context file. Codex / Cursor / OpenCode / Antigravity CLI read it directly. Claude Code reads it via `CLAUDE.md`, a symlink to this file.

> **Read this file like a table of contents.** Detail lives in `docs/`. Authoring conventions live in `docs/authoring.md`. Per-harness setup and capability deltas live in [`docs/harnesses.md`](docs/harnesses.md). This file should never grow beyond ~150 lines (per OpenAI's [harness-engineering](https://openai.com/index/harness-engineering/) practice).

## Map

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — top-level architectural overview (adapter framework, source-of-truth invariant, capability matrix summary)
- **[docs/architecture.md](docs/architecture.md)** — detailed design principles
- **[docs/plugins.md](docs/plugins.md)** — full plugin catalog (92 plugins by category)
- **[docs/agents.md](docs/agents.md)** — agent reference (202 agents, model tiers)
- **[docs/agent-skills.md](docs/agent-skills.md)** — skill reference (progressive disclosure model)
- **[docs/usage.md](docs/usage.md)** — commands, workflows, examples
- **[docs/authoring.md](docs/authoring.md)** — portable-content style guide (read before adding plugins)
- **[docs/harnesses.md](docs/harnesses.md)** — per-harness capability matrix
- **[docs/plugin-eval.md](docs/plugin-eval.md)** — three-layer quality evaluation framework
- **[docs/round-trip-results.md](docs/round-trip-results.md)** — real-CLI verification recipes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — how to contribute

## Working in this repo

- Python tooling: **uv** (package manager), **ruff** (lint/format), **ty** (type check). Do not use pip / mypy / black.
- Plugins live under `plugins/<name>/` with auto-discovery — see `docs/authoring.md` for frontmatter shapes.
- Plugin names: lowercase, hyphen-separated. Never use `__` (it's the adapter namespace separator).
- Never commit secrets. Never run destructive git (force-push, `reset --hard`, branch -D) without explicit ask.

## Quality gates (run these before pushing)

```bash
make validate STRICT=1     # structural validation across all harness outputs
make garden                # drift detection (dead links, stale artifacts, oversize skills)
make test                  # full pytest suite (plugin-eval + tools/tests/)
make smoke-test            # real-CLI subprocess tests against generated artifacts
```

CI (`.github/workflows/validate.yml`) runs all four on every PR plus installs OpenCode + Antigravity CLI for live verification.

## Regenerating per-harness artifacts

```bash
make generate HARNESS=codex        # .codex/skills, .codex/agents, .codex/plugins/<p>/, .agents/plugins/marketplace.json
make generate HARNESS=cursor       # .cursor-plugin/{marketplace,plugin}.json, .cursor/rules/
make generate HARNESS=opencode     # .opencode/{skills,agents,commands,plugins}/, opencode.json
make generate HARNESS=antigravity  # .antigravity/plugins/<p>/
make generate-all                  # all four
```

Generated artifacts are **committed** so each harness installs natively from a clone / GitHub URL (native-install commands in [`docs/harnesses.md`](docs/harnesses.md)). Run `make generate-all` before committing source changes — it also prunes artifacts whose source was removed; CI fails on drift. Source-of-truth lives only under `plugins/`; never hand-edit generated files.

## Skills (cross-harness)

181 skills under `plugins/*/skills/<n>/SKILL.md` — discoverable by every harness:

- **Claude Code**: auto-discovery via Anthropic's SKILL.md spec
- **Codex CLI**: mirrored to `.codex/skills/<plugin>__<skill>/` (8 KB body cap; detail in `references/details.md`)
- **OpenCode**: mirrored to `.opencode/skills/<plugin>-<skill>/` using hyphenated names for global install
- **Cursor**: reads `.claude/skills/` directly (no re-emit)
- **Antigravity CLI**: native plugins at `.antigravity/plugins/<p>/` — bare `skills/<skill>/SKILL.md` (no `<plugin>__` namespacing; the plugin dir already scopes it)

## Subagents (cross-harness)

202 subagents under `plugins/*/agents/<name>.md`. Per-harness transpilation:

- **Codex**: `.codex/agents/<plugin>__<agent>.toml` (drop `tools:`, map model alias to the GPT-5.x family, infer `sandbox_mode`)
- **OpenCode**: `.opencode/agents/<plugin>__<agent>.md` with `mode: subagent` + `permission:` block (locked agents — those with source `tools: []` — get deny-everything except base `skill`/`task`)
- **Antigravity CLI**: `.antigravity/plugins/<p>/agents/<agent>.md` (Markdown + YAML frontmatter, `model:` is a tier alias — `inherit`/`flash`/`pro`); TOML commands at `commands/<p>/<cmd>.toml` (agy reports these as "converted to skills"); global install via `make install-antigravity` symlinks each plugin into `~/.gemini/antigravity-cli/plugins/`
- **Cursor**: reads `.claude/agents/` directly

## Why this file is short

Per OpenAI's harness-engineering practice: this file is a **map**, not an encyclopedia. Procedural detail lives in skills (loaded on demand by agents). Reference material lives in `docs/` (loaded when an agent navigates). A single bloated AGENTS.md crowds out the task, rots quickly, and is hard to verify mechanically. Keep it lean; push detail elsewhere.
