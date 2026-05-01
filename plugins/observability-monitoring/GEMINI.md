# Observability Monitoring

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `database-optimizer` | inherit | Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures. ... |
| `network-engineer` | sonnet | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization... |
| `observability-engineer` | inherit | Build production-ready monitoring, logging, and tracing systems. Implements comprehensive observability strategies, S... |
| `performance-engineer` | inherit | Expert performance engineer specializing in modern observability, application optimization, and scalable system perfo... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/observability-monitoring:monitor-setup` | Monitoring and Observability Setup |
| `/observability-monitoring:slo-implement` | SLO Implementation Guide |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `distributed-tracing` | Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks. Use when... |
| `grafana-dashboards` | Create and manage production Grafana dashboards for real-time visualization of system and application metrics. Use when building monitori... |
| `prometheus-configuration` | Set up Prometheus for comprehensive metric collection, storage, and monitoring of infrastructure and applications. Use when implementing ... |
| `slo-implementation` | Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Use when establ... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures" → activates `database-optimizer`
- "Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks" → activates `distributed-tracing` skill
- In Claude Code: `/observability-monitoring:monitor-setup` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
