# Kubernetes Security Hardening

Implement comprehensive security hardening across Kubernetes cluster, control plane, and workloads with compliance validation:

[Extended thinking: This command establishes production-grade Kubernetes security following CIS benchmarks, NIST frameworks, and cloud-native security best practices. It covers control plane hardening, node security, pod security, network policies, RBAC, image security, runtime protection, compliance validation, and security monitoring. The workflow implements defense-in-depth security layers with automated enforcement, continuous scanning, and audit logging.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Security Framework
- **cis-benchmark**: CIS Kubernetes Benchmarks v1.7 hardening controls
- **nist-csf**: NIST Cybersecurity Framework implementation
- **pci-dss**: PCI-DSS compliance for payment systems
- **hipaa**: HIPAA compliance for healthcare
- **sox**: SOX compliance for financial systems
- **custom**: Custom security policies and requirements

### Hardening Scope
- **cluster-only**: Control plane and cluster-level security
- **workload-focus**: Pod security and container-level hardening
- **comprehensive**: Complete cluster to container hardening
- **compliance-audit**: Focus on audit and compliance validation

### Policy Enforcement
- **pod-security-standards**: Kubernetes Pod Security Standards (restricted/baseline/privileged)
- **kyverno**: Kyverno policy engine for flexible policies
- **opa-gatekeeper**: Open Policy Agent with Gatekeeper for complex policies
- **kubewarden**: Rust-based policy framework

### Monitoring & Response
- **falco**: Falco runtime threat detection
- **sysdig**: Sysdig secure runtime monitoring
- **aqua-security**: Aqua Security container monitoring
- **none**: Manual monitoring and response

## Phase 1: Security Assessment & Planning

1. **Conduct Security Assessment**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Conduct security assessment for Kubernetes cluster: $ARGUMENTS. Framework: $SECURITY_FRAMEWORK. Evaluate: control plane security (API server, etcd, scheduler), node security (kubelet, container runtime), pod security (container images, runtime permissions), network security (policies, service mesh), RBAC (access control), secrets management, audit logging, compliance status. Create security assessment report with gaps, risks, and remediation priorities."
   - Expected output: Security assessment report with gaps and priorities
   - Context: Current cluster configuration, security requirements

2. **Design Security Architecture**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Design security architecture for: $ARGUMENTS using framework: $SECURITY_FRAMEWORK. Create: control plane hardening plan, node hardening procedures, pod security policies, RBAC model, network policy strategy, secret management approach, image security controls, audit logging architecture. Design for scope: $HARDENING_SCOPE. Include compliance mapping to $SECURITY_FRAMEWORK requirements."
   - Expected output: Detailed security architecture design
   - Context: Assessment findings, compliance requirements

## Phase 2: Control Plane & Infrastructure Hardening

3. **Harden Kubernetes Control Plane**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Harden Kubernetes control plane for: $ARGUMENTS. Configure: API server (--authorization-mode=RBAC, --admission-control, --enable-audit-log), etcd encryption at rest, audit logging with detailed events, kubeconfig file permissions, TLS certificates and rotation, service account token auto-mounting disabled by default, disable anonymous access. For managed services (EKS/AKS/GKE): configure control plane audit logs, network policies, RBAC synchronization. Test and validate all changes."
   - Expected output: Hardened control plane configuration
   - Context: Kubernetes distribution, current configuration

4. **Secure Kubernetes Nodes**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Secure Kubernetes nodes for: $ARGUMENTS. Configure: kubelet security (--authorization-mode=Webhook, --authentication-required, --read-only-port=0), container runtime security (cgroup v2, SELinux/AppArmor), kernel parameters hardening (sysctl), firewall rules, SSH key rotation, OS patches and updates. Implement: node access restrictions, bastion host for SSH, encrypted communication, service account credential rotation, network segmentation."
   - Expected output: Node security hardening procedures
   - Context: Kubernetes distribution, infrastructure setup

5. **Implement Network Security**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Implement network security for: $ARGUMENTS. Create: NetworkPolicy for pod-to-pod communication (deny-all default, allow specific flows), ingress/egress controls, DNS policy hardening. If using service mesh: configure mTLS enforcement, authorization policies, traffic encryption. Configure: cluster network segmentation, node network policies, external access restrictions, DDoS protection. Validate policies with network traffic analysis."
   - Expected output: Network policies and configurations
   - Context: Network topology, traffic patterns

## Phase 3: Pod & Container Security

6. **Configure Pod Security Standards**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure pod security for: $ARGUMENTS using policy: $POLICY_ENFORCEMENT. If Pod Security Standards: define restricted/baseline/privileged policies per namespace. If Kyverno: create policies for image registry validation, container image scanning requirement, no root containers, read-only filesystem, resource limits. If OPA-Gatekeeper: write policies for compliance validation. If Kubewarden: configure Rust policies. Implement: gradual rollout from audit to enforce mode, namespace baseline enforcement."
   - Expected output: Pod security policies and configurations
   - Context: Policy enforcement choice, compliance requirements

7. **Secure Container Images**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Secure container images for: $ARGUMENTS. Implement: image signing with Sigstore/Cosign, image scanning with Trivy/Aqua before deployment, admission controller requiring signed images, image registry authentication and RBAC, image pull secrets management. Configure: approved registry allowlist, base image scanning, vulnerability thresholds for blocking deployment, supply chain security (SLSA levels), SBOM generation. Document image build security practices."
   - Expected output: Image security controls and validation
   - Context: Container registry setup, compliance requirements

8. **Harden Runtime Security**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Configure runtime security for: $ARGUMENTS using monitoring: $MONITORING_RESPONSE. If Falco: deploy Falco DaemonSet, configure detection rules for suspicious behavior (privilege escalation, shell spawning, file modifications), integrate with SIEM for alerting. If Sysdig: set up runtime insights and threat detection. If Aqua Security: configure runtime scanning. Implement: capability dropping, seccomp profiles, AppArmor/SELinux profiles. Configure response actions (kill pod, alert, block execution)."
   - Expected output: Runtime security monitoring and policies
   - Context: Monitoring choice, threat model

## Phase 4: Access Control & Secrets

9. **Implement RBAC Model**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Implement RBAC for: $ARGUMENTS. Design roles for: cluster administrators, namespace owners, developers, read-only access, CI/CD system. Create ClusterRoles and ClusterRoleBindings following least privilege principle. Implement: service account per application, pod security policies via RBAC, namespace resource quotas. Configure: workload identity (IRSA/Workload Identity), external user authentication (OIDC/LDAP), audit logging of all RBAC decisions. Document RBAC model and access request process."
   - Expected output: RBAC configuration and documentation
   - Context: Organizational structure, access requirements

10. **Secure Secret Management**
    - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
    - Prompt: "Configure secret management for: $ARGUMENTS. Implement: encryption at rest for secrets (etcd encryption), external secrets management (HashiCorp Vault/AWS Secrets Manager), secret rotation policies, audit logging of secret access, service account credential rotation. Configure: secret access RBAC, secret encryption in transit, secret scanning in Git (prevent hardcoding), secret injection via sidecars. Document secrets management procedures and recovery processes."
    - Expected output: Secret management configuration
    - Context: Secret storage, compliance requirements

## Phase 5: Compliance & Audit

11. **Implement Audit Logging**
    - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
    - Prompt: "Configure audit logging for: $ARGUMENTS. Implement: API audit logging (request/response/metadata), audit log retention (minimum 90 days), secure audit log storage (immutable, encrypted). Configure: sensitive resource audit (secrets, RBAC changes), audit log analysis and alerting, compliance event tracking. Integrate: SIEM for audit log analysis, long-term storage in cloud provider or S3, automated alerting on suspicious activities. Document audit logging procedures and compliance mapping."
    - Expected output: Audit logging setup and monitoring
    - Context: Compliance requirements, logging infrastructure

12. **Compliance Validation & Documentation**
    - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
    - Prompt: "Validate compliance for: $ARGUMENTS against framework: $SECURITY_FRAMEWORK. Create: compliance checklist mapped to requirements, automated scanning tools (kubesec, kubeseal-verify, OPA policies), compliance reports generation. For each requirement: document control implementation, test procedures, audit evidence. Create: security runbooks, incident response procedures, security policy documentation. Implement continuous compliance monitoring with automated alerts on violations."
    - Expected output: Compliance validation procedures and documentation
    - Context: Security framework, audit requirements

13. **Security Monitoring & Alerting**
    - Use Task tool with subagent_type="observability-monitoring::observability-engineer"
    - Prompt: "Set up security monitoring for: $ARGUMENTS. Configure: intrusion detection dashboards, privilege escalation alerts, unauthorized access attempts monitoring, policy violation alerts, certificate expiration alerts, image vulnerability scanning results monitoring. Create dashboards for: security posture, compliance status, threat detection events, audit trail visualization. Set up alerting for: critical vulnerabilities, policy violations, access anomalies, configuration drift from security baselines."
    - Expected output: Security monitoring and alerting setup
    - Context: Monitoring infrastructure, threat priorities

## Phase 6: Documentation & Training

14. **Generate Security Documentation**
    - Use Task tool with subagent_type="documentation-generation::docs-architect"
    - Prompt: "Create security documentation for: $ARGUMENTS. Include: security architecture overview, control plane hardening procedures, node security hardening, pod security policies explanation, RBAC model documentation, secrets management procedures, network policies documentation, incident response procedures, compliance mapping to $SECURITY_FRAMEWORK, security training materials. Create: security runbooks, troubleshooting guides, policy exceptions request process, security audit procedures."
    - Expected output: Comprehensive security documentation
    - Context: Security implementation, compliance requirements

15. **Create Security Testing & Validation**
    - Use Task tool with subagent_type="cicd-automation::deployment-engineer"
    - Prompt: "Create security testing pipeline for: $ARGUMENTS. Set up: container image scanning (Trivy, Aqua), manifest validation (kubesec, Kyverno testing), RBAC verification tests, network policy validation, compliance scanning (kubesec, OPA policies), penetration testing automation. Create: security baseline tests, policy violation detection, compliance report generation, vulnerability tracking. Implement continuous security testing in CI/CD pipeline with quality gates."
    - Expected output: Security testing and validation pipeline
    - Context: CI/CD infrastructure, testing requirements

## Execution Parameters

### Required Parameters
- **--cluster-name**: Kubernetes cluster to secure
- **--security-framework**: Security framework (cis-benchmark|nist-csf|pci-dss|hipaa|sox|custom)
- **--hardening-scope**: Scope of hardening (cluster-only|workload-focus|comprehensive|compliance-audit)

### Optional Parameters
- **--policy-engine**: Policy enforcement (pod-security-standards|kyverno|opa-gatekeeper|kubewarden) - default: pod-security-standards
- **--monitoring-tool**: Runtime monitoring (falco|sysdig|aqua-security|none) - default: falco
- **--network-policy-enabled**: Enable network policies (true|false) - default: true
- **--service-mesh-enabled**: Use service mesh for security (true|false) - default: false
- **--audit-log-retention**: Audit log retention days (default: 90)
- **--enable-encryption-at-rest**: Encrypt secrets at rest (true|false) - default: true
- **--compliance-validation**: Enable compliance checks (true|false) - default: true

## Success Criteria

- Control plane hardened per framework
- Nodes secured with kernel hardening and OS patches
- Network policies restrict traffic to intended flows
- Pod security policies enforced
- Container images secured and scanned
- Runtime security monitoring operational
- RBAC enforces least privilege
- Secrets encrypted and rotated
- Audit logging enabled and retained
- Compliance validated against framework
- Security monitoring and alerting operational
- All security controls documented
- Team trained on security procedures
- Incident response procedures established

## Security Controls Implemented

1. **Control Plane** - API server, etcd, scheduler hardening
2. **Nodes** - kubelet, container runtime, OS hardening
3. **Network** - NetworkPolicy, service mesh, ingress controls
4. **Pods** - Pod Security Standards, admission controllers
5. **Images** - Scanning, signing, registry validation
6. **Runtime** - Falco/Sysdig, threat detection
7. **Access** - RBAC, service accounts, authentication
8. **Secrets** - Encryption, rotation, external management
9. **Audit** - Comprehensive logging and monitoring
10. **Compliance** - Framework validation and reporting

Security hardening for cluster: $ARGUMENTS
