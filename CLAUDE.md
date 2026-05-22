# Project: claude-agents

Multi-harness agentic plugin marketplace — **82 plugins (81 local + 1 external via git-subdir)**, 191 agents, 155 skills, 102 commands. Native source-of-truth for Claude Code; also supports OpenAI Codex CLI, Cursor, OpenCode, and Gemini CLI via per-harness adapters under `tools/adapters/`.

## Map

- **[docs/architecture.md](docs/architecture.md)** — design principles
- **[docs/plugins.md](docs/plugins.md)** — full plugin catalog
- **[docs/agents.md](docs/agents.md)** — agent reference (by category, with model tiers)
- **[docs/agent-skills.md](docs/agent-skills.md)** — skill reference
- **[docs/usage.md](docs/usage.md)** — commands and workflows
- **[docs/authoring.md](docs/authoring.md)** — plugin authoring + portability guide
- **[docs/plugin-eval.md](docs/plugin-eval.md)** — quality evaluation framework
- **[docs/harnesses.md](docs/harnesses.md)** — cross-harness capability matrix
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — how to contribute

Per-harness setup guides: [CODEX.md](CODEX.md) · [CURSOR.md](CURSOR.md) · [OPENCODE.md](OPENCODE.md) · [GEMINI.md](GEMINI.md)

## Repository structure

```
.claude-plugin/marketplace.json   # SOURCE OF TRUTH (committed)
plugins/                          # SOURCE OF TRUTH (committed) — 81 local plugins
docs/                             # All documentation
tools/                            # Adapters, generators, validators, gardener
plugins/plugin-eval/              # Three-layer quality evaluation framework

# Generated (gitignored, regenerated via `make generate HARNESS=<x>`):
.codex/   AGENTS.md               # Codex CLI artifacts
.cursor-plugin/   .cursor/        # Cursor artifacts
.opencode/   opencode.json        # OpenCode artifacts
commands/   agents/   skills/     # Gemini CLI artifacts (at extension root)
```

## Plugin authoring (canonical reference)

Full conventions, frontmatter shapes, and cross-harness portability rules live in
**[docs/authoring.md](docs/authoring.md)**. The 60-second summary:

- Plugin = `plugins/<name>/` with `.claude-plugin/plugin.json` (only `name` required)
- Agents in `agents/*.md`, commands in `commands/*.md`, skills in `skills/<n>/SKILL.md`
- Auto-discovered; no need to enumerate in `plugin.json`
- Plugin names: lowercase, hyphen-separated, **no `__`** (adapter namespace separator)

## Development

- **Python tooling**: `uv` (package manager), `ruff` (lint/format), `ty` (type check).
  Do not use pip, mypy, or black.
- **Quality gates**: `make validate` (structural), `make garden` (drift detection),
  `cd plugins/plugin-eval && uv run pytest` (test suite).
- **Cross-harness regeneration**: `make generate-all` (all four target harnesses).

## Model tiers

| Tier | Model | Use |
|---|---|---|
| 1 | Opus | Architecture, security, code review, production coding |
| 2 | inherit | User-chosen — complex tasks, AI/ML, frontend/mobile, specialized |
| 3 | Sonnet | Docs, testing, debugging, support |
| 4 | Haiku | Fast ops, SEO, deployment, simple tasks |
