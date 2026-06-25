# Architecture

Top-level architectural map for the claude-agents marketplace. Detail lives in [`docs/architecture.md`](docs/architecture.md); this file is the index per the OpenAI [harness-engineering](https://openai.com/index/harness-engineering/) pattern.

## Invariants

1. **Single source of truth.** All agent / skill / command authoring happens under `plugins/<name>/`. Generated harness-specific artifacts (`.codex/skills/`, `.codex/agents/`, `.opencode/`, `.copilot/`, `commands/`, `agents/`, `skills/` at extension root for Gemini) are produced by adapters and gitignored. The exception: small native-install registries (`.agents/plugins/marketplace.json`, `plugins/*/.codex-plugin/plugin.json`, `.cursor-plugin/`, `.cursor/rules/`, `gemini-extension.json`) are committed — they only point at the source `plugins/`, so the invariant holds. Never hand-edit generated files.

2. **One canonical context file.** `AGENTS.md` at repo root is the only context file authored directly. Claude Code reads `CLAUDE.md`, a symlink to `AGENTS.md`. Gemini CLI reads it via `.gemini/settings.json` `context.fileName`. Codex / Cursor / OpenCode read `AGENTS.md` natively.

3. **Adapters own per-harness mechanics; source content stays portable.** Authors write Claude-Code-quality markdown. Adapters under `tools/adapters/` handle every harness-specific transform (frontmatter rewriting, model-alias mapping, body-size caps, tool-name remapping). Source files never carry harness conditional logic.

4. **Mechanical enforcement with remediation hints.** Every lint / validator finding ships with a concrete fix string. `make validate`, `make garden`, and the `plugin-eval` `harness_portability` dimension all follow this convention.

5. **Progressive disclosure all the way down.** Context files (`AGENTS.md`, `CLAUDE.md`, etc.) cap at ~150 lines. Skill bodies cap at ~8 KB (Codex's hard limit). Detail offloads to `docs/` and `references/details.md`. Detail is loaded on demand, not pre-injected.

## Component overview

```
claude-agents/
├── AGENTS.md                       # Canonical context file (committed)
├── CLAUDE.md                       # symlink → AGENTS.md (Claude-specific addenda live in AGENTS.md)
├── ARCHITECTURE.md                 # This file
├── README.md                       # User-facing GitHub landing page
├── GEMINI.md                       # Gemini-specific setup (auto-loaded by Gemini CLI)
├── CONTRIBUTING.md                 # Contributor entry point
├── .claude-plugin/marketplace.json # Plugin registry (source of truth)
├── .gemini/settings.json           # Gemini CLI → AGENTS.md redirect
├── plugins/                        # SOURCE OF TRUTH (85 local plugins; 3 externals in marketplace)
│   └── <name>/
│       ├── .claude-plugin/plugin.json
│       ├── agents/*.md
│       ├── commands/*.md
│       └── skills/<n>/{SKILL.md, references/, assets/}
├── tools/
│   ├── adapters/                   # Per-harness adapter framework
│   │   ├── base.py                 # Parser, HarnessAdapter ABC, helpers
│   │   ├── capabilities.py         # Capability matrix; consumed by every adapter
│   │   ├── codex.py / cursor.py / opencode.py / gemini.py / copilot.py
│   │   └── cursor_rules/           # Hand-curated .mdc rules
│   ├── generate.py                 # Unified CLI: `make generate HARNESS=<x>`
│   ├── validate_generated.py       # Structural validation
│   ├── doc_gardener.py             # Drift detection (per harness-engineering)
│   └── tests/                      # Adapter + behavioral + CLI smoke tests
└── docs/                           # Detailed reference docs
    ├── architecture.md             # Full architecture (this file is the map)
    ├── plugins.md / agents.md / agent-skills.md  # Catalogs
    ├── usage.md                    # User workflows
    ├── authoring.md                # Portable-content style guide
    ├── harnesses.md                # Cross-harness capability matrix
    ├── plugin-eval.md              # Quality evaluation framework
    └── round-trip-results.md       # Real-CLI verification recipes
```

## Cross-harness adapter framework

Each adapter consumes the canonical `plugins/` source and emits harness-native artifacts:

| Adapter | Output | What it does |
|---|---|---|
| `codex.py` | committed `.agents/plugins/marketplace.json` + `plugins/*/.codex-plugin/plugin.json`; gitignored `.codex/skills/`, `.codex/agents/*.toml` | Marketplace + per-plugin manifests (point at source `plugins/`); Markdown → TOML transform, 8 KB body cap with `references/` overflow, sandbox_mode heuristic, collision detection |
| `cursor.py` | `.cursor-plugin/`, `.cursor/rules/*.mdc` | Marketplace manifests + hand-curated rules. Cursor reads `.claude/` directly for skills/agents |
| `opencode.py` | `.opencode/agents/`, `.opencode/commands/`, `.opencode/skills/` | Permission block from `tools:` allowlist (locked agents preserve intent); strict lowercase tool names; OpenCode-safe skill names |
| `copilot.py` | `.copilot/agents/`, `.copilot/skills/`, `.copilot/commands/` | Markdown agent profiles + SKILL.md skills + commands-as-skills; model maps to native Claude models |
| `gemini.py` | `skills/`, `agents/`, `commands/*.toml` at extension root | Native skills + April-2026 subagents; `@{path}` injection for large command bodies |

Detail in [`docs/harnesses.md`](docs/harnesses.md) (capability matrix per harness) and [`docs/architecture.md`](docs/architecture.md) (full design rationale).

## Quality gates

Three mechanical gates, each runnable as a make target and wired into CI:

1. **`make validate`** — structural validation of every generated artifact. Errors block CI; warnings advisory.
2. **`make garden`** — drift detection (dead links, stale artifacts, oversize skills, marketplace orphans). Sorted by severity with per-kind summary.
3. **`make test`** — full pytest suite (386 tests: adapters + validators + gardener + real-source + round-trip + real-CLI smoke).

CI workflow: [`.github/workflows/validate.yml`](.github/workflows/validate.yml) runs all three on every PR, plus a `cli-smoke-test` job that installs OpenCode + Gemini and exercises them against the generated artifacts.

## Plugin component model

Each plugin is a directory under `plugins/`. Three component types, all auto-discovered:

- **Agents** (`agents/<name>.md`) — domain experts. Frontmatter: `name`, `description` ("Use PROACTIVELY when …"), `model: opus|sonnet|haiku|inherit`, optional `tools:`, optional `color:`.
- **Skills** (`skills/<n>/SKILL.md`) — modular knowledge with progressive disclosure. Frontmatter: `name`, `description` (must include a recognized trigger phrase like "Use when …"). Supporting material in `references/`, templates in `assets/`.
- **Commands** (`commands/<n>.md`) — slash commands. Frontmatter: `description`, `argument-hint`.

Full conventions in [`docs/authoring.md`](docs/authoring.md). Authoring for portability across all five harnesses is the main concern; the adapter framework handles per-harness mechanics.

## Model tiers

| Tier | Model | Use |
|---|---|---|
| 1 | Opus | Architecture, security, code review, production coding |
| 2 | inherit | Complex tasks — user chooses model (AI/ML, backend, specialized) |
| 3 | Sonnet | Docs, testing, debugging, support |
| 4 | Haiku | Fast ops, SEO, deployment, simple tasks |

Per-harness adapter maps these aliases to native model IDs at generation time (see `tools/adapters/capabilities.py:MODEL_ALIASES`).

## See also

- [`docs/architecture.md`](docs/architecture.md) — full design rationale, file ownership, capability matrix detail
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/) — the practices this repo follows
- [agents.md spec](https://agents.md/) — the AGENTS.md convention this repo adopts
