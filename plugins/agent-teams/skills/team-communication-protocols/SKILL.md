---
name: team-communication-protocols
description: Structured messaging protocols for agent team communication including message type selection, plan approval, shutdown procedures, and anti-patterns to avoid. Use this skill when establishing team communication norms, handling plan approvals, or managing team shutdown.
version: 1.0.2
---

# Team Communication Protocols

Protocols for effective communication between agent teammates, including message type selection, plan approval workflows, shutdown procedures, and common anti-patterns to avoid.

## When to Use This Skill

- Establishing communication norms for a new team
- Choosing between message types (message, broadcast, shutdown_request)
- Handling plan approval workflows
- Managing graceful team shutdown
- Discovering teammate identities and capabilities

## Message Type Selection

### `message` (Direct Message) — Default Choice

Send to a single specific teammate:

```json
{
  "type": "message",
  "recipient": "implementer-1",
  "content": "Your API endpoint is ready. You can now build the frontend form.",
  "summary": "API endpoint ready for frontend"
}
```

**Use for**: Task updates, coordination, questions, integration notifications.

### `broadcast` — Use Sparingly

Send to ALL teammates simultaneously:

```json
{
  "type": "broadcast",
  "content": "Critical: shared types file has been updated. Pull latest before continuing.",
  "summary": "Shared types updated"
}
```

**Use ONLY for**: Critical blockers affecting everyone, major changes to shared resources.

**Why sparingly?**: Each broadcast sends N separate messages (one per teammate), consuming API resources proportional to team size.

### `shutdown_request` — Graceful Termination

Request a teammate to shut down:

```json
{
  "type": "shutdown_request",
  "recipient": "reviewer-1",
  "content": "Review complete, shutting down team."
}
```

The teammate responds with `shutdown_response` (approve or reject with reason).

## Communication Anti-Patterns

| Anti-Pattern                            | Problem                                  | Better Approach                        |
| --------------------------------------- | ---------------------------------------- | -------------------------------------- |
| Broadcasting routine updates            | Wastes resources, noise                  | Direct message to affected teammate    |
| Sending JSON status messages            | Not designed for structured data         | Use TaskUpdate to update task status   |
| Not communicating at integration points | Teammates build against stale interfaces | Message when your interface is ready   |
| Micromanaging via messages              | Overwhelms teammates, slows work         | Check in at milestones, not every step |
| Using UUIDs instead of names            | Hard to read, error-prone                | Always use teammate names              |
| Ignoring idle teammates                 | Wasted capacity                          | Assign new work or shut down           |

## Plan Approval Workflow

When a teammate is spawned with `plan_mode_required`:

1. Teammate creates a plan using read-only exploration tools
2. Teammate calls `ExitPlanMode` which sends a `plan_approval_request` to the lead
3. Lead reviews the plan
4. Lead responds with `plan_approval_response`:

**Approve**:

```json
{
  "type": "plan_approval_response",
  "request_id": "abc-123",
  "recipient": "implementer-1",
  "approve": true
}
```

**Reject with feedback**:

```json
{
  "type": "plan_approval_response",
  "request_id": "abc-123",
  "recipient": "implementer-1",
  "approve": false,
  "content": "Please add error handling for the API calls"
}
```

## Shutdown Protocol

### Graceful Shutdown Sequence

1. **Lead sends shutdown_request** to each teammate
2. **Teammate receives request** as a JSON message with `type: "shutdown_request"`
3. **Teammate responds** with `shutdown_response`:
   - `approve: true` — Teammate saves state and exits
   - `approve: false` + reason — Teammate continues working
4. **Lead handles rejections** — Wait for teammate to finish, then retry
5. **After all teammates shut down** — Call `Teammate` cleanup

### Handling Rejections

If a teammate rejects shutdown:

- Check their reason (usually "still working on task")
- Wait for their current task to complete
- Retry shutdown request
- If urgent, user can force shutdown

## Teammate Discovery

Find team members by reading the config file:

**Location**: `~/.claude/teams/{team-name}/config.json`

**Structure**:

```json
{
  "members": [
    {
      "name": "security-reviewer",
      "agentId": "uuid-here",
      "agentType": "team-reviewer"
    },
    {
      "name": "perf-reviewer",
      "agentId": "uuid-here",
      "agentType": "team-reviewer"
    }
  ]
}
```

**Always use `name`** for messaging and task assignment. Never use `agentId` directly.
