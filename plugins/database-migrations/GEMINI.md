# Database Migrations

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `database-admin` | sonnet | Expert database administrator specializing in modern cloud databases, automation, and reliability engineering. Master... |
| `database-optimizer` | inherit | Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures. ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/database-migrations:migration-observability` | Migration monitoring, CDC, and observability infrastructure |
| `/database-migrations:sql-migrations` | SQL database migrations with zero-downtime strategies for PostgreSQL, MySQL, SQL Server |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert database administrator specializing in modern cloud databases, automation, and reliability engineering" → activates `database-admin`
- In Claude Code: `/database-migrations:migration-observability` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
