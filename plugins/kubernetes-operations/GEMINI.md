# Kubernetes Operations

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `kubernetes-architect` | opus | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `gitops-workflow` | Implement GitOps workflows with ArgoCD and Flux for automated, declarative Kubernetes deployments with continuous reconciliation. Use whe... |
| `helm-chart-scaffolding` | Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when crea... |
| `k8s-manifest-generator` | Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security sta... |
| `k8s-security-policies` | Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC for production-grade security. Use when secur... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration" → activates `kubernetes-architect`
- "Implement GitOps workflows with ArgoCD and Flux for automated, declarative Kubernetes deployments with continuous reconciliation" → activates `gitops-workflow` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
