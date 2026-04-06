---
name: quality-gate
description: "Verify agent task completion with file-change validation, test execution, secret scanning, and scope checking"
---

# Quality Gate

Run this skill after any agent reports a task as complete. Agent output is a CLAIM. Test output is EVIDENCE.

## Steps

### 1. File Change Validation
```bash
git diff --stat
git diff HEAD~1 --name-only
```
If no files changed, the task is **REJECTED**.

### 2. Test Execution
```bash
npm test > /tmp/current-results.txt 2>&1
```
Record: total tests, passed, failed, skipped. New failures are blockers.

### 3. Secret Scan
```bash
CHANGED=$(git diff HEAD~1 --name-only)
grep -rn "sk-\|AKIA\|ghp_" $CHANGED 2>/dev/null
grep -rn 'password\s*=\s*["\''][^"\'']*["\'']' $CHANGED 2>/dev/null
grep -rn "BEGIN.*PRIVATE KEY" $CHANGED 2>/dev/null
```
Any match is a **BLOCKER**.

### 4. Build Check
```bash
npm run build  # or: cargo build, go build, python -m py_compile
```
Build failure = task **FAILED**.

### 5. Scope Check
Verify only intended files were modified. Flag unexpected changes as scope creep.

## Verdicts

| Verdict | Meaning |
|---------|---------|
| VERIFIED | All checks pass |
| FAILED | Tests fail or build broken |
| BLOCKED | Secrets found |
| REJECTED | No files changed |
| INCOMPLETE | Partial work done |
