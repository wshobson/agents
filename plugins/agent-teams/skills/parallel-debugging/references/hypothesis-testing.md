# Hypothesis Testing Reference

Task templates, evidence formats, and arbitration decision trees for parallel debugging.

## Hypothesis Task Template

```markdown
## Hypothesis Investigation: {Hypothesis Title}

### Hypothesis Statement

{Clear, falsifiable statement about the root cause}

### Failure Mode Category

{Logic Error | Data Issue | State Problem | Integration Failure | Resource Issue | Environment}

### Investigation Scope

- Files to examine: {file list or directory}
- Related tests: {test files}
- Git history: {relevant date range or commits}

### Evidence Criteria

**Confirming evidence** (if I find these, hypothesis is supported):

1. {Observable condition 1}
2. {Observable condition 2}

**Falsifying evidence** (if I find these, hypothesis is wrong):

1. {Observable condition 1}
2. {Observable condition 2}

### Report Format

- Confidence: High/Medium/Low
- Evidence: list with file:line citations
- Causal chain: step-by-step from cause to symptom
- Recommended fix: if confirmed
```

## Evidence Report Template

```markdown
## Investigation Report: {Hypothesis Title}

### Verdict: {Confirmed | Falsified | Inconclusive}

### Confidence: {High (>80%) | Medium (50-80%) | Low (<50%)}

### Confirming Evidence

1. `src/api/users.ts:47` — {description of what was found}
2. `src/middleware/auth.ts:23` — {description}

### Contradicting Evidence

1. `tests/api/users.test.ts:112` — {description of what contradicts}

### Causal Chain (if confirmed)

1. {First cause} →
2. {Intermediate effect} →
3. {Observable symptom}

### Recommended Fix

{Specific code change with location}

### Additional Notes

{Anything discovered that may be relevant to other hypotheses}
```

## Arbitration Decision Tree

```
All investigators reported?
├── NO → Wait for remaining reports
└── YES → Count confirmed hypotheses
          ├── 0 confirmed
          │   ├── Any medium confidence? → Investigate further
          │   └── All low/falsified? → Generate new hypotheses
          ├── 1 confirmed
          │   └── High confidence?
          │       ├── YES → Declare root cause, propose fix
          │       └── NO → Flag as likely cause, recommend verification
          └── 2+ confirmed
              └── Are they related?
                  ├── YES → Compound issue (multiple contributing causes)
                  └── NO → Rank by confidence, declare highest as primary
```

## Common Hypothesis Patterns by Error Type

### "500 Internal Server Error"

1. Unhandled exception in request handler (Logic Error)
2. Database connection failure (Resource Issue)
3. Missing environment variable (Environment)

### "Race condition / intermittent failure"

1. Shared state mutation without locking (State Problem)
2. Async operation ordering assumption (Logic Error)
3. Cache staleness window (State Problem)

### "Works locally, fails in production"

1. Environment variable mismatch (Environment)
2. Different dependency version (Environment)
3. Resource limits (memory, connections) (Resource Issue)

### "Regression after deploy"

1. New code introduced bug (Logic Error)
2. Configuration change (Integration Failure)
3. Database migration issue (Data Issue)
