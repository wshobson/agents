---
name: assess-product-maturity
description: Comprehensive product team maturity assessment using FAANG-level standards across six dimensions. Generates detailed report with maturity score, gap analysis, and prioritized recommendations.
---

# Assess Product Maturity Command

## Purpose

Conduct a comprehensive assessment of your product team's maturity level across six core dimensions: Technical Excellence, Product Management, Engineering Practices, Team & Culture, Delivery & Operations, and Data & Analytics. Compare your current state against world-class standards from AWS, Google, Amazon, Netflix, Meta, and other industry leaders.

## What This Command Does

This command will guide you through a structured assessment process that:

1. **Conducts Discovery**: Asks targeted questions about your team's practices
2. **Evaluates Dimensions**: Scores each of the six maturity dimensions (1-5 scale)
3. **Calculates Maturity Level**: Determines overall maturity (Level 1-5)
4. **Identifies Gaps**: Compares current state vs. world-class standards
5. **Generates Report**: Creates detailed assessment with findings and recommendations
6. **Provides Roadmap**: Prioritized improvement plan with quick wins

## When to Use

- Starting a transformation initiative
- Quarterly or annual team health checks
- Benchmarking against industry standards
- Justifying investment in improvements
- Understanding strengths and weaknesses
- Planning capability roadmaps
- Comparing multiple teams

## Before You Begin

### Time Required
- **Quick Assessment**: 30-45 minutes (high-level)
- **Standard Assessment**: 2-3 hours (recommended)
- **Comprehensive Assessment**: 1-2 days (includes interviews and artifact review)

### Participants Needed
- Product Manager or Product Leader
- Engineering Manager or Tech Lead
- 2-3 Individual Contributors (engineers)
- Optional: Designer, QA, DevOps, Data roles

### Information to Gather
- Access to codebase and CI/CD pipelines
- Recent deployment history
- Incident reports (last 3 months)
- Product metrics dashboards
- Team structure and org chart
- Current roadmap and OKRs

## Assessment Process

I will guide you through the following phases:

### Phase 1: Context Setting (10 minutes)

**Questions:**
- What is your company/product domain?
- How large is your engineering organization?
- What is your team structure?
- What are your biggest current challenges?
- What prompted this assessment?

### Phase 2: Six-Dimension Deep Dive (90-120 minutes)

For each dimension, I will ask 10-15 discovery questions covering:

**Dimension 1: Technical Excellence**
- Architecture and scalability
- Code quality and standards
- Testing practices
- CI/CD maturity
- Infrastructure and observability
- Security practices

**Dimension 2: Product Management**
- Product vision and strategy
- Discovery and validation processes
- Roadmapping and prioritization
- Metrics and analytics
- Customer feedback loops
- Market awareness

**Dimension 3: Engineering Practices**
- Development workflow
- Code review process
- Release management
- Monitoring and alerting
- Documentation
- Technology stack

**Dimension 4: Team & Culture**
- Team structure and autonomy
- Collaboration patterns
- Learning and development
- Ownership and accountability
- Innovation and psychological safety
- Remote/distributed practices

**Dimension 5: Delivery & Operations**
- Deployment frequency
- Reliability and uptime
- Scalability and performance
- Incident management
- SRE practices
- Business continuity

**Dimension 6: Data & Analytics**
- Data infrastructure
- Product analytics
- Business intelligence
- Experimentation capability
- Machine learning operations
- Data governance

### Phase 3: Artifact Review (30-60 minutes)

I will ask you to share or describe:
- Sample CI/CD pipeline configuration
- Recent deployment history
- Example pull request
- Monitoring dashboard
- Incident post-mortem
- Product roadmap document

### Phase 4: Scoring and Analysis (30 minutes)

I will:
- Score each dimension (1-5)
- Calculate overall maturity level
- Identify strengths and gaps
- Compare against industry benchmarks
- Highlight quick wins

### Phase 5: Report Generation (automated)

I will generate a comprehensive report including:

