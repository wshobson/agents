# Seo Analysis Monitoring

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `seo-authority-builder` | sonnet | Analyzes content for E-E-A-T signals and suggests improvements to build authority and trust. Identifies missing credi... |
| `seo-cannibalization-detector` | haiku | Analyzes multiple provided pages to identify keyword overlap and potential cannibalization issues. Suggests different... |
| `seo-content-refresher` | haiku | Identifies outdated elements in provided content and suggests updates to maintain freshness. Finds statistics, dates,... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Analyzes content for E-E-A-T signals and suggests improvements to build authority and trust" → activates `seo-authority-builder`

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
