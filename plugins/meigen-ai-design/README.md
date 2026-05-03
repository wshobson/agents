# MeiGen AI Design

AI image generation plugin with creative workflow orchestration, parallel multi-direction output, prompt engineering, and a 1,300+ curated inspiration library.

## Prerequisites

This plugin requires the **meigen** MCP server. Install it by adding to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "meigen": {
      "command": "npx",
      "args": ["-y", "meigen@1.2.13"]
    }
  }
}
```

**Restart Claude Code** after adding the configuration.

Requires Node.js 18+.

## Provider Setup

Configure at least one provider to enable image generation. **Free features** (gallery search, prompt enhancement, model listing, preference management) work without any provider configured.

### Option A: MeiGen Cloud (Recommended)

1. Sign up at [meigen.ai](https://www.meigen.ai)
2. Click avatar → Settings → API Keys → create a new key (starts with `meigen_sk_`)
3. Set environment variable:

```bash
export MEIGEN_API_TOKEN=meigen_sk_your_token_here
```

### Option B: Local ComfyUI (Free, Private)

1. Install and run [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
2. Set environment variable:

```bash
export COMFYUI_URL=http://localhost:8188
```

3. Export workflows from ComfyUI (API format JSON) and import via the plugin

### Option C: OpenAI-compatible API (Bring Your Own Key)

Works with any OpenAI-compatible image generation API (OpenAI, Together AI, Fireworks AI, etc.):

```bash
export OPENAI_API_KEY=your_key_here
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_MODEL=gpt-image-1
```

Alternatively, store configuration in `~/.config/meigen/config.json`.

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `gallery-researcher` | haiku | Search 1,300+ curated gallery, find references, build mood boards |
| `prompt-crafter` | haiku | Write multiple distinct prompts for parallel image generation |
| `image-generator` | inherit | Execute `generate_image` calls and relay results |

## Commands

| Command | Description |
|---------|-------------|
| `/meigen-ai-design:gen <prompt>` | Quick image generation — skips intent assessment |
| `/meigen-ai-design:find <keywords>` | Quick gallery search — browse inspiration |

## Free Features (No API Key)

These tools work immediately without any provider setup:
- **search_gallery** — Search 1,300+ curated AI image prompts
- **enhance_prompt** — Expand brief descriptions into detailed generation prompts
- **list_models** — List available models across all configured providers
- **manage_preferences** — Save default style, aspect ratio, and favorite prompts

## Verification

After setup, test with a free feature:
> "Search the gallery for product photography inspiration"

Then test generation:
> "Generate a product photo for a glass perfume bottle on marble"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MCP tools not available | Restart Claude Code after adding `.mcp.json` configuration |
| "No image generation providers configured" | Configure at least one provider (see Provider Setup above) |
| API key / authentication errors | Verify env vars or check `~/.config/meigen/config.json` |
| ComfyUI connection refused | Ensure ComfyUI is running at the configured URL |
| Generation timeout | Server may be under high load — try again in a moment |
| Empty gallery search results | Try different keywords or broader terms |

## Links

- [npm package](https://www.npmjs.com/package/meigen)
- [GitHub](https://github.com/jau123/MeiGen-AI-Design-MCP)
- [Homepage](https://www.meigen.ai)
- [Demo Video](https://youtu.be/JQ3DZ1DXqvs)

## License

MIT
