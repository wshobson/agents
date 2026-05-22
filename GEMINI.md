# claude-agents for Gemini CLI

Multi-harness plugin marketplace consumed as a Gemini CLI extension. Native skills,
subagents, and slash commands — auto-discovered from the extension root.

> This file is a table of contents, not an encyclopedia. Detail lives in `docs/`.

## Setup

```bash
gemini extensions install https://github.com/wshobson/agents
cd ~/.gemini/extensions/claude-code-workflows
make generate HARNESS=gemini
# restart Gemini CLI
```

## What you get

- **Skills**: 153 skills under `skills/<plugin>__<skill>/SKILL.md`. Describe a task to activate.
- **Subagents**: 185 subagents under `agents/<plugin>__<agent>.md`. Invoke with `@<agent>`.
- **Slash commands**: 100 commands at `/<plugin>:<command>`. Use `/help` to list.

## Map

- [`docs/plugins.md`](docs/plugins.md) — full catalog of all 82 plugins
- [`docs/harnesses.md`](docs/harnesses.md) — per-harness capability matrix
- [`docs/authoring.md`](docs/authoring.md) — portable content style guide
- [`docs/architecture.md`](docs/architecture.md) — design principles

## Different from Claude Code

| Capability | Claude Code | Gemini CLI |
|---|---|---|
| Plugin installation | `/plugin install` | `gemini extensions install <url>` |
| Per-agent tool allowlist | `tools:` (always) | `tools:` (honored) |
| Skill / agent discovery | native | native (skills/, agents/ at extension root) |
| Model assignment | per-agent | session-level (override via `model:` frontmatter) |
| `TodoWrite` | yes | no equivalent |

Plugin source content stays Claude-Code-optimized — the adapter handles per-harness mechanics.

## Regenerating

```bash
make generate HARNESS=gemini
make generate HARNESS=gemini PLUGIN=javascript-typescript
make clean-generated HARNESS=gemini && make generate HARNESS=gemini
```

## Safety

Agents in this marketplace follow standard safety conventions: no secret logging, no
unrequested commits, explicit user approval at checkpoints, isolation to the project
directory. See `docs/architecture.md` for the full safety model.
