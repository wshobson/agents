# MeiGen AI Design

Find visual inspiration, create images and videos, and reuse your MeiGen favorites, boards and generation history through the hosted MCP service.

## Connect

This plugin includes a native HTTP MCP connection to `https://www.meigen.ai/api/mcp`. In Claude Code, use `/mcp` to authenticate MeiGen and complete browser sign-in. New connections do not need Node.js, npm or an API key. Tools update on the server; this package supplies the connection and optional creative helpers.

Other hosts must support HTTP MCP and OAuth. If a host does not load the bundled `.mcp.json`, add that URL through its MCP connection settings and sign in. Generated helper files alone do not establish a connection. Interactive pages appear only in hosts supporting MCP Apps; other hosts receive tool text and result URLs.

Before upgrading from 1.x, inspect existing MeiGen connections privately. A saved stdio/API-key/BYOK entry may take precedence. Back up its configuration and credentials, deliberately choose remote OAuth, then keep one active MeiGen connection. Do not silently change the provider or billing account. Legacy BYOK and local-file handling remain on `meigen@3.4.0`; ComfyUI requires the older release that supplied it. See the [migration guide](https://github.com/jau123/MeiGen-AI-Design-MCP/blob/main/MIGRATION.md).

## Use

| Command | Purpose |
| --- | --- |
| `/meigen-ai-design:find <keywords>` | Search visual inspiration |
| `/meigen-ai-design:gen <prompt>` | Generate with the supplied prompt and choices |

The gallery-researcher, prompt-crafter and image-generator helpers are optional. Direct tool calls are supported; existing prompts and approved output scope are preserved.

Use live `list_models` and `list_skills` for current parameters, availability and prices. Image/video generation and the five image workflows use purchased credits only, not daily free credits. Favorites, boards, history and characters require the relevant OAuth permissions. Saving requires a user request or prior opt-in.

## Verify and recover

Call `list_models` or `list_skills` without generating or uploading to verify connectivity; this does not prove private-account access. Authenticate through the host for protected tools. Never paste passwords or keys into chat.

Keep each request ID and use `check_generation` or `check_skill` after an interrupted submission. Do not create another paid job just to check status. The remote service returns URLs and cannot read local paths; use a supported upload or accessible reference URL. Uploaded references receive public URLs. Downloading and display depend on the host.

[Connection guide](https://github.com/jau123/MeiGen-AI-Design-MCP/blob/main/SETUP.md) · [Source](https://github.com/jau123/MeiGen-AI-Design-MCP) · [MeiGen](https://www.meigen.ai)

MIT
