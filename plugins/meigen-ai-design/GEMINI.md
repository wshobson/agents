# Meigen Ai Design

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `gallery-researcher` | haiku | >- Gallery search and inspiration agent. Delegates here when user wants to find references, explore styles, build a m... |
| `image-generator` | inherit | >- Image generation executor agent. Delegates here for ALL generate_image calls to keep the main conversation context... |
| `prompt-crafter` | haiku | >- Batch prompt writing agent. Delegates here when you need to write multiple distinct prompts at once — for parallel... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/meigen-ai-design:find` `<keywords>` | >- Quick gallery search. Use when user runs /meigen-ai-design:find with keywords to browse inspiration. |
| `/meigen-ai-design:gen` `<prompt>` | >- Quick image generation. Use when user runs /meigen-ai-design:gen with a prompt. Skips intent assessment, generates... |

## Gemini CLI Usage

**Example natural language triggers:**

- ">- Gallery search and inspiration agent" → activates `gallery-researcher`
- In Claude Code: `/meigen-ai-design:find` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
