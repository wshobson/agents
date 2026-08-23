# gbr-pair — Build Remote Agent

Pair a phone running **Build Remote Agent** to a desktop agent session in this marketplace (Cursor, Claude Code, Codex, Antigravity CLI).

Protocol `gbr/1`. Phone is spectator + veto, not orchestrator.

Independent product by Linespotting AB. Not affiliated with xAI or SpaceX.

Website: https://grokbuildremote.com/  
Agent (MIT): https://github.com/LinespottingOrg/GrokBuildRemote-Agents

## Install + pair

```bash
curl -fsSL https://grokbuildremote.com/install.sh | bash   # Windows: irm https://grokbuildremote.com/install.ps1 | iex
gbr-agent version    # need v0.6.0+
gbr-agent pair && gbr-agent run
```

Phone: open Build Remote Agent → scan the QR **or** type the printed 8-char code. Unpair on the phone before a new mailbox.

## Attach (only these)

| How | Where |
|-----|--------|
| Bot API | `http://127.0.0.1:8788` after `gbr-agent run` |
| MCP | stdio `gbr-mcp` (`GrokBuildRemote-Agents/mcp/gbr-mcp`) |

```bash
curl -sS http://127.0.0.1:8788/health
curl -sS http://127.0.0.1:8788/v1/sessions
```

Do not commit mailbox keys. Phone **Settings → Bot API** is the only place the relay key is copied.

Skill: `skills/gbr/SKILL.md`.
