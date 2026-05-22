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

- **155 skills** at `skills/<plugin>__<skill>/SKILL.md` — described in `AGENTS.md`. Describe a task to activate.
- **191 subagents** at `agents/<plugin>__<agent>.md` — invoke with `@<agent>`.
- **102 slash commands** at `/<plugin>:<command>` — use `/help` to list.

## Gemini-specific differences

| Capability | Claude Code | Gemini CLI |
|---|---|---|
| Plugin installation | `/plugin install` | `gemini extensions install <url>` |
| Context file | reads CLAUDE.md natively | reads via `.gemini/settings.json` redirect to AGENTS.md |
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
