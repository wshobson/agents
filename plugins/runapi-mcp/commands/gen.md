---
description: >-
  Quick RunAPI generation. Use when the user runs /runapi:gen with a prompt
  and wants to skip broad exploration.
argument-hint: <prompt>
---

# Quick Generate

Create a RunAPI media task from `$ARGUMENTS`.

## Instructions

1. If `$ARGUMENTS` is empty, ask for the prompt or task description.
2. Call `mcp__runapi__list_models` with the most likely modality filter.
3. Call `mcp__runapi__get_model_info` with the selected service, action, and model slug, then obey returned input rules.
4. If the selected task is video, music, or a batch, ask for confirmation before creating it.
5. Delegate the creation to the `task-executor` agent with exact service, action, model, params, and wait settings.
6. Present task ID, status, output URLs, and cost fields when available.

Do not invent model slugs.
Do not quote prices without `mcp__runapi__check_pricing`.
Do not describe generated media content.
