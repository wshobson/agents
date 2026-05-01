# Plugin Eval

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `eval-judge` | sonnet | LLM judge for plugin quality assessment. Scores skills on triggering accuracy, orchestration fitness, output quality,... |
| `eval-orchestrator` | opus | Orchestrates plugin quality evaluation. Use PROACTIVELY when evaluating, scoring, or certifying plugin quality. |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/plugin-eval:certify` `<path>` | Full quality certification with badge |
| `/plugin-eval:compare` `<skill-a> <skill-b>` | Compare two skills head-to-head |
| `/plugin-eval:eval` `<path> [--depth quick|standard]` | Evaluate a plugin or skill for quality |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `evaluation-methodology` | PluginEval quality methodology — dimensions, rubrics, statistical methods, and scoring formulas. Use this skill when understanding how pl... |

## Gemini CLI Usage

**Example natural language triggers:**

- "LLM judge for plugin quality assessment" → activates `eval-judge`
- "PluginEval quality methodology — dimensions, rubrics, statistical methods, and scoring formulas" → activates `evaluation-methodology` skill
- In Claude Code: `/plugin-eval:certify` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
