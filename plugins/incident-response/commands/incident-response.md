---
description: "Orchestrate multi-agent incident response with modern SRE practices for rapid resolution and learning"
argument-hint: "<incident description> [--severity P0|P1|P2|P3]"
---

# Incident Response Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.incident-response/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.incident-response/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress incident response session:
  Incident: [incident from state]
  Severity: [severity from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.incident-response/` directory and `state.json`:

```json
{
  "incident": "$ARGUMENTS",
  "status": "in_progress",
  "severity": "P1",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--severity` flag. Default to P1 if not specified.

### 3. Parse incident description

Extract the incident description from `$ARGUMENTS` (everything before the flags). This is referenced as `$INCIDENT` in prompts below.

---

## Phase 1: Detection & Triage (Steps 1-3)

### Step 1: Incident Detection and Classification

Use the Task tool to launch the incident responder agent:

```
Task:
  subagent_type: "incident-responder"
  description: "URGENT: Classify incident: $INCIDENT"
  prompt: |
    URGENT: Detect and classify incident: $INCIDENT

    Determine:
    1. Incident severity (P0-P3) based on impact assessment
    2. Affected services and their dependencies
    3. User impact and business risk
    4. Initial incident command structure needed
    5. SLO violation status and error budget impact

    Check: error budgets, recent deployments, configuration changes, and monitoring alerts.

    Provide structured output with: SEVERITY, AFFECTED_SERVICES, USER_IMPACT,
    BUSINESS_RISK, INCIDENT_COMMAND, SLO_STATUS.
```

Save output to `.incident-response/01-classification.md`.

Update `state.json`: set `current_step` to 2, update severity from classification, add step 1 to `completed_steps`.

### Step 2: Observability Analysis

Read `.incident-response/01-classification.md`.

```
Task:
  subagent_type: "general-purpose"
  description: "Observability sweep for incident: $INCIDENT"
  prompt: |
    You are an observability engineer. Perform rapid observability sweep for this incident.

    Context: [Insert contents of .incident-response/01-classification.md]

    Query and analyze:
    1. Distributed tracing (OpenTelemetry/Jaeger) for request flow
    2. Metrics correlation (Prometheus/Grafana/DataDog) for anomalies
    3. Log aggregation (ELK/Splunk) for error patterns
    4. APM data for performance degradation points
    5. Real User Monitoring for user experience impact

    Identify anomalies, error patterns, and service degradation points.

    Provide structured output with: TRACE_ANALYSIS, METRICS_ANOMALIES, LOG_PATTERNS,
    APM_FINDINGS, RUM_IMPACT, SERVICE_HEALTH_MATRIX.
```

Save output to `.incident-response/02-observability.md`.

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

### Step 3: Initial Mitigation

Read `.incident-response/01-classification.md` and `.incident-response/02-observability.md`.

```
Task:
  subagent_type: "incident-responder"
  description: "Immediate mitigation for: $INCIDENT"
  prompt: |
    Implement immediate mitigation for this incident.

    Classification: [Insert contents of .incident-response/01-classification.md]
    Observability: [Insert contents of .incident-response/02-observability.md]

    Actions to evaluate and implement:
    1. Traffic throttling/rerouting if needed
    2. Feature flag disabling for affected features
    3. Circuit breaker activation
    4. Rollback assessment for recent deployments
    5. Scale resources if capacity-related

    Prioritize user experience restoration.

    Provide structured output with: MITIGATION_ACTIONS, TEMPORARY_FIXES,
    ROLLBACK_DECISIONS, SERVICE_STATUS_AFTER, USER_IMPACT_REDUCTION.
```

Save output to `.incident-response/03-mitigation.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the triage results.

Display a summary from `.incident-response/01-classification.md` and `.incident-response/03-mitigation.md` and ask:

```
Triage and initial mitigation complete.

Severity: [from classification]
Affected services: [from classification]
Mitigation status: [from mitigation]
User impact reduction: [from mitigation]

1. Approve — proceed to investigation and root cause analysis
2. Request changes — adjust mitigation or severity
3. Pause — save progress and stop here (mitigation in place)
```

Do NOT proceed to Phase 2 until the user approves.

---

## Phase 2: Investigation & Root Cause (Steps 4-6)

### Step 4: Deep System Debugging

Read `.incident-response/02-observability.md` and `.incident-response/03-mitigation.md`.

```
Task:
  subagent_type: "debugger"
  description: "Deep debugging for: $INCIDENT"
  prompt: |
    Conduct deep debugging for this incident using observability data.

    Observability: [Insert contents of .incident-response/02-observability.md]
    Mitigation: [Insert contents of .incident-response/03-mitigation.md]

    Investigate:
    1. Stack traces and error logs
    2. Database query performance and locks
    3. Network latency and timeouts
    4. Memory leaks and CPU spikes
    5. Dependency failures and cascading errors

    Apply Five Whys analysis to identify root cause.

    Provide structured output with: ROOT_CAUSE, CONTRIBUTING_FACTORS,
    DEPENDENCY_IMPACT_MAP, FIVE_WHYS_ANALYSIS.
```

Save output to `.incident-response/04-debugging.md`.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

### Step 5: Security Assessment

Read `.incident-response/04-debugging.md`.

```
Task:
  subagent_type: "general-purpose"
  description: "Security assessment for: $INCIDENT"
  prompt: |
    You are a security auditor. Assess security implications of this incident.

    Debug findings: [Insert contents of .incident-response/04-debugging.md]

    Check:
    1. DDoS attack indicators
    2. Authentication/authorization failures
    3. Data exposure risks
    4. Certificate issues
    5. Suspicious access patterns

    Review WAF logs, security groups, and audit trails.

    Provide structured output with: SECURITY_ASSESSMENT, BREACH_ANALYSIS,
    VULNERABILITY_IDENTIFICATION, DATA_EXPOSURE_RISK, REMEDIATION_STEPS.
```

### Step 6: Performance Analysis

Read `.incident-response/04-debugging.md`.

Launch in parallel with Step 5:

```
Task:
  subagent_type: "general-purpose"
  description: "Performance analysis for: $INCIDENT"
  prompt: |
    You are a performance engineer. Analyze performance aspects of this incident.

    Debug findings: [Insert contents of .incident-response/04-debugging.md]

    Examine:
    1. Resource utilization patterns
    2. Query optimization opportunities
    3. Caching effectiveness
    4. Load balancer health
    5. CDN performance
    6. Autoscaling triggers

    Identify bottlenecks and capacity issues.

    Provide structured output with: PERFORMANCE_BOTTLENECKS, RESOURCE_RECOMMENDATIONS,
    OPTIMIZATION_OPPORTUNITIES, CAPACITY_ISSUES.
```

After both complete, consolidate into `.incident-response/05-investigation.md`:

```markdown
# Investigation: $INCIDENT

## Root Cause (from debugging)

[From Step 4]

## Security Assessment

[From Step 5]

## Performance Analysis

[From Step 6]

## Combined Findings

[Synthesis of all investigation results]
```

Update `state.json`: set `current_step` to "checkpoint-2", add steps 4-6 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display investigation results from `.incident-response/05-investigation.md` and ask:

```
Investigation complete. Please review .incident-response/05-investigation.md

Root cause: [brief summary]
Security concerns: [summary]
Performance issues: [summary]

1. Approve — proceed to fix implementation and deployment
2. Request changes — investigate further
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Resolution & Recovery (Steps 7-8)

### Step 7: Fix Implementation

Read `.incident-response/05-investigation.md`.

```
Task:
  subagent_type: "general-purpose"
  description: "Implement production fix for: $INCIDENT"
  prompt: |
    You are a senior backend architect. Design and implement a production fix for this incident.

    Investigation: [Insert contents of .incident-response/05-investigation.md]

    Requirements:
    1. Minimal viable fix for rapid deployment
    2. Risk assessment and rollback capability
    3. Staged rollout plan with monitoring
    4. Validation criteria and health checks
    5. Consider both immediate fix and long-term solution

    Provide structured output with: FIX_IMPLEMENTATION, DEPLOYMENT_STRATEGY,
    VALIDATION_PLAN, ROLLBACK_PROCEDURES, LONG_TERM_SOLUTION.
```

Save output to `.incident-response/06-fix.md`.

Update `state.json`: set `current_step` to 8, add step 7 to `completed_steps`.

### Step 8: Deployment and Validation

Read `.incident-response/06-fix.md`.

```
Task:
  subagent_type: "devops-troubleshooter"
  description: "Deploy and validate fix for: $INCIDENT"
  prompt: |
    Execute emergency deployment for incident fix.

    Fix details: [Insert contents of .incident-response/06-fix.md]

    Process:
    1. Blue-green or canary deployment strategy
    2. Progressive rollout with monitoring
    3. Health check validation at each stage
    4. Rollback triggers configured
    5. Real-time monitoring during deployment

    Provide structured output with: DEPLOYMENT_STATUS, VALIDATION_RESULTS,
    MONITORING_DASHBOARD, ROLLBACK_READINESS, SERVICE_HEALTH_POST_DEPLOY.
```

Save output to `.incident-response/07-deployment.md`.

Update `state.json`: set `current_step` to "checkpoint-3", add step 8 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — User Approval Required

Display deployment results from `.incident-response/07-deployment.md` and ask:

```
Fix deployed and validated.

Deployment status: [from deployment]
Service health: [from deployment]
Rollback ready: [yes/no]

1. Approve — proceed to communication and postmortem
2. Rollback — revert the deployment
3. Pause — save progress and monitor
```

Do NOT proceed to Phase 4 until the user approves.

---

## Phase 4: Communication & Coordination (Steps 9-10)

### Step 9: Stakeholder Communication

Read `.incident-response/01-classification.md`, `.incident-response/05-investigation.md`, and `.incident-response/07-deployment.md`.

```
Task:
  subagent_type: "general-purpose"
  description: "Manage incident communication for: $INCIDENT"
  prompt: |
    You are a communications specialist. Manage incident communication for this incident.

    Classification: [Insert contents of .incident-response/01-classification.md]
    Investigation: [Insert contents of .incident-response/05-investigation.md]
    Deployment: [Insert contents of .incident-response/07-deployment.md]

    Create:
    1. Status page updates (public-facing)
    2. Internal engineering updates (technical details)
    3. Executive summary (business impact/ETA)
    4. Customer support briefing (talking points)
    5. Timeline documentation with key decisions

    Provide structured output with: STATUS_PAGE_UPDATE, ENGINEERING_UPDATE,
    EXECUTIVE_SUMMARY, SUPPORT_BRIEFING, INCIDENT_TIMELINE.
```

Save output to `.incident-response/08-communication.md`.

Update `state.json`: set `current_step` to 10, add step 9 to `completed_steps`.

### Step 10: Customer Impact Assessment

Read `.incident-response/01-classification.md` and `.incident-response/07-deployment.md`.

```
Task:
  subagent_type: "incident-responder"
  description: "Assess customer impact for: $INCIDENT"
  prompt: |
    Assess and document customer impact for this incident.

    Classification: [Insert contents of .incident-response/01-classification.md]
    Resolution: [Insert contents of .incident-response/07-deployment.md]

    Analyze:
    1. Affected user segments and geography
    2. Failed transactions or data loss
    3. SLA violations and contractual implications
    4. Customer support ticket volume
    5. Revenue impact estimation
    6. Proactive customer outreach recommendations

    Provide structured output with: CUSTOMER_IMPACT_REPORT, SLA_ANALYSIS,
    REVENUE_IMPACT, OUTREACH_RECOMMENDATIONS.
```

Save output to `.incident-response/09-customer-impact.md`.

Update `state.json`: set `current_step` to 11, add step 10 to `completed_steps`.

---

## Phase 5: Postmortem & Prevention (Steps 11-13)

### Step 11: Blameless Postmortem

Read all `.incident-response/*.md` files.

```
Task:
  subagent_type: "general-purpose"
  description: "Blameless postmortem for: $INCIDENT"
  prompt: |
    You are an SRE documentation specialist. Conduct a blameless postmortem for this incident.

    Context: [Insert contents of all .incident-response/*.md files]

    Document:
    1. Complete incident timeline with decisions
    2. Root cause and contributing factors (systems focus, not people)
    3. What went well in response
    4. What could improve
    5. Action items with owners and deadlines
    6. Lessons learned for team education

    Follow SRE postmortem best practices. Focus on systems, not blame.

    Provide structured output with: INCIDENT_TIMELINE, ROOT_CAUSE_SUMMARY,
    WHAT_WENT_WELL, IMPROVEMENTS, ACTION_ITEMS, LESSONS_LEARNED.
```

Save output to `.incident-response/10-postmortem.md`.

Update `state.json`: set `current_step` to 12, add step 11 to `completed_steps`.

### Step 12: Monitoring Enhancement

Read `.incident-response/05-investigation.md` and `.incident-response/10-postmortem.md`.

```
Task:
  subagent_type: "general-purpose"
  description: "Enhance monitoring for: $INCIDENT prevention"
  prompt: |
    You are an observability engineer. Enhance monitoring to prevent recurrence of this incident.

    Investigation: [Insert contents of .incident-response/05-investigation.md]
    Postmortem: [Insert contents of .incident-response/10-postmortem.md]

    Implement:
    1. New alerts for early detection
    2. SLI/SLO adjustments if needed
    3. Dashboard improvements for visibility
    4. Runbook automation opportunities
    5. Chaos engineering scenarios for testing

    Ensure alerts are actionable and reduce noise.

    Provide structured output with: NEW_ALERTS, SLO_ADJUSTMENTS, DASHBOARD_UPDATES,
    RUNBOOK_AUTOMATION, CHAOS_SCENARIOS.
```

Save output to `.incident-response/11-monitoring.md`.

Update `state.json`: set `current_step` to 13, add step 12 to `completed_steps`.

### Step 13: System Hardening

Read `.incident-response/05-investigation.md` and `.incident-response/10-postmortem.md`.

```
Task:
  subagent_type: "general-purpose"
  description: "System hardening for: $INCIDENT prevention"
  prompt: |
    You are a senior backend architect. Design system improvements to prevent recurrence.

    Investigation: [Insert contents of .incident-response/05-investigation.md]
    Postmortem: [Insert contents of .incident-response/10-postmortem.md]

    Propose:
    1. Architecture changes for resilience (circuit breakers, bulkheads)
    2. Graceful degradation strategies
    3. Capacity planning adjustments
    4. Technical debt prioritization
    5. Dependency reduction opportunities
    6. Implementation roadmap

    Provide structured output with: ARCHITECTURE_IMPROVEMENTS, RESILIENCE_PATTERNS,
    CAPACITY_PLAN, TECH_DEBT_ITEMS, IMPLEMENTATION_ROADMAP.
```

Save output to `.incident-response/12-hardening.md`.

Update `state.json`: set `current_step` to "complete", add step 13 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Incident response complete: $INCIDENT

## Files Created
[List all .incident-response/ output files]

## Response Summary
- Classification: .incident-response/01-classification.md
- Observability: .incident-response/02-observability.md
- Mitigation: .incident-response/03-mitigation.md
- Debugging: .incident-response/04-debugging.md
- Investigation: .incident-response/05-investigation.md
- Fix: .incident-response/06-fix.md
- Deployment: .incident-response/07-deployment.md
- Communication: .incident-response/08-communication.md
- Customer Impact: .incident-response/09-customer-impact.md
- Postmortem: .incident-response/10-postmortem.md
- Monitoring: .incident-response/11-monitoring.md
- Hardening: .incident-response/12-hardening.md

## Immediate Follow-ups
1. Verify service stability over the next 24 hours
2. Complete all postmortem action items
3. Deploy monitoring enhancements within 1 week
4. Schedule system hardening work
5. Conduct team learning session on lessons learned

## Success Criteria
- Service restored within SLA targets
- Postmortem completed within 48 hours
- All action items assigned with deadlines
- Monitoring improvements deployed within 1 week
- No recurrence of the same root cause
```

Production incident requiring immediate response: $ARGUMENTS
