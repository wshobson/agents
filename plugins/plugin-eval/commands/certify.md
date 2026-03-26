---
description: Full quality certification with badge
argument-hint: <path>
---

Run the complete PluginEval certification pipeline (all three layers + Elo ranking) and assign a quality badge.

This takes 15-20 minutes and uses your Max plan for all LLM calls.

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval certify {argument} --output markdown
```
