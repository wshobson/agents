---
name: analysis-result-interpretation
description: Interprets and acts on analysis results from Gemini CLI. Covers result formats, confidence levels, actionability assessment, decision frameworks, and communication strategies. Use when deciding how to respond to analysis findings or formulating follow-up actions.
---

# Analysis Result Interpretation Skill

## When to Use This Skill

- Understanding what Gemini CLI analysis results mean
- Deciding what action to take based on findings
- Interpreting confidence levels and relevance scores
- Formatting analysis results for team communication
- Bridging gap between analysis output and business decisions
- Determining when additional investigation is needed

## Result Format Understanding

### JSON Result Structure

Gemini CLI returns structured JSON with consistent format:

```json
{
  "status": "success|error|partial",
  "command": "original_command_executed",
  "query_time_ms": 1234,
  "codebase_size": {
    "files": 5000,
    "lines_of_code": 1000000
  },
  "results": [
    {
      "type": "finding",
      "severity": "critical|high|medium|low|info",
      "confidence": 0.95,
      "location": "path/to/file.ts:123",
      "context": "Code snippet showing context",
      "description": "What was found",
      "impact": "Why it matters",
      "recommendation": "What to do about it",
      "tags": ["performance", "security"]
    }
  ],
  "summary": {
    "total_findings": 42,
    "by_severity": {
      "critical": 2,
      "high": 5,
      "medium": 15,
      "low": 20
    }
  },
  "metadata": {
    "execution_time_ms": 5000,
    "scope": "codebase",
    "timestamp": "2025-10-26T10:30:00Z"
  }
}
```

### Understanding Confidence Scores

| Confidence | Meaning | Actionability |
|------------|---------|---------------|
| 0.95-1.0 | Virtually certain | Take action immediately |
| 0.85-0.94 | Very likely | Prioritize for review/action |
| 0.70-0.84 | Likely | Include in backlog, review |
| 0.50-0.69 | Moderate confidence | Investigate further before action |
| <0.50 | Low confidence | Flag for human review, don't act |

### Understanding Severity Levels

| Severity | Urgency | Response Timeline | Example |
|----------|---------|-------------------|---------|
| Critical | Immediate | Fix today, blocks work | Active memory leak, security vulnerability |
| High | This week | Prioritize for sprint | Large refactoring need, major code smell |
| Medium | This month | Include in planning | Code duplication, minor architectural issue |
| Low | Backlog | Address in refactoring | Style issue, minor improvement |
| Info | Context only | Reference material | Code structure information, statistics |

## Actionability Assessment

When you see results, ask:

### 1. Is this Confident Enough?
- Confidence > 0.85? → Proceed with action
- Confidence 0.70-0.85? → Review with team before action
- Confidence < 0.70? → Investigate further, don't assume

### 2. Is This Severity Justified?
- Critical finding about non-critical code? → Downgrade to High
- Low-level finding about critical code? → Upgrade to Medium
- Does severity match business impact? → Adjust as needed

### 3. Is This Actionable Right Now?
- Can fix in next 1-2 days? → Add to sprint
- Would require large refactor? → Add to backlog with estimation
- Requires investigation first? → Create investigation task
- Needs team discussion? → Schedule design review

### 4. What's the Cost-Benefit?
- Effort to fix: Low effort + High impact → Do immediately
- Effort to fix: High effort + Low impact → Defer to backlog
- Effort to fix: High effort + High impact → Estimate and prioritize
- Effort to fix: Low effort + Low impact → Nice-to-have, do if time allows

## Result Interpretation Patterns

### Pattern 1: Security Finding

```json
{
  "severity": "critical",
  "description": "SQL injection vulnerability in user search",
  "location": "src/api/users.ts:45",
  "impact": "Attacker could access database directly",
  "recommendation": "Use parameterized queries"
}
```

**Interpretation:**
- Confidence + Critical severity = Act immediately
- Check if vulnerability is exploitable in current code path
- Create security incident if in production
- Fix and deploy as hotfix
- Add regression test

**Action:** IMMEDIATE

### Pattern 2: Code Smell Finding

```json
{
  "severity": "medium",
  "description": "Large class with 50+ methods",
  "location": "src/services/UserService.ts:1-2000",
  "impact": "Hard to test, maintain, understand",
  "recommendation": "Extract domain responsibilities into separate classes"
}
```

**Interpretation:**
- Medium severity + moderate confidence = Prioritize for next sprint
- Estimate refactoring effort (likely 2-3 days)
- Break into smaller refactoring PRs
- Add to backlog with estimated story points

**Action:** BACKLOG (HIGH PRIORITY)

### Pattern 3: Informational Finding

```json
{
  "severity": "info",
  "description": "Codebase uses 12 different HTTP client libraries",
  "location": "Multiple files",
  "impact": "Inconsistency, maintenance burden",
  "recommendation": "Standardize on one HTTP client across codebase"
}
```

