---
description: "Execute a comprehensive TDD workflow with strict red-green-refactor discipline"
argument-hint: "<feature or module to implement> [--incremental|--suite] [--coverage 80]"
---

# TDD Cycle Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.tdd-cycle/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.tdd-cycle/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress TDD cycle session:
  Feature: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.tdd-cycle/` directory and `state.json`:

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "mode": "suite",
  "coverage_target": 80,
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--incremental`, `--suite`, and `--coverage` flags. Use defaults if not specified (mode: suite, coverage: 80).

### 3. Parse feature description

Extract the feature description from `$ARGUMENTS` (everything before the flags). This is referenced as `$FEATURE` in prompts below.

---

## Configuration

### Coverage Thresholds

- Minimum line coverage: parsed from `--coverage` flag (default 80%)
- Minimum branch coverage: 75%
- Critical path coverage: 100%

### Refactoring Triggers

- Cyclomatic complexity > 10
- Method length > 20 lines
- Class length > 200 lines
- Duplicate code blocks > 3 lines

---

## Phase 1: Test Specification and Design (Steps 1-2)

### Step 1: Requirements Analysis

Use the Task tool to analyze requirements:

```
Task:
  subagent_type: "general-purpose"
  description: "Analyze requirements for TDD: $FEATURE"
  prompt: |
    You are a software architect specializing in test-driven development.

    Analyze requirements for: $FEATURE

    ## Deliverables
    1. Define acceptance criteria with clear pass/fail conditions
    2. Identify edge cases (null/empty, boundary values, error states, concurrent access)
    3. Create a comprehensive test scenario matrix mapping requirements to test cases
    4. Categorize tests: unit, integration, contract, property-based
    5. Identify external dependencies that will need mocking

    Write your complete analysis as a single markdown document.
```

Save the agent's output to `.tdd-cycle/01-requirements.md`.

Update `state.json`: set `current_step` to 2, add `"01-requirements.md"` to `files_created`, add step 1 to `completed_steps`.

### Step 2: Test Architecture Design

Read `.tdd-cycle/01-requirements.md` to load requirements context.

Use the Task tool to design test architecture:

```
Task:
  subagent_type: "general-purpose"
  description: "Design test architecture for $FEATURE"
  prompt: |
    You are a test automation expert specializing in test architecture and TDD workflows.

    Design test architecture for: $FEATURE

    ## Requirements
    [Insert full contents of .tdd-cycle/01-requirements.md]

    ## Deliverables
    1. Test structure and organization (directory layout, naming conventions)
    2. Fixture design (shared setup, teardown, test data factories)
    3. Mock/stub strategy (what to mock, what to use real implementations for)
    4. Test data strategy (generators, factories, edge case data sets)
    5. Test execution order and parallelization plan
    6. Framework-specific configuration (matching project's existing test framework)

    Ensure architecture supports isolated, fast, reliable tests.
    Write your complete design as a single markdown document.
```

Save the agent's output to `.tdd-cycle/02-test-architecture.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 2 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the test specification and architecture for review.

Display a summary of the requirements analysis from `.tdd-cycle/01-requirements.md` and test architecture from `.tdd-cycle/02-test-architecture.md` (key test scenarios, architecture decisions, mock strategy) and ask:

```
Test specification and architecture complete. Please review:
- .tdd-cycle/01-requirements.md
- .tdd-cycle/02-test-architecture.md

1. Approve — proceed to RED phase (write failing tests)
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: RED — Write Failing Tests (Steps 3-4)

### Step 3: Write Unit Tests (Failing)

Read `.tdd-cycle/01-requirements.md` and `.tdd-cycle/02-test-architecture.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Write failing unit tests for $FEATURE"
  prompt: |
    You are a test automation expert specializing in TDD red phase.

    Write FAILING unit tests for: $FEATURE

    ## Requirements
    [Insert contents of .tdd-cycle/01-requirements.md]

    ## Test Architecture
    [Insert contents of .tdd-cycle/02-test-architecture.md]

    ## Instructions
    1. Tests must fail initially — DO NOT implement production code
    2. Include edge cases, error scenarios, and happy paths
    3. Use the project's existing test framework and conventions
    4. Follow Arrange-Act-Assert pattern
    5. Use descriptive test names (should_X_when_Y)
    6. Ensure failures are for the RIGHT reasons (missing implementation, not syntax errors)

    Write all test files. Report what test files were created and what they cover.
