---
description: >-
  Guide the user through RunAPI API key setup for Claude Code and other MCP
  hosts.
argument-hint: ""
---

# RunAPI Setup

Guide the user through local RunAPI MCP configuration.

## Instructions

1. Explain that free catalog tools work without a key.
2. Explain that `create_task`, `get_task`, `check_balance`, and `chat` require `RUNAPI_API_KEY`.
3. Tell the user to create a key in the RunAPI dashboard.
4. Show one setup option:

```bash
export RUNAPI_API_KEY="your_runapi_key"
```

5. If they prefer a config file, show:

```json
{
  "apiKey": "your_runapi_key"
}
```

stored at `~/.config/runapi/config.json`.

6. Tell them to restart the MCP host after changing environment variables.

Do not ask the user to paste the key into the conversation.
Do not run shell commands unless the user explicitly asks.