```markdown
# Product Maturity Assessment Report
## [Your Team/Company Name] - [Date]

---

## Executive Summary

**Overall Maturity Level**: [Level X.X / 5.0]
**Primary Classification**: [Initial / Managed / Defined / Measured / Optimizing]

**Key Strengths**:
- [Top 3 strengths]

**Critical Gaps**:
- [Top 3 gaps]

**Recommended Focus Areas**:
1. [Highest priority area]
2. [Second priority area]
3. [Third priority area]

---

## Dimensional Scores

| Dimension | Score | Level | Gap to Level 4 |
|-----------|-------|-------|----------------|
| Technical Excellence | X.X | Level N | Y.Y points |
| Product Management | X.X | Level N | Y.Y points |
| Engineering Practices | X.X | Level N | Y.Y points |
| Team & Culture | X.X | Level N | Y.Y points |
| Delivery & Operations | X.X | Level N | Y.Y points |
| Data & Analytics | X.X | Level N | Y.Y points |

**Weighted Average**: [X.X / 5.0]

---

## Dimension 1: Technical Excellence

### Current State (Level X.X)
[Description of current practices]

### Evidence Observed:
✅ **Strengths:**
- [Specific strength with example]
- [Specific strength with example]

⚠️ **Gaps:**
- [Specific gap with impact]
- [Specific gap with impact]

### Industry Benchmark (Level 4-5):
[What FAANG companies do in this area]

### Gap Analysis:
[Detailed comparison of current vs. target state]

### Recommendations:
1. **Quick Win** (0-1 month): [Specific action]
2. **Medium-term** (1-3 months): [Specific action]
3. **Long-term** (3-6 months): [Specific action]

---

[Repeat for each dimension...]

---

## Overall Gap Analysis

### Distance from Target State

**Current**: Level X.X (Managed/Defined)
**Target**: Level 4.0 (Quantitatively Managed)
**Gap**: Y.Y points

**Estimated Timeline to Level 4**: [6-18 months]
**Estimated Investment**: [Team allocation, tooling budget]

### Comparison to Industry Benchmarks

**DORA Metrics:**
| Metric | Your Team | Elite (FAANG) | Gap |
|--------|-----------|---------------|-----|
| Deploy Frequency | [X/day] | Multiple/day | [Gap] |
| Lead Time | [X hours] | < 1 hour | [Gap] |
| Change Failure Rate | [X%] | 0-15% | [Gap] |
| MTTR | [X hours] | < 1 hour | [Gap] |

---

## Prioritized Improvement Roadmap

### Phase 1: Foundation (0-3 months)
**Goal**: Quick wins and foundational practices

**High-Impact Initiatives:**
1. [Initiative]: [Description, Expected Impact, Effort]
2. [Initiative]: [Description, Expected Impact, Effort]
3. [Initiative]: [Description, Expected Impact, Effort]

**Success Metrics:**
- [Metric]: [Current] → [Target]
- [Metric]: [Current] → [Target]

**Investment Required:**
- Team capacity: [X% for 3 months]
- Budget: [$X for tools/training]

---

### Phase 2: Standardization (3-6 months)
**Goal**: Consistent practices organization-wide

**Key Initiatives:**
1. [Initiative]: [Description, Expected Impact, Effort]
2. [Initiative]: [Description, Expected Impact, Effort]

**Success Metrics:**
- [Metric]: [Current] → [Target]

---

### Phase 3: Optimization (6-12 months)
**Goal**: Data-driven, advanced practices

**Key Initiatives:**
1. [Initiative]: [Description, Expected Impact, Effort]
2. [Initiative]: [Description, Expected Impact, Effort]

**Success Metrics:**
- [Metric]: [Current] → [Target]

---

## Risks and Mitigation

### Implementation Risks:
1. **Risk**: [Description]
   - **Impact**: [High/Medium/Low]
   - **Mitigation**: [Strategy]

2. **Risk**: [Description]
   - **Impact**: [High/Medium/Low]
   - **Mitigation**: [Strategy]

---

## Next Steps

### Immediate Actions (This Week):
1. [ ] Share report with leadership
2. [ ] Socialize findings with team
3. [ ] Form improvement working group
4. [ ] Prioritize Phase 1 initiatives
5. [ ] Secure budget and resources

### Next Month:
1. [ ] Launch Phase 1 initiatives
2. [ ] Set up success metrics dashboard
3. [ ] Schedule monthly progress reviews
4. [ ] Begin training programs

---

## Appendix

### Assessment Methodology
[Description of process, questions asked, artifacts reviewed]

### Reference Materials
- Product Maturity Model framework
- FAANG best practices
- Industry benchmarks (DORA, etc.)

### Glossary
[Definitions of key terms]
```

## After the Assessment

### Report Delivery

You will receive:
1. **Full Report**: Comprehensive markdown document (can be exported to PDF)
2. **Executive Slide**: One-page summary for leadership
3. **Roadmap Board**: Prioritized backlog of improvements
4. **Metrics Dashboard Template**: Track progress over time

### Follow-up Actions

I can help you with:
- Presenting findings to leadership
- Creating detailed implementation plans
- Setting up metrics dashboards
- Defining success criteria
- Running transformation workshops
- Coaching teams through changes

### Re-assessment Cadence

**Recommended frequency:**
- **Quarterly**: Quick check (30 min) on progress
- **Semi-annual**: Standard assessment (2-3 hours)
- **Annual**: Comprehensive assessment (1-2 days)

## Example Assessment Output

Here's what a sample assessment might look like:

```markdown
# Assessment Summary: Acme Corp Payments Team

**Overall Maturity**: 2.8 / 5.0 (Defined)
**Date**: January 2025
**Assessor**: Product Maturity Advisor

## Key Findings:

### Strengths ✅
- Strong code review culture (100% coverage)
- Modern CI/CD pipeline (GitHub Actions)
- Quarterly OKRs well-defined

### Critical Gaps ⚠️
- No A/B testing capability (decisions by opinion)
- Manual deployment to production (risk)
- Limited observability (can't debug issues quickly)

### Top 3 Priorities:
1. **Implement feature flags** (2 weeks, high impact)
   - Enable progressive rollout
   - Reduce deployment risk
   - Decouple deploy from release

2. **Set up observability stack** (1 month, critical)
   - Implement structured logging
   - Add distributed tracing
   - Create operational dashboards

3. **Build A/B testing framework** (2 months, transformative)
   - Data-driven product decisions
   - Validate features before full launch
   - Reduce wasted engineering

**Expected Impact**: Move from Level 2.8 → 3.5 in 6 months
```

## Tips for Best Results

**Be Honest:**
- Assessment is confidential
- Accurate picture enables better recommendations
- No judgment, only learning

**Bring Evidence:**
- Examples better than descriptions
- Metrics better than feelings
- Show, don't tell

**Include Diverse Perspectives:**
- Not just leadership view
- Individual contributors' reality
- Cross-functional input

**Focus on Systems, Not People:**
- Process failures, not individual failures
- What are the patterns?
- What enables or blocks success?

## Getting Started

Ready to assess your product team maturity?

Let's begin with the context-setting questions:

1. Tell me about your product and company
2. How large is your engineering organization?
3. What is your current team structure?
4. What are your biggest challenges right now?
5. What outcome are you hoping for from this assessment?

---

**Note**: This assessment uses the product-maturity-advisor agent and leverages the product-maturity-model, tech-excellence-practices, product-development-lifecycle, and team-culture-patterns skills for comprehensive evaluation.
