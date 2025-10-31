# Kubernetes GitOps Setup

Set up complete GitOps infrastructure with ArgoCD or Flux CD for declarative, Git-driven Kubernetes deployments across multi-cluster environments:

[Extended thinking: This command establishes production-grade GitOps infrastructure following OpenGitOps principles. It sets up the GitOps tool (ArgoCD or Flux), configures repository structure, implements secret management, establishes sync policies, sets up progressive delivery strategies, and configures monitoring and alerts. The workflow supports single-cluster and multi-cluster scenarios with proper RBAC, access control, and audit logging. Each phase ensures security, reliability, and operational visibility.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### GitOps Platform
- **argocd**: ArgoCd with declarative applications, advanced sync policies, and web UI
- **flux**: Flux v2 with GitRepository and Kustomization resources, lighter footprint
- **jenkins-x**: Enterprise GitOps with pipeline automation and promotion

### Deployment Strategy
- **kustomize**: Kubernetes-native templating with overlays per environment
- **helm**: Helm charts with values files per environment
- **mixed**: Combination of Helm and Kustomize where appropriate

### Repository Structure
- **mono-repo**: Single repository for all applications and infrastructure
- **multi-repo**: Separate repos per application with centralized infrastructure
- **hierarchical**: Organization repos (apps) + environment repos (deployments)

### Cluster Scope
- **single-cluster**: Single Kubernetes cluster GitOps setup
- **multi-cluster**: Multi-cluster management with hub-and-spoke pattern
- **multi-tenancy**: Multi-tenant GitOps with namespace isolation

### Secret Management
- **external-secrets**: External Secrets Operator with secret backend integration
- **sealed-secrets**: Sealed Secrets for encrypting secrets in Git
- **vault**: HashiCorp Vault integration for secret management
- **cloud-native**: Native cloud provider secret services (AWS Secrets Manager, Azure KeyVault)

## Phase 1: GitOps Infrastructure Setup

1. **Assess Requirements & Design**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Assess GitOps requirements for: $ARGUMENTS. Determine: cluster scope ($CLUSTER_SCOPE), deployment strategy ($DEPLOYMENT_STRATEGY), secret management approach ($SECRET_MANAGEMENT). Design GitOps architecture: repository structure ($REPOSITORY_STRUCTURE), sync policies, RBAC strategy, multi-cluster if needed. Create architecture document with components, data flows, and decision rationale."
   - Expected output: GitOps architecture design document
   - Context: Current Kubernetes setup, deployment requirements

2. **Prepare Git Repository**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Prepare Git repository structure for GitOps: $ARGUMENTS. Using repository pattern: $REPOSITORY_STRUCTURE. Create: base directory structure for $DEPLOYMENT_STRATEGY, environment overlays (dev/staging/prod), infrastructure-as-code templates, secrets encryption setup. Create branch protection rules, CODEOWNERS file, contribution guidelines. Set up webhook integration for GitOps tool."
   - Expected output: Structured Git repository, documentation
   - Context: Repository pattern, deployment strategy

3. **Install GitOps Tool**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Install and configure GitOps tool: $GITOPS_PLATFORM on cluster: $ARGUMENTS. Configure: service account and RBAC for the tool, storage backend (Redis for ArgoCD), ingress with TLS for web UI. Set up authentication (OIDC/SAML/native). Configure high availability if production. Create initial admin credentials and documentation. Test connectivity to Git repository."
   - Expected output: GitOps tool installed and operational
   - Context: Kubernetes cluster, GitOps platform choice

4. **Configure Secret Management**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Set up secret management: $SECRET_MANAGEMENT for GitOps: $ARGUMENTS. If External Secrets: install operator, configure SecretStore connections to secret backends, create ExternalSecret resources. If Sealed Secrets: install controller, configure sealing key storage and backup. If Vault: configure authentication, create policy for applications. If cloud-native: configure workload identity/IRSA. Implement secret rotation policies and audit logging."
   - Expected output: Secret management system operational
   - Context: Secret management choice, GitOps setup

## Phase 2: Repository & Application Structure

5. **Create Repository Structure**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Implement repository structure for: $ARGUMENTS. Using pattern: $REPOSITORY_STRUCTURE and strategy: $DEPLOYMENT_STRATEGY. Create: apps/ directory with application Helm charts/Kustomize bases, environments/ with dev/staging/prod overlays, infrastructure/ for platform components, docs/ with architecture and runbooks. Create YAML templates for Apps (ArgoCD) or Kustomizations (Flux). Implement consistency validation (policies, linting)."
   - Expected output: Complete repository structure with templates
   - Context: Repository pattern, deployment strategy

6. **Set Up Environment Overlays**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Create environment overlays for: $ARGUMENTS using strategy: $DEPLOYMENT_STRATEGY. For each environment (development/staging/production): create overlay directory with resource customization (replicas, resource limits, ingress hosts). Configure environment-specific secrets, configmaps, and namespaces. Implement kustomization.yaml or values-{env}.yaml with environment-specific parameters. Include environment-specific sync policies and approval gates."
   - Expected output: Environment overlay structure
   - Context: Deployment strategy, environments

7. **Configure GitOps Applications**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure GitOps applications for: $ARGUMENTS using $GITOPS_PLATFORM. Create: Application manifests (ArgoCD) or Kustomization resources (Flux) for each service. Configure: source repository, target revisions, sync policies (automated/manual), prune and selfHeal settings, notification webhooks. Set up health checks for custom resources. Implement sync waves for ordered deployment. Configure destination namespaces and RBAC per application."
   - Expected output: Application definitions ready for deployment
   - Context: GitOps tool, application structure

## Phase 3: Progressive Delivery & Multi-Cluster

8. **Implement Progressive Delivery**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Set up progressive delivery for: $ARGUMENTS using $GITOPS_PLATFORM. Implement: canary deployments via Argo Rollouts or Flagger, analysis metrics from Prometheus/DataDog, traffic splitting via service mesh (Istio/Linkerd) or ingress controller. Create: stages for canary (10%->50%->100% traffic), rollback triggers on error rate/latency thresholds. Configure feature flags integration for controlled rollout. Document promotion criteria between environments."
   - Expected output: Progressive delivery setup with automation
   - Context: GitOps setup, deployment strategy

9. **Configure Multi-Cluster Management**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure multi-cluster GitOps for: $ARGUMENTS using $GITOPS_PLATFORM. If $CLUSTER_SCOPE is multi-cluster: set up hub cluster with central ArgoCD/Flux, register spoke clusters as deployment targets. Configure: cluster authentication, cluster secrets for kubeconfig, cluster labels for targeting. Implement cluster-specific overlays for different cloud providers/regions. Set up cross-cluster networking and secret synchronization. Configure disaster recovery with multi-region failover."
   - Expected output: Multi-cluster GitOps configuration
   - Context: Cluster scope, GitOps platform

10. **Set Up Notifications & Observability**
    - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
    - Prompt: "Configure notifications and observability for: $ARGUMENTS GitOps. Set up: Slack/Teams notifications for sync status and failures, email alerts for manual approvals, GitHub/GitLab notifications on deployment completion. Configure: audit logging of all sync operations, metrics export for GitOps tool (sync duration, success rate), Prometheus scraping of GitOps metrics. Create dashboards for GitOps health, sync status, and audit trail. Set up alerting on sync failures and out-of-sync resources."
    - Expected output: Notifications and monitoring configured
    - Context: GitOps setup, notification preferences

## Phase 4: Security, Access Control & Documentation

11. **Implement Access Control & Security**
    - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
    - Prompt: "Configure access control for: $ARGUMENTS GitOps. Implement: RBAC for GitOps tool (developers, operators, admins), Project/Team isolation in ArgoCD or Flux, Git repository branch protection and code review requirements, CODEOWNERS for approval gates. Configure: audit logging for all operations, immutable GitOps tool logs, read-only Git history, secrets encryption at rest and in transit. Implement pod security policies for GitOps tool itself."
    - Expected output: Access control and security policies
    - Context: GitOps setup, organizational requirements

12. **Generate Documentation & Runbooks**
    - Use Task tool with subagent_type="documentation-generation::docs-architect"
    - Prompt: "Generate GitOps documentation for: $ARGUMENTS. Create: architecture overview with diagrams, repository structure guide, onboarding guide for developers, deployment procedures step-by-step, troubleshooting guide (sync failures, drift detection, rollback), security and access control guide, secrets management procedures, disaster recovery runbook, monitoring and alerting setup guide. Include CLI commands, common issues and solutions."
    - Expected output: Complete GitOps documentation and runbooks
    - Context: GitOps setup, operational procedures

13. **Create Testing & Validation Pipeline**
    - Use Task tool with subagent_type="cicd-automation::deployment-engineer"
    - Prompt: "Create validation pipeline for: $ARGUMENTS GitOps. Set up: pre-commit hooks for YAML validation, CI pipeline for testing manifests (kubeval, Helm lint, OPA policies), staging environment sync validation before production deployment, smoke tests post-deployment, drift detection automated remediation. Create: canary validation before full rollout, automated rollback on critical metric thresholds. Document validation results and approval gates."
    - Expected output: Validation and testing pipeline
    - Context: GitOps infrastructure, CI/CD integration

## Phase 5: Runbook & Troubleshooting

14. **Create Operational Runbooks**
    - Use Task tool with subagent_type="documentation-generation::docs-architect"
    - Prompt: "Create operational runbooks for: $ARGUMENTS GitOps. Include procedures: deploying new application, updating existing application, promoting changes through environments, rolling back bad deployment, debugging sync failures, recovering from secrets leak, restoring from Git state corruption, scaling applications, updating GitOps tool. Each runbook: step-by-step instructions, expected outcomes, troubleshooting tips, rollback procedures."
    - Expected output: Operational runbooks
    - Context: GitOps setup, operational experience

## Execution Parameters

### Required Parameters
- **--cluster-name**: Kubernetes cluster name and description
- **--gitops-platform**: GitOps tool to use (argocd|flux|jenkins-x)
- **--repository-url**: Git repository URL for GitOps state

### Optional Parameters
- **--cluster-scope**: Scope of deployment (single-cluster|multi-cluster|multi-tenancy) - default: single-cluster
- **--deployment-strategy**: Template strategy (kustomize|helm|mixed) - default: kustomize
- **--repository-structure**: Repo organization (mono-repo|multi-repo|hierarchical) - default: mono-repo
- **--secret-management**: Secret handling (external-secrets|sealed-secrets|vault|cloud-native) - default: external-secrets
- **--enable-multi-region**: Enable multi-region setup (true|false) - default: false
- **--enable-progressive-delivery**: Enable canary/blue-green (true|false) - default: true
- **--notification-channel**: Notifications (slack|teams|email|github) - default: slack
- **--enable-multi-cluster-hub**: Set up as multi-cluster hub (true|false) - default: false

## Success Criteria

- GitOps tool installed and operational
- Git repository structured for GitOps with all environments
- Secret management system integrated and operational
- All applications deployed via GitOps
- Sync policies configured appropriately
- Progressive delivery (canary/blue-green) operational
- RBAC enforced for access control
- Audit logging enabled for all operations
- Multi-cluster setup working (if applicable)
- Notifications configured for critical events
- Documentation complete
- Validation/testing pipeline operational
- Team trained on GitOps workflows
- Runbooks available for common operations

## Example Workflows Included

1. **Deploy new application** - Git push triggers deployment
2. **Update application** - Git commit triggers rolling update
3. **Promote through environments** - Auto-promotion or approval gates
4. **Rollback deployment** - Git revert triggers automatic rollback
5. **Cluster synchronization** - Manual trigger for force sync
6. **Multi-cluster deployment** - Deploy to multiple clusters simultaneously
7. **Secrets rotation** - Automated secret updates from backend
8. **Disaster recovery** - Cluster recreation from Git state

GitOps setup for: $ARGUMENTS
