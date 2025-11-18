---
name: product-development-lifecycle
description: Complete product development lifecycle from ideation to launch used by AWS, Google, Amazon, Netflix, and Meta. Use when planning product development, discovery processes, roadmapping, experimentation, launch strategies, or establishing product management practices.
---

# Product Development Lifecycle

## When to Use This Skill

- Establishing product development processes
- Improving product discovery and validation
- Setting up experimentation frameworks
- Planning product launches and rollouts
- Defining roadmapping and prioritization
- Implementing OKRs and metrics
- Adopting customer-centric development
- Learning from FAANG product practices

## Overview

End-to-end product development lifecycle based on practices from the world's leading product companies. Covers discovery, planning, development, launch, and optimization phases with proven frameworks and techniques.

## Product Development Philosophy

### Amazon: Working Backwards

**Core Principle:** Start with the customer and work backwards to the technology.

**Process:**
1. Write the press release (PR)
2. Write the FAQ
3. Define customer experience
4. Build

**Press Release Template:**
```markdown
# [Product Name] - Press Release

**[City, Date]** – [Company] today announced [Product Name], a [one-sentence description].

## Problem
[What customer problem does this solve? Why is this important?]

## Solution
[How does this product solve the problem? What makes it unique?]

## Quote from Company Leader
"[Why are we excited about this? What's the vision?]" said [Name, Title].

## How It Works
[Simple explanation of how customers will use it]

## Quote from Customer
"[How will this improve their life/work?]" said [Fictional Customer Name].

## Get Started
[How can customers access this today?]
```

**FAQ Template:**
```markdown
# [Product Name] - FAQ

## External FAQ (Customer-Facing)

**Q: Who is this for?**
A: [Target customer segment and use cases]

**Q: How much does it cost?**
A: [Pricing model and justification]

**Q: How is this different from [Competitor]?**
A: [Differentiation and unique value]

**Q: What if I need help?**
A: [Support model and resources]

## Internal FAQ (Team-Facing)

**Q: Why now?**
A: [Market timing and urgency]

**Q: What are the dependencies?**
A: [Technical, organizational, external]

**Q: How will we measure success?**
A: [Key metrics and targets]

**Q: What are the risks?**
A: [Technical, business, competitive risks]

**Q: What resources are needed?**
A: [Team size, timeline, budget]
```

**Benefits:**
- Forces clarity on customer value
- Prevents building for technology's sake
- Creates alignment across teams
- Provides clear vision and goals

### Google: OKRs (Objectives and Key Results)

**Framework:**
- **Objectives**: Ambitious, qualitative goals
- **Key Results**: Measurable, quantitative outcomes

**Characteristics:**
- Quarterly cadence
- Aspirational (60-70% achievement is success)
- Transparent across organization
- Decoupled from performance reviews

**OKR Template:**
```markdown
# Q1 2025 OKRs - Payments Team

## Objective 1: Become the fastest checkout in the industry
**Why it matters:** Speed directly impacts conversion. Every 100ms of latency costs 1% conversion.

### Key Results:
1. Reduce checkout time from 45s to 20s (p50)
2. Achieve 99.95% availability for payment API
3. Increase mobile conversion rate from 3.2% to 4.5%

**Current Progress (Week 6/13):**
- KR1: 32s achieved (50% progress) 🟨
- KR2: 99.92% achieved (70% progress) 🟨
- KR3: 3.8% achieved (40% progress) 🟨

## Objective 2: Expand payment methods to reach global customers
**Why it matters:** 40% of cart abandonment is due to limited payment options.

### Key Results:
1. Launch Apple Pay and Google Pay (currently card-only)
2. Support 5 new currencies (currently USD, EUR)
3. Achieve 10% of revenue from new payment methods

**Current Progress (Week 6/13):**
- KR1: Apple Pay launched, Google Pay in QA (75% progress) 🟩
- KR2: 2 currencies launched (GBP, CAD), 3 in dev (40% progress) 🟨
- KR3: 3% achieved (30% progress) 🟨
```

**Best Practices:**
- Limit to 3-5 objectives per team
- Each objective has 2-4 key results
- Stretch goals (not sandbag commitments)
- Weekly check-ins on progress
- Quarterly retrospectives

