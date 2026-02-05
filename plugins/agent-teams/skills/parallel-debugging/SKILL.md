---
name: parallel-debugging
description: Debug complex issues using competing hypotheses with parallel investigation, evidence collection, and root cause arbitration. Use this skill when debugging bugs with multiple potential causes, performing root cause analysis, or organizing parallel investigation workflows.
version: 1.0.2
---

# Parallel Debugging

Framework for debugging complex issues using the Analysis of Competing Hypotheses (ACH) methodology with parallel agent investigation.

## When to Use This Skill

- Bug has multiple plausible root causes
- Initial debugging attempts haven't identified the issue
- Issue spans multiple modules or components
- Need systematic root cause analysis with evidence
- Want to avoid confirmation bias in debugging

## Hypothesis Generation Framework

Generate hypotheses across 6 failure mode categories:

### 1. Logic Error

- Incorrect conditional logic (wrong operator, missing case)
- Off-by-one errors in loops or array access
- Missing edge case handling
- Incorrect algorithm implementation

### 2. Data Issue

- Invalid or unexpected input data
- Type mismatch or coercion error
- Null/undefined/None where value expected
- Encoding or serialization problem
- Data truncation or overflow

### 3. State Problem

- Race condition between concurrent operations
- Stale cache returning outdated data
- Incorrect initialization or default values
- Unintended mutation of shared state
- State machine transition error

### 4. Integration Failure

- API contract violation (request/response mismatch)
- Version incompatibility between components
- Configuration mismatch between environments
- Missing or incorrect environment variables
- Network timeout or connection failure

### 5. Resource Issue

- Memory leak causing gradual degradation
- Connection pool exhaustion
- File descriptor or handle leak
- Disk space or quota exceeded
- CPU saturation from inefficient processing

### 6. Environment

- Missing runtime dependency
- Wrong library or framework version
- Platform-specific behavior difference
- Permission or access control issue
- Timezone or locale-related behavior

## Evidence Collection Standards

### What Constitutes Evidence

| Evidence Type     | Strength | Example                                                         |
| ----------------- | -------- | --------------------------------------------------------------- |
| **Direct**        | Strong   | Code at `file.ts:42` shows `if (x > 0)` should be `if (x >= 0)` |
| **Correlational** | Medium   | Error rate increased after commit `abc123`                      |
| **Testimonial**   | Weak     | "It works on my machine"                                        |
| **Absence**       | Variable | No null check found in the code path                            |

### Citation Format

Always cite evidence with file:line references:

```
**Evidence**: The validation function at `src/validators/user.ts:87`
does not check for empty strings, only null/undefined. This allows
empty email addresses to pass validation.
```

### Confidence Levels

| Level               | Criteria                                                                            |
| ------------------- | ----------------------------------------------------------------------------------- |
| **High (>80%)**     | Multiple direct evidence pieces, clear causal chain, no contradicting evidence      |
| **Medium (50-80%)** | Some direct evidence, plausible causal chain, minor ambiguities                     |
| **Low (<50%)**      | Mostly correlational evidence, incomplete causal chain, some contradicting evidence |

## Result Arbitration Protocol

After all investigators report:

### Step 1: Categorize Results

- **Confirmed**: High confidence, strong evidence, clear causal chain
- **Plausible**: Medium confidence, some evidence, reasonable causal chain
- **Falsified**: Evidence contradicts the hypothesis
- **Inconclusive**: Insufficient evidence to confirm or falsify

### Step 2: Compare Confirmed Hypotheses

If multiple hypotheses are confirmed, rank by:

1. Confidence level
2. Number of supporting evidence pieces
3. Strength of causal chain
4. Absence of contradicting evidence

### Step 3: Determine Root Cause

- If one hypothesis clearly dominates: declare as root cause
- If multiple hypotheses are equally likely: may be compound issue (multiple contributing causes)
- If no hypotheses confirmed: generate new hypotheses based on evidence gathered

### Step 4: Validate Fix

Before declaring the bug fixed:

- [ ] Fix addresses the identified root cause
- [ ] Fix doesn't introduce new issues
- [ ] Original reproduction case no longer fails
- [ ] Related edge cases are covered
- [ ] Relevant tests are added or updated
