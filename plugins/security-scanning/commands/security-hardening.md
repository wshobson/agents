---
description: "Orchestrate comprehensive security hardening with defense-in-depth strategy across all application layers"
argument-hint: "<target description> [--depth quick|standard|comprehensive] [--compliance owasp,soc2,gdpr,hipaa,pci-dss]"
---

# Security Hardening Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.security-hardening/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.security-hardening/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress security hardening session:
  Target: [target from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.security-hardening/` directory and `state.json`:

```json
{
  "target": "$ARGUMENTS",
  "status": "in_progress",
  "depth": "comprehensive",
  "compliance_frameworks": ["owasp"],
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--depth` and `--compliance` flags. Use defaults if not specified.

### 3. Parse target description

Extract the target description from `$ARGUMENTS` (everything before the flags). This is referenced as `$TARGET` in prompts below.

---

## Phase 1: Assessment & Threat Modeling (Steps 1–3)

### Step 1: Vulnerability Scanning

Use the Task tool to launch the security auditor agent:

```
Task:
  subagent_type: "security-auditor"
  description: "Comprehensive vulnerability scan of $TARGET"
  prompt: |
    Perform a comprehensive security assessment on: $TARGET.

    ## Instructions
    1. Execute SAST analysis (Semgrep/SonarQube patterns)
    2. Identify DAST scanning targets (OWASP ZAP patterns)
    3. Perform dependency audit (Snyk/Trivy patterns)
    4. Run secrets detection (GitLeaks/TruffleHog patterns)
    5. Generate SBOM for supply chain analysis
    6. Identify OWASP Top 10 vulnerabilities, CWE weaknesses, and CVE exposures
    7. Assign CVSS scores to all findings

    Provide a detailed vulnerability report with: CVSS scores, exploitability analysis,
    attack surface mapping, secrets exposure report, and SBOM inventory.
```

Save the agent's output to `.security-hardening/01-vulnerability-scan.md`.

Update `state.json`: set `current_step` to 2, add step 1 to `completed_steps`.

### Step 2: Threat Modeling & Risk Analysis

Read `.security-hardening/01-vulnerability-scan.md` to load vulnerability context.

Use the Task tool to launch the threat modeling expert:

```
Task:
  subagent_type: "threat-modeling-expert"
  description: "Threat modeling and risk analysis for $TARGET"
  prompt: |
    Conduct threat modeling using STRIDE methodology for: $TARGET.

    ## Vulnerability Context
    [Insert full contents of .security-hardening/01-vulnerability-scan.md]

    ## Instructions
    1. Analyze attack vectors and create attack trees
    2. Assess business impact of identified vulnerabilities
    3. Map threats to MITRE ATT&CK framework
    4. Prioritize risks based on likelihood and impact
    5. Use vulnerability scan results to inform threat priorities

    Provide: threat model diagrams, risk matrix with prioritized vulnerabilities,
    attack scenario documentation, and business impact analysis.
```

Save the agent's output to `.security-hardening/02-threat-model.md`.

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

### Step 3: Architecture Security Review

Read `.security-hardening/01-vulnerability-scan.md` and `.security-hardening/02-threat-model.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Architecture security review for $TARGET"
  prompt: |
    You are a backend security architect. Review the architecture for security weaknesses in: $TARGET.

    ## Vulnerability Scan Results
    [Insert contents of .security-hardening/01-vulnerability-scan.md]

    ## Threat Model
    [Insert contents of .security-hardening/02-threat-model.md]

    ## Instructions
    1. Evaluate service boundaries, data flow security, authentication/authorization architecture
    2. Review encryption implementation and network segmentation
    3. Design zero-trust architecture patterns where applicable
    4. Create a data classification matrix
    5. Reference the threat model and vulnerability findings in your recommendations

    Provide: security architecture assessment, zero-trust design recommendations,
    service mesh security requirements, and data classification matrix.
```

Save the agent's output to `.security-hardening/03-architecture-review.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the assessment results for review.

Display a summary of findings from `.security-hardening/01-vulnerability-scan.md`, `.security-hardening/02-threat-model.md`, and `.security-hardening/03-architecture-review.md` (critical vulnerabilities count, top threats, key architecture concerns) and ask:

```
Security assessment complete. Please review:
- .security-hardening/01-vulnerability-scan.md
- .security-hardening/02-threat-model.md
- .security-hardening/03-architecture-review.md

Critical vulnerabilities: [count]
High-risk threats: [count]
Architecture concerns: [count]

1. Approve — proceed to vulnerability remediation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: Vulnerability Remediation (Steps 4–7)

### Step 4: Critical Vulnerability Fixes

Read `.security-hardening/01-vulnerability-scan.md` and `.security-hardening/02-threat-model.md`.

Use the Task tool:

```
Task:
  subagent_type: "security-auditor"
  description: "Remediate critical vulnerabilities for $TARGET"
  prompt: |
    Coordinate immediate remediation of critical vulnerabilities (CVSS 7+) in: $TARGET.

    ## Vulnerability Scan Results
    [Insert contents of .security-hardening/01-vulnerability-scan.md]

    ## Threat Model
    [Insert contents of .security-hardening/02-threat-model.md]

    ## Instructions
    1. Fix SQL injections with parameterized queries
    2. Fix XSS with output encoding
    3. Fix authentication bypasses with secure session management
    4. Fix insecure deserialization with input validation
    5. Apply security patches for known CVEs
    6. Document all changes and regression test requirements

    Provide: patched code with vulnerability fixes, security patch documentation,
    and regression test requirements.
```

Save the agent's output to `.security-hardening/04-critical-fixes.md`.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

### Step 5: Backend Security Hardening

Read `.security-hardening/03-architecture-review.md` and `.security-hardening/04-critical-fixes.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Backend security hardening for $TARGET"
  prompt: |
    You are a backend security engineer. Implement comprehensive backend security controls for: $TARGET.

    ## Architecture Review
    [Insert contents of .security-hardening/03-architecture-review.md]

    ## Critical Fixes Applied
    [Insert contents of .security-hardening/04-critical-fixes.md]

    ## Instructions
    1. Add input validation with OWASP ESAPI patterns
    2. Implement rate limiting and DDoS protection
    3. Secure API endpoints with OAuth2/JWT validation
    4. Add encryption for data at rest/transit using AES-256/TLS 1.3
    5. Implement secure logging without PII exposure
    6. Build upon the critical fixes already applied

    Provide: hardened API endpoints, validation middleware, encryption implementation,
    and secure configuration templates.
```

Save the agent's output to `.security-hardening/05-backend-hardening.md`.

Update `state.json`: set `current_step` to 6, add step 5 to `completed_steps`.

### Step 6: Frontend Security Implementation

Read `.security-hardening/03-architecture-review.md` and `.security-hardening/05-backend-hardening.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Frontend security implementation for $TARGET"
  prompt: |
    You are a frontend security engineer. Implement frontend security measures for: $TARGET.

    ## Architecture Review
    [Insert contents of .security-hardening/03-architecture-review.md]

    ## Backend Hardening
    [Insert contents of .security-hardening/05-backend-hardening.md]

    ## Instructions
    1. Configure CSP headers with nonce-based policies
    2. Implement XSS prevention with DOMPurify
    3. Secure authentication flows with PKCE OAuth2
    4. Add SRI for external resources
    5. Implement secure cookie handling with SameSite/HttpOnly/Secure flags
    6. Complement backend security with client-side protections

    Provide: secure frontend components, CSP policy configuration,
    authentication flow implementation, and security headers configuration.
```

Save the agent's output to `.security-hardening/06-frontend-hardening.md`.

**Note:** If the target has no frontend component (pure backend/API), skip this step — write a brief note in `06-frontend-hardening.md` explaining why it was skipped, and continue.

Update `state.json`: set `current_step` to 7, add step 6 to `completed_steps`.

### Step 7: Mobile Security Hardening

Read `.security-hardening/03-architecture-review.md` and `.security-hardening/05-backend-hardening.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Mobile security hardening for $TARGET"
  prompt: |
    You are a mobile security engineer. Implement mobile app security for: $TARGET.

    ## Architecture Review
    [Insert contents of .security-hardening/03-architecture-review.md]

    ## Backend Hardening
    [Insert contents of .security-hardening/05-backend-hardening.md]

    ## Instructions
    1. Add certificate pinning
    2. Implement biometric authentication
    3. Secure local storage with encryption
    4. Obfuscate code with ProGuard/R8
    5. Implement anti-tampering and root/jailbreak detection
    6. Secure IPC communications

    Provide: hardened mobile application configuration, security configuration files,
    obfuscation rules, and certificate pinning implementation.
```

Save the agent's output to `.security-hardening/07-mobile-hardening.md`.

**Note:** If the target has no mobile component, skip this step — write a brief note in `07-mobile-hardening.md` explaining why it was skipped, and continue.

Update `state.json`: set `current_step` to "checkpoint-2", add step 7 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of all remediation work from steps 4–7 and ask:

```
Vulnerability remediation complete. Please review:
- .security-hardening/04-critical-fixes.md
- .security-hardening/05-backend-hardening.md
- .security-hardening/06-frontend-hardening.md
- .security-hardening/07-mobile-hardening.md

Critical fixes applied: [count]
Backend controls added: [summary]
Frontend controls added: [summary]
Mobile controls added: [summary]

1. Approve — proceed to security controls & validation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Security Controls & Infrastructure (Steps 8–10)

### Step 8: Authentication & Authorization Enhancement

Read `.security-hardening/03-architecture-review.md` and `.security-hardening/05-backend-hardening.md`.

Use the Task tool:

```
Task:
  subagent_type: "security-auditor"
  description: "Enhance authentication and authorization for $TARGET"
  prompt: |
    Implement a modern authentication system for: $TARGET.

    ## Architecture Review
    [Insert contents of .security-hardening/03-architecture-review.md]

    ## Backend Hardening
    [Insert contents of .security-hardening/05-backend-hardening.md]

    ## Instructions
    1. Deploy OAuth2/OIDC with PKCE
    2. Implement MFA with TOTP/WebAuthn/FIDO2
    3. Add risk-based authentication
    4. Implement RBAC/ABAC with principle of least privilege
    5. Add session management with secure token rotation
    6. Strengthen access controls based on architecture review

    Provide: authentication service configuration, MFA implementation,
    authorization policies, and session management system.
```

Save the agent's output to `.security-hardening/08-auth-enhancement.md`.

Update `state.json`: set `current_step` to 9, add step 8 to `completed_steps`.

### Step 9: Infrastructure Security Controls

Read `.security-hardening/03-architecture-review.md` and `.security-hardening/08-auth-enhancement.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Deploy infrastructure security controls for $TARGET"
  prompt: |
    You are an infrastructure security engineer. Deploy infrastructure security controls for: $TARGET.

    ## Architecture Review
    [Insert contents of .security-hardening/03-architecture-review.md]

    ## Auth Enhancement
    [Insert contents of .security-hardening/08-auth-enhancement.md]

    ## Instructions
    1. Configure WAF rules for OWASP protection
    2. Implement network segmentation with micro-segmentation
    3. Deploy IDS/IPS systems
    4. Configure cloud security groups and NACLs
    5. Implement DDoS protection with rate limiting and geo-blocking

    Provide: WAF configuration, network security policies, IDS/IPS rules,
    and cloud security configurations.
```

Save the agent's output to `.security-hardening/09-infra-security.md`.

Update `state.json`: set `current_step` to 10, add step 9 to `completed_steps`.

### Step 10: Secrets Management Implementation

Read `.security-hardening/01-vulnerability-scan.md` and `.security-hardening/09-infra-security.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement secrets management for $TARGET"
  prompt: |
    You are a DevOps security engineer. Implement enterprise secrets management for: $TARGET.

    ## Vulnerability Scan Results
    [Insert contents of .security-hardening/01-vulnerability-scan.md]

    ## Infrastructure Security
    [Insert contents of .security-hardening/09-infra-security.md]

    ## Instructions
    1. Deploy HashiCorp Vault or AWS Secrets Manager configuration
    2. Implement secret rotation policies
    3. Remove hardcoded secrets
    4. Configure least-privilege IAM roles
    5. Implement encryption key management with HSM support

    Provide: secrets management configuration, rotation policies,
    IAM role definitions, and key management procedures.
```

Save the agent's output to `.security-hardening/10-secrets-management.md`.

Update `state.json`: set `current_step` to "checkpoint-3", add step 10 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — User Approval Required

Display a summary of security controls from steps 8–10 and ask:

```
Security controls implementation complete. Please review:
- .security-hardening/08-auth-enhancement.md
- .security-hardening/09-infra-security.md
- .security-hardening/10-secrets-management.md

Auth controls: [summary]
Infrastructure controls: [summary]
Secrets management: [summary]

1. Approve — proceed to validation & compliance
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 4 until the user approves.

---

## Phase 4: Validation & Compliance (Steps 11–13)

### Step 11: Penetration Testing & Validation

Read `.security-hardening/04-critical-fixes.md`, `.security-hardening/05-backend-hardening.md`, and `.security-hardening/08-auth-enhancement.md`.

Use the Task tool:

```
Task:
  subagent_type: "security-auditor"
  description: "Penetration testing and validation for $TARGET"
  prompt: |
    Execute comprehensive penetration testing for: $TARGET.

    ## Critical Fixes Applied
    [Insert contents of .security-hardening/04-critical-fixes.md]

    ## Backend Hardening
    [Insert contents of .security-hardening/05-backend-hardening.md]

    ## Auth Enhancement
    [Insert contents of .security-hardening/08-auth-enhancement.md]

    ## Instructions
    1. Perform authenticated and unauthenticated testing
    2. Execute API security testing
    3. Test business logic vulnerabilities
    4. Attempt privilege escalation
    5. Validate all security controls effectiveness
    6. Use Burp Suite, Metasploit, and custom exploit patterns

    Provide: penetration test report, proof-of-concept exploits,
    remediation validation, and security control effectiveness metrics.
```

Save the agent's output to `.security-hardening/11-pentest-results.md`.

Update `state.json`: set `current_step` to 12, add step 11 to `completed_steps`.

### Step 12: Compliance & Standards Verification

Read `.security-hardening/11-pentest-results.md`.

Use the Task tool:

```
Task:
  subagent_type: "security-auditor"
  description: "Compliance verification for $TARGET"
  prompt: |
    Verify compliance with security frameworks for: $TARGET.

    ## Penetration Test Results
    [Insert contents of .security-hardening/11-pentest-results.md]

    ## Compliance Frameworks to Validate
    [Insert compliance_frameworks from state.json — default: OWASP]

    ## Instructions
    1. Validate against OWASP ASVS Level 2
    2. Validate against CIS Benchmarks
    3. Check SOC2 Type II requirements if applicable
    4. Verify GDPR/CCPA privacy controls if applicable
    5. Check HIPAA/PCI-DSS requirements if applicable
    6. Generate compliance attestation reports

    Provide: compliance assessment report, gap analysis,
    remediation requirements, and audit evidence collection.
```

Save the agent's output to `.security-hardening/12-compliance-report.md`.

Update `state.json`: set `current_step` to 13, add step 12 to `completed_steps`.

### Step 13: Security Monitoring & SIEM Integration

Read `.security-hardening/09-infra-security.md` and `.security-hardening/12-compliance-report.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement security monitoring and SIEM for $TARGET"
  prompt: |
    You are a security operations engineer specializing in SIEM and incident response.
    Implement security monitoring and SIEM integration for: $TARGET.

    ## Infrastructure Security
    [Insert contents of .security-hardening/09-infra-security.md]

    ## Compliance Report
    [Insert contents of .security-hardening/12-compliance-report.md]

    ## Instructions
    1. Deploy SIEM integration (Splunk/ELK/Sentinel configuration)
    2. Configure security event correlation rules
    3. Implement behavioral analytics for anomaly detection
    4. Set up automated incident response playbooks
    5. Create security dashboards and alerting
    6. Ensure monitoring covers compliance requirements

    Provide: SIEM configuration, correlation rules, incident response playbooks,
    security dashboards, and alert definitions.
```

Save the agent's output to `.security-hardening/13-monitoring-siem.md`.

Update `state.json`: set `current_step` to "complete", add step 13 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Security hardening complete: $TARGET

## Output Files
- .security-hardening/01-vulnerability-scan.md
- .security-hardening/02-threat-model.md
- .security-hardening/03-architecture-review.md
- .security-hardening/04-critical-fixes.md
- .security-hardening/05-backend-hardening.md
- .security-hardening/06-frontend-hardening.md
- .security-hardening/07-mobile-hardening.md
- .security-hardening/08-auth-enhancement.md
- .security-hardening/09-infra-security.md
- .security-hardening/10-secrets-management.md
- .security-hardening/11-pentest-results.md
- .security-hardening/12-compliance-report.md
- .security-hardening/13-monitoring-siem.md

## Summary by Phase
- **Assessment**: [vulnerability count] vulnerabilities found, [threat count] threats modeled
- **Remediation**: [fix count] critical fixes applied, backend/frontend/mobile hardened
- **Controls**: Auth enhanced, infrastructure secured, secrets managed
- **Validation**: Pentest [pass/fail], compliance [frameworks validated]

## Success Criteria
- [ ] All critical vulnerabilities (CVSS 7+) remediated
- [ ] OWASP Top 10 vulnerabilities addressed
- [ ] Zero high-risk findings in penetration testing
- [ ] Compliance frameworks validation passed
- [ ] Security monitoring detecting and alerting on threats
- [ ] All secrets managed through secure vault
- [ ] Authentication implements MFA and secure session management
- [ ] Security tests integrated into CI/CD pipeline

## Next Steps
1. Review all generated security artifacts
2. Run the full security test suite to verify controls
3. Deploy monitoring configuration to production
4. Schedule regular security reviews
```