### Meta: Move Fast and Data-Driven

**Principles:**
- Bias for action over analysis paralysis
- Ship early, iterate based on data
- Rigorous A/B testing for all decisions
- Fail fast, learn fast

**Development Cycle:**
1. **Hypothesis**: What do we believe?
2. **Build**: MVP to test hypothesis
3. **Ship**: Release to small % of users
4. **Measure**: Collect data on key metrics
5. **Decide**: Scale, iterate, or kill
6. **Repeat**: Next iteration

**Experimentation Culture:**
- 1000s of experiments running simultaneously
- Statistical rigor (minimum sample size, significance)
- Guardrail metrics (prevent harming core metrics)
- Experiment repository (learn from past tests)

### Netflix: Context, Not Control

**Principles:**
- High-level context (strategy, goals, constraints)
- High autonomy (teams decide how to achieve goals)
- Freedom and responsibility
- Highly aligned, loosely coupled

**Product Development:**
- Teams own product areas end-to-end
- Empowered to make decisions
- Regular context sharing (strategy, data, user research)
- Review outputs, not activities

## Discovery Phase

### Opportunity Identification

**Sources:**
1. **Customer feedback**: Support tickets, surveys, interviews
2. **Data analysis**: Usage patterns, drop-off points, bottlenecks
3. **Market research**: Competitive analysis, industry trends
4. **Team insights**: Engineer suggestions, designer observations
5. **Strategic goals**: Company OKRs, business objectives

**Opportunity Assessment:**
```markdown
# Opportunity Template

## Problem Statement
[What problem are we solving? For whom?]

## Evidence
- Customer feedback: [Quotes, ticket volume, NPS comments]
- Data: [Usage stats, conversion rates, error rates]
- Market: [Competitive landscape, industry trends]

## Opportunity Size
- Affected users: [Number, percentage of base]
- Frequency: [How often do they encounter this?]
- Severity: [How painful is this problem?]
- Business impact: [Revenue, retention, acquisition]

## Strategic Fit
- Aligns with OKRs: [Which objectives?]
- Competitive advantage: [Differentiation]
- Technical feasibility: [Low/Medium/High complexity]

## Success Criteria
[How will we know if we've solved this problem?]
```

### User Research

**Google HEART Framework:**
- **H**appiness: Satisfaction, NPS, perceived ease of use
- **E**ngagement: Frequency, intensity, depth of use
- **A**doption: New users, feature adoption
- **R**etention: Return rate, churn
- **T**ask success: Completion rate, time, errors

**Research Methods:**
1. **User interviews**: Qualitative insights (5-8 users)
2. **Surveys**: Quantitative validation (100+ users)
3. **Usability testing**: Observe users completing tasks
4. **Field studies**: Watch users in natural environment
5. **Data analysis**: Behavioral patterns in product

**Interview Script Template:**
```markdown
# User Interview Script: [Feature/Problem]

## Introduction (5 min)
- Thank you for your time
- Purpose: Understand how you [use product/face problem]
- No wrong answers, honest feedback valuable
- Recording with permission for notes only

## Background (10 min)
- Tell me about your role and responsibilities
- How does [problem area] fit into your work?
- What tools do you currently use for this?

## Current Experience (20 min)
- Walk me through the last time you [task]
- What went well? What was frustrating?
- Show me how you do this today (if possible)
- What workarounds have you developed?

## Future State (15 min)
- If you had a magic wand, how would this work?
- What's most important to you in a solution?
- What have you tried in the past?

## Wrap-up (5 min)
- Anything else you'd like to share?
- Can we follow up as we develop solutions?
```

### Prototyping and Validation

**Fidelity Levels:**
1. **Sketches**: Paper, whiteboard (validate concepts)
2. **Wireframes**: Low-fidelity (validate structure)
3. **Mockups**: High-fidelity (validate design)
4. **Prototypes**: Interactive (validate flow)
5. **Alpha/Beta**: Working code (validate functionality)

**Validation Techniques:**
- **Fake door test**: Button that logs interest but doesn't work
- **Wizard of Oz**: Manual backend simulating automated feature
- **Smoke test**: Landing page with signup to gauge interest
- **Prototype test**: Interactive mockup with real users
- **Beta test**: Limited release to early adopters

