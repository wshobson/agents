# Seo Technical Optimization

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `seo-keyword-strategist` | haiku | Analyzes keyword usage in provided content, calculates density, suggests semantic variations and LSI keywords based o... |
| `seo-meta-optimizer` | haiku | Creates optimized meta titles, descriptions, and URL suggestions based on character limits and best practices. Genera... |
| `seo-snippet-hunter` | haiku | Formats content to be eligible for featured snippets and SERP features. Creates snippet-optimized content blocks base... |
| `seo-structure-architect` | haiku | Analyzes and optimizes content structure including header hierarchy, suggests schema markup, and internal linking opp... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Analyzes keyword usage in provided content, calculates density, suggests semantic variations and LSI keywords based on the topic" → activates `seo-keyword-strategist`

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
