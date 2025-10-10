---
model: claude-sonnet-4-5-20250929
---

Write comprehensive failing tests following TDD red phase principles:

[Extended thinking: This tool uses the test-automator agent to generate comprehensive failing tests that properly define expected behavior. It ensures tests fail for the right reasons and establishes a solid foundation for implementation.]

## Test Generation Process

Use Task tool with subagent_type="test-automator" to generate failing tests.

Prompt: "Generate comprehensive FAILING tests for: $ARGUMENTS. Follow TDD red phase principles:

1. **Test Structure Setup**
   - Choose appropriate testing framework for the language/stack
   - Set up test fixtures and necessary imports
   - Configure test runners and assertion libraries
   - Establish test naming conventions (should_X_when_Y format)

2. **Behavior Definition**
   - Define clear expected behaviors from requirements
   - Cover happy path scenarios thoroughly
   - Include edge cases and boundary conditions
   - Add error handling and exception scenarios
   - Consider null/undefined/empty input cases

3. **Test Implementation**
   - Write descriptive test names that document intent
   - Keep tests focused on single behaviors (one assertion per test when possible)
   - Use Arrange-Act-Assert (AAA) pattern consistently
   - Implement test data builders for complex objects
   - Avoid test interdependencies - each test must be isolated

4. **Failure Verification**
   - Ensure tests actually fail when run
   - Verify failure messages are meaningful and diagnostic
   - Confirm tests fail for the RIGHT reasons (not syntax/import errors)
   - Check that error messages guide implementation
   - Validate test isolation - no cascading failures

5. **Test Categories**
   - **Unit Tests**: Isolated component behavior
   - **Integration Tests**: Component interaction scenarios
   - **Contract Tests**: API and interface contracts
   - **Property Tests**: Invariants and mathematical properties
   - **Acceptance Tests**: User story validation

6. **Framework-Specific Patterns**
   - **JavaScript/TypeScript**: Jest, Mocha, Vitest patterns
   - **Python**: pytest fixtures and parameterization
   - **Java**: JUnit5 annotations and assertions
   - **C#**: NUnit/xUnit attributes and theory data
   - **Go**: Table-driven tests and subtests
   - **Ruby**: RSpec expectations and contexts

7. **Test Quality Checklist**
   ✓ Tests are readable and self-documenting
   ✓ Failure messages clearly indicate what went wrong
   ✓ Tests follow DRY principle with appropriate abstractions
   ✓ Coverage includes positive, negative, and edge cases
   ✓ Tests can serve as living documentation
   ✓ No implementation details leaked into tests
   ✓ Tests use meaningful test data, not 'foo' and 'bar'

8. **Common Anti-Patterns to Avoid**
   - Writing tests that pass immediately
   - Testing implementation instead of behavior
   - Overly complex test setup
   - Brittle tests tied to specific implementations
   - Tests with multiple responsibilities
   - Ignored or commented-out tests
   - Tests without clear assertions

Output should include:
- Complete test file(s) with all necessary imports
- Clear documentation of what each test validates
- Verification commands to run tests and see failures
- Metrics: number of tests, coverage areas, test categories
- Next steps for moving to green phase"

## Validation Steps

After test generation:
1. Run tests to confirm they fail
2. Verify failure messages are helpful
3. Check test independence and isolation
4. Ensure comprehensive coverage
5. Document any assumptions made

## Recovery Process

If tests don't fail properly:
- Debug import/syntax issues first
- Ensure test framework is properly configured
- Verify assertions are actually checking behavior
- Add more specific assertions if needed
- Consider missing test categories

## Integration Points

- Links to tdd-green.md for implementation phase
- Coordinates with tdd-refactor.md for improvement phase
- Integrates with CI/CD for automated verification
- Connects to test coverage reporting tools

## Best Practices

- Start with the simplest failing test
- One behavior change at a time
- Tests should tell a story of the feature
- Prefer many small tests over few large ones
- Use test naming as documentation
- Keep test code as clean as production code

Test requirements: $ARGUMENTS