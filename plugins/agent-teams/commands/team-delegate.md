---
description: "Task delegation dashboard for managing team workload, assignments, and rebalancing"
argument-hint: "[team-name] [--assign task-id=member-name] [--message member-name 'content'] [--rebalance]"
---

# Team Delegate

Manage task assignments and team workload. Provides a delegation dashboard showing unassigned tasks, member workloads, blocked tasks, and rebalancing suggestions.

## Pre-flight Checks

1. Parse `$ARGUMENTS` for team name and action flags:
   - `--assign task-id=member-name`: assign a specific task to a member
   - `--message member-name 'content'`: send a message to a specific member
   - `--rebalance`: analyze and rebalance workload distribution

2. Read team config from `~/.claude/teams/{team-name}/config.json` using the Read tool
3. Call `TaskList` to get current state

## Action: Assign Task

If `--assign` flag is provided:

1. Parse task ID and member name from `task-id=member-name` format
2. Use `TaskUpdate` to set the task owner
3. Use `SendMessage` with `type: "message"` to notify the member:
   - recipient: member name
   - content: "You've been assigned task #{id}: {subject}. {task description}"
4. Confirm: "Task #{id} assigned to {member-name}"

## Action: Send Message

If `--message` flag is provided:

1. Parse member name and message content
2. Use `SendMessage` with `type: "message"`:
   - recipient: member name
   - content: the message content
3. Confirm: "Message sent to {member-name}"

## Action: Rebalance

If `--rebalance` flag is provided:

1. Analyze current workload distribution:
   - Count tasks per member (in_progress + pending assigned)
   - Identify members with 0 tasks (idle)
   - Identify members with 3+ tasks (overloaded)
   - Check for blocked tasks that could be unblocked

2. Generate rebalancing suggestions:

   ```
   ## Workload Analysis

   Member          Tasks    Status
   ─────────────────────────────────
   implementer-1   3        overloaded
   implementer-2   1        balanced
   implementer-3   0        idle

   Suggestions:
   1. Move task #5 from implementer-1 to implementer-3
   2. Assign unassigned task #7 to implementer-3
   ```

3. Ask user for confirmation before executing rebalancing
4. Execute approved moves with `TaskUpdate` and `SendMessage`

## Default: Delegation Dashboard

If no action flag is provided, display the full delegation dashboard:

```
## Delegation Dashboard: {team-name}

### Unassigned Tasks
  #5  Review error handling patterns
  #7  Add integration tests

### Member Workloads
  implementer-1   3 tasks (1 in_progress, 2 pending)
  implementer-2   1 task  (1 in_progress)
  implementer-3   0 tasks (idle)

### Blocked Tasks
  #6  Blocked by #4 (in_progress, owner: implementer-1)

### Suggestions
  - Assign #5 to implementer-3 (idle)
  - Assign #7 to implementer-2 (low workload)
```

**Tip**: Use Shift+Tab to enter Claude Code's built-in delegate mode for ad-hoc task delegation.
