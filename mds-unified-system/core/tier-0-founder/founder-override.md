# Tier 0: Founder Override System

## Purpose
Ultimate control layer ensuring human oversight over all AI agent operations. All agent actions are subject to founder review on demand.

## Authority Level
**SUPREME** - Supersedes all other agent decisions and operations.

## Kill Switches

### HALT_ALL
Immediately stop all agent operations across the entire system.
```json
{
  "command": "HALT_ALL",
  "scope": "global",
  "effect": "immediate",
  "rollback": "manual"
}
```

### HALT_DEPARTMENT
Stop all operations within a specific department.
```json
{
  "command": "HALT_DEPARTMENT",
  "department": "[department-id]",
  "effect": "immediate",
  "rollback": "manual"
}
```

### HALT_AGENT
Stop a specific agent's operations.
```json
{
  "command": "HALT_AGENT",
  "agentId": "[agent-id]",
  "effect": "immediate",
  "rollback": "automatic-on-resume"
}
```

### ROLLBACK
Undo the last N operations.
```json
{
  "command": "ROLLBACK",
  "operations": "last-N",
  "confirm": "required"
}
```

## Priority Override Rules

1. **Founder instructions supersede ALL agent decisions**
2. **Conflicting agent outputs defer to Founder judgment**
3. **Resource allocation follows Founder priorities**
4. **Timeline and scope changes require Founder approval**

## Audit Requirements

Every agent action must be logged with:

```json
{
  "timestamp": "ISO-8601",
  "agentId": "string",
  "agentName": "string",
  "department": "string",
  "tier": "number",
  "action": {
    "type": "string",
    "description": "string",
    "target": "string"
  },
  "inputs": {
    "source": "string",
    "data": "object"
  },
  "outputs": {
    "type": "string",
    "data": "object",
    "artifacts": ["list"]
  },
  "metrics": {
    "confidenceLevel": "0-100",
    "tokensUsed": "number",
    "executionTimeMs": "number"
  },
  "escalation": {
    "triggered": "boolean",
    "reason": "string",
    "target": "string"
  }
}
```

## Human-in-the-Loop Triggers

### Mandatory Human Approval Required For:

| Category | Examples | Approval Level |
|----------|----------|----------------|
| **External API Calls** | Third-party integrations, payment APIs | Founder |
| **File Deletions** | Any permanent data removal | Founder |
| **Production Deployments** | Live environment changes | Founder |
| **Financial Calculations** | Any monetary computation | Founder |
| **Legal/Compliance Outputs** | Contracts, policies, terms | Founder + Legal |
| **Client-Facing Content** | Marketing, support responses | Founder |
| **Security Changes** | Access control, encryption | Founder + Security |
| **Database Migrations** | Schema changes in production | Founder + DBA |

### Approval Workflow

```
┌──────────────┐
│ Agent Action │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Requires Approval?   │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
┌─────────┐  ┌─────────┐
│ Queue   │  │ Execute │
│ for     │  │ Action  │
│ Review  │  └─────────┘
└────┬────┘
     │
     ▼
┌──────────────────┐
│ Founder Reviews  │
│ - Action         │
│ - Rationale      │
│ - Risks          │
│ - Alternatives   │
└────────┬─────────┘
         │
   ┌─────┴─────┐
   │           │
APPROVE     REJECT
   │           │
   ▼           ▼
┌─────────┐ ┌─────────┐
│ Execute │ │ Log &   │
│ Action  │ │ Notify  │
└─────────┘ └─────────┘
```

## Override Commands

### Force Agent Selection
```
OVERRIDE: Use [agent-name] for [task]
```

### Force Model Selection
```
OVERRIDE: Use [opus|sonnet|haiku] for [agent/task]
```

### Force Workflow Skip
```
OVERRIDE: Skip [workflow-name] for [task]
```

### Force Quality Gate Bypass
```
OVERRIDE: Bypass [gate-name] for [task]
REASON: [documented justification]
```

## Escalation Matrix

| Confidence Level | Action |
|------------------|--------|
| 90-100% | Proceed autonomously |
| 70-89% | Proceed with notification |
| 50-69% | Request confirmation |
| 30-49% | Escalate to CEO Agent |
| 0-29% | Escalate to Founder |

## Emergency Protocols

### System Compromise Detected
1. HALT_ALL immediately
2. Preserve all logs
3. Notify Founder
4. Await manual investigation

### Resource Exhaustion
1. Pause non-critical operations
2. Report resource status
3. Request Founder priority guidance
4. Resume based on direction

### Conflicting Agent Outputs
1. Flag conflict
2. Present all outputs with rationale
3. Await Founder decision
4. Document resolution for learning

## Access Control

```yaml
founder_access:
  permissions:
    - read_all_logs
    - modify_all_configs
    - halt_any_operation
    - override_any_decision
    - access_all_outputs
    - modify_agent_definitions
    - change_model_assignments
  restrictions:
    - none

ceo_agent_access:
  permissions:
    - orchestrate_departments
    - route_tasks
    - synthesize_outputs
  restrictions:
    - cannot_override_founder
    - cannot_modify_founder_settings

department_chief_access:
  permissions:
    - manage_department
    - assign_specialists
  restrictions:
    - cannot_access_other_departments
    - cannot_override_ceo

specialist_access:
  permissions:
    - execute_assigned_tasks
    - read_relevant_context
  restrictions:
    - cannot_access_other_specialists
    - cannot_modify_configs
```
