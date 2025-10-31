# Kubernetes Manifest Scaffolding

Generate production-ready Kubernetes manifests with proper configurations, resource limits, health checks, and best practices:

[Extended thinking: This command scaffolds complete Kubernetes deployment configurations with comprehensive resource management, observability integration, security policies, and networking setup. The workflow generates manifests for deployments, services, configmaps, secrets, ingress, RBAC, and monitoring. Each manifest follows Kubernetes best practices and includes annotations for GitOps, security scanning, and cost tracking. The output is organized for Kustomize or Helm integration and includes validation checks.]

## Configuration Options

### Application Type
- **stateless-api**: REST/GraphQL API with horizontal scaling
- **stateful-app**: Database-backed application with persistence
- **background-job**: Batch job or cronjob workload
- **data-pipeline**: ETL/streaming data processing
- **worker-queue**: Message queue consumer workload
- **ml-service**: ML model serving with resource optimization

### Kubernetes Distribution
- **vanilla**: Standard Kubernetes (self-managed, cloud-agnostic)
- **eks**: AWS Elastic Kubernetes Service optimizations
- **aks**: Azure Kubernetes Service optimizations
- **gke**: Google Kubernetes Engine optimizations
- **openshift**: Red Hat OpenShift specific features

### Environment Tier
- **development**: Minimal resources, single replica
- **staging**: Medium resources, 2-3 replicas, testing-ready
- **production**: Full HA configuration, auto-scaling, monitoring

### Package Format
- **plain-yaml**: Raw Kubernetes manifests
- **kustomize**: Kustomize bases and overlays for environments
- **helm**: Helm chart structure with values templates

## Phase 1: Requirement Analysis

1. **Define Application Specifications**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Analyze application requirements for Kubernetes deployment: $ARGUMENTS. Determine: resource requirements (CPU/memory), scaling needs, persistence requirements, networking topology, security requirements. Assess application type: $APP_TYPE. Create specification document with deployment parameters, observability needs, and operational requirements."
   - Expected output: Application specification with resource estimates, topology design
   - Context: Application type, environment tier, distribution

2. **Design Kubernetes Architecture**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Design Kubernetes architecture for: $ARGUMENTS. Using application specs: [include from step 1]. Define namespace strategy, workload types (Deployment/StatefulSet/DaemonSet), service types, ingress strategy, storage requirements. Design for environment: $ENVIRONMENT. Include networking, RBAC, and GitOps structure."
   - Expected output: Architecture diagram, manifest structure plan
   - Context: Application requirements, environment tier

## Phase 2: Manifest Generation

3. **Generate Core Manifests**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Generate Kubernetes manifests for: $ARGUMENTS. Using architecture design: [from step 2]. Create: Deployment/StatefulSet with resource requests/limits, health probes, lifecycle hooks. Include service definition with appropriate type. Add ConfigMap and Secret templates for configuration. Use package format: $PACKAGE_FORMAT. Include comprehensive annotations for cost tracking, security scanning, and GitOps."
   - Expected output: Core manifests (Deployment, Service, ConfigMap, Secret)
   - Context: Architecture design, application specifications

4. **Add Networking & Ingress**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure networking for: $ARGUMENTS. Add NetworkPolicy for ingress/egress control. Create Ingress configuration for external access with TLS/SSL termination. If distribution is $DISTRIBUTION, include distribution-specific ingress controller setup. Configure service discovery and inter-pod communication policies."
   - Expected output: Ingress, NetworkPolicy, service configuration
   - Context: Networking requirements, traffic patterns

5. **Configure Security & RBAC**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Add security hardening for: $ARGUMENTS. Create ServiceAccount with minimal RBAC permissions. Add PodSecurityPolicy/Pod Security Standards restrictions. Configure Pod Security Context (runAsNonRoot, readOnlyRootFilesystem, capabilities). Add network policies for zero-trust networking. Include secrets management strategy using External Secrets or Sealed Secrets."
   - Expected output: ServiceAccount, Role/RoleBinding, security policies
   - Context: Security requirements, compliance needs

6. **Set Up Observability**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure observability for: $ARGUMENTS. Add ServiceMonitor for Prometheus metrics collection. Configure structured logging with labels and annotations. Create PrometheusRule for alerting on application metrics. Add tracing instrumentation via OpenTelemetry sidecars. Include dashboards configuration for Grafana. Set up SLO/SLI definitions."
   - Expected output: ServiceMonitor, logging config, alerting rules
   - Context: Observability requirements, monitoring stack

