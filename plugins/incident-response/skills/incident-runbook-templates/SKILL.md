---
name: incident-runbook-templates
description: Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. Use this skill when building a service outage runbook for a payment processing system; creating database incident procedures covering connection pool exhaustion, replication lag, and disk space alerts; onboarding new on-call engineers who need step-by-step recovery guides written for a 3 AM brain; or standardizing escalation matrices across multiple engineering teams.
---

# Incident Runbook Templates

Production-ready templates for incident response runbooks covering detection, triage, mitigation, resolution, and communication.

## When to Use This Skill

- Creating incident response procedures
- Building service-specific runbooks
- Establishing escalation paths
- Documenting recovery procedures
- Responding to active incidents
- Onboarding on-call engineers

## Core Concepts

### 1. Incident Severity Levels

| Severity | Impact                     | Response Time     | Example                 |
| -------- | -------------------------- | ----------------- | ----------------------- |
| **SEV1** | Complete outage, data loss | 15 min            | Production down         |
| **SEV2** | Major degradation          | 30 min            | Critical feature broken |
| **SEV3** | Minor impact               | 2 hours           | Non-critical bug        |
| **SEV4** | Minimal impact             | Next business day | Cosmetic issue          |

### 2. Runbook Structure

```
1. Overview & Impact
2. Detection & Alerts
3. Initial Triage
4. Mitigation Steps
5. Root Cause Investigation
6. Resolution Procedures
7. Verification & Rollback
8. Communication Templates
9. Escalation Matrix
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's
- **Keep runbooks updated** - Review after every incident
- **Test runbooks regularly** - Game days, chaos engineering
- **Include rollback steps** - Always have an escape hatch
- **Document assumptions** - What must be true for steps to work
- **Link to dashboards** - Quick access during stress

### Don'ts
- **Don't assume knowledge** - Write for 3 AM brain
- **Don't skip verification** - Confirm each step worked
- **Don't forget communication** - Keep stakeholders informed
- **Don't work alone** - Escalate early
- **Don't skip postmortems** - Learn from every incident

## Troubleshooting

### Runbook steps work in staging but fail during a real incident

Steps often assume preconditions that are true in a healthy environment but not during an outage. For each command in your runbook, add a prerequisite check and a "what to do if this command fails" note:

```bash
# Step: Check pod status
kubectl get pods -n payments

# Prerequisites: kubectl configured, kubeconfig points to correct cluster
# If this fails: run `aws eks update-kubeconfig --name prod-cluster --region us-east-1`
# Expected output: pods in Running state
```

### On-call engineer panics and skips steps out of order

Add a numbered checklist at the top of the runbook that mirrors the section numbers, so responders can track progress under stress without reading the full document:

```markdown
## Quick Checklist
- [ ] 1. Declare incident severity and open war room
- [ ] 2. Check service health (Section 4.1)
- [ ] 3. Check recent deployments (Section 4.1)
- [ ] 4. Roll back if deploy is suspect (Section 4.1)
- [ ] 5. Post initial notification to #payments-incidents
- [ ] 6. Escalate if > 15 min unresolved
```

### Runbook is outdated — commands reference old cluster names or endpoints

Runbooks rot because they're updated manually. Include a "Last Verified" date and owner at the top, and add a CI check that validates all `curl` endpoints and `kubectl` context names are still valid:

```markdown
## Runbook Metadata
| Field | Value |
|---|---|
| Last verified | 2024-11-15 |
| Owner | @platform-team |
| Review cadence | After every SEV1/SEV2 |
```

### Stakeholder communication is delayed while engineers are heads-down

Assign a dedicated incident communicator role (separate from the incident commander) whose only job is to post status updates. Add a standing agenda in the communication template:

```
Update every 15 minutes (even if no new information):
- Current status (Investigating / Mitigating / Monitoring)
- Impact (what is broken, who is affected, % of traffic)
- What we are doing right now
- Next update in: 15 minutes
```

### Database runbook commands cause additional downtime when run incorrectly

Add explicit warnings before destructive SQL commands and require a dry-run output check before executing:

```sql
-- WARNING: This terminates active connections. Verify count first.
-- DRY RUN (check count before terminating):
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle' AND query_start < now() - interval '10 minutes';

-- EXECUTE only after verifying count is reasonable (< 50):
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE state = 'idle' AND query_start < now() - interval '10 minutes';
```

## Related Skills

- `postmortem-writing` - After resolving an incident, use postmortem templates to capture root cause and preventive actions
- `on-call-handoff-patterns` - Structure shift handoffs so the incoming responder has full context on active incidents