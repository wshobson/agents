---
description: "Implement minimal code to make failing tests pass in TDD green phase"
argument-hint: "<description of failing tests or test file paths>"
---

# TDD Green Phase

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Implement only what tests require.** Do NOT add features, optimizations, or error handling beyond what failing tests demand.
2. **Run tests after each change.** Verify progress incrementally — do not batch implement and hope it works.
3. **Halt on failure.** If tests remain red after implementation or existing tests break, STOP and present the error to the user.
4. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
5. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. Execute directly.

## Implementation Process

Use the Task tool to implement minimal passing code:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement minimal code to pass failing tests"
  prompt: |
    You are a test automation expert implementing the GREEN phase of TDD.

    Implement MINIMAL code to make these failing tests pass: $ARGUMENTS

    Follow TDD green phase principles:

    1. **Pre-Implementation Analysis**
       - Review all failing tests and their error messages
       - Identify the simplest path to make tests pass
       - Map test requirements to minimal implementation needs
       - Avoid premature optimization or over-engineering
       - Focus only on making tests green, not perfect code

    2. **Implementation Strategy**
       - **Fake It**: Return hard-coded values when appropriate
       - **Obvious Implementation**: When solution is trivial and clear
       - **Triangulation**: Generalize only when multiple tests require it
       - Start with the simplest test and work incrementally
       - One test at a time — don't try to pass all at once

    3. **Code Structure Guidelines**
       - Write the minimal code that could possibly work
       - Avoid adding functionality not required by tests
       - Use simple data structures initially
       - Defer architectural decisions until refactor phase
       - Keep methods/functions small and focused
       - Don't add error handling unless tests require it

    4. **Progressive Implementation**
       - Make first test pass with simplest possible code
       - Run tests after each change to verify progress
       - Add just enough code for next failing test
       - Resist urge to implement beyond test requirements
       - Keep track of technical debt for refactor phase
       - Document assumptions and shortcuts taken

    5. **Success Criteria**
       - All tests pass (green)
       - No extra functionality beyond test requirements
       - Code is readable even if not optimal
       - No broken existing functionality
       - Clear path to refactoring identified

    Output should include:
    - Complete implementation code
    - Test execution results showing all green
    - List of shortcuts taken for later refactoring
    - Technical debt documentation
    - Readiness assessment for refactor phase
```

## Post-Implementation Checks

After implementation:

1. Run full test suite to confirm all tests pass
2. Verify no existing tests were broken
3. Document areas needing refactoring
4. Check implementation is truly minimal
5. Record implementation time for metrics

## Recovery Process

If tests still fail:

- Review test requirements carefully
- Check for misunderstood assertions
- Add minimal code to address specific failures
- Avoid the temptation to rewrite from scratch
- Consider if tests themselves need adjustment

## Integration Points

- Follows from tdd-red test creation
- Prepares for tdd-refactor improvements
- Updates test coverage metrics
- Triggers CI/CD pipeline verification
- Documents technical debt for tracking
