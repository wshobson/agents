---
description: "Intelligent issue resolution with multi-agent debugging, root cause analysis, and verified fix implementation"
argument-hint: "<issue description> [--verification minimal|standard|comprehensive] [--prevention none|immediate|comprehensive]"
---

# Intelligent Issue Resolution Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.smart-fix/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.smart-fix/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress smart-fix session:
  Issue: [issue from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.smart-fix/` directory and `state.json`:

```json
{
  "issue": "$ARGUMENTS",
  "status": "in_progress",
  "verification_level": "standard",
  "prevention_focus": "immediate",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--verification` and `--prevention` flags. Use defaults if not specified.

### 3. Parse issue description

Extract the issue description from `$ARGUMENTS` (everything before the flags). This is referenced as `$ISSUE` in prompts below.

---

## Phase 1: Issue Analysis (Steps 1-2)

### Step 1: Error Detection and Context Gathering

Use the Task tool to launch the error detective agent:

```
Task:
  subagent_type: "error-detective"
  description: "Analyze error context for: $ISSUE"
  prompt: |
    Analyze error traces, logs, and observability data for: $ISSUE

    Deliverables:
    1. Error signature analysis: exception type, message patterns, frequency, first occurrence
    2. Stack trace deep dive: failure location, call chain, involved components
    3. Reproduction steps: minimal test case, environment requirements, data fixtures needed
    4. Observability context:
       - Sentry/DataDog error groups and trends
       - Distributed traces showing request flow (OpenTelemetry/Jaeger)
       - Structured logs (JSON logs with correlation IDs)
       - APM metrics: latency spikes, error rates, resource usage
    5. User impact assessment: affected user segments, error rate, business metrics impact
    6. Timeline analysis: when did it start, correlation with deployments/config changes
    7. Related symptoms: similar errors, cascading failures, upstream/downstream impacts

    Modern debugging techniques to employ:
    - AI-assisted log analysis (pattern detection, anomaly identification)
    - Distributed trace correlation across microservices
    - Production-safe debugging (no code changes, use observability data)
    - Error fingerprinting for deduplication and tracking

    Provide structured output with: ERROR_SIGNATURE, FREQUENCY, FIRST_SEEN, STACK_TRACE,
    REPRODUCTION, OBSERVABILITY_LINKS, USER_IMPACT, TIMELINE, RELATED_ISSUES.
```

Save the agent's output to `.smart-fix/01-error-analysis.md`.

Update `state.json`: set `current_step` to 2, add step 1 to `completed_steps`.

### Step 2: Root Cause Identification

Read `.smart-fix/01-error-analysis.md` to load error context.

Use the Task tool to launch the debugger agent:

```
Task:
  subagent_type: "debugger"
  description: "Identify root cause for: $ISSUE"
  prompt: |
    Perform root cause investigation using error-detective output:

    Context from Error-Detective:
    [Insert full contents of .smart-fix/01-error-analysis.md]

    Deliverables:
    1. Root cause hypothesis with supporting evidence
    2. Code-level analysis: variable states, control flow, timing issues
    3. Git bisect analysis: identify introducing commit (automate with git bisect run)
    4. Dependency analysis: version conflicts, API changes, configuration drift
    5. State inspection: database state, cache state, external API responses
    6. Failure mechanism: why does the code fail under these specific conditions
    7. Fix strategy options with tradeoffs (quick fix vs proper fix)

    Context needed for next phase:
    - Exact file paths and line numbers requiring changes
    - Data structures or API contracts affected
    - Dependencies that may need updates
    - Test scenarios to verify the fix
    - Performance characteristics to maintain

    Provide structured output with: ROOT_CAUSE, INTRODUCING_COMMIT, AFFECTED_FILES,
    FAILURE_MECHANISM, DEPENDENCIES, FIX_STRATEGY, TESTING_REQUIREMENTS.
```

Save the agent's output to `.smart-fix/02-root-cause.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 2 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present findings for review.

Display a summary from `.smart-fix/01-error-analysis.md` and `.smart-fix/02-root-cause.md` (error signature, root cause, fix strategy) and ask:

```
Issue analysis complete. Please review:
- .smart-fix/01-error-analysis.md (error context)
- .smart-fix/02-root-cause.md (root cause and fix strategy)

Root cause: [brief summary]
Recommended fix: [brief summary]

1. Approve — proceed to deep investigation and fix
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: Deep Investigation (Steps 3-4)

### Step 3: Deep Code Analysis

Read `.smart-fix/01-error-analysis.md` and `.smart-fix/02-root-cause.md`.

Use the Task tool to launch the debugger agent:

```
Task:
  subagent_type: "debugger"
  description: "Deep code analysis for: $ISSUE"
  prompt: |
    Perform deep code analysis and bisect investigation:

    Context from Phase 1:
    [Insert contents of .smart-fix/02-root-cause.md]

    Deliverables:
    1. Code path analysis: trace execution from entry point to failure
    2. Variable state tracking: values at key decision points
    3. Control flow analysis: branches taken, loops, async operations
    4. Git bisect automation: create bisect script to identify exact breaking commit
    5. Dependency compatibility matrix: version combinations that work/fail
    6. Configuration analysis: environment variables, feature flags, deployment configs
    7. Timing and race condition analysis: async operations, event ordering, locks
    8. Memory and resource analysis: leaks, exhaustion, contention

    Provide structured output with: CODE_PATH, STATE_AT_FAILURE, BISECT_RESULT,
    DEPENDENCY_ISSUES, CONFIGURATION_DRIFT, RACE_CONDITIONS, ISOLATION_VERIFICATION.
```

Save output to `.smart-fix/03-deep-analysis.md`.

Update `state.json`: set `current_step` to 4, add step 3 to `completed_steps`.

### Step 4: Code Review Deep Dive

Read `.smart-fix/02-root-cause.md` and `.smart-fix/03-deep-analysis.md`.

Use the Task tool to launch the code reviewer agent:

```
Task:
  subagent_type: "code-reviewer"
  description: "Review code logic for: $ISSUE"
  prompt: |
    Review code logic and identify design issues:

    Context from Deep Analysis:
    [Insert contents of .smart-fix/03-deep-analysis.md]

    Deliverables:
    1. Logic flaw analysis: incorrect assumptions, missing edge cases, wrong algorithms
    2. Type safety gaps: where stronger types could prevent the issue
    3. Error handling review: missing try-catch, unhandled promises, panic scenarios
    4. Contract validation: input validation gaps, output guarantees not met
    5. Architectural issues: tight coupling, missing abstractions, layering violations
    6. Similar patterns: other code locations with same vulnerability
    7. Fix design: minimal change vs refactoring vs architectural improvement

    Review checklist:
    - Are null/undefined values handled correctly?
    - Are async operations properly awaited/chained?
    - Are error cases explicitly handled?
    - Are type assertions safe?
    - Are API contracts respected?
    - Are side effects isolated?

    Provide structured output with: LOGIC_FLAWS, TYPE_SAFETY_GAPS, ERROR_HANDLING_GAPS,
    SIMILAR_VULNERABILITIES, FIX_DESIGN, REFACTORING_OPPORTUNITIES, ARCHITECTURAL_CONCERNS.
```

Save output to `.smart-fix/04-code-review.md`.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

---

## Phase 3: Fix Implementation (Step 5)

### Step 5: Implement Fix

Read `.smart-fix/02-root-cause.md`, `.smart-fix/03-deep-analysis.md`, and `.smart-fix/04-code-review.md`.

Route to the appropriate agent based on the codebase language. Use `general-purpose` with role context for language-specific fixes:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement fix for: $ISSUE"
  prompt: |
    You are a senior software engineer. Implement a production-safe fix with comprehensive test coverage.

    Context from investigation:
    - Root cause: [Insert from .smart-fix/02-root-cause.md]
    - Code review: [Insert from .smart-fix/04-code-review.md]

    Deliverables:
    1. Minimal fix implementation addressing root cause (not symptoms)
    2. Unit tests: specific failure case reproduction, edge cases, error paths
    3. Integration tests: end-to-end scenarios with real dependencies
    4. Regression tests: tests for similar vulnerabilities found in code review
    5. Production-safe practices:
       - Feature flags for gradual rollout
       - Graceful degradation if fix fails
       - Structured logging for debugging
       - Monitoring hooks for fix verification

    Implementation requirements:
    - Follow existing code patterns and conventions
    - Add strategic debug logging (JSON structured logs)
    - Include comprehensive type annotations
    - Update error messages to be actionable
    - Maintain backward compatibility

    Report: FIX_SUMMARY, CHANGED_FILES, NEW_FILES, TEST_COVERAGE, TEST_RESULTS,
    BREAKING_CHANGES, OBSERVABILITY_ADDITIONS, BACKWARD_COMPATIBILITY.
```

Save output to `.smart-fix/05-implementation.md`.

Update `state.json`: set `current_step` to "checkpoint-2", add step 5 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of the fix from `.smart-fix/05-implementation.md` and ask:

```
Fix implementation complete. Please review .smart-fix/05-implementation.md

Changes: [summary of files changed]
Tests: [summary of test coverage]
Breaking changes: [none or details]

1. Approve — proceed to verification
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 4 until the user approves.

---

## Phase 4: Verification (Steps 6-8)

### Step 6: Regression Testing

Read `.smart-fix/05-implementation.md`.

Use the Task tool to launch the test automator:

```
Task:
  subagent_type: "test-automator"
  description: "Regression testing for: $ISSUE fix"
  prompt: |
    Run comprehensive regression testing and verify fix quality:

    Context:
    [Insert contents of .smart-fix/05-implementation.md]

    Deliverables:
    1. Full test suite execution: unit, integration, end-to-end, contract tests
    2. Regression detection: compare results before/after, identify new failures
    3. Test quality assessment: coverage metrics, test determinism
    4. Security testing: auth checks, input validation, injection prevention
    5. Cross-environment testing: staging/QA validation

    Report: TEST_RESULTS, CODE_COVERAGE, REGRESSION_DETECTED, SECURITY_SCAN, TEST_QUALITY.
```

### Step 7: Performance Validation

Read `.smart-fix/05-implementation.md`.

Launch in parallel with Step 6:

```
Task:
  subagent_type: "general-purpose"
  description: "Performance validation for: $ISSUE fix"
  prompt: |
    You are a performance engineer. Measure performance impact and validate no regressions.

    Context:
    [Insert contents of .smart-fix/05-implementation.md]

    Deliverables:
    1. Performance benchmarks: response time (p50, p95, p99), throughput, resource utilization
    2. Comparison with baseline: before/after metrics
    3. Load testing: stress test, soak test for memory leaks, spike test
    4. APM analysis: distributed trace analysis, slow query detection, N+1 patterns
    5. Production readiness: capacity planning impact, scaling characteristics

    Report: PERFORMANCE_BASELINE, PERFORMANCE_AFTER_FIX, PERFORMANCE_IMPACT,
    LOAD_TEST_RESULTS, APM_INSIGHTS, PRODUCTION_READY.
```

### Step 8: Security Review

Read `.smart-fix/05-implementation.md`.

Launch in parallel with Steps 6-7:

```
Task:
  subagent_type: "general-purpose"
  description: "Security review for: $ISSUE fix"
  prompt: |
    You are a security auditor. Review the fix for security vulnerabilities.

    Context:
    [Insert contents of .smart-fix/05-implementation.md]

    Review for: OWASP Top 10, authentication/authorization flaws, input validation gaps,
    data protection issues, dependency vulnerabilities, and security anti-patterns.

    Provide findings with severity, location, and specific fix recommendations.
```

After all three complete, consolidate into `.smart-fix/06-verification.md`:

```markdown
# Verification: $ISSUE

## Test Results

[Summary from Step 6]

## Performance Validation

[Summary from Step 7]

## Security Review

[Summary from Step 8]

## Action Items

[Critical/high findings that need addressing]
```

If there are Critical or High severity findings, address them before proceeding.

Update `state.json`: set `current_step` to "checkpoint-3", add steps 6-8 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — User Approval Required

Display verification results from `.smart-fix/06-verification.md` and ask:

```
Verification complete. Please review .smart-fix/06-verification.md

Test results: [pass/fail summary]
Performance impact: [improved/neutral/degraded]
Security findings: [X critical, Y high, Z medium]

1. Approve — proceed to final review and documentation
2. Request changes — tell me what to fix
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 5 until the user approves.

---

## Phase 5: Final Review & Prevention (Steps 9-10)

### Step 9: Final Code Review

Read `.smart-fix/05-implementation.md` and `.smart-fix/06-verification.md`.

```
Task:
  subagent_type: "code-reviewer"
  description: "Final review for: $ISSUE fix"
  prompt: |
    Perform final code review and approve for deployment:

    Implementation: [Insert contents of .smart-fix/05-implementation.md]
    Verification: [Insert contents of .smart-fix/06-verification.md]

    Deliverables:
    1. Code quality review: conventions, patterns, error handling, observability
    2. Architecture review: boundaries, coupling, scalability
    3. Security review: vulnerabilities, validation, auth
    4. Deployment readiness: rollback plan, feature flags, monitoring
    5. Risk assessment: blast radius, rollout strategy, success metrics

    Report: REVIEW_STATUS, DEPLOYMENT_RISK, ROLLBACK_PLAN, ROLLOUT_STRATEGY,
    MONITORING_REQUIREMENTS, FINAL_VERDICT.
```

Save output to `.smart-fix/07-final-review.md`.

Update `state.json`: set `current_step` to 10, add step 9 to `completed_steps`.

### Step 10: Documentation & Prevention

Read all `.smart-fix/*.md` files.

```
Task:
  subagent_type: "general-purpose"
  description: "Document fix and prevention for: $ISSUE"
  prompt: |
    You are a technical writer and SRE specialist. Document the fix and implement prevention strategies.

    Context:
    [Insert contents of all .smart-fix/*.md files]

    Deliverables:
    1. Code documentation: inline comments for non-obvious logic, function docs
    2. Operational documentation: CHANGELOG entry, release notes, runbook entry
    3. Prevention through static analysis: linting rules, stricter type checking
    4. Monitoring and alerting: error rate alerts, custom metrics, SLO dashboards
    5. Architectural improvements: similar vulnerability patterns, refactoring proposals
    6. Postmortem document (if high-severity): timeline, root cause, action items

    Report: DOCUMENTATION_UPDATES, PREVENTION_MEASURES, MONITORING_ADDED,
    ARCHITECTURAL_IMPROVEMENTS, SIMILAR_VULNERABILITIES, FOLLOW_UP_TASKS.
```

Save output to `.smart-fix/08-prevention.md`.

Update `state.json`: set `current_step` to "complete", add step 10 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Issue resolution complete: $ISSUE

## Files Created
[List all .smart-fix/ output files]

## Resolution Summary
- Error Analysis: .smart-fix/01-error-analysis.md
- Root Cause: .smart-fix/02-root-cause.md
- Deep Analysis: .smart-fix/03-deep-analysis.md
- Code Review: .smart-fix/04-code-review.md
- Implementation: .smart-fix/05-implementation.md
- Verification: .smart-fix/06-verification.md
- Final Review: .smart-fix/07-final-review.md
- Prevention: .smart-fix/08-prevention.md

## Next Steps
1. Review all generated code and documentation
2. Run the full test suite to verify everything passes
3. Create a pull request with the implementation
4. Deploy using the rollout strategy in .smart-fix/07-final-review.md
5. Monitor using the alerts configured in .smart-fix/08-prevention.md
```

Issue to resolve: $ARGUMENTS
