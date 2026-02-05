---
description: "Launch a multi-reviewer parallel code review with specialized review dimensions"
argument-hint: "<target> [--reviewers security,performance,architecture,testing,accessibility] [--base-branch main]"
---

# Team Review

Orchestrate a multi-reviewer parallel code review where each reviewer focuses on a specific quality dimension. Produces a consolidated, deduplicated report organized by severity.

## Pre-flight Checks

1. Verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
2. Parse `$ARGUMENTS`:
   - `<target>`: file path, directory, git diff range (e.g., `main...HEAD`), or PR number (e.g., `#123`)
   - `--reviewers`: comma-separated dimensions (default: `security,performance,architecture`)
   - `--base-branch`: base branch for diff comparison (default: `main`)

## Phase 1: Target Resolution

1. Determine target type:
   - **File/Directory**: Use as-is for review scope
   - **Git diff range**: Use Bash to run `git diff {range} --name-only` to get changed files
   - **PR number**: Use Bash to run `gh pr diff {number} --name-only` to get changed files
2. Collect the full diff content for distribution to reviewers
3. Display review scope to user: "{N} files to review across {M} dimensions"

## Phase 2: Team Spawn

1. Use `Teammate` tool with `operation: "spawnTeam"`, team name: `review-{timestamp}`
2. For each requested dimension, use `Task` tool to spawn a teammate:
   - `name`: `{dimension}-reviewer` (e.g., "security-reviewer")
   - `subagent_type`: "agent-teams:team-reviewer"
   - `prompt`: Include the dimension assignment, target files, and diff content
3. Use `TaskCreate` for each reviewer's task:
   - Subject: "Review {target} for {dimension} issues"
   - Description: Include file list, diff content, and dimension-specific checklist

## Phase 3: Monitor and Collect

1. Wait for all review tasks to complete (check `TaskList` periodically)
2. As each reviewer completes, collect their structured findings
3. Track progress: "{completed}/{total} reviews complete"

## Phase 4: Consolidation

1. **Deduplicate**: Merge findings that reference the same file:line location
2. **Resolve conflicts**: If reviewers disagree on severity, use the higher rating
3. **Organize by severity**: Group findings as Critical, High, Medium, Low
4. **Cross-reference**: Note findings that appear in multiple dimensions

## Phase 5: Report and Cleanup

1. Present consolidated report:

   ```
   ## Code Review Report: {target}

   Reviewed by: {dimensions}
   Files reviewed: {count}

   ### Critical ({count})
   [findings...]

   ### High ({count})
   [findings...]

   ### Medium ({count})
   [findings...]

   ### Low ({count})
   [findings...]

   ### Summary
   Total findings: {count} (Critical: N, High: N, Medium: N, Low: N)
   ```

2. Send `shutdown_request` to all reviewers
3. Call `Teammate` cleanup to remove team resources
