---
model: claude-sonnet-4-5-20250929
---

Implement security-first architecture and hardening measures with coordinated agent orchestration:

[Extended thinking: This workflow prioritizes security at every layer of the application stack. Multiple agents work together to identify vulnerabilities, implement secure patterns, and ensure compliance with security best practices.]

## Phase 1: Security Assessment

### 1. Initial Security Audit
- Use Task tool with subagent_type="security-auditor"
- Prompt: "Perform comprehensive security audit on: $ARGUMENTS. Identify vulnerabilities, compliance gaps, and security risks across all components."
- Output: Vulnerability report, risk assessment, compliance gaps

### 2. Architecture Security Review
- Use Task tool with subagent_type="backend-architect"
- Prompt: "Review and redesign architecture for security: $ARGUMENTS. Focus on secure service boundaries, data isolation, and defense in depth. Use findings from security audit."
- Output: Secure architecture design, service isolation strategy, data flow diagrams

## Phase 2: Security Implementation

### 3. Backend Security Hardening
- Use Task tool with subagent_type="backend-architect"
- Prompt: "Implement backend security measures for: $ARGUMENTS. Include authentication, authorization, input validation, and secure data handling based on security audit findings."
- Output: Secure API implementations, auth middleware, validation layers

### 4. Infrastructure Security
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Implement infrastructure security for: $ARGUMENTS. Configure firewalls, secure secrets management, implement least privilege access, and set up security monitoring."
- Output: Infrastructure security configs, secrets management, monitoring setup

### 5. Frontend Security
- Use Task tool with subagent_type="frontend-developer"
- Prompt: "Implement frontend security measures for: $ARGUMENTS. Include CSP headers, XSS prevention, secure authentication flows, and sensitive data handling."
- Output: Secure frontend code, CSP policies, auth integration

## Phase 3: Compliance and Testing

### 6. Compliance Verification
- Use Task tool with subagent_type="security-auditor"
- Prompt: "Verify compliance with security standards for: $ARGUMENTS. Check OWASP Top 10, GDPR, SOC2, or other relevant standards. Validate all security implementations."
- Output: Compliance report, remediation requirements

### 7. Security Testing
- Use Task tool with subagent_type="test-automator"
- Prompt: "Create security test suites for: $ARGUMENTS. Include penetration tests, security regression tests, and automated vulnerability scanning."
- Output: Security test suite, penetration test results, CI/CD integration

## Phase 4: Deployment and Monitoring

### 8. Secure Deployment
- Use Task tool with subagent_type="deployment-engineer"
- Prompt: "Implement secure deployment pipeline for: $ARGUMENTS. Include security gates, vulnerability scanning in CI/CD, and secure configuration management."
- Output: Secure CI/CD pipeline, deployment security checks, rollback procedures

### 9. Security Monitoring Setup
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Set up security monitoring and incident response for: $ARGUMENTS. Include intrusion detection, log analysis, and automated alerting."
- Output: Security monitoring dashboards, alert rules, incident response procedures

## Coordination Notes
- Security findings from each phase inform subsequent implementations
- All agents must prioritize security in their recommendations
- Regular security reviews between phases ensure nothing is missed
- Document all security decisions and trade-offs

Security hardening target: $ARGUMENTS