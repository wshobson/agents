---
model: claude-sonnet-4-5-20250929
---

Implement minimal code to make failing tests pass in TDD green phase:

[Extended thinking: This tool uses the test-automator agent to implement the minimal code necessary to make tests pass. It focuses on simplicity, avoiding over-engineering while ensuring all tests become green.]

## Implementation Process

Use Task tool with subagent_type="test-automator" to implement minimal passing code.

Prompt: "Implement MINIMAL code to make these failing tests pass: $ARGUMENTS. Follow TDD green phase principles:

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
   - One test at a time - don't try to pass all at once

3. **Code Structure Guidelines**
   - Write the minimal code that could possibly work
   - Avoid adding functionality not required by tests
   - Use simple data structures initially
   - Defer architectural decisions until refactor phase
   - Keep methods/functions small and focused
   - Don't add error handling unless tests require it

4. **Language-Specific Patterns**
   - **JavaScript/TypeScript**: Simple functions, avoid classes initially
   - **Python**: Functions before classes, simple returns
   - **Java**: Minimal class structure, no patterns yet
   - **C#**: Basic implementations, no interfaces yet
   - **Go**: Simple functions, defer goroutines/channels
   - **Ruby**: Procedural before object-oriented when possible

5. **Progressive Implementation**
   - Make first test pass with simplest possible code
   - Run tests after each change to verify progress
   - Add just enough code for next failing test
   - Resist urge to implement beyond test requirements
   - Keep track of technical debt for refactor phase
   - Document assumptions and shortcuts taken

6. **Common Green Phase Techniques**
   - Hard-coded returns for initial tests
   - Simple if/else for limited test cases
   - Basic loops only when iteration tests require
   - Minimal data structures (arrays before complex objects)
   - In-memory storage before database integration
   - Synchronous before asynchronous implementation

7. **Success Criteria**
   ✓ All tests pass (green)
   ✓ No extra functionality beyond test requirements
   ✓ Code is readable even if not optimal
   ✓ No broken existing functionality
   ✓ Implementation time is minimized
   ✓ Clear path to refactoring identified

8. **Anti-Patterns to Avoid**
   - Gold plating or adding unrequested features
   - Implementing design patterns prematurely
   - Complex abstractions without test justification
   - Performance optimizations without metrics
   - Adding tests during green phase
   - Refactoring during implementation
   - Ignoring test failures to move forward

9. **Implementation Metrics**
   - Time to green: Track implementation duration
   - Lines of code: Measure implementation size
   - Cyclomatic complexity: Keep it low initially
   - Test pass rate: Must reach 100%
   - Code coverage: Verify all paths tested

10. **Validation Steps**
    - Run all tests and confirm they pass
    - Verify no regression in existing tests
    - Check that implementation is truly minimal
    - Document any technical debt created
    - Prepare notes for refactoring phase

Output should include:
- Complete implementation code
- Test execution results showing all green
- List of shortcuts taken for later refactoring
- Implementation time metrics
- Technical debt documentation
- Readiness assessment for refactor phase"

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

- Follows from tdd-red.md test creation
- Prepares for tdd-refactor.md improvements
- Updates test coverage metrics
- Triggers CI/CD pipeline verification
- Documents technical debt for tracking

## Best Practices

- Embrace "good enough" for this phase
- Speed over perfection (perfection comes in refactor)
- Make it work, then make it right, then make it fast
- Trust that refactoring phase will improve code
- Keep changes small and incremental
- Celebrate reaching green state!

Tests to make pass: $ARGUMENTS