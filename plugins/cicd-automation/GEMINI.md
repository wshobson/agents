# Cicd Automation

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `cloud-architect` | opus | Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/O... |
| `deployment-engineer` | haiku | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automati... |
| `devops-troubleshooter` | sonnet | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. M... |
| `kubernetes-architect` | opus | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and... |
| `terraform-specialist` | opus | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructu... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/cicd-automation:workflow-automate` | Workflow Automation |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `deployment-pipeline-design` | Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Use this skill when designing zero... |
| `github-actions-templates` | Create production-ready GitHub Actions workflows for automated testing, building, and deploying applications. Use when setting up CI/CD w... |
| `gitlab-ci-patterns` | Build GitLab CI/CD pipelines with multi-stage workflows, caching, and distributed runners for scalable automation. Use when implementing ... |
| `secrets-management` | Implement secure secrets management for CI/CD pipelines using Vault, AWS Secrets Manager, or native platform solutions. Use when handling... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns" → activates `cloud-architect`
- "Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration" → activates `deployment-pipeline-design` skill
- In Claude Code: `/cicd-automation:workflow-automate` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
