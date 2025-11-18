# Feature Prioritization Matrix

## RICE Scoring Template

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| Feature A | 1000 | 3 | 80% | 4 | 600 | 🔥 High |
| Feature B | 500 | 2 | 90% | 2 | 450 | 🔥 High |
| Feature C | 2000 | 1 | 60% | 3 | 400 | ⚡ Med |
| Feature D | 300 | 3 | 50% | 6 | 75 | ❄️ Low |

**RICE Formula**: (Reach × Impact × Confidence) / Effort

**Scoring Guide**:
- **Reach**: Users impacted per quarter
- **Impact**: 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal
- **Confidence**: 100%=High, 80%=Medium, 50%=Low
- **Effort**: Person-months (0.5, 1, 2, 4, 8, etc.)

---

## Value vs Complexity Matrix

```
High Value
│
│  QUICK WINS      STRATEGIC
│  ┌─────────┐    ┌─────────┐
│  │ Feature │    │ Feature │
│  │    A    │    │    B    │
│  └─────────┘    └─────────┘
│
│  FILL-INS       TIME SINKS
│  ┌─────────┐    ┌─────────┐
│  │ Feature │    │ Feature │
│  │    C    │    │    D    │
│  └─────────┘    └─────────┘
│
└──────────────────────────── High Complexity
```

**Decision Framework**:
- **Quick Wins** (High Value, Low Complexity): Do first
- **Strategic** (High Value, High Complexity): Plan carefully, phased approach
- **Fill-Ins** (Low Value, Low Complexity): Do if excess capacity
- **Time Sinks** (Low Value, High Complexity): Avoid or defer

---

## MoSCoW Prioritization

### Must Have (Critical for launch)
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

### Should Have (Important but not critical)
- [ ] Feature 4
- [ ] Feature 5

### Could Have (Nice to have)
- [ ] Feature 6
- [ ] Feature 7

### Won't Have (Explicitly out of scope)
- [ ] Feature 8
- [ ] Feature 9

---

## Weighted Scoring Model

| Criteria | Weight | Feature A | Feature B | Feature C |
|----------|--------|-----------|-----------|-----------|
| **User Value** | 30% | 9 (2.7) | 7 (2.1) | 5 (1.5) |
| **Business Impact** | 25% | 8 (2.0) | 9 (2.25) | 6 (1.5) |
| **Strategic Fit** | 20% | 7 (1.4) | 8 (1.6) | 6 (1.2) |
| **Feasibility** | 15% | 9 (1.35) | 5 (0.75) | 8 (1.2) |
| **Time to Market** | 10% | 6 (0.6) | 9 (0.9) | 7 (0.7) |
| **Total Score** | 100% | **8.05** | **7.6** | **6.1** |

**Priority**: Feature A > Feature B > Feature C

---

## Kano Model Classification

### Basic Needs (Must-Haves)
*Expected features, dissatisfaction if absent*
- Feature 1
- Feature 2

### Performance Needs (More is Better)
*Linear satisfaction, competitive differentiators*
- Feature 3
- Feature 4

### Delighters (Unexpected Features)
*Non-linear satisfaction, create delight*
- Feature 5
- Feature 6

**Strategy**:
1. Ensure all basic needs covered
2. Compete on performance needs
3. Differentiate with 1-2 delighters

---

## Opportunity Scoring

**Question to Users**: "How important is [feature] to you?" and "How satisfied are you with current solution?"

| Feature | Importance | Satisfaction | Opportunity Gap | Priority |
|---------|------------|--------------|-----------------|----------|
| Feature A | 9.2 | 3.1 | 6.1 | 🔥 High |
| Feature B | 8.5 | 4.2 | 4.3 | ⚡ Med |
| Feature C | 7.8 | 6.5 | 1.3 | ❄️ Low |
| Feature D | 6.2 | 5.8 | 0.4 | ❄️ Low |

**Opportunity Gap** = Importance - Satisfaction

**Priority**: Largest gap = highest priority

---

## Decision Log

| Date | Feature | Decision | Rationale | Outcome |
|------|---------|----------|-----------|---------|
| 2025-01-15 | Feature A | ✅ Build | High RICE score, strategic fit | Shipped Q1 |
| 2025-01-15 | Feature B | ⏸️ Defer | Low impact, high effort | Revisit Q3 |
| 2025-01-15 | Feature C | ❌ Kill | Not aligned with strategy | Deprioritized |

---

## Stakeholder Input

| Stakeholder | Top Priority | Rationale |
|-------------|--------------|-----------|
| Engineering | Feature B | Technical debt reduction |
| Marketing | Feature A | Competitive differentiation |
| Sales | Feature C | Customer requests (enterprise) |
| Support | Feature D | Reduce support tickets |

**Consensus**: [Balanced view considering all perspectives]
