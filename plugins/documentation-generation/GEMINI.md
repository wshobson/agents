# Documentation Generation

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `api-documenter` | sonnet | Master API documentation with OpenAPI 3.1, AI-powered tools, and modern developer experience practices. Create intera... |
| `docs-architect` | sonnet | Creates comprehensive technical documentation from existing codebases. Analyzes architecture, design patterns, and im... |
| `mermaid-expert` | haiku | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and ... |
| `reference-builder` | haiku | Creates exhaustive technical references and API documentation. Generates comprehensive parameter listings, configurat... |
| `tutorial-engineer` | sonnet | Creates step-by-step tutorials and educational content from code. Transforms complex concepts into progressive learni... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/documentation-generation:doc-generate` | Automated Documentation Generation |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `architecture-decision-records` | Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenti... |
| `changelog-automation` | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, g... |
| `openapi-spec-generation` | Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentat... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master API documentation with OpenAPI 3.1, AI-powered tools, and modern developer experience practices" → activates `api-documenter`
- "Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation" → activates `architecture-decision-records` skill
- In Claude Code: `/documentation-generation:doc-generate` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