```

Save a summary to `.tdd-cycle/03-failing-tests.md` (list of test files, test count, coverage areas).

Update `state.json`: set `current_step` to 4, add step 3 to `completed_steps`.

### Step 4: Verify Test Failure

Use the Task tool with the local code-reviewer agent:

```
Task:
  subagent_type: "code-reviewer"
  description: "Verify tests fail correctly for $FEATURE"
  prompt: |
    Verify that all tests for: $FEATURE are failing correctly.

    ## Failing Tests
    [Insert contents of .tdd-cycle/03-failing-tests.md]

    ## Instructions
    1. Run the test suite and confirm all new tests fail
    2. Ensure failures are for the right reasons (missing implementation, not test errors)
    3. Confirm no false positives (tests that accidentally pass)
    4. Verify no existing tests were broken
    5. Check test quality: meaningful names, proper assertions, good error messages

    Report your findings. This is a GATE — do not approve if tests pass or fail for wrong reasons.
```

Save output to `.tdd-cycle/04-failure-verification.md`.

**GATE**: Do not proceed to Phase 3 unless all tests fail appropriately. If verification fails, fix tests and re-verify.

Update `state.json`: set `current_step` to "checkpoint-2", add step 4 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of the failing tests from `.tdd-cycle/03-failing-tests.md` and verification from `.tdd-cycle/04-failure-verification.md` and ask:

```
RED phase complete. All tests are failing as expected.

Test count: [number]
Coverage areas: [summary]
Verification: [pass/fail summary]

1. Approve — proceed to GREEN phase (make tests pass)
2. Request changes — adjust tests before implementing
3. Pause — save progress and stop here
```

---

## Phase 3: GREEN — Make Tests Pass (Steps 5-6)

### Step 5: Minimal Implementation

Read `.tdd-cycle/01-requirements.md`, `.tdd-cycle/02-test-architecture.md`, and `.tdd-cycle/03-failing-tests.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement minimal code to pass tests for $FEATURE"
  prompt: |
    You are a backend architect implementing the GREEN phase of TDD.

    Implement MINIMAL code to make tests pass for: $FEATURE

    ## Requirements
    [Insert contents of .tdd-cycle/01-requirements.md]

    ## Test Architecture
    [Insert contents of .tdd-cycle/02-test-architecture.md]

    ## Failing Tests
    [Insert contents of .tdd-cycle/03-failing-tests.md]

    ## Instructions
    1. Focus ONLY on making tests green — no extra features or optimizations
    2. Use the simplest implementation that passes each test
    3. Follow the project's existing code patterns and conventions
    4. Keep methods/functions small and focused
    5. Don't add error handling unless tests require it
    6. Document shortcuts taken for the refactor phase

    Write all code files. Report what files were created/modified and any technical debt noted.
```

Save a summary to `.tdd-cycle/05-implementation.md`.

Update `state.json`: set `current_step` to 6, add step 5 to `completed_steps`.

### Step 6: Verify Test Success

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Verify all tests pass for $FEATURE"
  prompt: |
    You are a test automation expert verifying TDD green phase completion.

    Run all tests for: $FEATURE and verify they pass.

    ## Implementation
    [Insert contents of .tdd-cycle/05-implementation.md]

    ## Instructions
    1. Run the full test suite
    2. Verify ALL new tests pass (green)
    3. Verify no existing tests were broken
    4. Check test coverage metrics against targets
    5. Confirm implementation is truly minimal (no gold plating)

    Report test execution results, coverage metrics, and any issues found.
```

Save output to `.tdd-cycle/06-green-verification.md`.

**GATE**: All tests must pass before proceeding. If tests fail, return to Step 5 and fix.

Update `state.json`: set `current_step` to "checkpoint-3", add step 6 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — User Approval Required

Display results from `.tdd-cycle/06-green-verification.md` and ask:

```
GREEN phase complete. All tests passing.

Test results: [pass/fail counts]
Coverage: [metrics]

1. Approve — proceed to REFACTOR phase
2. Request changes — adjust implementation
3. Pause — save progress and stop here
```

