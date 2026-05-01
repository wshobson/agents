# Python Development

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `django-pro` | opus | Master Django 5.x with async views, DRF, Celery, and Django Channels. Build scalable web applications with proper arc... |
| `fastapi-pro` | opus | Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, an... |
| `python-pro` | opus | Master Python 3.12+ with modern features, async programming, performance optimization, and production-ready practices... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/python-development:python-scaffold` | Python Project Scaffolding |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `async-python-patterns` | Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, ... |
| `python-anti-patterns` | Use this skill when reviewing Python code for common anti-patterns to avoid. Use as a checklist when reviewing code, before finalizing im... |
| `python-background-jobs` | Python background job patterns including task queues, workers, and event-driven architecture. Use when implementing async task processing... |
| `python-code-style` | Python code style, linting, formatting, naming conventions, and documentation standards. Use when writing new code, reviewing style, conf... |
| `python-configuration` | Python configuration management via environment variables and typed settings. Use when externalizing config, setting up pydantic-settings... |
| `python-design-patterns` | Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance. Use this skill wh... |
| `python-error-handling` | Python error handling patterns including input validation, exception hierarchies, and partial failure handling. Use when implementing val... |
| `python-observability` | Python observability patterns including structured logging, metrics, and distributed tracing. Use when adding logging, implementing metri... |
| `python-packaging` | Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI. Use when packaging P... |
| `python-performance-optimization` | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, o... |
| `python-project-structure` | Python project organization, module architecture, and public API design. Use when setting up new projects, organizing modules, defining p... |
| `python-resilience` | Python resilience patterns including automatic retries, exponential backoff, timeouts, and fault-tolerant decorators. Use when adding ret... |
| `python-resource-management` | Python resource management with context managers, cleanup patterns, and streaming. Use when managing connections, file handles, implement... |
| `python-testing-patterns` | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, se... |
| `python-type-safety` | Python type safety with type hints, generics, protocols, and strict type checking. Use when adding type annotations, implementing generic... |
| `uv-package-manager` | Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows. Use when ... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master Django 5.x with async views, DRF, Celery, and Django Channels" → activates `django-pro`
- "Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications" → activates `async-python-patterns` skill
- In Claude Code: `/python-development:python-scaffold` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
