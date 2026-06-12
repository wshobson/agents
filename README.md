# Agentic Plugin Marketplace

> Production-ready agentic workflow building blocks: **84 plugins**, **192 agents**,
> **156 skills**, **102 commands** — built for Claude Code and consumed natively by
> OpenAI Codex CLI, Cursor, OpenCode, Gemini CLI, and GitHub Copilot from a single Markdown source.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blueviolet)](#claude-code) [![Codex CLI](https://img.shields.io/badge/Codex%20CLI-supported-black)](docs/harnesses.md) [![Cursor](https://img.shields.io/badge/Cursor-supported-purple)](docs/harnesses.md) [![OpenCode](https://img.shields.io/badge/OpenCode-supported-green)](docs/harnesses.md) [![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-supported-blue)](GEMINI.md) [![Copilot](https://img.shields.io/badge/Copilot-supported-lightgrey)](docs/harnesses.md)

> [!NOTE]
> One source-of-truth (`plugins/`), five harnesses. Each harness gets idiomatic,
> harness-native artifacts — not lowest-common-denominator translations.
> See [docs/harnesses.md](docs/harnesses.md) for the capability matrix.

## Quick start

Pick your harness:

### Claude Code

```bash
/plugin marketplace add wshobson/agents
/plugin install python-development          # or any of 84 plugins
```

[→ Full Claude Code setup, troubleshooting, and plugin catalog](docs/usage.md)

### Codex CLI · Cursor · OpenCode · Gemini CLI · Copilot

Codex and Cursor install natively from the committed registries (which point at the source `plugins/`):

```bash
npx codex-marketplace add wshobson/agents        # Codex; then install individual plugins
# Cursor: add the marketplace, then `/plugin install <name>` (reads .cursor-plugin/ + source)
```

Gemini and OpenCode install via clone + generate (the transformed trees are gitignored):

```bash
gh repo clone wshobson/agents ~/agents && cd ~/agents
make generate HARNESS=gemini && gemini extensions install .   # Gemini
make install-opencode                                          # OpenCode (runs generate + symlinks)
```

Setup details and per-harness gotchas: [docs/harnesses.md](docs/harnesses.md). Gemini-specific setup: [GEMINI.md](GEMINI.md) (also auto-loaded by Gemini CLI).

## What's inside

| | Count | What it is |
|---|---:|---|
| **Plugins** | 84 | Granular, single-purpose installable units (82 local + 2 external via git-subdir) |
| **Agents** | 192 | Domain experts (architecture, languages, infra, security, data, ML, docs, business, SEO) |
| **Skills** | 156 | Modular knowledge packages with progressive disclosure (load when activated) |
| **Commands** | 102 | Slash commands: scaffolding, security scans, test gen, infrastructure setup |
| **Orchestrators** | 16 | Multi-agent coordination workflows (full-stack, security, ML, incident response) |

Browse the catalog: [docs/plugins.md](docs/plugins.md) · [docs/agents.md](docs/agents.md) · [docs/agent-skills.md](docs/agent-skills.md)

## How it works

Each plugin is isolated and composable: agents, commands, and skills are auto-discovered
from directory structure. **Installing a plugin loads only its components into
context** — not the whole marketplace.

```
plugins/python-development/
├── .claude-plugin/plugin.json
├── agents/             # 3 Python agents (python-pro, django-pro, fastapi-pro)
├── commands/           # 1 scaffolding command
└── skills/             # 16 specialized skills (async, testing, packaging, …)
```

Tiered model strategy:

| Tier | Model | Use |
|---|---|---|
| 0 | Fable 5  | Longest-horizon autonomous work — large migrations, multi-hour runs (opt-in, premium cost) |
| 1 | Opus     | Architecture, security, code review, production-critical |
| 2 | inherit  | User-chosen — backend, frontend, AI/ML, specialized |
| 3 | Sonnet   | Docs, testing, debugging, API references |
| 4 | Haiku    | Fast operational tasks, SEO, deployment, content |

[→ Model configuration details](docs/agents.md#model-configuration)

## Multi-harness support

This marketplace ships to five agentic harnesses from one Markdown source. Each adapter
emits harness-native artifacts (not lowest-common-denominator translations):

| Harness | Generates | Notes |
|---|---|---|
| **Claude Code** | (source-of-truth) | Native `marketplace.json` + `plugins/` |
| **Codex CLI** | `.agents/plugins/marketplace.json` + `plugins/*/.codex-plugin/plugin.json` (committed); `.codex/skills/`, `.codex/agents/` (gitignored) | 8 KB skill cap respected; commands → skills |
| **Cursor** | `.cursor-plugin/`, `.cursor/rules/` | Thin marketplace + curated rules; reuses `.claude/` |
| **OpenCode** | `.opencode/agents/`, `.opencode/commands/`, `.opencode/skills/` | `permission:` block from `tools:` allowlist; OpenCode-safe skill names |
| **Gemini CLI** | `skills/`, `agents/`, `commands/` (TOML) | Native skills + subagents (April 2026 spec) |
| **Copilot** | `.copilot/agents/`, `.copilot/skills/`, `.copilot/commands/` | Markdown agent profiles + SKILL.md skills + commands-as-skills; model maps to native Claude models |

```bash
make generate-all                        # all five
make validate                            # structural checks
make garden                              # drift / dead-link / cap detection
```

Codex and Cursor install from source via committed registries; Gemini and OpenCode install via clone + `make`.

[→ Full capability matrix and per-harness deep-dives](docs/harnesses.md)

## Quality evaluation

[`plugin-eval`](plugins/plugin-eval/) is a three-layer evaluation framework for measuring
and certifying plugin/skill quality:

- **Static** — deterministic structural analysis (<2s, free)
- **LLM Judge** — semantic evaluation across 4 dimensions (~30s, Haiku + Sonnet)
- **Monte Carlo** — statistical reliability via 50-100 simulated runs (~2-5 min)

```bash
uv run plugin-eval score path/to/skill --depth quick
uv run plugin-eval certify path/to/skill
```

[→ PluginEval framework documentation](docs/plugin-eval.md)

## Documentation map

Detail lives in `docs/`. Read in this order:

- **[docs/plugins.md](docs/plugins.md)** — full catalog of all 84 plugins
- **[docs/agents.md](docs/agents.md)** — all 192 agents by category
- **[docs/agent-skills.md](docs/agent-skills.md)** — 156 skills with progressive disclosure
- **[docs/usage.md](docs/usage.md)** — commands, workflows, examples
- **[docs/architecture.md](docs/architecture.md)** — design principles
- **[docs/harnesses.md](docs/harnesses.md)** — cross-harness capability matrix
- **[docs/authoring.md](docs/authoring.md)** — portable-content style guide
- **[docs/plugin-eval.md](docs/plugin-eval.md)** — quality evaluation framework
- **[docs/round-trip-results.md](docs/round-trip-results.md)** — real-CLI verification recipes

Gemini-specific setup: [GEMINI.md](GEMINI.md). All other harness setup, capability deltas, and gotchas live in [docs/harnesses.md](docs/harnesses.md).

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md) · Authoring: [docs/authoring.md](docs/authoring.md)

## External Memory Integration

[Pensyve](https://github.com/major7apps/pensyve) is included as an external
`git-subdir` entry for Claude Code. Pensyve also maintains direct upstream
integrations for this marketplace's other supported harnesses.

| Harness | Pensyve integration |
|---|---|
| Claude Code | `/plugin install pensyve` from this marketplace (`integrations/claude-code`) |
| Codex CLI | [integrations/codex-plugin](https://github.com/major7apps/pensyve/tree/main/integrations/codex-plugin) |
| Cursor | [integrations/cursor](https://github.com/major7apps/pensyve/tree/main/integrations/cursor) |
| OpenCode | [integrations/opencode-plugin](https://github.com/major7apps/pensyve/tree/main/integrations/opencode-plugin) |
| Gemini CLI | `gemini extensions install https://github.com/major7apps/pensyve` |
| Copilot | `.copilot/` in repo root or `~/.copilot/` via `make install-copilot` |

## License

MIT — see [LICENSE](LICENSE).

## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=wshobson/agents&type=date&legend=top-left)](https://www.star-history.com/#wshobson/agents&type=date&legend=top-left)
