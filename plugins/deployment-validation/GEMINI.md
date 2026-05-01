# Deployment Validation

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `cloud-architect` | sonnet | Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/O... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/deployment-validation:config-validate` | Configuration Validation |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns" → activates `cloud-architect`
- In Claude Code: `/deployment-validation:config-validate` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
