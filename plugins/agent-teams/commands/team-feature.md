---
description: "Develop features in parallel with multiple agents using file ownership boundaries and dependency management"
argument-hint: "<feature-description> [--team-size N] [--branch feature/name] [--plan-first]"
---

# Team Feature

Orchestrate parallel feature development with multiple implementer agents. Decomposes features into work streams with strict file ownership, manages dependencies, and verifies integration.

## Pre-flight Checks

1. Verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
2. Parse `$ARGUMENTS`:
   - `<feature-description>`: description of the feature to build
   - `--team-size N`: number of implementers (default: 2)
   - `--branch`: git branch name (default: auto-generated from feature description)
   - `--plan-first`: decompose and get user approval before spawning

## Phase 1: Analysis

1. Analyze the feature description to understand scope
2. Explore the codebase to identify:
   - Files that will need modification
   - Existing patterns and conventions to follow
   - Integration points with existing code
   - Test files that need updates

## Phase 2: Decomposition

1. Decompose the feature into work streams:
   - Each stream gets exclusive file ownership (no overlapping files)
   - Define interface contracts between streams
   - Identify dependencies between streams (blockedBy/blocks)
   - Balance workload across streams

2. If `--plan-first` is set:
   - Present the decomposition to the user:

     ```
     ## Feature Decomposition: {feature}

     ### Stream 1: {name}
     Owner: implementer-1
     Files: {list}
     Dependencies: none

     ### Stream 2: {name}
     Owner: implementer-2
     Files: {list}
     Dependencies: blocked by Stream 1 (needs interface from {file})

     ### Integration Contract
     {shared types/interfaces}
     ```

   - Wait for user approval before proceeding
   - If user requests changes, adjust decomposition

## Phase 3: Team Spawn

1. If `--branch` specified, use Bash to create and checkout the branch:
   ```
   git checkout -b {branch-name}
   ```
2. Use `Teammate` tool with `operation: "spawnTeam"`, team name: `feature-{timestamp}`
3. Spawn a `team-lead` agent to coordinate
4. For each work stream, use `Task` tool to spawn a `team-implementer`:
   - `name`: `implementer-{n}`
   - `subagent_type`: "agent-teams:team-implementer"
   - `prompt`: Include owned files, interface contracts, and implementation requirements

## Phase 4: Task Creation

1. Use `TaskCreate` for each work stream:
   - Subject: "{stream name}"
   - Description: Owned files, requirements, interface contracts, acceptance criteria
2. Use `TaskUpdate` to set `blockedBy` relationships for dependent streams
3. Assign tasks to implementers with `TaskUpdate` (set `owner`)

## Phase 5: Monitor and Coordinate

1. Monitor `TaskList` for progress
2. As implementers complete tasks:
   - Check for integration issues
   - Unblock dependent tasks
   - Rebalance if needed
3. Handle integration point coordination:
   - When an implementer completes an interface, notify dependent implementers

## Phase 6: Integration Verification

After all tasks complete:

1. Use Bash to verify the code compiles/builds: run appropriate build command
2. Use Bash to run tests: run appropriate test command
3. If issues found, create fix tasks and assign to appropriate implementers
4. Report integration status to user

## Phase 7: Cleanup

1. Present feature summary:

   ```
   ## Feature Complete: {feature}

   Files modified: {count}
   Streams completed: {count}/{total}
   Tests: {pass/fail}

   Changes are on branch: {branch-name}
   ```

2. Send `shutdown_request` to all teammates
3. Call `Teammate` cleanup
