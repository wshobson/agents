@AGENTS.md

## Claude Code

This file imports the canonical [`AGENTS.md`](AGENTS.md) (Anthropic's [recommended pattern](https://code.claude.com/docs/en/memory#agentsmd-interop) for repos that adopt the cross-harness convention). Any Claude-Code-specific addenda live below.

### Native features unique to Claude Code

- **Per-agent tool allowlist** — `tools:` frontmatter honored verbatim (Cursor / Codex are coarser; the OpenCode adapter translates this into a `permission:` block).
- **`Task` / `Agent` spawn tool** — fan-out parallel subagent execution. (Codex requires naming an agent in prose to delegate.)
- **`TodoWrite`** — native progress tracking. (Not available in Codex / Cursor / Gemini.)
- **Slash-command marketplace** — full `/plugin install`, `/plugin marketplace` workflow.

### Claude-Code-only paths

- `.claude-plugin/marketplace.json` — plugin registry (source of truth)
- `plugins/<name>/.claude-plugin/plugin.json` — per-plugin manifest

All other working conventions, quality gates, and component models are described in `AGENTS.md` above.