7. **Add Storage Configuration**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure storage for: $ARGUMENTS. For stateful applications: define PersistentVolumeClaim with appropriate storage class and size. Configure data backup strategy via Velero. For stateless apps: validate no persistent state. Add backup schedules and recovery testing procedures."
   - Expected output: PersistentVolumeClaim, backup configuration
   - Context: Data persistence requirements

8. **Package & Validate**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Package manifests for: $ARGUMENTS. Organize in $PACKAGE_FORMAT structure. If Kustomize: create base directory with core manifests, overlay directories for dev/staging/prod. If Helm: create chart structure with values.yaml templates and chart.yaml. Run validation: kubeval or Helm lint. Generate dry-run manifests for review. Include deployment checklist and validation steps."
   - Expected output: Packaged manifests, validation report, deployment guide
   - Context: All generated manifests, deployment requirements

## Phase 3: Documentation & Deployment

9. **Generate Documentation**
   - Use Task tool with subagent_type="documentation-generation::docs-architect"
   - Prompt: "Create deployment documentation for: $ARGUMENTS. Include: manifest explanation for each file, values/parameters guide, deployment instructions step-by-step, configuration for different environments, troubleshooting guide, scaling procedures, backup/restore procedures, security checklist, monitoring dashboard setup."
   - Expected output: Deployment guide, configuration reference, operations runbook
   - Context: All manifests, operational procedures

10. **Create Deployment Automation**
    - Use Task tool with subagent_type="cicd-automation::deployment-engineer"
    - Prompt: "Create GitOps deployment workflow for: $ARGUMENTS. Using manifests: [include from steps 3-8]. Set up ArgoCD Application or Flux Kustomization for automated deployment. Configure sync policies, health checks, automated rollback on failure. Create deployment hooks for pre-sync validation and post-sync testing. Include canary/blue-green strategy if applicable."
    - Expected output: GitOps configuration, deployment workflow
    - Context: Manifests, deployment strategy

## Execution Parameters

### Required Parameters
- **--app-name**: Application name and brief description
- **--app-type**: Application type (stateless-api|stateful-app|background-job|data-pipeline|worker-queue|ml-service)
- **--environment**: Deployment environment (development|staging|production)

### Optional Parameters
- **--distribution**: Kubernetes distribution (vanilla|eks|aks|gke|openshift) - default: vanilla
- **--replicas**: Number of replicas for production (default: 3)
- **--package-format**: Output format (plain-yaml|kustomize|helm) - default: kustomize
- **--image-registry**: Container registry (gcr.io|ecr|acr|docker.io) - default: gcr.io
- **--resource-profile**: Resource allocation preset (minimal|standard|high-performance) - default: standard
- **--enable-hpa**: Enable Horizontal Pod Autoscaler (true|false) - default: true
- **--storage-size**: PersistentVolume size for stateful apps (e.g., 20Gi)
- **--tls-enabled**: Enable TLS for ingress (true|false) - default: true
- **--namespace**: Kubernetes namespace (default: app namespace or provided)

## Success Criteria

- All required manifests generated and validated
- Resource requests and limits properly configured
- Health checks (liveness, readiness, startup) configured
- Network policies restrict traffic appropriately
- RBAC follows principle of least privilege
- Pod Security Standards applied
- Observability fully configured (metrics, logs, traces)
- Secrets managed securely (not in YAML)
- Manifests organized for GitOps (Kustomize or Helm)
- Dry-run validation shows no errors
- Documentation complete and clear
- Deployment checklist ready for execution
- GitOps automation workflow configured

## Example Manifests Included

1. **Deployment/StatefulSet** - Main workload with proper resource management
2. **Service** - Internal and external access configuration
3. **Ingress** - External traffic routing with TLS
4. **ConfigMap** - Application configuration
5. **Secret** - Sensitive data references (templates)
6. **ServiceAccount** - Identity and access control
7. **NetworkPolicy** - Network segmentation
8. **PersistentVolumeClaim** - Data persistence (if needed)
9. **PodDisruptionBudget** - High availability during maintenance
10. **HorizontalPodAutoscaler** - Automatic scaling rules
11. **ServiceMonitor** - Prometheus metrics collection
12. **PrometheusRule** - Alerting rules
13. **ValidatingWebhookConfiguration** - Policy enforcement
14. **RBAC resources** - ServiceAccount, Role, RoleBinding

## Best Practices Implemented

- Resource requests/limits prevent resource starvation
- Health probes enable self-healing
- Network policies enforce security
- RBAC follows least privilege principle
- Non-root containers for security
- Read-only root filesystem where possible
- Proper logging and monitoring setup
- Graceful shutdown handling
- Pod Disruption Budgets for availability
- Horizontal Pod Autoscaling for efficiency
- GitOps-ready structure
- Production-grade security defaults

Manifest scaffold for application: $ARGUMENTS
