# Deployment Strategies

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `deployment-engineer` | haiku | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automati... |
| `terraform-specialist` | opus | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructu... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation" → activates `deployment-engineer`

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
