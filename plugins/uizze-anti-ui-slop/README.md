# UIZZE anti-ui-slop

Stop coding agents from shipping generic UI. This portable workflow grounds web
and iOS interface decisions in 800,000+ real screens, then applies a
product-specific design contract, required interaction states, and a hard
finish gate before shipping.

## Skill

- `anti-ui-slop` — use before designing or reviewing web and iOS UI, and before
  declaring an agent-built interface finished.

## Installation

### Claude Code and Cursor

```text
/plugin install uizze-anti-ui-slop
```

Run that command after adding `wshobson/agents` as a marketplace. It applies to
Claude Code and Cursor. Codex CLI, OpenCode, Gemini CLI, and GitHub Copilot use
their own native install paths. Follow the repository's
[cross-harness installation guide](../../docs/harnesses.md) for those clients.

The free workflow does not require an account. The optional UIZZE preview MCP is
available at https://uizze.com/mcp/preview and must not be treated as connected
unless its tools are actually available. If you use it, send only sanitized
rendered HTML or CSS that the user explicitly approved. Remove scripts, event
handlers, credentials, tokens, cookies, private URLs, user data, and source maps.
If approval or sanitization is unavailable, run the local finish gate instead.

## License

MIT. Canonical source: https://github.com/uizze/uizze