---

## Phase 4: REFACTOR — Improve Code Quality (Steps 7-8)

### Step 7: Code Refactoring

Read `.tdd-cycle/05-implementation.md` and `.tdd-cycle/06-green-verification.md`.

Use the Task tool with the local code-reviewer agent:

```
Task:
  subagent_type: "code-reviewer"
  description: "Refactor implementation for $FEATURE"
  prompt: |
    Refactor the implementation for: $FEATURE while keeping all tests green.

    ## Implementation
    [Insert contents of .tdd-cycle/05-implementation.md]

    ## Green Verification
    [Insert contents of .tdd-cycle/06-green-verification.md]

    ## Instructions
    1. Apply SOLID principles where appropriate
    2. Remove code duplication
    3. Improve naming for clarity
    4. Optimize performance where tests support it
    5. Run tests after each refactoring step — tests MUST remain green
    6. Apply refactoring triggers: complexity > 10, method > 20 lines, class > 200 lines, duplication > 3 lines

    Report all refactoring changes made and confirm tests still pass.
```

Save output to `.tdd-cycle/07-refactored-code.md`.

Update `state.json`: set `current_step` to 8, add step 7 to `completed_steps`.

### Step 8: Test Refactoring

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Refactor tests for $FEATURE"
  prompt: |
    You are a test automation expert refactoring tests for clarity and maintainability.

    Refactor tests for: $FEATURE

    ## Current Tests
    [Insert contents of .tdd-cycle/03-failing-tests.md]

    ## Refactored Code
    [Insert contents of .tdd-cycle/07-refactored-code.md]

    ## Instructions
    1. Remove test duplication — extract common fixtures
    2. Improve test names for clarity and documentation value
    3. Ensure tests still provide the same coverage
    4. Optimize test execution speed where possible
    5. Verify coverage metrics unchanged or improved

    Report all test refactoring changes and confirm coverage is maintained.
```

Save output to `.tdd-cycle/08-refactored-tests.md`.

Update `state.json`: set `current_step` to "checkpoint-4", add step 8 to `completed_steps`.

---

## PHASE CHECKPOINT 4 — User Approval Required

Display refactoring summary from `.tdd-cycle/07-refactored-code.md` and `.tdd-cycle/08-refactored-tests.md` and ask:

```
REFACTOR phase complete.

Code changes: [summary of refactoring]
Test changes: [summary of test improvements]
Coverage: [maintained/improved]

1. Approve — proceed to integration testing
2. Request changes — adjust refactoring
3. Pause — save progress and stop here
```

---

## Phase 5: Integration and Extended Testing (Steps 9-11)

### Step 9: Write Integration Tests (Failing First)

Read `.tdd-cycle/07-refactored-code.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Write failing integration tests for $FEATURE"
  prompt: |
    You are a test automation expert writing integration tests in TDD style.

    Write FAILING integration tests for: $FEATURE

    ## Refactored Implementation
    [Insert contents of .tdd-cycle/07-refactored-code.md]

    ## Instructions
    1. Test component interactions, API contracts, and data flow
    2. Tests must fail initially (follow red-green-refactor)
    3. Focus on integration points identified in the architecture
    4. Include contract tests for API boundaries
    5. Follow existing project test patterns

    Write test files and report what they cover.
```

Save output to `.tdd-cycle/09-integration-tests.md`.

Update `state.json`: set `current_step` to 10, add step 9 to `completed_steps`.

### Step 10: Implement Integration

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement integration code for $FEATURE"
  prompt: |
    You are a backend architect implementing integration code.

    Implement integration code for: $FEATURE to make integration tests pass.

    ## Integration Tests
    [Insert contents of .tdd-cycle/09-integration-tests.md]

    ## Instructions
    1. Focus on component interaction and data flow
    2. Implement only what's needed to pass integration tests
    3. Follow existing project patterns for integration code

    Write code and report what was created/modified.
```

Save output to `.tdd-cycle/10-integration-impl.md`.

Update `state.json`: set `current_step` to 11, add step 10 to `completed_steps`.

