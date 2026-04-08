---
name: team-communication-protocols
description: Structured messaging protocols for agent team communication including message type selection, plan approval, shutdown procedures, and anti-patterns to avoid. Use this skill when establishing communication norms for a newly spawned team, when deciding whether to send a direct message or a broadcast, when a team-lead needs to review and approve an implementer's plan before work begins, when orchestrating a graceful team shutdown after all tasks are complete, or when debugging why teammates are not coordinating correctly at integration points.
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
5. **After all teammates shut down** — Call `TeamDelete` to remove team resources

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

## Troubleshooting

**A teammate is not responding to messages.**
Check the teammate's task status. If it is idle, it may have completed its task and is waiting to be assigned new work or shut down. If it is still active, it may be mid-execution and will process messages once the current operation finishes.

**The lead is sending broadcasts for every status update.**
This is a common anti-pattern. Broadcasts are expensive — each one sends N messages. Use direct messages (`type: "message"`) for point-to-point updates. Reserve broadcasts for critical shared-resource changes like an updated interface contract.

**A teammate rejected a shutdown request unexpectedly.**
The teammate is still working. Check the rejection reason in the `shutdown_response` content field, wait for the work to finish, then retry. Never force-terminate a teammate that has unsaved work.

**A plan_approval_request arrived but the request_id is missing.**
The teammate called `ExitPlanMode` without the required request context. Have the teammate re-enter plan mode, complete exploration, and call `ExitPlanMode` again. The `request_id` is generated automatically by the plan mode system.

**Two teammates are waiting on each other and neither is making progress.**
This is a deadlock: both are blocked waiting for the other to finish first. The lead should send a direct message to one teammate with a stub or partial result so it can unblock and proceed.

## Related Skills

- [team-composition-patterns](../team-composition-patterns/SKILL.md) — Select agent types and team size before establishing communication norms
- [parallel-feature-development](../parallel-feature-development/SKILL.md) — Use communication protocols to coordinate integration handoffs between parallel implementers
