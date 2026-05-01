# Seo Content Creation

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `seo-content-auditor` | sonnet | Analyzes provided content for quality, E-E-A-T signals, and SEO best practices. Scores content and provides improveme... |
| `seo-content-planner` | haiku | Creates comprehensive content outlines and topic clusters for SEO. Plans content calendars and identifies topic gaps.... |
| `seo-content-writer` | sonnet | Writes SEO-optimized content based on provided keywords and topic briefs. Creates engaging, comprehensive content fol... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Analyzes provided content for quality, E-E-A-T signals, and SEO best practices" → activates `seo-content-auditor`

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
