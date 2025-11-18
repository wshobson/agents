---
name: security-architecture
description: Enterprise security architecture включая zero trust, defense in depth, identity management, encryption, compliance (GDPR, SOC 2, HIPAA). Используйте когда проектируете security controls, проводите threat modeling или обеспечиваете compliance.
---

# Security Architecture

## Когда использовать этот скилл

- Проектирование security architecture для cloud systems
- Implementing zero trust architecture
- Threat modeling и risk assessment
- Designing identity и access management (IAM)
- Ensuring compliance (GDPR, HIPAA, SOC 2, PCI-DSS)
- Implementing encryption at rest и in transit
- Designing security monitoring и incident response

## Zero Trust Architecture

```yaml
Principles:
  Never_Trust_Always_Verify:
    - "Не доверять network location (inside vs outside)"
    - "Verify каждый request независимо от источника"
    - "Assume breach - проектировать для минимизации blast radius"

  Least_Privilege_Access:
    - "Users получают minimum необходимые permissions"
    - "Just-in-time (JIT) access для privileged operations"
    - "Regular access reviews и revocation"

  Micro-Segmentation:
    - "Network segmentation на granular level"
    - "Zero trust network access (ZTNA)"
    - "Service-to-service authentication (mTLS)"

Implementation:
  Identity_Verification:
    Multi_Factor_Authentication:
      factors:
        - "Something you know (password)"
        - "Something you have (phone, hardware token)"
        - "Something you are (biometric)"
      enforcement: "Required для all users, особенно privileged accounts"

    Risk_Based_Authentication:
      signals:
        - "Location (new IP, country)"
        - "Device (registered vs unknown)"
        - "Behavior (unusual activity patterns)"
      actions:
        - "Step-up authentication (additional MFA challenge)"
        - "Block access"
        - "Alert security team"

  Device_Trust:
    endpoint_security:
      - "Device enrollment и management (MDM/UEM)"
      - "Compliance checks (OS version, encryption, antivirus)"
      - "Certificate-based authentication"
    examples:
      - "Microsoft Intune"
      - "Google BeyondCorp"
      - "Okta Device Trust"

  Application_Security:
    authentication:
      - "OAuth 2.0, OpenID Connect"
      - "Service accounts with short-lived tokens"
      - "API keys с rotation policies"

    authorization:
      - "RBAC (Role-Based Access Control)"
      - "ABAC (Attribute-Based Access Control)"
      - "Policy-as-Code (OPA, Cedar)"

  Network_Security:
    micro_segmentation:
      - "Security groups per service/tier"
      - "Network policies (Kubernetes NetworkPolicy)"
      - "Application-level firewalls"

    encryption:
      - "TLS 1.3 для all traffic"
      - "mTLS для service-to-service (Istio, App Mesh)"
      - "VPN или private connectivity (Direct Connect, ExpressRoute)"

Platforms:
  - "Microsoft Zero Trust Framework"
  - "Google BeyondCorp"
  - "AWS Zero Trust Architecture"
  - "Okta Identity Cloud"
```

## Defense in Depth

```yaml
Layers:
  1_Perimeter_Security:
    components:
      - "WAF (Web Application Firewall)"
      - "DDoS protection (AWS Shield, Azure DDoS, CloudFlare)"
      - "API Gateway с rate limiting"
    tools:
      AWS: "WAF, Shield, CloudFront"
      Azure: "Azure WAF, DDoS Protection, Front Door"
      GCP: "Cloud Armor, Cloud CDN"

  2_Network_Security:
    segmentation:
      - "VPC/VNet isolation"
      - "Public, private, isolated subnets"
      - "Security groups, NACLs, NSGs"
    monitoring:
      - "VPC Flow Logs"
      - "Network traffic analysis"
      - "Intrusion detection (IDS/IPS)"

  3_Application_Security:
    secure_coding:
      - "Input validation, output encoding"
      - "Parameterized queries (prevent SQL injection)"
      - "CSRF tokens, SameSite cookies"
    dependency_management:
      - "SCA (Software Composition Analysis)"
      - "Vulnerability scanning (Snyk, Dependabot)"
      - "Regular updates, patch management"

  4_Identity_and_Access:
    principles:
      - "Principle of least privilege"
      - "Separation of duties"
      - "Regular access reviews"
    implementation:
      - "IAM roles и policies"
      - "JIT access (Teleport, CyberArk)"
      - "Privileged access management (PAM)"

  5_Data_Security:
    encryption_at_rest:
      - "AES-256 для disk encryption"
      - "Transparent Data Encryption (TDE) для databases"
      - "KMS для key management (rotation, auditing)"
    encryption_in_transit:
      - "TLS 1.3 minimum"
      - "Certificate management (ACM, Let's Encrypt)"
      - "mTLS для internal services"
    data_classification:
      - "Public, Internal, Confidential, Restricted"
      - "DLP (Data Loss Prevention) policies"
      - "Masking, tokenization для PII"

  6_Monitoring_and_Logging:
    logging:
      - "Centralized logging (CloudWatch, Azure Monitor, Cloud Logging)"
      - "Audit logs для all privileged actions"
      - "Immutable audit trail (WORM storage)"
    monitoring:
      - "SIEM (Splunk, Sentinel, Chronicle)"
      - "Anomaly detection (GuardDuty, Security Center)"
      - "Real-time alerts"
    retention:
      - "Compliance-driven (7 years для некоторых regulations)"
      - "Lifecycle policies для cost optimization"

  7_Incident_Response:
    preparation:
      - "Incident response plan (IRP)"
      - "Runbooks для common scenarios"
      - "Security team training, tabletop exercises"
    detection:
      - "Automated threat detection"
      - "24/7 SOC monitoring"
    response:
      - "Isolation, containment, eradication"
      - "Forensics, root cause analysis"
      - "Post-incident review, lessons learned"
```

