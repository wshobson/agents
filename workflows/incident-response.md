---
model: claude-sonnet-4-5-20250929
---

Respond to production incidents with coordinated agent expertise for rapid resolution:

[Extended thinking: This workflow handles production incidents with urgency and precision. Multiple specialized agents work together to identify root causes, implement fixes, and prevent recurrence.]

## Phase 1: Immediate Response

### 1. Incident Assessment
- Use Task tool with subagent_type="incident-responder"
- Prompt: "URGENT: Assess production incident: $ARGUMENTS. Determine severity, impact, and immediate mitigation steps. Time is critical."
- Output: Incident severity, impact assessment, immediate actions

### 2. Initial Troubleshooting
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Investigate production issue: $ARGUMENTS. Check logs, metrics, recent deployments, and system health. Identify potential root causes."
- Output: Initial findings, suspicious patterns, potential causes

## Phase 2: Root Cause Analysis

### 3. Deep Debugging
- Use Task tool with subagent_type="debugger"
- Prompt: "Debug production issue: $ARGUMENTS using findings from initial investigation. Analyze stack traces, reproduce issue if possible, identify exact root cause."
- Output: Root cause identification, reproduction steps, debug analysis

### 4. Performance Analysis (if applicable)
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Analyze performance aspects of incident: $ARGUMENTS. Check for resource exhaustion, bottlenecks, or performance degradation."
- Output: Performance metrics, resource analysis, bottleneck identification

### 5. Database Investigation (if applicable)
- Use Task tool with subagent_type="database-optimizer"
- Prompt: "Investigate database-related aspects of incident: $ARGUMENTS. Check for locks, slow queries, connection issues, or data corruption."
- Output: Database health report, query analysis, data integrity check

## Phase 3: Resolution Implementation

### 6. Fix Development
- Use Task tool with subagent_type="backend-architect"
- Prompt: "Design and implement fix for incident: $ARGUMENTS based on root cause analysis. Ensure fix is safe for immediate production deployment."
- Output: Fix implementation, safety analysis, rollout strategy

### 7. Emergency Deployment
- Use Task tool with subagent_type="deployment-engineer"
- Prompt: "Deploy emergency fix for incident: $ARGUMENTS. Implement with minimal risk, include rollback plan, and monitor deployment closely."
- Output: Deployment execution, rollback procedures, monitoring setup

## Phase 4: Stabilization and Prevention

### 8. System Stabilization
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Stabilize system after incident fix: $ARGUMENTS. Monitor system health, clear any backlogs, and ensure full recovery."
- Output: System health report, recovery metrics, stability confirmation

### 9. Security Review (if applicable)
- Use Task tool with subagent_type="security-auditor"
- Prompt: "Review security implications of incident: $ARGUMENTS. Check for any security breaches, data exposure, or vulnerabilities exploited."
- Output: Security assessment, breach analysis, hardening recommendations

## Phase 5: Post-Incident Activities

### 10. Monitoring Enhancement
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Enhance monitoring to prevent recurrence of: $ARGUMENTS. Add alerts, improve observability, and set up early warning systems."
- Output: New monitoring rules, alert configurations, observability improvements

### 11. Test Coverage
- Use Task tool with subagent_type="test-automator"
- Prompt: "Create tests to prevent regression of incident: $ARGUMENTS. Include unit tests, integration tests, and chaos engineering scenarios."
- Output: Test implementations, regression prevention, chaos tests

### 12. Documentation
- Use Task tool with subagent_type="incident-responder"
- Prompt: "Document incident postmortem for: $ARGUMENTS. Include timeline, root cause, impact, resolution, and lessons learned. No blame, focus on improvement."
- Output: Postmortem document, action items, process improvements

## Coordination Notes
- Speed is critical in early phases - parallel agent execution where possible
- Communication between agents must be clear and rapid
- All changes must be safe and reversible
- Document everything for postmortem analysis

Production incident: $ARGUMENTS