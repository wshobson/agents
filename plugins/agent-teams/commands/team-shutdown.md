---
description: "Gracefully shut down an agent team, collect final results, and clean up resources"
argument-hint: "[team-name] [--force] [--keep-tasks]"
---

# Team Shutdown

Gracefully shut down an active agent team by sending shutdown requests to all teammates, collecting final results, and cleaning up team resources.

## Phase 1: Pre-Shutdown

1. Parse `$ARGUMENTS` for team name and flags:
   - If no team name, check for active teams (same discovery as team-status)
   - `--force`: skip waiting for graceful shutdown responses
   - `--keep-tasks`: preserve task list after cleanup

2. Read team config from `~/.claude/teams/{team-name}/config.json` using the Read tool
3. Call `TaskList` to check for in-progress tasks

4. If there are in-progress tasks and `--force` is not set:
   - Display warning: "Warning: {N} tasks are still in progress"
   - List the in-progress tasks
   - Ask user: "Proceed with shutdown? In-progress work may be lost."

## Phase 2: Graceful Shutdown

For each teammate in the team:

1. Use `SendMessage` with `type: "shutdown_request"` to request graceful shutdown
   - Include content: "Team shutdown requested. Please finish current work and save state."
2. Wait for shutdown responses
   - If teammate approves: mark as shut down
   - If teammate rejects: report to user with reason
   - If `--force`: don't wait for responses

## Phase 3: Cleanup

1. Display shutdown summary:

   ```
   Team "{team-name}" shutdown complete.

   Members shut down: {N}/{total}
   Tasks completed: {completed}/{total}
   Tasks remaining: {remaining}
   ```

2. Unless `--keep-tasks` is set, call `Teammate` tool with `operation: "cleanup"` to remove team and task directories

3. If `--keep-tasks` is set, inform user: "Task list preserved at ~/.claude/tasks/{team-name}/"