**Validation Checklist:**
```markdown
## Pre-Build Validation

- [ ] Problem validated with 5+ customers
- [ ] Solution mockups tested with 5+ users
- [ ] Competitive alternatives evaluated
- [ ] Success metrics defined
- [ ] Technical feasibility confirmed
- [ ] Business case approved
- [ ] Risks identified and mitigated
```

## Planning Phase

### Roadmapping

**Amazon: 6-Pager Narrative**

Instead of slides, write a 6-page narrative document:

```markdown
# [Feature Name] - 6-Pager

## 1. Introduction (0.5 pages)
[What are we proposing? Why now?]

## 2. Goals (0.5 pages)
[What business and customer goals does this achieve?]

## 3. Tenets (0.5 pages)
[What principles guide our decisions?]
- Customer obsession: [How does this help customers?]
- Ownership: [Who owns this?]
- Operational excellence: [How will we operate this?]

## 4. State of the Business (1 page)
[Current metrics, problems, opportunities]

## 5. Approach (2 pages)
[Detailed solution, architecture, user experience]

## 6. Financials (1 page)
[Cost, revenue impact, ROI analysis]

## 7. Appendix (not counted in 6 pages)
[Supporting data, mockups, research]
```

**Meeting Structure:**
- First 20 minutes: Silent reading of document
- Next 40+ minutes: Discussion and decisions
- Forces clear thinking and writing
- Everyone starts with same context

**Prioritization Framework: RICE**

Used by Intercom and many product teams:

