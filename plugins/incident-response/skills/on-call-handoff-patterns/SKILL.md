---
name: on-call-handoff-patterns
description: Master on-call shift handoffs with context transfer, escalation procedures, and documentation. Use this skill when transitioning on-call responsibilities between engineers and ensuring the incoming responder has full situational awareness, when writing a shift summary that captures active incidents, ongoing investigations, and recent changes, when handing off mid-incident so a fresh engineer can take over the incident commander role without losing context, when onboarding a new engineer to the on-call rotation for the first time, or when auditing and improving the quality of existing handoff processes across teams.
---

# On-Call Handoff Patterns

Effective patterns for on-call shift transitions, ensuring continuity, context transfer, and reliable incident response across shifts.

## When to Use This Skill

- Transitioning on-call responsibilities
- Writing shift handoff summaries
- Documenting ongoing investigations
- Establishing on-call rotation procedures
- Improving handoff quality
- Onboarding new on-call engineers

## Core Concepts

### 1. Handoff Components

| Component                  | Purpose                 |
| -------------------------- | ----------------------- |
| **Active Incidents**       | What's currently broken |
| **Ongoing Investigations** | Issues being debugged   |
| **Recent Changes**         | Deployments, configs    |
| **Known Issues**           | Workarounds in place    |
| **Upcoming Events**        | Maintenance, releases   |

### 2. Handoff Timing

```
Recommended: 30 min overlap between shifts

Outgoing:
├── 15 min: Write handoff document
└── 15 min: Sync call with incoming

Incoming:
├── 15 min: Review handoff document
├── 15 min: Sync call with outgoing
└── 5 min: Verify alerting setup
```

## Templates

### Template 1: Shift Handoff Document

````markdown
# On-Call Handoff: Platform Team

**Outgoing**: @alice (2024-01-15 to 2024-01-22)
**Incoming**: @bob (2024-01-22 to 2024-01-29)
**Handoff Time**: 2024-01-22 09:00 UTC

---

## 🔴 Active Incidents

### None currently active

No active incidents at handoff time.

---

## 🟡 Ongoing Investigations

### 1. Intermittent API Timeouts (ENG-1234)

**Status**: Investigating
**Started**: 2024-01-20
**Impact**: ~0.1% of requests timing out

**Context**:

- Timeouts correlate with database backup window (02:00-03:00 UTC)
- Suspect backup process causing lock contention
- Added extra logging in PR #567 (deployed 01/21)

**Next Steps**:

- [ ] Review new logs after tonight's backup
- [ ] Consider moving backup window if confirmed

**Resources**:

