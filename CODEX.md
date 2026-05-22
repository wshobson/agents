# claude-agents for Codex CLI

Multi-harness plugin marketplace consumed by OpenAI Codex CLI. Skills, subagents, and an
`AGENTS.md` map are emitted to the paths Codex expects.

> Source-of-truth lives under `plugins/`. The artifacts under `.codex/` and the top-level
> `AGENTS.md` are generated. Edit a plugin's markdown; regenerate; don't hand-edit the
> output.

## Setup

```bash
gh repo clone wshobson/agents ~/agents
cd ~/agents
make generate HARNESS=codex
ln -s ~/agents/.codex/skills ~/.codex/skills/claude-agents
ln -s ~/agents/.codex/agents ~/.codex/agents/claude-agents
```

`AGENTS.md` lives at the repo root and is read automatically when Codex is launched from
that directory (or by any subdirectory — Codex walks root → cwd, merging).

## What you get

- **Skills**: every Claude Code plugin's skills mirrored as Codex skills under
  `.codex/skills/<plugin>__<skill>/SKILL.md`. Browse with `/skills`.
- **Subagents**: every Claude Code agent transpiled to TOML at
  `.codex/agents/<plugin>__<agent>.toml`. Invoke by naming the agent in prose
  (e.g. *"have `backend-development__backend-architect` design the order service"*),
  not via `/agent`.
- **Commands as skills**: Codex deprecated `~/.codex/prompts/` in favor of skills, so
  each Claude command becomes a skill. Same content, same discovery model.
- **AGENTS.md**: a ≤150-line table of contents pointing at `docs/`, not an encyclopedia.

## Day-to-day

Describe your task naturally and Codex finds the right skill via its 2% / 8 KB budget. If
you want to delegate, name the subagent:

```
> Have `comprehensive-review__architect-review` look over the proposed change in
> src/server/order.ts and report which architectural invariants it violates.
```

## What's different from Claude Code

| Capability | Claude Code | Codex |
|---|---|---|
| Skill body cap | none | 8 KB (overflow → `references/details.md`) |
| Per-agent tool allowlist | `tools:` frontmatter | only `sandbox_mode` (read-only / workspace-write) |
| Spawn syntax | `Task`/`Agent` tool | name the agent in prose |
| `TodoWrite` | yes | no equivalent |
| Slash commands | native | converted to skills |
| Model aliases | `opus`/`sonnet`/`haiku` | GPT-5 family (mapped at generation) |

The plugin source content stays Claude-Code-optimized — the adapter handles per-harness
mechanics so you don't have to.

## Regenerating

Whenever you pull upstream changes:

```bash
make generate HARNESS=codex
```

To regenerate one plugin only:

```bash
make generate HARNESS=codex PLUGIN=javascript-typescript
```

To wipe and start fresh:

```bash
make clean-generated HARNESS=codex && make generate HARNESS=codex
```

## Authoring caveats

The same markdown plugin source ships to all harnesses. To stay portable:

- Don't put more than 8 KB of body in any `SKILL.md` — push detail into
  `references/` files alongside.
- Don't write `the Read tool` / `the Bash tool` in skill bodies — the adapter rewrites
  these to action verbs but the rewrite is conservative. Prefer
  *"open the file"* / *"run the shell command"* from the start.
- Don't name a custom agent `default`, `worker`, or `explorer` — those collide with
  Codex built-in roles and the adapter will rename them with a warning.

See `docs/authoring.md` for the full portable-content style guide.

## Reference

- `docs/harnesses.md` — capability matrix across all four supported harnesses
- `docs/plugin-eval.md` — `harness_portability` dimension that flags non-portable patterns
- `AGENTS.md` (generated) — the in-Codex map of the repo
