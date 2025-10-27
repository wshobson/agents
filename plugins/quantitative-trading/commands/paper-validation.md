---
name: paper-validation
description: Complete validation workflow for quantitative trading strategy papers - validates statistical soundness, feasibility, complexity, and economic viability.
---

You are orchestrating a comprehensive paper validation workflow to answer three core questions:

1. **Is the strategy statistically sound?**
2. **Is it feasible to implement?**
3. **What's the complexity level?** (LOW/MEDIUM/HIGH)

# Paper Validation Workflow

Run the following agents in sequence to validate a quantitative trading strategy paper.

## Input

The user will provide a path to a paper (markdown or PDF). Extract the path and use it for validation.

## Workflow Steps

### Step 1: Parse Paper

**Agent:** `paper-analyzer`

**Task:**
```
Parse the paper at [PATH] and extract:
- Strategy methodology
- Data requirements
- Statistical claims (Sharpe ratio, returns, sample period)
- Parameters tested
- Universe specification
- Rebalancing frequency

Generate structured summary for downstream validation.
```

**Output:** Structured paper summary

---

### Step 2: Assess Feasibility

**Agent:** `implementation-feasibility-analyst`

**Task:**
```
Based on the paper summary from step 1, assess implementation feasibility:

1. Data availability (can we get the required data?)
2. Infrastructure requirements (laptop/server/cluster?)
3. Development timeline (weeks to implement)
4. Expertise requirements (junior/senior/specialist)
5. Any critical blockers?

Provide GO/NO-GO decision on feasibility.
```

**Decision Point:**
- If **NOT FEASIBLE** → Skip remaining steps, generate rejection report
- If **FEASIBLE** → Continue to Step 3

---

### Step 3: Assess Complexity

**Agent:** `complexity-assessor`

**Task:**
```
Score implementation complexity across three dimensions:

1. Implementation Time: <2 weeks (LOW) / 2-8 weeks (MEDIUM) / >8 weeks (HIGH)
2. Infrastructure: Laptop (LOW) / Server (MEDIUM) / Cluster (HIGH)
3. Expertise: Junior (LOW) / Senior (MEDIUM) / Specialist (HIGH)

Provide overall complexity score: LOW / MEDIUM / HIGH
```

**Output:** Complexity assessment with justification

---

### Step 4: Validate Statistics

**Agent:** `statistical-validator`

**Task:**
```
Validate statistical soundness:

1. Sharpe ratio significance (is sample size adequate?)
2. Robustness across time periods
3. Red flag detection (data mining, overfitting indicators)
4. Economic plausibility checks

Apply informed skepticism but trust reasonable peer review.
Provide performance haircut recommendation if needed.
```

**Output:** Statistical validation report with SOUND / CONCERNS / RED FLAGS assessment

---

### Step 5: Assess Economic Viability

**Agent:** `economic-viability-analyst`

**Task:**
```
Assess economic viability:

1. Transaction cost modeling (realistic costs)
2. Net Sharpe calculation (after costs)
3. Capacity estimation (liquidity constraints)
4. Economic mechanism validation (why does this work?)
5. Risk-reward assessment

Provide VIABLE / MARGINAL / NOT VIABLE decision.
```

**Output:** Economic viability report with net performance estimates

---

### Step 6: Synthesize & Recommend

**Agent:** `research-orchestrator`

**Task:**
```
Synthesize all validation results and generate comprehensive report:

**Core Questions:**
1. Is it statistically sound? ✅ / ⚠️ / ❌
2. Is it feasible to implement? ✅ / ⚠️ / ❌
3. What's the complexity? LOW / MEDIUM / HIGH

**Final Recommendation:**
- ✅ DEPLOY
- ⚠️ DEPLOY WITH CAUTION
- 🔍 INVESTIGATE FURTHER
- ❌ REJECT

Include:
- Executive summary
- Detailed validation results from all agents
- Risk assessment
- Implementation roadmap (if approved)
- Suggested allocation and monitoring plan

Generate publication-quality validation report.
```

**Output:** Complete paper validation report

---

## Execution Instructions

1. **Parse the paper path** from user input
2. **Run agents sequentially** in the order specified above
3. **Stop early if feasibility fails** (no point validating infeasible strategies)
4. **Collect all agent outputs** for final synthesis
5. **Generate comprehensive report** answering all 10 validation questions:
   - Q1-Q3: Core questions (statistical soundness, feasibility, complexity)
   - Q4-Q10: Extended questions (economic viability, mechanism, risks, robustness, replication, red flags, recommendation)

## Example Usage

```
User: Validate this paper: /path/to/volume-shocks-paper.md