## Compliance Frameworks

```yaml
GDPR:
  scope: "EU residents' personal data"

  requirements:
    data_residency:
      - "Store EU data в EU regions"
      - "Restrict cross-border transfers"

    right_to_erasure:
      - "Delete personal data on request"
      - "Cascading deletes across systems"

    data_portability:
      - "Export user data в machine-readable format (JSON, CSV)"

    breach_notification:
      - "Notify authorities в течение 72 hours"
      - "Notify affected individuals if high risk"

    privacy_by_design:
      - "Minimize data collection"
      - "Pseudonymization, anonymization"
      - "Encryption by default"

  implementation:
    data_mapping: "Inventory всех PII, data flows"
    consent_management: "Explicit consent, opt-in"
    dpia: "Data Protection Impact Assessments для high-risk processing"

SOC_2:
  scope: "Security controls для service organizations"

  trust_service_criteria:
    security:
      - "Access controls (authentication, authorization)"
      - "System monitoring, incident response"

    availability:
      - "System uptime SLAs"
      - "Disaster recovery, business continuity"

    processing_integrity:
      - "Data processing accuracy, completeness"
      - "Error handling, validation"

    confidentiality:
      - "Data encryption, access restrictions"

    privacy:
      - "Collection, use, retention, disclosure, disposal"

  audit:
    type1: "Design of controls (point in time)"
    type2: "Operating effectiveness (6-12 months)"

  implementation:
    policies: "Written policies, procedures"
    controls: "Technical controls implementation"
    evidence: "Continuous monitoring, log collection"

HIPAA:
  scope: "Protected Health Information (PHI)"

  requirements:
    administrative:
      - "Risk assessment, management"
      - "Workforce training"
      - "Business associate agreements (BAA)"

    physical:
      - "Facility access controls"
      - "Workstation security"
      - "Device и media controls"

    technical:
      - "Access controls (unique user IDs)"
      - "Audit controls (logs)"
      - "Integrity controls (checksums)"
      - "Transmission security (encryption)"

  implementation:
    encryption: "AES-256 at rest, TLS in transit"
    audit_logs: "All PHI access logged, 6 year retention"
    access_controls: "Role-based, minimum necessary"

PCI_DSS:
  scope: "Cardholder data (CHD)"

  requirements:
    network_security:
      - "Firewall protection"
      - "No default passwords"

    cardholder_data_protection:
      - "Encrypt stored CHD"
      - "Encrypt CHD in transit (TLS)"
      - "Mask PAN (show only last 4 digits)"

    vulnerability_management:
      - "Antivirus software"
      - "Secure systems, applications"

    access_control:
      - "Restrict access by business need-to-know"
      - "Unique IDs, strong authentication"

    monitoring:
      - "Track и monitor all access to network resources и CHD"
      - "Regular testing of security systems"

  compliance_levels:
    level1: "> 6M transactions/year"
    level2: "1M - 6M transactions/year"
    level3: "20K - 1M e-commerce transactions/year"
    level4: "< 20K e-commerce transactions/year"

  implementation:
    tokenization: "Replace PAN with tokens"
    pci_scope_reduction: "Minimize systems в PCI scope"
    third_party: "Use PCI-compliant payment processors (Stripe, Adyen)"
```

## Threat Modeling

```yaml
STRIDE:
  Spoofing:
    threat: "Impersonating user или service"
    mitigation:
      - "Strong authentication (MFA)"
      - "Certificate-based authentication"
      - "mTLS для services"

  Tampering:
    threat: "Modifying data или code"
    mitigation:
      - "Digital signatures"
      - "Integrity checks (checksums, hashes)"
      - "Immutable infrastructure"

  Repudiation:
    threat: "Denying actions taken"
    mitigation:
      - "Comprehensive audit logging"
      - "Non-repudiation (digital signatures)"
      - "Timestamping"

  Information_Disclosure:
    threat: "Unauthorized data access"
    mitigation:
      - "Encryption at rest и in transit"
      - "Access controls (RBAC, ABAC)"
      - "Data masking, tokenization"

  Denial_of_Service:
    threat: "Making system unavailable"
    mitigation:
      - "Rate limiting, throttling"
      - "DDoS protection"
      - "Auto-scaling, redundancy"

  Elevation_of_Privilege:
    threat: "Gaining unauthorized permissions"
    mitigation:
      - "Principle of least privilege"
      - "Input validation"
      - "Regular patching"

Process:
  1_Decompose_Application:
    - "Create data flow diagrams (DFD)"
    - "Identify trust boundaries"
    - "Enumerate assets"

  2_Identify_Threats:
    - "Apply STRIDE to each component"
    - "Use threat libraries (CAPEC, OWASP Top 10)"

  3_Rank_Risks:
    - "DREAD scoring (Damage, Reproducibility, Exploitability, Affected users, Discoverability)"
    - "Probability × Impact matrix"

  4_Mitigate:
    - "Implement security controls"
    - "Accept, transfer, или avoid risks"

  5_Validate:
    - "Security testing (SAST, DAST, penetration testing)"
    - "Continuous threat modeling"

Tools:
  - "Microsoft Threat Modeling Tool"
  - "OWASP Threat Dragon"
  - "IriusRisk"
```

## Справочные материалы

Для примеров см. директорию `references/`:
- Zero trust architecture diagrams
- Security control mappings
- Compliance checklists
- Threat modeling templates
- Incident response playbooks

---

**Примечание**: Security patterns основаны на NIST, CIS Benchmarks, и практиках AWS, Azure, Google Cloud.
