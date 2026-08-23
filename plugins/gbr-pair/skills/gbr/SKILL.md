---
name: gbr
description: >
  Pair a phone running Build Remote Agent to this desktop AI agent.
  Requires gbr-agent run on the host. Attach via Bot API 127.0.0.1:8788 or gbr-mcp.
  Use when the user wants mobile spectator / inject into this CLI or Cursor session.
---

# Build Remote Agent — pairing device

One adapter. Protocol `gbr/1`. No fourth pair protocol.

Independent product by Linespotting AB. Not affiliated with xAI or SpaceX.

## Pair (unchanged)

1. Phone: [Build Remote Agent](https://grokbuildremote.com/) → Connect.
2. PC: `gbr-agent pair` — browser QR **and** printed 8-char code.
3. Phone scans QR **or** types the 8-char code.
4. PC: `gbr-agent run` (keep it running).

```bash
curl -fsSL https://grokbuildremote.com/install.sh | bash
gbr-agent version    # need v0.6.0+
gbr-agent pair && gbr-agent run
```

Unpair on the phone before a new mailbox. Force-close is not enough.

## Attach (only these)

| How | Where |
|-----|--------|
| Bot API | `http://127.0.0.1:8788` after `gbr-agent run` |
| MCP | `gbr-mcp` stdio (same JSON as Bot API) |

Phone is spectator + veto, not orchestrator.

```bash
curl -sS http://127.0.0.1:8788/health
curl -sS http://127.0.0.1:8788/v1/sessions
```

## MCP

```bash
git clone https://github.com/LinespottingOrg/GrokBuildRemote-Agents.git
cd GrokBuildRemote-Agents/mcp/gbr-mcp && npm install
node bin/gbr-mcp.js --diagnose
```

Remote bots: phone **Settings → Bot API** copies relay URL + mailbox id + key. Never commit the key.

## Loop

diagnose → open/attach → lock → inject → wait idle → harvest excerpt → iterate or close

Docs: https://github.com/LinespottingOrg/GrokBuildRemote-Agents/blob/main/docs/BOT-API.md
