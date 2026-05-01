# Dotnet Contribution

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `dotnet-architect` | sonnet | Expert .NET backend architect specializing in C#, ASP.NET Core, Entity Framework, Dapper, and enterprise application ... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `dotnet-backend-patterns` | Master C#/.NET backend development patterns for building robust APIs, MCP servers, and enterprise applications. Covers async/await, depen... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert .NET backend architect specializing in C#, ASP.NET Core, Entity Framework, Dapper, and enterprise application patterns" → activates `dotnet-architect`
- "Master C#/.NET backend development patterns for building robust APIs, MCP servers, and enterprise applications" → activates `dotnet-backend-patterns` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
