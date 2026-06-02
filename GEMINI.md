# Gemini CLI — setup guide

> The canonical context file is [`AGENTS.md`](AGENTS.md) at the repo root. Gemini CLI reads it via `.gemini/settings.json` (`context.fileName`). This guide covers Gemini-specific setup only.

## Install

```bash
gemini extensions install https://github.com/wshobson/agents
cd ~/.gemini/extensions/claude-code-workflows
make generate HARNESS=gemini
# restart Gemini CLI
```

## What you get

- **156 skills** at `skills/<plugin>__<skill>/SKILL.md` — described in `AGENTS.md`. Describe a task to activate.
- **192 subagents** at `agents/<plugin>__<agent>.md` — invoke with `@<agent>`.
- **102 slash commands** at `/<plugin>:<command>` — use `/help` to list.

## Companion Memory Extension

Pensyve is maintained upstream as a separate Gemini CLI extension with MCP-backed
memory and context injection:

```bash
gemini extensions install https://github.com/major7apps/pensyve
```

## Gemini-specific differences

| Capability | Claude Code | Gemini CLI |
|---|---|---|
| Plugin installation | `/plugin install` | `gemini extensions install <url>` |
| Context file | reads `CLAUDE.md` (a symlink to `AGENTS.md`) | reads via `.gemini/settings.json` redirect to AGENTS.md |
| Per-agent tool allowlist | `tools:` (always) | `tools:` (honored — remapped to Gemini-native names) |
| Skill / agent discovery | native | native (skills/, agents/ at extension root) |
| Model assignment | per-agent | session-level (override via `model:` frontmatter) |
| `TodoWrite` tool | yes | no equivalent |

## Regenerating

```bash
make generate HARNESS=gemini                            # all plugins
make generate HARNESS=gemini PLUGIN=javascript-typescript   # one plugin
make clean-generated HARNESS=gemini                     # remove output
```

## See also

- [`AGENTS.md`](AGENTS.md) — canonical context (cross-harness conventions)
- [`docs/harnesses.md`](docs/harnesses.md) — full capability matrix
- [`docs/round-trip-results.md`](docs/round-trip-results.md) — Gemini round-trip verification recipe
