UPDATED !

# TDD Agent Usage Examples

This document demonstrates how to use the TDD-related agents in Claude Code for test-driven development workflows.

## TDD Orchestrator Agent

The `tdd-orchestrator` agent manages the complete TDD workflow, coordinating between multiple specialized agents.

### Basic Usage

```bash
# Invoke TDD orchestrator for a new feature
Use the Task tool with subagent_type="tdd-orchestrator"
Prompt: "Implement user authentication with TDD approach using JWT tokens"

# The orchestrator will:
# 1. Analyze requirements and design test strategy
# 2. Coordinate with test-automator for test creation
# 3. Manage the red-green-refactor cycle
# 4. Track metrics and ensure TDD compliance
```

### Advanced Orchestration

```bash
# Multi-team TDD coordination
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Coordinate TDD workflow across frontend, backend, and mobile teams for shopping cart feature"

# Property-based TDD
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Implement sort algorithm using property-based TDD with invariant checking"

# Legacy code TDD
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Add tests to legacy PaymentProcessor class before refactoring, using characterization tests"
```

## Test Automator with TDD Capabilities

The enhanced `test-automator` agent now includes comprehensive TDD support.

### Test-First Development

```bash
# Generate failing tests first
Use Task tool with subagent_type="test-automator"
Prompt: "Generate comprehensive failing tests for user registration with email verification. Ensure tests fail for the right reasons."

# Incremental test development
Use Task tool with subagent_type="test-automator"
Prompt: "Create incremental test suite for shopping cart: start with add item, then remove, then calculate total"

# Property-based TDD tests
Use Task tool with subagent_type="test-automator"
Prompt: "Generate property-based tests for string utilities library using hypothesis/fast-check"
```

### TDD Metrics and Compliance

```bash
# Track TDD metrics
Use Task tool with subagent_type="test-automator"
Prompt: "Analyze codebase and generate TDD compliance report: test-first percentage, cycle times, refactoring frequency"

# Verify TDD discipline
Use Task tool with subagent_type="test-automator"
Prompt: "Check if recent commits followed TDD: tests written before implementation"
```

## Language-Specific TDD Examples

### Python TDD

```bash
Use Task tool with subagent_type="python-pro"
Prompt: "Implement binary search tree with TDD approach using pytest. Start with failing tests for insert, search, delete operations."

Use Task tool with subagent_type="test-automator"
Prompt: "Generate Python pytest tests for REST API with TDD: write contract tests first, then unit tests, following Chicago school TDD"
```

### JavaScript/TypeScript TDD

```bash
Use Task tool with subagent_type="typescript-pro"
Prompt: "Build React component using TDD with Jest and React Testing Library. Start with behavior tests, then implement minimally."

Use Task tool with subagent_type="javascript-pro"
Prompt: "Implement Express middleware with TDD approach, using Mocha and Chai. Follow London school with mocks."
```

### Java TDD

```bash
Use Task tool with subagent_type="java-pro"
Prompt: "Create Spring Boot service with TDD using JUnit 5 and Mockito. Start with integration tests, then unit tests."
```

### Go TDD

```bash
Use Task tool with subagent_type="golang-pro"
Prompt: "Build gRPC service with TDD approach using Go's testing package and testify. Include table-driven tests."
```

## TDD Workflow Patterns

### Classic Red-Green-Refactor

```bash
# Step 1: RED - Write failing test
Use Task tool with subagent_type="test-automator"
Prompt: "Write failing test for fibonacci function that handles negative numbers"

# Step 2: GREEN - Minimal implementation
Use Task tool with subagent_type="python-pro"
Prompt: "Implement minimal fibonacci function to make the test pass"

# Step 3: REFACTOR - Improve code
Use Task tool with subagent_type="code-reviewer"
Prompt: "Refactor fibonacci implementation for performance while keeping tests green"
```

### Outside-In TDD (London School)

```bash
# Start with acceptance test
Use Task tool with subagent_type="test-automator"
Prompt: "Write acceptance test for user login flow using Cucumber/Gherkin"

# Work inward with mocks
Use Task tool with subagent_type="test-automator"
Prompt: "Write unit tests for login controller with mocked dependencies"

# Implement with TDD
Use Task tool with subagent_type="backend-architect"
Prompt: "Implement login controller to satisfy tests, using dependency injection"
```

### Inside-Out TDD (Chicago School)

```bash
# Start with unit tests
Use Task tool with subagent_type="test-automator"
Prompt: "Write unit tests for individual calculation functions"

# Build up to integration
Use Task tool with subagent_type="test-automator"
Prompt: "Write integration tests combining calculation functions"

# Final acceptance tests
Use Task tool with subagent_type="test-automator"
Prompt: "Write end-to-end tests for complete calculation workflow"
```

## Specialized TDD Scenarios

### API Development with TDD

```bash
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "
Develop REST API for blog platform with TDD:
1. Start with OpenAPI spec
2. Generate contract tests from spec
3. Implement endpoints test-first
4. Add integration tests
5. Include performance tests
"
```

### Microservices TDD

```bash
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "
Build microservice with TDD approach:
- Contract tests for API
- Unit tests for business logic
- Integration tests for database
- Component tests for service
- End-to-end tests for workflows
"
```

### Frontend Component TDD

```bash
Use Task tool with subagent_type="frontend-developer"
Prompt: "
Build date picker component with TDD:
1. Test component renders
2. Test date selection
3. Test keyboard navigation
4. Test accessibility
5. Test date validation
All tests first, then implementation
"
```

