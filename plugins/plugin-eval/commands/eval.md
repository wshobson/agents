---
description: Evaluate a plugin or skill for quality
argument-hint: <path> [--depth quick|standard|deep]
---

Run the PluginEval quality evaluation on a plugin or skill directory.

## Usage

/eval <path> — evaluate at standard depth (Layers 1+2)
/eval <path> --depth quick — static analysis only (instant)
/eval <path> --depth deep — full evaluation with Monte Carlo (15-20 min)

## What It Does

1. Parses the plugin/skill structure (frontmatter, sections, references)
2. Runs static analysis for anti-patterns and structural quality
3. At standard+ depth: LLM judge assesses triggering, orchestration, output quality, scope
4. At deep+ depth: Monte Carlo simulation measures statistical reliability
5. Produces a composite score (0-100), dimension breakdown, and quality badge

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval score {argument} --depth standard --output markdown
```
