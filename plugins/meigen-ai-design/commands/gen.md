---
name: gen
description: >-
  Quick image generation. Use when user runs /meigen:gen with a prompt.
  Skips intent assessment, generates directly.
argument-hint: <prompt>
---

# Quick Generate

Generate an image immediately from the user's description. This is the fast path — skip exploration and go straight to generation.

## Instructions

1. Look at the user's prompt: `$ARGUMENTS`
2. If the prompt is very short (under 10 words), call `enhance_prompt` first to enrich it, then use the enhanced result
3. If the prompt is already detailed (10+ words), use it directly
4. Delegate to the **image-generator** agent with the prompt (keeps base64 data out of main context)
5. When the agent returns, show a brief one-line creative comment about the generation

Do NOT:
- Ask for confirmation before generating
- Suggest alternatives or options
- Run search_gallery for references
- Give lengthy explanations or describe the image
- Call generate_image directly — always delegate to image-generator agent

This is a quick-fire command. Generate and show.
