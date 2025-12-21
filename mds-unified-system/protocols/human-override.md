# Human Override Protocol

## Purpose
Ensure human oversight for critical, irreversible, or high-stakes operations.

## Mandatory Human Approval Matrix

| Category | Examples | Approval Level | Rationale |
|----------|----------|----------------|-----------|
| **External API Calls** | Payment APIs, third-party services | Founder | Side effects, costs |
| **File Deletions** | rm -rf, database drops | Founder | Irreversible data loss |
| **Production Deployments** | Deploy to prod, DNS changes | Founder | User impact |
| **Financial Operations** | Pricing changes, billing | Founder | Monetary consequences |
| **Legal/Compliance** | Terms of service, privacy policies | Founder + Legal | Legal liability |
| **Client-Facing Content** | Marketing emails, support responses | Founder | Brand reputation |
| **Security Changes** | Auth config, encryption settings | Founder + Security | Security posture |
| **Database Migrations** | Schema changes in production | Founder + DBA | Data integrity |
| **Access Control** | User permissions, API keys | Founder | Security |
| **Configuration Changes** | Production env vars | Founder | System stability |

## Override Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                     Agent Prepares Action                     │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  Is action in override list? │
              └──────────────┬───────────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
                  YES                 NO
                   │                   │
                   ▼                   ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Queue for Human │  │ Execute Action  │
          │     Review      │  └─────────────────┘
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────────────────────────┐
          │         Present to Human:           │
          │  • Action description               │
          │  • Rationale                        │
          │  • Potential risks                  │
          │  • Alternatives                     │
          │  • Rollback plan                    │
          └────────────────┬────────────────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │   Human Decision      │
               └───────────┬───────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
          APPROVE       MODIFY        REJECT
             │             │             │
             ▼             ▼             ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │  Execute   │ │  Adjust    │ │  Log &     │
     │  Action    │ │  & Retry   │ │  Notify    │
     └────────────┘ └────────────┘ └────────────┘
```

## Approval Request Format

```markdown
## Human Approval Required

**Action Type:** [Category from matrix]
**Requested By:** [Agent ID]
**Timestamp:** [ISO-8601]

### Action Description
[Clear, concise description of what will happen]

### Rationale
[Why this action is necessary]

### Scope of Impact
- **Systems affected:** [List]
- **Users affected:** [Number/scope]
- **Data affected:** [Type and volume]

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [How to mitigate] |

### Alternatives Considered
1. [Alternative 1] - Rejected because [reason]
2. [Alternative 2] - Rejected because [reason]

### Rollback Plan
[Steps to undo if something goes wrong]

### Required Response
- [ ] APPROVE - Proceed with action
- [ ] MODIFY - [Specify modifications needed]
- [ ] REJECT - Do not proceed

**Approval Deadline:** [If time-sensitive]
```

## Approval Response Format

```markdown
## Human Decision

**Request ID:** [Reference]
**Decision:** APPROVE / MODIFY / REJECT
**Decided By:** [Human identifier]
**Timestamp:** [ISO-8601]

### Decision Details
[Any notes or conditions]

### Modifications (if MODIFY)
[Specific changes required]

### Rejection Reason (if REJECT)
[Why rejected and what should happen instead]
```

## Emergency Override

For truly urgent situations:

```markdown
## Emergency Override Request

**URGENCY:** CRITICAL
**Time Sensitivity:** [Must act within X minutes/hours]

**Emergency Justification:**
[Why this cannot wait for standard approval]

**Proposed Action:**
[What needs to happen]

**If No Response By [Deadline]:**
[What will happen - proceed or abort]
```

## Audit Trail Requirements

Every human override must log:

```json
{
  "requestId": "ovr_abc123",
  "requestTimestamp": "2025-01-15T10:30:00Z",
  "requestingAgent": "deployment-engineer",
  "actionCategory": "production-deployment",
  "actionDescription": "Deploy v2.1.0 to production",
  "riskAssessment": {
    "overall": "medium",
    "risks": [...]
  },
  "decision": "approved",
  "decisionBy": "founder",
  "decisionTimestamp": "2025-01-15T10:35:00Z",
  "conditions": null,
  "executionTimestamp": "2025-01-15T10:36:00Z",
  "executionResult": "success",
  "rollbackRequired": false
}
```

## Delegation Rules

Founder may delegate specific approvals:

| Delegation | To Whom | Conditions |
|------------|---------|------------|
| Staging deployments | CTO Agent | Non-production only |
| Documentation updates | Docs Chief | No code changes |
| Test environment changes | Quality Chief | Isolated environments |

## Override Bypass Conditions

Actions that can bypass override (with logging):

1. **Read-only operations** - No side effects
2. **Local development** - No production impact
3. **Explicit pre-approval** - User granted in advance
4. **Rollback of failed deployment** - Emergency recovery

## Quality Metrics

Track:
- Override requests per day
- Approval/rejection ratio
- Time to decision
- Emergency overrides
- Rollbacks required post-approval
