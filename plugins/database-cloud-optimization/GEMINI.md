# Database Cloud Optimization

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `backend-architect` | inherit | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. Ma... |
| `cloud-architect` | sonnet | Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/O... |
| `database-architect` | inherit | Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and ... |
| `database-optimizer` | inherit | Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures. ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/database-cloud-optimization:cost-optimize` | Cloud Cost Optimization |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems" → activates `backend-architect`
- In Claude Code: `/database-cloud-optimization:cost-optimize` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
