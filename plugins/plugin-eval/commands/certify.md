---
description: Full quality certification with badge
argument-hint: <path>
---

Run PluginEval at deep depth and assign a quality badge. For a skill directory, deep depth runs the static layer plus the experimental LLM judge and Monte Carlo layers. For a plugin directory, only the static layer runs.

For a skill, this makes 55 model calls through your Max plan. For a plugin directory, it makes none.

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval certify {argument} --output markdown
```