- Dashboard: [API Latency](https://grafana/d/api-latency)
- Thread: #platform-eng (01/20, 14:32)

---

### 2. Memory Growth in Auth Service (ENG-1235)

**Status**: Monitoring
**Started**: 2024-01-18
**Impact**: None yet (proactive)

**Context**:

- Memory usage growing ~5% per day
- No memory leak found in profiling
- Suspect connection pool not releasing properly

**Next Steps**:

- [ ] Review heap dump from 01/21
- [ ] Consider restart if usage > 80%

**Resources**:

- Dashboard: [Auth Service Memory](https://grafana/d/auth-memory)
- Analysis doc: [Memory Investigation](https://docs/eng-1235)

---

## 🟢 Resolved This Shift

### Payment Service Outage (2024-01-19)

- **Duration**: 23 minutes
- **Root Cause**: Database connection exhaustion
- **Resolution**: Rolled back v2.3.4, increased pool size
- **Postmortem**: [POSTMORTEM-89](https://docs/postmortem-89)
- **Follow-up tickets**: ENG-1230, ENG-1231

---

## 📋 Recent Changes

### Deployments

| Service      | Version | Time        | Notes                      |
| ------------ | ------- | ----------- | -------------------------- |
| api-gateway  | v3.2.1  | 01/21 14:00 | Bug fix for header parsing |
| user-service | v2.8.0  | 01/20 10:00 | New profile features       |
| auth-service | v4.1.2  | 01/19 16:00 | Security patch             |

### Configuration Changes

- 01/21: Increased API rate limit from 1000 to 1500 RPS
- 01/20: Updated database connection pool max from 50 to 75

### Infrastructure

- 01/20: Added 2 nodes to Kubernetes cluster
- 01/19: Upgraded Redis from 6.2 to 7.0

---

## ⚠️ Known Issues & Workarounds

### 1. Slow Dashboard Loading

**Issue**: Grafana dashboards slow on Monday mornings
**Workaround**: Wait 5 min after 08:00 UTC for cache warm-up
**Ticket**: OPS-456 (P3)

### 2. Flaky Integration Test

**Issue**: `test_payment_flow` fails intermittently in CI
**Workaround**: Re-run failed job (usually passes on retry)
**Ticket**: ENG-1200 (P2)

---

## 📅 Upcoming Events

| Date        | Event                | Impact              | Contact       |
| ----------- | -------------------- | ------------------- | ------------- |
| 01/23 02:00 | Database maintenance | 5 min read-only     | @dba-team     |
| 01/24 14:00 | Major release v5.0   | Monitor closely     | @release-team |
| 01/25       | Marketing campaign   | 2x traffic expected | @platform     |

---

## 📞 Escalation Reminders

| Issue Type      | First Escalation     | Second Escalation |
| --------------- | -------------------- | ----------------- |
| Payment issues  | @payments-oncall     | @payments-manager |
| Auth issues     | @auth-oncall         | @security-team    |
| Database issues | @dba-team            | @infra-manager    |
| Unknown/severe  | @engineering-manager | @vp-engineering   |

---

## 🔧 Quick Reference

### Common Commands

```bash
# Check service health
kubectl get pods -A | grep -v Running

# Recent deployments
kubectl get events --sort-by='.lastTimestamp' | tail -20

# Database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Clear cache (emergency only)
redis-cli FLUSHDB
```
````

### Important Links

- [Runbooks](https://wiki/runbooks)
- [Service Catalog](https://wiki/services)
- [Incident Slack](https://slack.com/incidents)
- [PagerDuty](https://pagerduty.com/schedules)

---

## Handoff Checklist

### Outgoing Engineer

- [x] Document active incidents
- [x] Document ongoing investigations
- [x] List recent changes
- [x] Note known issues
- [x] Add upcoming events
- [x] Sync with incoming engineer

### Incoming Engineer

- [ ] Read this document
- [ ] Join sync call
- [ ] Verify PagerDuty is routing to you
- [ ] Verify Slack notifications working
- [ ] Check VPN/access working
- [ ] Review critical dashboards

````

### Template 2: Quick Handoff (Async)

```markdown
# Quick Handoff: @alice → @bob

## TL;DR
- No active incidents
- 1 investigation ongoing (API timeouts, see ENG-1234)
- Major release tomorrow (01/24) - be ready for issues

## Watch List
1. API latency around 02:00-03:00 UTC (backup window)
2. Auth service memory (restart if > 80%)

## Recent
- Deployed api-gateway v3.2.1 yesterday (stable)
- Increased rate limits to 1500 RPS

## Coming Up
- 01/23 02:00 - DB maintenance (5 min read-only)
- 01/24 14:00 - v5.0 release

## Questions?
I'll be available on Slack until 17:00 today.
````

### Template 3: Incident Handoff (Mid-Incident)

```markdown
# INCIDENT HANDOFF: Payment Service Degradation

**Incident Start**: 2024-01-22 08:15 UTC
**Current Status**: Mitigating
**Severity**: SEV2

---

## Current State

- Error rate: 15% (down from 40%)
- Mitigation in progress: scaling up pods
- ETA to resolution: ~30 min

## What We Know

1. Root cause: Memory pressure on payment-service pods
2. Triggered by: Unusual traffic spike (3x normal)
3. Contributing: Inefficient query in checkout flow

## What We've Done

- Scaled payment-service from 5 → 15 pods
- Enabled rate limiting on checkout endpoint
- Disabled non-critical features

## What Needs to Happen

1. Monitor error rate - should reach <1% in ~15 min
2. If not improving, escalate to @payments-manager
3. Once stable, begin root cause investigation

## Key People

- Incident Commander: @alice (handing off)
- Comms Lead: @charlie
- Technical Lead: @bob (incoming)

## Communication

- Status page: Updated at 08:45
- Customer support: Notified
- Exec team: Aware

## Troubleshooting

**Incoming engineer misses a critical issue because the handoff document was incomplete.**
Use the outgoing checklist as a gate: do not mark handoff complete until every section has at least one entry (or an explicit "none"). Make incomplete handoffs a blameless postmortem action item.

**A 30-minute sync call is not possible due to timezone gaps.**
Fall back to the async quick handoff template (Template 2). Supplement with a short Loom or voice memo walking through the watch list. Ensure the incoming engineer has a direct contact method if they have follow-up questions.

**The incoming engineer inherits a mid-incident and is immediately overwhelmed.**
Use the incident handoff template (Template 3) specifically. The outgoing engineer should remain available on Slack for 15 minutes after handoff, even if off-call, to answer clarifying questions.

**On-call handoff documents are inconsistently formatted across teams.**
Adopt the shift handoff template organization-wide and store completed handoffs in a shared location (wiki, Notion, Confluence). Link each handoff from the on-call schedule entry in PagerDuty.

**Incoming engineer cannot verify their alerting is working before the outgoing engineer logs off.**
Add a standard step: outgoing engineer fires a test alert and confirms incoming engineer receives it in PagerDuty and Slack before ending the overlap window.

## Related Skills

- [incident-classification](../../skills/incident-classification/SKILL.md) — Classify and prioritize incidents that need to be included in the handoff document
- [postmortem-facilitation](../../skills/postmortem-facilitation/SKILL.md) — Turn resolved incidents from the shift into structured postmortems