- **R**each: How many users affected?
- **I**mpact: How much does it move the needle? (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
- **C**onfidence: How certain are we? (100%=high, 80%=medium, 50%=low)
- **E**ffort: How many person-months?

**Score = (Reach × Impact × Confidence) / Effort**

Example:
```markdown
# Q1 Roadmap Prioritization

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| Mobile checkout | 10K users/mo | 3 (massive) | 80% | 2 months | 12.0 | P0 |
| Payment retry | 2K users/mo | 2 (high) | 100% | 0.5 months | 8.0 | P0 |
| Multi-currency | 5K users/mo | 2 (high) | 50% | 3 months | 1.7 | P1 |
| Dark mode | 50K users/mo | 0.5 (low) | 80% | 1 month | 20.0 | P2 |
```

### Sprint Planning

**Two-Week Sprint Cycle:**

**Week 1:**
- Monday: Sprint planning (2 hours)
- Daily: Standups (15 min)
- Wednesday: Mid-sprint check-in (30 min)
- Friday: Demo to stakeholders (30 min)

**Week 2:**
- Monday: Continue work
- Daily: Standups (15 min)
- Thursday: Testing and polish
- Friday: Retrospective (1 hour), Sprint planning for next (2 hours)

**Sprint Planning Template:**
```markdown
# Sprint 47 - Jan 15-26, 2025

## Sprint Goal
Launch mobile checkout MVP to 10% of traffic

## Capacity
- Team size: 6 engineers
- Availability: 10 days × 6 people = 60 person-days
- Velocity: 40 story points (based on last 3 sprints)
- Buffer: 20% for interruptions = 32 points committed

## Committed Stories

### Must Have (Sprint Goal)
- [8 pts] Mobile checkout UI components
- [5 pts] Payment API mobile integration
- [3 pts] Analytics instrumentation
- [5 pts] A/B test setup for 10% rollout
- [3 pts] Error handling and retry logic

### Should Have (If capacity)
- [8 pts] Apple Pay integration

### Nice to Have
- [5 pts] Google Pay integration

## Definition of Done
- [ ] Code reviewed and approved
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Deployed to staging
- [ ] QA tested
- [ ] Docs updated
- [ ] Demo-able
```

## Development Phase

### Agile Development

**Daily Standup (15 minutes):**
- What did you accomplish yesterday?
- What will you do today?
- What blockers do you have?

**Best Practices:**
- Stand up (keeps it short)
- Timebox strictly to 15 minutes
- Focus on blockers
- Detailed discussions after standup
- Update sprint board before standup

### Feature Flags and Progressive Rollout

**Feature Flag Strategy:**
```javascript
// Feature flag system
const featureFlags = {
  'mobile-checkout': {
    enabled: true,
    rollout: {
      type: 'percentage',
      percentage: 10,  // 10% of users
    },
    targeting: {
      segments: ['mobile', 'new-users'],
      regions: ['US', 'CA'],
    },
  },
  'apple-pay': {
    enabled: false,  // Not ready yet
  },
};

// Usage in code
if (featureFlags.isEnabled('mobile-checkout', user)) {
  return <MobileCheckout />;
} else {
  return <DesktopCheckout />;
}
```

**Rollout Stages:**
1. **Internal (1%)**: Team only, dogfooding
2. **Alpha (5%)**: Early adopters, opt-in
3. **Beta (25%)**: Broader audience, monitoring closely
4. **GA (100%)**: General availability, remove flag

**Rollback Plan:**
```markdown
## Rollback Procedure

### Trigger Conditions
- Error rate > 1%
- Latency p99 > 2x baseline
- Conversion rate < 90% of control
- Critical bug discovered

### Rollback Steps
1. Set feature flag to 0% (immediate)
2. Verify metrics return to normal
3. Notify stakeholders
4. Debug and fix issue
5. Plan re-launch
```

### Code Reviews

**Google-Style Code Review:**

**Reviewer Responsibilities:**
- Understand the change completely
- Provide constructive feedback
- Focus on design, correctness, complexity
- Respond within 24 hours (for small changes)

**Author Responsibilities:**
- Keep changes small (< 400 lines)
- Write clear description and test plan
- Address all comments or explain why not
- Don't merge until approvals

**Review Template:**
```markdown
## Summary
[What does this PR do?]

## Motivation
[Why is this change needed?]

## Changes
- Added [feature/fix]
- Modified [component]
- Refactored [logic]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manually tested in staging
- [ ] Performance tested (if relevant)

## Screenshots
[For UI changes]

## Deployment Plan
[How will this be rolled out?]

## Rollback Plan
[How to revert if issues?]

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No new warnings or errors
- [ ] Backward compatible
```

## Launch Phase

### Pre-Launch Checklist

**Technical Readiness:**
```markdown
## Technical Checklist

### Code
- [ ] Code reviewed and approved
- [ ] All tests passing (unit, integration, e2e)
- [ ] Security review completed
- [ ] Performance benchmarks met
- [ ] Accessibility tested
- [ ] Browser/device compatibility verified

### Infrastructure
- [ ] Capacity planning completed
- [ ] Load testing passed
- [ ] Monitoring and alerts configured
- [ ] Logging instrumented
- [ ] Error tracking setup
- [ ] Feature flags configured

### Operations
- [ ] Runbook created
- [ ] Rollback plan documented
- [ ] On-call rotation notified
- [ ] Incident response plan ready
- [ ] Support team trained

### Data
- [ ] Analytics instrumented
- [ ] A/B test configured
- [ ] Success metrics dashboard created
- [ ] Data privacy reviewed
```

**Go-to-Market Readiness:**
```markdown
## GTM Checklist

### Messaging
- [ ] Product positioning defined
- [ ] Value proposition clear
- [ ] Key messages documented
- [ ] FAQ prepared

### Content
- [ ] Landing page ready
- [ ] Blog post drafted
- [ ] Documentation published
- [ ] Video demo created

### Enablement
- [ ] Sales team trained
- [ ] Support team trained
- [ ] Customer success briefed
- [ ] Internal announcement prepared

### Launch
- [ ] Launch date confirmed
- [ ] Launch sequence planned
- [ ] Stakeholders aligned
- [ ] Success criteria defined
```

### Launch Strategies

**Soft Launch:**
- Launch to small audience first
- Gather feedback and iterate
- Build confidence before full launch
- Example: Launch to 1% of users for 1 week

**Hard Launch:**
- Launch to everyone at once
- High risk, high visibility
- Requires extensive testing
- Example: Super Bowl ad with full availability

**Phased Rollout (Recommended):**
```markdown
## Phased Rollout Plan

### Week 1: Internal (1%)
- Audience: Company employees
- Goal: Dogfooding, catch obvious bugs
- Success criteria: No critical bugs

### Week 2: Alpha (5%)
- Audience: Early adopters, power users
- Goal: Validate core functionality
- Success criteria: Core metrics stable

### Week 3-4: Beta (25%)
- Audience: Broader user base
- Goal: Scale testing, gather feedback
- Success criteria: Metrics improving

### Week 5-6: General Availability (100%)
- Audience: All users
- Goal: Full launch
- Success criteria: Hit OKR targets
```

## Optimization Phase

### Metrics and Analysis

**Product Metrics Hierarchy:**
```
North Star Metric (one metric that matters most)
    ↓
Primary Metrics (3-5 key product metrics)
    ↓
Secondary Metrics (supporting metrics)
    ↓
Guardrail Metrics (ensure no harm)
```

**Example for E-commerce:**
```markdown
## Metrics Framework

### North Star Metric
- **Revenue per user**: $45/month target

### Primary Metrics
- Conversion rate: 3.5% target
- Average order value: $75 target
- Purchase frequency: 2x/month target

### Secondary Metrics
- Cart add rate
- Checkout initiation rate
- Payment success rate
- Delivery satisfaction

### Guardrail Metrics
- Load time < 2s
- Error rate < 0.1%
- Support ticket volume
- Refund rate
```

### A/B Testing

**Experiment Design:**
```markdown
# Experiment: New Checkout Flow

## Hypothesis
Reducing checkout steps from 5 to 3 will increase conversion rate by 15%.

## Variants
- **Control**: Current 5-step checkout
- **Treatment**: New 3-step checkout

## Success Metrics
- **Primary**: Conversion rate (checkout started → purchase completed)
- **Secondary**: Time to complete checkout, error rate
- **Guardrail**: Average order value (should not decrease)

## Design
- **Split**: 50/50 random assignment
- **Duration**: 2 weeks
- **Sample size**: 10,000 users per variant (80% power, 5% significance)
- **Segments**: All users, mobile and desktop

## Launch Criteria
- Treatment conversion > Control conversion
- Statistical significance (p < 0.05)
- No negative impact on guardrail metrics
- No increase in support tickets

## Results (After 2 weeks)
- Control conversion: 3.2%
- Treatment conversion: 3.8% (+18.75%)
- Statistical significance: p = 0.003 ✅
- Average order value: No change ✅
- Support tickets: -10% (fewer errors) ✅

**Decision: Ship to 100%**
```

### Continuous Improvement

**Iteration Cycle:**
1. **Measure**: Track metrics, user feedback
2. **Analyze**: Identify problems and opportunities
3. **Hypothesize**: What could improve metrics?
4. **Test**: Run experiment
5. **Learn**: Analyze results
6. **Decide**: Ship, iterate, or kill
7. **Repeat**: Next iteration

**Retrospective Template:**
```markdown
# Feature Retrospective: Mobile Checkout

## What Went Well
- Launched on time
- No major incidents
- Positive user feedback
- Conversion improved 18%

## What Didn't Go Well
- Load testing missed edge case
- Documentation incomplete at launch
- Design iterations took longer than expected

## What We Learned
- Simplifying flow has big impact
- Need better load testing scenarios
- Earlier design involvement helps

## Action Items
- [ ] Improve load testing suite (Owner: @eng)
- [ ] Update launch checklist to include docs (Owner: @pm)
- [ ] Involve design earlier in planning (Owner: @team)

## Metrics
- Launched: 2025-01-15
- Time to 100%: 6 weeks
- Conversion: +18% ✅
- NPS: +5 points ✅
- Support tickets: -10% ✅
```

## Reference Materials

See `references/` directory for:
- Complete templates for each phase
- Example PRDs and 6-pagers
- User research scripts
- Experiment design examples
- Launch checklists

See `assets/` directory for:
- Process flow diagrams
- Timeline examples
- Prioritization matrices
- Dashboard mockups

## Success Indicators

This skill is being applied effectively when:
- Clear product development process
- Customer-validated ideas before building
- Data-driven decisions
- Regular shipping cadence
- Measurable impact on metrics
- Continuous learning and iteration
- Strong cross-functional collaboration
