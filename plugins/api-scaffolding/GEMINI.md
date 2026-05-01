# Api Scaffolding

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `backend-architect` | inherit | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. Ma... |
| `django-pro` | opus | Master Django 5.x with async views, DRF, Celery, and Django Channels. Build scalable web applications with proper arc... |
| `fastapi-pro` | opus | Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, an... |
| `graphql-architect` | opus | Master modern GraphQL with federation, performance optimization, and enterprise security. Build scalable schemas, imp... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `fastapi-templates` | Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building n... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems" → activates `backend-architect`
- "Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling" → activates `fastapi-templates` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