### Step 11: Performance and Edge Case Tests

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Add performance and edge case tests for $FEATURE"
  prompt: |
    You are a test automation expert adding extended test coverage.

    Add performance tests and additional edge case tests for: $FEATURE

    ## Current Implementation
    [Insert contents of .tdd-cycle/10-integration-impl.md]

    ## Instructions
    1. Add stress tests and boundary tests
    2. Add error recovery tests
    3. Include performance benchmarks where appropriate
    4. Ensure all new tests pass

    Write test files and report coverage improvements.
```

Save output to `.tdd-cycle/11-extended-tests.md`.

Update `state.json`: set `current_step` to 12, add step 11 to `completed_steps`.

---

## Phase 6: Final Review (Step 12)

### Step 12: Final Code Review

Read all `.tdd-cycle/*.md` files.

Use the Task tool with the local code-reviewer agent:

```
Task:
  subagent_type: "code-reviewer"
  description: "Final TDD review of $FEATURE"
  prompt: |
    Perform comprehensive final review of: $FEATURE

    ## All Artifacts
    [Insert contents of all .tdd-cycle/*.md files]

    ## Instructions
    1. Verify TDD process was followed (red-green-refactor discipline)
    2. Check code quality and SOLID principle adherence
    3. Assess test quality and coverage completeness
    4. Verify no anti-patterns (test-after, skipped refactoring, etc.)
    5. Suggest any remaining improvements

    Provide a final review report with findings and recommendations.
```

Save output to `.tdd-cycle/12-final-review.md`.

Update `state.json`: set `current_step` to "complete", add step 12 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
TDD cycle complete: $FEATURE

## Files Created
[List all .tdd-cycle/ output files]

## TDD Metrics
- Test count: [total tests written]
- Coverage: [line/branch/function coverage]
- Phases completed: Specification > RED > GREEN > REFACTOR > Integration > Review
- Mode: [incremental|suite]

## Artifacts
- Requirements: .tdd-cycle/01-requirements.md
- Test Architecture: .tdd-cycle/02-test-architecture.md
- Failing Tests: .tdd-cycle/03-failing-tests.md
- Failure Verification: .tdd-cycle/04-failure-verification.md
- Implementation: .tdd-cycle/05-implementation.md
- Green Verification: .tdd-cycle/06-green-verification.md
- Refactored Code: .tdd-cycle/07-refactored-code.md
- Refactored Tests: .tdd-cycle/08-refactored-tests.md
- Integration Tests: .tdd-cycle/09-integration-tests.md
- Integration Impl: .tdd-cycle/10-integration-impl.md
- Extended Tests: .tdd-cycle/11-extended-tests.md
- Final Review: .tdd-cycle/12-final-review.md

## Next Steps
1. Review all generated code and test files
2. Run the full test suite to verify everything passes
3. Create a pull request with the implementation
4. Monitor coverage metrics in CI
```

## Incremental Development Mode

When `--incremental` flag is present:

1. Write ONE failing test
2. Make ONLY that test pass
3. Refactor if needed
4. Repeat for next test

The orchestrator adjusts the RED-GREEN-REFACTOR phases to operate on a single test at a time rather than full test suites.

## Validation Checklists

### RED Phase Validation

- [ ] All tests written before implementation
- [ ] All tests fail with meaningful error messages
- [ ] Test failures are due to missing implementation
- [ ] No test passes accidentally

### GREEN Phase Validation

- [ ] All tests pass
- [ ] No extra code beyond test requirements
- [ ] Coverage meets minimum thresholds
- [ ] No test was modified to make it pass

### REFACTOR Phase Validation

- [ ] All tests still pass after refactoring
- [ ] Code complexity reduced
- [ ] Duplication eliminated
- [ ] Performance improved or maintained
- [ ] Test readability improved

## Anti-Patterns to Avoid

- Writing implementation before tests
- Writing tests that already pass
- Skipping the refactor phase
- Writing multiple features without tests
- Modifying tests to make them pass
- Ignoring failing tests
- Writing tests after implementation

## Failure Recovery

If TDD discipline is broken:

1. **STOP** immediately
2. Identify which phase was violated
3. Rollback to last valid state
4. Resume from correct phase
5. Document lesson learned
