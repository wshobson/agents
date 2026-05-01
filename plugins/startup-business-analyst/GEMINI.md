# Startup Business Analyst

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `startup-analyst` | inherit | Expert startup business analyst specializing in market sizing, financial modeling, competitive analysis, and strategi... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/startup-business-analyst:business-case` | Generate comprehensive investor-ready business case document with market, solution, financials, and strategy |
| `/startup-business-analyst:financial-projections` | Create detailed 3-5 year financial model with revenue, costs, cash flow, and scenarios |
| `/startup-business-analyst:market-opportunity` | Generate comprehensive market opportunity analysis with TAM/SAM/SOM calculations |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `competitive-landscape` | Analyze competition, identify differentiation opportunities, and develop winning market positioning strategies using Porter's Five Forces... |
| `market-sizing-analysis` | Calculate TAM/SAM/SOM for market opportunities using top-down, bottom-up, and value theory methodologies. Use this skill when sizing mark... |
| `startup-financial-modeling` | Build comprehensive 3-5 year financial models with revenue projections, cost structures, cash flow analysis, and scenario planning for ea... |
| `startup-metrics-framework` | Track, calculate, and optimize key performance metrics for SaaS, marketplace, consumer, and B2B startups from seed through Series A, incl... |
| `team-composition-analysis` | Design optimal team structures, hiring plans, compensation strategies, and equity allocation for early-stage startups from pre-seed throu... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert startup business analyst specializing in market sizing, financial modeling, competitive analysis, and strategic planning for early-stage companies" → activates `startup-analyst`
- "Analyze competition, identify differentiation opportunities, and develop winning market positioning strategies using Porter's Five Forces, Blue Ocean Strategy, and positioning maps" → activates `competitive-landscape` skill
- In Claude Code: `/startup-business-analyst:business-case` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
