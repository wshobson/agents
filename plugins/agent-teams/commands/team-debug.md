---
description: "Debug issues using competing hypotheses with parallel investigation by multiple agents"
argument-hint: "<error-description-or-file> [--hypotheses N] [--scope files|module|project]"
---

# Team Debug

Debug complex issues using the Analysis of Competing Hypotheses (ACH) methodology. Multiple debugger agents investigate different hypotheses in parallel, gathering evidence to confirm or falsify each one.

## Pre-flight Checks

1. Verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
2. Parse `$ARGUMENTS`:
   - `<error-description-or-file>`: description of the bug, error message, or path to a file exhibiting the issue
   - `--hypotheses N`: number of hypotheses to generate (default: 3)
   - `--scope`: investigation scope — `files` (specific files), `module` (module/package), `project` (entire project)

## Phase 1: Initial Triage

1. Analyze the error description or file:
   - If file path: read the file, look for obvious issues, collect error context
   - If error description: search the codebase for related code, error messages, stack traces
2. Identify the symptom clearly: what is failing, when, and how
3. Gather initial context: recent git changes, related tests, configuration

## Phase 2: Hypothesis Generation

Generate N hypotheses about the root cause, covering different failure mode categories:

1. **Logic Error** — Incorrect algorithm, wrong condition, off-by-one, missing edge case
2. **Data Issue** — Invalid input, type mismatch, null/undefined, encoding problem
3. **State Problem** — Race condition, stale cache, incorrect initialization, mutation bug
4. **Integration Failure** — API contract violation, version mismatch, configuration error
5. **Resource Issue** — Memory leak, connection exhaustion, timeout, disk space
6. **Environment** — Missing dependency, wrong version, platform-specific behavior

Present hypotheses to user: "Generated {N} hypotheses. Spawning investigators..."

## Phase 3: Investigation

1. Use `Teammate` tool with `operation: "spawnTeam"`, team name: `debug-{timestamp}`
2. For each hypothesis, use `Task` tool to spawn a teammate:
   - `name`: `investigator-{n}` (e.g., "investigator-1")
   - `subagent_type`: "agent-teams:team-debugger"
   - `prompt`: Include the hypothesis, investigation scope, and relevant context
3. Use `TaskCreate` for each investigator's task:
   - Subject: "Investigate hypothesis: {hypothesis summary}"
   - Description: Full hypothesis statement, scope boundaries, evidence criteria

## Phase 4: Evidence Collection

1. Monitor TaskList for completion
2. As investigators complete, collect their evidence reports
3. Track: "{completed}/{total} investigations complete"

## Phase 5: Arbitration

1. Compare findings across all investigators:
   - Which hypotheses were confirmed (high confidence)?
   - Which were falsified (contradicting evidence)?
   - Which are inconclusive (insufficient evidence)?

2. Rank confirmed hypotheses by:
   - Confidence level (High > Medium > Low)
   - Strength of causal chain
   - Amount of supporting evidence
   - Absence of contradicting evidence

3. Present root cause analysis:

   ```
   ## Debug Report: {error description}

   ### Root Cause (Most Likely)
   **Hypothesis**: {description}
   **Confidence**: {High/Medium/Low}
   **Evidence**: {summary with file:line citations}
   **Causal Chain**: {step-by-step from cause to symptom}

   ### Recommended Fix
   {specific fix with code changes}

   ### Other Hypotheses
   - {hypothesis 2}: {status} — {brief evidence summary}
   - {hypothesis 3}: {status} — {brief evidence summary}
   ```

## Phase 6: Cleanup

1. Send `shutdown_request` to all investigators
2. Call `Teammate` cleanup to remove team resources
