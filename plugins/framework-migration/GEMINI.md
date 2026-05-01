# Framework Migration

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `architect-review` | opus | Master software architect specializing in modern architecture patterns, clean architecture, microservices, event-driv... |
| `legacy-modernizer` | sonnet | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/framework-migration:code-migrate` | Generate comprehensive migration plans and scripts for transitioning codebases between frameworks, languages, version... |
| `/framework-migration:deps-upgrade` | Plan and execute safe, incremental dependency upgrades with minimal risk — including breaking-change migration paths ... |
| `/framework-migration:legacy-modernize` `<legacy codebase path or description> [--strategy parallel-systems|big-bang|by-feature|database-first|api-first]` | Orchestrate legacy system modernization using the strangler fig pattern with gradual component replacement |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `angular-migration` | Migrate from AngularJS to Angular using hybrid mode, incremental component rewriting, and dependency injection updates. Use when upgradin... |
| `database-migration` | Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use wh... |
| `dependency-upgrade` | Manage major dependency version upgrades with compatibility analysis, staged rollout, and comprehensive testing. Use when upgrading frame... |
| `react-modernization` | Upgrade React applications to latest versions, migrate from class components to hooks, and adopt concurrent features. Use when modernizin... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master software architect specializing in modern architecture patterns, clean architecture, microservices, event-driven systems, and DDD" → activates `architect-review`
- "Migrate from AngularJS to Angular using hybrid mode, incremental component rewriting, and dependency injection updates" → activates `angular-migration` skill
- In Claude Code: `/framework-migration:code-migrate` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
