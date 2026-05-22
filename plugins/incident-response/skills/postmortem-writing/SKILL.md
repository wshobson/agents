---
name: postmortem-writing
description: Write effective blameless postmortems with root cause analysis, timelines, and action items. Use when conducting incident reviews, writing postmortem documents, or improving incident response processes.
---

# Postmortem Writing

Comprehensive guide to writing effective, blameless postmortems that drive organizational learning and prevent incident recurrence.

## When to Use This Skill

- Conducting post-incident reviews
- Writing postmortem documents
- Facilitating blameless postmortem meetings
- Identifying root causes and contributing factors
- Creating actionable follow-up items
- Building organizational learning culture

## Core Concepts

### 1. Blameless Culture

| Blame-Focused            | Blameless                         |
| ------------------------ | --------------------------------- |
| "Who caused this?"       | "What conditions allowed this?"   |
| "Someone made a mistake" | "The system allowed this mistake" |
| Punish individuals       | Improve systems                   |
| Hide information         | Share learnings                   |
| Fear of speaking up      | Psychological safety              |

### 2. Postmortem Triggers

- SEV1 or SEV2 incidents
- Customer-facing outages > 15 minutes
- Data loss or security incidents
- Near-misses that could have been severe
- Novel failure modes
- Incidents requiring unusual intervention

## Quick Start

### Postmortem Timeline

```
Day 0: Incident occurs
Day 1-2: Draft postmortem document
Day 3-5: Postmortem meeting
Day 5-7: Finalize document, create tickets
Week 2+: Action item completion
Quarterly: Review patterns across incidents
```

## Templates and detailed worked examples

Full template library and detailed worked examples live in `references/details.md`. Read that file when you need the concrete templates.

## References
- [Connection Pool Best Practices](internal-wiki/connection-pools)
- [Deployment Runbook](internal-wiki/deployment-runbook)
```

### Template 2: 5 Whys Analysis

```markdown
# 5 Whys Analysis: [Incident]

## Problem Statement

Payment service experienced 47-minute outage due to database connection exhaustion.

## Analysis

### Why #1: Why did the service fail?

**Answer**: Database connections were exhausted, causing all new requests to fail.

**Evidence**: Metrics showed connection count at 100/100 (max), with 500+ pending requests.

---

### Why #2: Why were database connections exhausted?

**Answer**: Each incoming request opened a new database connection instead of using the connection pool.

**Evidence**: Code diff shows direct `DriverManager.getConnection()` instead of pooled `DataSource`.

---

### Why #3: Why did the code bypass the connection pool?

**Answer**: A developer refactored the repository class and inadvertently changed the connection acquisition method.

**Evidence**: PR #1234 shows the change, made while fixing a different bug.

---

### Why #4: Why wasn't this caught in code review?

**Answer**: The reviewer focused on the functional change (the bug fix) and didn't notice the infrastructure change.

**Evidence**: Review comments only discuss business logic.

---

### Why #5: Why isn't there a safety net for this type of change?

**Answer**: We lack automated tests that verify connection pool behavior and lack documentation about our connection patterns.

**Evidence**: Test suite has no tests for connection handling; wiki has no article on database connections.

## Root Causes Identified

1. **Primary**: Missing automated tests for infrastructure behavior
2. **Secondary**: Insufficient documentation of architectural patterns
3. **Tertiary**: Code review checklist doesn't include infrastructure considerations

## Systemic Improvements

| Root Cause    | Improvement                       | Type       |
| ------------- | --------------------------------- | ---------- |
| Missing tests | Add infrastructure behavior tests | Prevention |
| Missing docs  | Document connection patterns      | Prevention |
| Review gaps   | Update review checklist           | Detection  |
| No canary     | Implement canary deployments      | Mitigation |
```

### Template 3: Quick Postmortem (Minor Incidents)

```markdown
# Quick Postmortem: [Brief Title]

**Date**: 2024-01-15 | **Duration**: 12 min | **Severity**: SEV3

## What Happened

API latency spiked to 5s due to cache miss storm after cache flush.

## Timeline

- 10:00 - Cache flush initiated for config update
- 10:02 - Latency alerts fire
- 10:05 - Identified as cache miss storm
- 10:08 - Enabled cache warming
- 10:12 - Latency normalized

## Root Cause

Full cache flush for minor config update caused thundering herd.

## Fix

- Immediate: Enabled cache warming
- Long-term: Implement partial cache invalidation (ENG-999)

## Lessons

Don't full-flush cache in production; use targeted invalidation.
```

## Facilitation Guide

### Running a Postmortem Meeting

```markdown
## Meeting Structure (60 minutes)

### 1. Opening (5 min)

- Remind everyone of blameless culture
- "We're here to learn, not to blame"
- Review meeting norms

### 2. Timeline Review (15 min)

- Walk through events chronologically
- Ask clarifying questions
- Identify gaps in timeline

### 3. Analysis Discussion (20 min)

- What failed?
- Why did it fail?
- What conditions allowed this?
- What would have prevented it?

### 4. Action Items (15 min)

- Brainstorm improvements
- Prioritize by impact and effort
- Assign owners and due dates

### 5. Closing (5 min)

- Summarize key learnings
- Confirm action item owners
- Schedule follow-up if needed

## Facilitation Tips

- Keep discussion on track
- Redirect blame to systems
- Encourage quiet participants
- Document dissenting views
- Time-box tangents
```

## Anti-Patterns to Avoid

| Anti-Pattern            | Problem                    | Better Approach                 |
| ----------------------- | -------------------------- | ------------------------------- |
| **Blame game**          | Shuts down learning        | Focus on systems                |
| **Shallow analysis**    | Doesn't prevent recurrence | Ask "why" 5 times               |
| **No action items**     | Waste of time              | Always have concrete next steps |
| **Unrealistic actions** | Never completed            | Scope to achievable tasks       |
| **No follow-up**        | Actions forgotten          | Track in ticketing system       |

## Best Practices

### Do's

- **Start immediately** - Memory fades fast
- **Be specific** - Exact times, exact errors
- **Include graphs** - Visual evidence
- **Assign owners** - No orphan action items
- **Share widely** - Organizational learning

### Don'ts

- **Don't name and shame** - Ever
- **Don't skip small incidents** - They reveal patterns
- **Don't make it a blame doc** - That kills learning
- **Don't create busywork** - Actions should be meaningful
- **Don't skip follow-up** - Verify actions completed
