---
description: Full quality certification with badge
argument-hint: <path>
---

Run PluginEval at deep depth and assign a quality badge. For a skill directory, deep depth runs the static layer plus the experimental LLM judge and Monte Carlo layers. For a plugin directory, only the static layer runs.

This takes 15-20 minutes and uses your Max plan for all LLM calls.

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval certify {argument} --output markdown
```
