# Story Development Workflow

## Purpose
Implement user stories following TDD practices with comprehensive testing and documentation.

## Trigger
- User story assigned
- Feature development started
- Bug fix assigned

## Agents Involved
| Agent | Role | Model |
|-------|------|-------|
| python-pro / javascript-pro / etc. | Primary developer | sonnet |
| test-automator | Test creation | sonnet |
| tdd-orchestrator | TDD guidance | opus |
| code-reviewer | Review | opus |
| security-auditor | Security scan | opus |

## Workflow Steps

### Step 1: Story Analysis
**Agent:** tdd-orchestrator
**Actions:**
1. Review user story and acceptance criteria
2. Break down into technical tasks
3. Identify test scenarios
4. Plan implementation approach

**Output:** Technical task breakdown

### Step 2: Test First (Red Phase)
**Agent:** test-automator
**Actions:**
1. Write failing tests for acceptance criteria
2. Create unit test stubs
3. Define integration test scenarios
4. Verify tests fail appropriately

**Output:** Failing test suite

### Step 3: Implementation (Green Phase)
**Agent:** [language-pro agent]
**Actions:**
1. Implement minimal code to pass tests
2. Follow coding standards
3. Handle edge cases
4. Ensure all tests pass

**Output:** Working implementation

### Step 4: Refactor
**Agent:** [language-pro agent]
**Actions:**
1. Improve code quality
2. Remove duplication
3. Enhance readability
4. Optimize performance (if needed)
5. Ensure tests still pass

**Output:** Refactored code

### Step 5: Integration Testing
**Agent:** test-automator
**Actions:**
1. Run integration tests
2. Test with dependencies
3. Verify API contracts
4. Check database interactions

**Output:** Integration test results

### Step 6: Security Scan
**Agent:** security-auditor
**Actions:**
1. Run SAST analysis
2. Check for vulnerabilities
3. Verify secure coding practices
4. Scan dependencies

**Output:** Security scan report

### Step 7: Code Review
**Agent:** code-reviewer
**Actions:**
1. Review code quality
2. Check architecture compliance
3. Verify test coverage
4. Assess documentation

**Output:** Code review feedback

### Step 8: Documentation
**Agent:** docs-architect
**Actions:**
1. Update API documentation
2. Add code comments where needed
3. Update README if applicable
4. Create/update runbook entries

**Output:** Updated documentation

### Step 9: Merge & Deploy
**Agent:** deployment-engineer
**Actions:**
1. Merge approved code
2. Deploy to staging
3. Run smoke tests
4. Promote to production (if approved)

**Output:** Deployed feature

## TDD Cycle Reference
```
┌─────────────────────────────────────┐
│                                     │
│    ┌─────┐                          │
│    │ RED │ ← Write failing test     │
│    └──┬──┘                          │
│       │                             │
│       ▼                             │
│   ┌───────┐                         │
│   │ GREEN │ ← Make test pass        │
│   └───┬───┘                         │
│       │                             │
│       ▼                             │
│  ┌──────────┐                       │
│  │ REFACTOR │ ← Clean up code       │
│  └────┬─────┘                       │
│       │                             │
│       └─────────────────────────────┘
```

## Exit Criteria
- All acceptance criteria met
- All tests passing
- Code review approved
- Security scan passed
- Documentation updated
- Successfully deployed
