# claude-agents for OpenCode

Multi-harness plugin marketplace consumed by [OpenCode](https://github.com/sst/opencode).
Skills are read directly from `.claude/skills/`; agents and commands are transpiled to
`.opencode/`.

> Source-of-truth lives under `plugins/`. The `.opencode/` tree and `opencode.json` are
> generated.

## Setup

```bash
gh repo clone wshobson/agents ~/agents
cd ~/agents
make generate HARNESS=opencode
bun add -g opencode-ai  # or: npm install -g opencode-ai
```

Then point OpenCode at this repo (or copy `.opencode/` and `opencode.json` into your
target project). Skills work automatically because OpenCode honors `.claude/skills/`.

## What you get

- **Skills**: read directly from `plugins/*/skills/` (OpenCode's `.claude/` compatibility).
  Toggle off with `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` if you want isolation.
- **Subagents**: every Claude Code agent transpiled to `.opencode/agents/<plugin>__<agent>.md`
  with `mode: subagent`, full provider-prefixed model ID, and a `permission:` block
  derived from the source `tools:` allowlist (deny-everything-else).
- **Commands**: `.opencode/commands/<plugin>__<command>.md` with lowercased tool refs
  and `subtask: true` when the command orchestrates subagents.

## What's different from Claude Code

| Capability | Claude Code | OpenCode |
|---|---|---|
| Tool name case | `Read`, `Bash`, `Grep` (CamelCase) | `read`, `bash`, `grep` (lowercase, strict) |
| Per-agent tool allowlist | `tools: Read, Grep` | `permission:` block (allow/ask/deny per key) |
| Model alias | `opus`/`sonnet`/`haiku` | `anthropic/claude-opus-4-7` (full provider path) |
| Agent mode | implicit | required: `mode: primary|subagent|all` |
| `TodoWrite` | yes | yes |
| `Task`/`Agent` spawn | yes | yes (as `task`) |

The `permission:` block is finer-grained than Claude Code's allowlist — every operation
(`read`/`edit`/`write`/`bash`/`grep`/`glob`/`task`/`skill`/`webfetch`/`websearch`/etc.) is
explicitly `allow`/`ask`/`deny`. The adapter derives this from the source `tools:` field.

## Plugins (TypeScript code modules)

OpenCode also has a TypeScript plugin format (`.opencode/plugin/*.ts`) for adding custom
tools, hooks, and chat handlers. That authoring path is **not currently bridged** by this
marketplace — it lives outside the markdown plugin convention. If you want to ship code
plugins, do so as a separate npm package.

## Regenerating

```bash
make generate HARNESS=opencode
make generate HARNESS=opencode PLUGIN=javascript-typescript
make clean-generated HARNESS=opencode && make generate HARNESS=opencode
```

## Authoring caveats

See `docs/authoring.md` for the cross-harness style guide.

- Don't write CamelCase tool refs in skill/agent body text — OpenCode is strict about
  lowercase. The adapter rewrites a conservative set, but be explicit from the start.
- If you set `tools:` in your agent frontmatter, the adapter generates a permission deny
  block for everything else. If you want unrestricted access, omit `tools:`.
- `.env` reads are denied by default in OpenCode — even if you grant `read` permission.