**Interpretation:**
- Info level = FYI, context for decisions
- Not urgent but worth addressing in long-term planning
- Could be addressed during architectural refactoring
- Use as input to tech strategy discussions

**Action:** STRATEGIC PLANNING

## Decision Framework

```
Result received
├─ Status = error?
│   └─ Investigation needed → Debug Gemini CLI execution
│
├─ Status = partial?
│   └─ Some results missing → Re-run with broader scope
│
└─ Status = success?
    ├─ Severity = critical?
    │   ├─ Confidence > 0.85?
    │   │   └─ ACTION: Fix immediately, security incident if needed
    │   └─ Confidence < 0.85?
    │       └─ ACTION: Verify before acting
    │
    ├─ Severity = high?
    │   ├─ Effort < 1 day?
    │   │   └─ ACTION: Schedule for current sprint
    │   └─ Effort > 1 day?
    │       └─ ACTION: Estimate and add to backlog
    │
    ├─ Severity = medium?
    │   └─ ACTION: Add to backlog, schedule for future sprint
    │
    └─ Severity = low|info?
        └─ ACTION: Reference material or nice-to-have
```

## Communication Strategies

### For Leadership (Executive Summary)

Focus on business impact:

```markdown
# Codebase Analysis Summary

**Critical Issues:** 2 (Security vulnerabilities in auth module)
**High Issues:** 8 (Technical debt in data layer)
**Total Refactoring Effort Estimate:** 3 weeks

**Recommendation:** Prioritize security issues immediately (production impact),
schedule tech debt fixes for Q4 planning (maintainability improvement).
```

### For Development Team (Detailed Report)

Focus on how-to-fix:

```markdown
# Codebase Analysis - Developer Briefing

## Critical: SQL Injection in User Search
- **Location:** src/api/users.ts:45
- **Current Code:** `query = "SELECT * FROM users WHERE name='" + input + "'"`
- **Issue:** User input not escaped, allows SQL injection
- **Fix:** Use parameterized query: `db.query("SELECT * FROM users WHERE name=?", [input])`
- **Effort:** 1 hour
- **Testing:** Add unit test with injection payload

## High: Large UserService Class
- **Location:** src/services/UserService.ts
- **Size:** 2000 lines, 50+ methods
- **Issue:** Multiple responsibilities (user CRUD, auth, notifications)
- **Refactoring Plan:**
  1. Extract UserRepository (CRUD operations)
  2. Extract AuthService (authentication logic)
  3. Extract UserNotificationService (notifications)
- **Effort:** 3 days across 3 PRs
```

### For Stakeholders (Business Impact)

Focus on implications:

```markdown
# Technical Health Report

**Code Quality:** 6/10 (declining)
**Security:** 4/10 (2 critical vulnerabilities)
**Maintainability:** 5/10 (increasing technical debt)

**Impact on Velocity:**
- Current issues causing 20% of PR review rework
- Security issues pose business liability risk
- Tech debt slowing feature development by 15%

**Recommended Action:** Allocate 2 sprints for priority fixes
(ROI: 20% velocity improvement + risk reduction)
```

## Special Cases

### Case 1: High Confidence, Low Severity Finding

Example: "Database has unused indexes"

**Decision:** Low priority, but zero-cost optimization
**Action:** Include in maintenance window, don't create emergency ticket

### Case 2: Low Confidence, High Severity Finding

Example: "Possible memory leak (confidence 0.45)"

**Decision:** Cannot act on low confidence, but cannot ignore
**Action:** Create investigation task, require manual verification before fixing

### Case 3: Multiple Related Findings

Example: 5 different code smell findings in same class

**Decision:** Address together as unified refactoring
**Action:** Create single epic/story covering all related issues

## Follow-Up Questions

After reviewing analysis results, ask:

1. **Verification:** Have I verified this finding is accurate?
2. **Scope:** Is this finding relevant to current priorities?
3. **Priority:** Should this block other work?
4. **Cost:** Do I understand effort to fix?
5. **Benefit:** Is the benefit worth the effort?
6. **Timeline:** When should this be addressed?
7. **Owner:** Who should own the fix?
8. **Prevention:** How do we prevent this pattern recurring?

## Common Misinterpretations

| Misinterpretation | Reality | Correction |
|---|---|---|
| "Low confidence = probably wrong" | Low confidence = needs verification | Verify manually before dismissing |
| "Medium severity = not important" | Medium severity = should be fixed | Plan for next 1-2 sprints |
| "Info level = ignore" | Info = context for decisions | Use for strategic planning |
| "Many findings = crisis" | Could be normal variation | Assess trends over time |
| "One result = complete analysis" | Results are snapshot | Rerun analysis periodically |

## Trend Monitoring

Track results over time:

```
Weekly: Critical + High issues count
├─ Increasing? → Red flag, address immediately
├─ Stable? → Maintain current discipline
└─ Decreasing? → Good progress, continue

Monthly: Code quality trend
├─ Category breakdown (security, performance, structure)
├─ Average issue resolution time
└─ Tech debt growth rate
```
