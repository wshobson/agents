# Backend Development

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `backend-architect` | inherit | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. Ma... |
| `event-sourcing-architect` | inherit | Expert in event sourcing, CQRS, and event-driven architecture patterns. Masters event store design, projection buildi... |
| `graphql-architect` | opus | Master modern GraphQL with federation, performance optimization, and enterprise security. Build scalable schemas, imp... |
| `performance-engineer` | sonnet | Profile and optimize application performance including response times, memory usage, query efficiency, and scalabilit... |
| `security-auditor` | sonnet | Review code and architecture for security vulnerabilities, OWASP Top 10, auth flaws, and compliance issues. Use for s... |
| `tdd-orchestrator` | opus | Master TDD orchestrator specializing in red-green-refactor discipline, multi-agent workflow coordination, and compreh... |
| `temporal-python-pro` | inherit | Master Temporal workflow orchestration with Python SDK. Implements durable workflows, saga patterns, and distributed ... |
| `test-automator` | sonnet | Create comprehensive test suites including unit, integration, and E2E tests. Supports TDD/BDD workflows. Use for test... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/backend-development:feature-development` `<feature description> [--methodology tdd|bdd|ddd] [--complexity simple|medium|complex]` | Orchestrate end-to-end feature development from requirements to deployment |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `api-design-principles` | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when desig... |
| `architecture-patterns` | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use this s... |
| `cqrs-implementation` | Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing quer... |
| `event-store-design` | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store techno... |
| `microservices-patterns` | Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distri... |
| `projection-patterns` | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing q... |
| `saga-orchestration` | Implement saga patterns for distributed transactions and cross-aggregate workflows. Use this skill when implementing distributed transact... |
| `temporal-python-testing` | Test Temporal workflows with pytest, time-skipping, and mocking strategies. Covers unit testing, integration testing, replay testing, and... |
| `workflow-orchestration-patterns` | Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, ... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems" → activates `backend-architect`
- "Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers" → activates `api-design-principles` skill
- In Claude Code: `/backend-development:feature-development` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