### Database Migration TDD

```bash
Use Task tool with subagent_type="database-optimizer"
Prompt: "
Perform database migration with TDD:
1. Write tests for current schema behavior
2. Write tests for desired schema behavior
3. Implement migration to pass both
4. Include rollback tests
"
```

## TDD Anti-Pattern Detection

```bash
# Detect test-after development
Use Task tool with subagent_type="code-reviewer"
Prompt: "Review recent commits and identify where tests were written after implementation"

# Find over-mocked tests
Use Task tool with subagent_type="test-automator"
Prompt: "Analyze test suite and identify tests with excessive mocking that don't test real behavior"

# Identify missing test coverage
Use Task tool with subagent_type="test-automator"
Prompt: "Find code paths without tests and suggest test cases following TDD approach"
```

## TDD Metrics and Reporting

```bash
# Generate TDD dashboard
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Create TDD metrics dashboard showing: cycle times, test-first percentage, refactoring frequency, coverage trends"

# Team TDD assessment
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Assess team's TDD maturity level and provide improvement recommendations"

# TDD ROI analysis
Use Task tool with subagent_type="business-analyst"
Prompt: "Calculate ROI of TDD adoption: bug reduction, development speed, maintenance costs"
```

## TDD Learning and Katas

```bash
# TDD Kata practice
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Guide me through the Roman Numerals kata using strict TDD"

# TDD workshop material
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Create TDD workshop with exercises for team training"

# TDD code review
Use Task tool with subagent_type="code-reviewer"
Prompt: "Review this code for TDD best practices and provide specific improvement suggestions"
```

## Integration with CI/CD

```bash
# TDD pipeline setup
Use Task tool with subagent_type="deployment-engineer"
Prompt: "Setup CI/CD pipeline that enforces TDD: verify tests written before code, check coverage, track metrics"

# Pre-commit TDD hooks
Use Task tool with subagent_type="dx-optimizer"
Prompt: "Create git hooks that ensure TDD compliance before allowing commits"
```

## TDD for Different Architectures

### Hexagonal Architecture with TDD

```bash
Use Task tool with subagent_type="architect-review"
Prompt: "Implement hexagonal architecture service with TDD: start with domain tests, then ports, then adapters"
```

### Event-Driven TDD

```bash
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Build event-driven system with TDD: test event production, consumption, and choreography"
```

### Serverless TDD

```bash
Use Task tool with subagent_type="cloud-architect"
Prompt: "Develop Lambda functions with TDD approach, including local testing and integration tests"
```

## Common TDD Commands Combinations

### Full TDD Feature Development

```bash
# 1. Design tests with orchestrator
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Design comprehensive test strategy for payment processing feature"

# 2. Generate tests with automator
Use Task tool with subagent_type="test-automator"
Prompt: "Generate all test cases identified in strategy"

# 3. Implement with language expert
Use Task tool with subagent_type="python-pro"
Prompt: "Implement payment processing to pass tests incrementally"

# 4. Review and refactor
Use Task tool with subagent_type="code-reviewer"
Prompt: "Review implementation and suggest refactoring while maintaining green tests"

# 5. Optimize performance
Use Task tool with subagent_type="performance-engineer"
Prompt: "Optimize payment processing performance with TDD approach"
```

### TDD Bug Fix Workflow

```bash
# 1. Reproduce with test
Use Task tool with subagent_type="test-automator"
Prompt: "Write test that reproduces bug #123: user cannot login with special characters"

# 2. Fix minimally
Use Task tool with subagent_type="debugger"
Prompt: "Fix bug with minimal changes to make test pass"

# 3. Add edge cases
Use Task tool with subagent_type="test-automator"
Prompt: "Add additional test cases for edge cases related to bug"

# 4. Refactor if needed
Use Task tool with subagent_type="code-reviewer"
Prompt: "Suggest refactoring to prevent similar bugs"
```

## Best Practices for Agent Usage

1. **Start with tdd-orchestrator** for complex features requiring coordination
2. **Use test-automator** for test generation and verification
3. **Leverage language-specific agents** for implementation phase
4. **Employ code-reviewer** for refactoring phase
5. **Track with business-analyst** for metrics and ROI

## Troubleshooting

### When Tests Don't Fail

```bash
Use Task tool with subagent_type="test-automator"
Prompt: "Verify these tests actually fail when implementation is removed (mutation testing)"
```

### When TDD Feels Slow

```bash
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Optimize TDD workflow for faster feedback loops"
```

### When Team Resists TDD

```bash
Use Task tool with subagent_type="tdd-orchestrator"
Prompt: "Create gradual TDD adoption plan for team with training materials"
```

## Advanced TDD Techniques

### Approval Testing

```bash
Use Task tool with subagent_type="test-automator"
Prompt: "Setup approval testing for complex output verification"
```

### Snapshot Testing

```bash
Use Task tool with subagent_type="test-automator"
Prompt: "Implement snapshot testing for UI components with TDD"
```

### Contract Testing

```bash
Use Task tool with subagent_type="test-automator"
Prompt: "Create contract tests between services using Pact with TDD approach"
```

## Next Steps

1. Try the [TDD workflow commands](/workflows:tdd-cycle)
2. Practice with TDD katas using tdd-orchestrator
3. Integrate TDD agents into your development workflow
4. Track TDD metrics with test-automator
5. Share TDD success stories with your team
