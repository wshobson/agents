# Cloud Infrastructure

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `cloud-architect` | opus | Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/O... |
| `deployment-engineer` | haiku | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automati... |
| `hybrid-cloud-architect` | opus | Expert hybrid cloud architect specializing in complex multi-cloud solutions across AWS/Azure/GCP/OCI and private clou... |
| `kubernetes-architect` | opus | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and... |
| `network-engineer` | sonnet | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization... |
| `service-mesh-expert` | opus | Expert service mesh architect specializing in Istio, Linkerd, and cloud-native networking patterns. Masters traffic m... |
| `terraform-specialist` | opus | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructu... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `cost-optimization` | Optimize cloud costs across AWS, Azure, GCP, and OCI through resource rightsizing, tagging strategies, reserved instances, and spending a... |
| `hybrid-cloud-networking` | Configure secure, high-performance connectivity between on-premises infrastructure and cloud platforms using VPN and dedicated connection... |
| `istio-traffic-management` | Configure Istio traffic management including routing, load balancing, circuit breakers, and canary deployments. Use when implementing ser... |
| `linkerd-patterns` | Implement Linkerd service mesh patterns for lightweight, security-focused service mesh deployments. Use when setting up Linkerd, configur... |
| `mtls-configuration` | Configure mutual TLS (mTLS) for zero-trust service-to-service communication. Use when implementing zero-trust networking, certificate man... |
| `multi-cloud-architecture` | Design multi-cloud architectures using a decision framework to select and integrate services across AWS, Azure, GCP, and OCI. Use when bu... |
| `service-mesh-observability` | Implement comprehensive observability for service meshes including distributed tracing, metrics, and visualization. Use when setting up m... |
| `terraform-module-library` | Build reusable Terraform modules for AWS, Azure, GCP, and OCI infrastructure following infrastructure-as-code best practices. Use when cr... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert cloud architect specializing in AWS/Azure/GCP/OCI multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns" → activates `cloud-architect`
- "Optimize cloud costs across AWS, Azure, GCP, and OCI through resource rightsizing, tagging strategies, reserved instances, and spending analysis" → activates `cost-optimization` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
