# RunAPI MCP

AI image generation, video generation, music creation, text-to-speech, and LLM chat — 130+ models from Flux, Kling, Seedance, Veo, Suno, ElevenLabs, Claude, GPT, Gemini, and 18 providers in one MCP server.

## Install

```bash
# Claude Code
/plugin install runapi-mcp@agents

# Codex
codex plugin install runapi-mcp@agents
```

Or add manually to `.mcp.json`:

```json
{
  "mcpServers": {
    "runapi": {
      "command": "npx",
      "args": ["-y", "@runapi.ai/mcp@0.1.8"]
    }
  }
}
```

## Setup

1. Sign up at [runapi.ai](https://runapi.ai) and go to Dashboard > API Keys
2. Save your key:
   ```bash
   mkdir -p ~/.config/runapi && echo '{"api_key":"YOUR_KEY"}' > ~/.config/runapi/config.json
   ```
3. Restart your MCP host

Free catalog tools (model browsing, pricing) work without a key.

## Tools

| Tool | Auth | Description |
|---|---|---|
| list_models | Free | Browse 130+ AI models by modality, service, or action |
| get_model_info | Free | Inspect params, constraints, and pricing for a model |
| list_actions | Free | List endpoint actions grouped by modality |
| check_pricing | Free | Check pricing for a service + action + model |
| check_balance | Key | Check account balance and spending |
| create_task | Key | Create image/video/music/audio tasks, optionally poll until done |
| get_task | Key | Check status of an existing task |
| chat | Key | Call Claude, GPT, Gemini, DeepSeek LLM endpoints |

## Links

- [GitHub](https://github.com/runapi-ai/mcp)
- [npm](https://www.npmjs.com/package/@runapi.ai/mcp)
- [Pricing](https://runapi.ai/pricing)
