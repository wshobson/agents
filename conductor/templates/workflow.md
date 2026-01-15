# Development Workflow

## Core Principles

1. **plan.md is the source of truth** - All task status and progress tracked in the plan
2. **Test-Driven Development** - Red → Green → Refactor cycle with 80% coverage target
3. **CI/CD Compatibility** - All changes must pass automated pipelines before merge
4. **Incremental Progress** - Small, verifiable commits with clear purpose

## Task Lifecycle

### Step 1: Task Selection

- Review plan.md for next pending task
- Verify dependencies are complete
- Confirm understanding of acceptance criteria

### Step 2: Progress Marking

- Update task status in plan.md from `[ ]` to `[~]`
- Note start time if tracking velocity

### Step 3: Red Phase (Write Failing Tests)

- Write test(s) that define expected behavior
- Verify test fails for the right reason
- Keep tests focused and minimal

### Step 4: Green Phase (Make Tests Pass)

- Write minimum code to pass tests
- Avoid premature optimization
- Focus on correctness over elegance

### Step 5: Refactor Phase

- Improve code structure without changing behavior
- Apply relevant style guide conventions
- Remove duplication and clarify intent

### Step 6: Coverage Verification

- Run coverage report
- Ensure new code meets 80% threshold
- Add edge case tests if coverage gaps exist

### Step 7: Deviation Documentation

- If implementation differs from spec, document why
- Update spec if change is permanent
- Flag for review if uncertain

### Step 8: Code Commit

- Stage related changes only
- Write clear commit message referencing task
- Format: `[track-id] task: description`

### Step 9: Git Notes (Optional)

- Add implementation notes for complex changes
- Reference relevant decisions or trade-offs

### Step 10: Plan Update

- Mark task as `[x]` completed in plan.md
- Update any affected downstream tasks
- Note blockers or follow-up items

### Step 11: Plan Commit

- Commit plan.md changes separately
- Format: `[track-id] plan: mark task X complete`

## Phase Completion Protocol

### Checkpoint Commits

At the end of each phase:

1. Ensure all phase tasks are `[x]` complete
2. Run full test suite
3. Verify coverage meets threshold
4. Create checkpoint commit: `[track-id] checkpoint: phase N complete`

### Test Verification

```bash
{{TEST_COMMAND}}
{{COVERAGE_COMMAND}}
```

### Manual Approval Gates

Phases requiring approval before proceeding:

- Architecture changes
- API contract modifications
- Database schema changes
- Security-sensitive implementations

## Quality Assurance Gates

All code must pass these criteria before merge:

| Gate        | Requirement              | Command                  |
| ----------- | ------------------------ | ------------------------ |
| 1. Tests    | All tests passing        | `{{TEST_COMMAND}}`       |
| 2. Coverage | Minimum 80%              | `{{COVERAGE_COMMAND}}`   |
| 3. Style    | Follows style guide      | `{{LINT_COMMAND}}`       |
| 4. Docs     | Public APIs documented   | Manual review            |
| 5. Types    | No type errors           | `{{TYPE_CHECK_COMMAND}}` |
| 6. Linting  | No lint errors           | `{{LINT_COMMAND}}`       |
| 7. Mobile   | Responsive if applicable | Manual review            |
| 8. Security | No known vulnerabilities | `{{SECURITY_COMMAND}}`   |

## Development Commands

### Environment Setup

```bash
{{SETUP_COMMAND}}
```

### Development Server

```bash
{{DEV_COMMAND}}
```

### Pre-Commit Checks

```bash
{{PRE_COMMIT_COMMAND}}
```

### Full Validation

```bash
{{VALIDATE_COMMAND}}
```

## Workflow Diagram

```
┌─────────────┐
│ Select Task │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Mark [~]    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ RED: Write  │
│ Failing Test│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ GREEN: Make │
│ Test Pass   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ REFACTOR    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Verify      │
│ Coverage    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Commit Code │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Mark [x]    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Commit Plan │
└─────────────┘
```
