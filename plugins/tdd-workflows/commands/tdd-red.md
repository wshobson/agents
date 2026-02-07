---
description: "Write comprehensive failing tests following TDD red phase principles"
argument-hint: "<feature or component to write tests for>"
---

# TDD Red Phase

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Write tests only — no production code.** Do NOT implement any production code during this phase.
2. **Verify tests fail.** All generated tests MUST fail when run. If any test passes, investigate and fix.
3. **Halt on error.** If test generation fails (syntax errors, import issues), STOP and present the error to the user.
4. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
5. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. Execute directly.

## Test Generation Process

Use the Task tool to generate failing tests:

```
Task:
  subagent_type: "general-purpose"
  description: "Generate comprehensive failing tests for TDD red phase"
  prompt: |
    You are a test automation expert specializing in TDD red phase test generation.

    Generate comprehensive FAILING tests for: $ARGUMENTS

    ## Core Requirements

    1. **Test Structure**
       - Framework-appropriate setup (Jest/pytest/JUnit/Go/RSpec — match project conventions)
       - Arrange-Act-Assert pattern
       - should_X_when_Y naming convention
       - Isolated fixtures with no interdependencies

    2. **Behavior Coverage**
       - Happy path scenarios
       - Edge cases (empty, null, boundary values)
       - Error handling and exceptions
       - Concurrent access (if applicable)

    3. **Failure Verification**
       - Tests MUST fail when run
       - Failures for RIGHT reasons (not syntax/import errors)
       - Meaningful diagnostic error messages
       - No cascading failures

    4. **Test Categories**
       - Unit: Isolated component behavior
       - Integration: Component interaction
       - Contract: API/interface contracts
       - Property: Mathematical invariants (if applicable)

    ## Quality Checklist

    - Readable test names documenting intent
    - One behavior per test
    - No implementation leakage
    - Meaningful test data (not 'foo'/'bar')
    - Tests serve as living documentation

    ## Anti-Patterns to Avoid

    - Tests passing immediately
    - Testing implementation vs behavior
    - Complex setup code
    - Multiple responsibilities per test
    - Brittle tests tied to specifics

    ## Output Requirements

    - Complete test files with imports
    - Documentation of test purpose
    - Commands to run and verify failures
    - Metrics: test count, coverage areas
    - Next steps for green phase
```

## Validation

After generation:

1. Run tests — confirm they fail
2. Verify helpful failure messages
3. Check test independence
4. Ensure comprehensive coverage

## Edge Case Categories

- **Null/Empty**: undefined, null, empty string/array/object
- **Boundaries**: min/max values, single element, capacity limits
- **Special Cases**: Unicode, whitespace, special characters
- **State**: Invalid transitions, concurrent modifications
- **Errors**: Network failures, timeouts, permissions
