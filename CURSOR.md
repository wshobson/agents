# claude-agents for Cursor

Multi-harness plugin marketplace consumed by Cursor 2.5+. Skills and agents are loaded
directly from `.claude/` (which Cursor reads natively); the adapter adds Cursor's plugin
marketplace manifests and a small set of curated `.cursor/rules/*.mdc`.

> Source-of-truth lives under `plugins/`. The artifacts under `.cursor-plugin/` and
> `.cursor/rules/` are generated.

## Setup

```bash
gh repo clone wshobson/agents ~/agents
cd ~/agents
make generate HARNESS=cursor
```

Then in Cursor: **Settings → Plugins → Add Local Plugin Source**, point at the repo root.
The full bundle of 82 plugins will appear in the marketplace browser.

For per-project use, copy `.cursor/rules/` into the target project's repo (or symlink), or
use the `Add to Workspace` action from the plugin marketplace.

## What you get

- **Plugins**: a marketplace at `.cursor-plugin/marketplace.json` listing all 82 plugins,
  with per-plugin manifests at `.cursor-plugin/plugins/<name>.json`.
- **Skills & agents**: read directly from `plugins/*/skills/` and `plugins/*/agents/` via
  Cursor's native `.claude/` compatibility. No duplication.
- **Curated rules**: three hand-tuned `.cursor/rules/*.mdc` files for project conventions,
  Python tooling, and authoring guidance.

## What's different from Claude Code

| Capability | Claude Code | Cursor |
|---|---|---|
| Per-agent tool allowlist | `tools:` frontmatter | not honored (only `readonly: true`) |
| Agent `color:` | shown in UI | ignored |
| Bare model aliases | `opus`/`sonnet`/`haiku` | use `inherit` for portability |
| `TodoWrite` | yes | no equivalent |
| `Task`/`Agent` spawn | native | native (auto-delegate via agent description) |
| Marketplace | `.claude-plugin/` | `.cursor-plugin/` (mirrored) |

## MDC rule format

Cursor only honors three keys in `.cursor/rules/*.mdc` frontmatter:

```mdc
---
description: When this rule applies
globs: ["**/*.py"]      # optional, for auto-attach mode
alwaysApply: false      # optional; true = inject every prompt
---
```

Folklore keys like `agentRequested:`, `mode:`, or `tags:` are not real — the adapter
validates curated rules and rejects unknown keys.

## Regenerating

```bash
make generate HARNESS=cursor
make generate HARNESS=cursor PLUGIN=javascript-typescript
make clean-generated HARNESS=cursor && make generate HARNESS=cursor
```

## Authoring caveats

See `docs/authoring.md` for the cross-harness style guide.

- Don't add a `.cursor/agents/` mirror — Cursor reads `.claude/agents/` directly and
  emitting both causes double-loading.
- Always-apply rules are injected into every prompt — keep each under ~200 words. The
  three curated rules in this repo already follow that budget.
