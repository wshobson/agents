# Database Design

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `database-architect` | opus | Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and ... |
| `sql-pro` | inherit | Master modern SQL with cloud-native databases, OLTP/OLAP optimization, and advanced query techniques. Expert in perfo... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `postgresql-table-design` | Use this skill when designing or reviewing a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, perfor... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and scalable database architectures" → activates `database-architect`
- "Use this skill when designing or reviewing a PostgreSQL-specific schema" → activates `postgresql-table-design` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
