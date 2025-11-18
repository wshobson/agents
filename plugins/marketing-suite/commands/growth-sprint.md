---
name: growth-sprint
description: Еженедельный growth sprint framework для планирования и запуска data-driven экспериментов роста с A/B testing, funnel analysis и experiment tracking.
---

# Growth Sprint Command

Orchestrates еженедельные growth sprints с hypothesis generation, experiment prioritization, execution tracking и results analysis.

## Цель

Создать repeatable framework для systematic growth experimentation:
- Генерация growth hypotheses на основе data
- Prioritization experiments (ICE/PIE scoring)
- Experiment design с statistical rigor
- Tracking & analysis dashboard
- Learning documentation & knowledge base

## Входные параметры

```
Growth focus area: [Acquisition / Activation / Retention / Revenue / Referral]
Current baseline metric: [Число]
Target improvement: [%]
Sprint duration: [1 week / 2 weeks]
Team capacity: [Hours available]
```

## Процесс Growth Sprint

### Monday: Sprint Planning (2-3 hours)

**1. Review Previous Week (30 min)**

```markdown
# Previous Week Review

## Experiments Completed
| Experiment | Hypothesis | Result | Decision |
|------------|-----------|---------|----------|
| Test #1    | [Hypothesis] | +X% (p=0.03) | ✅ Ship |
| Test #2    | [Hypothesis] | -Y% (p=0.15) | ❌ Kill |
| Test #3    | [Hypothesis] | Running | → Continue |

## Key Learnings
1. [Learning 1]: [Insight + future applications]
2. [Learning 2]: [Insight + future applications]

## Metrics Dashboard
- **Acquisition**: XXX new signups (↑5% vs last week)
- **Activation**: XX% reached aha moment (↓2% - investigate)
- **Retention**: XX% Day 7 retention (→ flat)
- **Revenue**: $XXX MRR (↑$XX)
- **Referral**: X% referral rate (↑1%)
```

**2. Data Analysis & Opportunity Identification (60 min)**

**Команда анализирует:**

**Funnel Analysis:**
```
Signups: 1000
  ↓ (-40%)
Activated (reached aha moment): 600
  ↓ (-50%)
Retained (Day 7): 300
  ↓ (-70%)
Paid conversion: 90 (9% of signups, 30% of retained)

🎯 Biggest drop-off: Signup → Activation (-40%)
```

**Cohort Analysis:**
```
Signups by week:
- Week 1: 500 users → 25% Day 30 retention
- Week 2: 600 users → 28% Day 30 retention ↑
- Week 3: 700 users → 30% Day 30 retention ↑ (improving!)
- Week 4: 800 users → TBD (too early)

✅ Positive trend: Recent improvements working
```

**Segment Analysis:**
```
By Source:
- Organic: 400 signups, 35% retention ⭐ Best
- Paid Social: 300 signups, 20% retention
- Paid Search: 200 signups, 25% retention
- Referral: 100 signups, 40% retention ⭐ Best

💡 Insight: Organic & Referral = highest quality
```

**User Behavior:**
```
High-retention users vs Low-retention:
- High: Used feature X within 24h (80% did)
- Low: Used feature X within 24h (20% did)

🎯 Hypothesis: Feature X usage = activation event
```

**3. Hypothesis Generation (30 min)**

**Brainstorm Format:**

```markdown
# Hypothesis Backlog

## Acquisition Ideas
1. **SEO content hub**
   - Hypothesis: Creating 20 high-quality guides will increase organic traffic by 30%
   - Reasoning: Competitors rank well для "how to" queries, we don't

2. **Referral program**
   - Hypothesis: Double-sided incentive will increase referrals from 5% to 15%
   - Reasoning: Dropbox model, current referrals = high LTV

## Activation Ideas
3. **Interactive onboarding**
   - Hypothesis: Replace video tutorial with interactive walkthrough → +15% activation
   - Reasoning: Users bounce on passive video, need hands-on

4. **Aha moment optimization**
   - Hypothesis: Prompting Feature X usage in first session → +20% Day 7 retention
   - Reasoning: Data shows Feature X usage correlates with retention

## Retention Ideas
5. **Email re-engagement**
   - Hypothesis: Personalized re-engagement series for inactive users → 10% resurrection
   - Reasoning: 60% of churned users never received targeted outreach

6. **In-app notifications**
   - Hypothesis: Smart notifications for feature discovery → +5% MAU
   - Reasoning: Users don't know about advanced features

[... 10-20 total ideas ...]
```

**4. ICE Scoring & Prioritization (30 min)**

```markdown
# Experiment Prioritization (ICE Framework)

| # | Hypothesis | Impact | Confidence | Ease | ICE Score | Priority |
|---|-----------|--------|------------|------|-----------|----------|
| 4 | Aha moment optimization | 9 | 7 | 8 | 8.0 | 🥇 P0 |
| 2 | Referral program | 8 | 6 | 5 | 6.3 | 🥈 P1 |
| 3 | Interactive onboarding | 8 | 5 | 4 | 5.7 | 🥉 P1 |
| 5 | Email re-engagement | 7 | 8 | 9 | 8.0 | 🥇 P0 |
| 1 | SEO content hub | 9 | 7 | 3 | 6.3 | 🥈 P1 |
| 6 | In-app notifications | 6 | 6 | 7 | 6.3 | 🥈 P1 |

**This week's focus**:
1. ✅ Aha moment optimization (high ICE, addresses biggest funnel drop)
2. ✅ Email re-engagement (high ICE, easy implementation)
```

**5. Sprint Commitment (30 min)**

```markdown
# This Week's Experiments

## Experiment #1: Aha Moment Optimization
**Owner**: [Name]
**Hypothesis**: Prompting Feature X usage in first session will increase Day 7 retention from 30% to 36% (+20%)
**Design**:
- Control: Current onboarding flow
- Variant: Modal prompt after signup: "Try Feature X now" with guided walkthrough
- Traffic: 50/50 split
- Sample size: 1000 users per variant (achievable this week)
- Duration: 7 days (to measure Day 7 retention)
**Success criteria**: p < 0.05, min +10% lift
**Engineering effort**: 4 hours
**Launch target**: Tuesday EOD

## Experiment #2: Email Re-engagement Campaign
**Owner**: [Name]
**Hypothesis**: 3-email sequence to inactive users (no activity 7+ days) will resurrect 10%
**Design**:
- Segment: Users inactive 7-30 days (not churned yet)
- Email 1 (Day 7): "We miss you" + new feature highlight
- Email 2 (Day 10): Customer success story + benefit reminder
- Email 3 (Day 14): "Last chance" + special offer/incentive
- Control: No emails (current state)
- Test: 50% get sequence, 50% control
**Success criteria**: 10%+ return rate (login within 7 days of email 1)
**Effort**: 2 hours (email copy + setup)
**Launch target**: Wednesday morning
```

### Tuesday-Thursday: Execution & Monitoring

**Daily Standup (15 min):**
```
- Yesterday: What shipped?
- Today: What's launching?
- Blockers: Any issues?
- Early signals: What data says?
```

**Experiment Launch Checklist:**
```markdown
## Launch Checklist: [Experiment Name]

### Pre-Launch
- [ ] Hypothesis documented
- [ ] Experiment design reviewed
- [ ] Success criteria defined
- [ ] Instrumentation/tracking implemented
- [ ] QA completed (test both variants)
- [ ] Sample size calculation done
- [ ] Duration planned

### Launch
- [ ] Feature flag enabled (gradual rollout: 10% → 50% → 100%)
- [ ] Monitoring dashboard set up
- [ ] Alerts configured (for anomalies)
- [ ] Team notified

### Monitoring
- [ ] Day 1: Check for technical issues
- [ ] Day 2-3: Early signals review
- [ ] Mid-week: Statistical power check
- [ ] End of week: Results analysis prep
```

**Real-Time Monitoring:**
```markdown
# Experiment #1: Live Monitoring

## Current Status (Day 3 / 7)
- Users per variant: 430 (Control), 445 (Variant)
- Feature X usage: 20% (Control), 38% (Variant) ✅ Working!
- Early retention signal: 32% vs 35% (too early, not significant)

## Alerts
- ⚠️ Variant load time +200ms → investigate performance
- ✅ No error rate increase
- ✅ Equal distribution (50/50 confirmed)

## Next Actions
- [ ] Investigate load time issue
- [ ] Continue running until 1000/variant
- [ ] Plan Day 7 retention analysis for next Monday
```

### Friday: Analysis & Planning (2-3 hours)

**1. Experiment Results Analysis (60 min)**

```markdown
# Experiment Results: Aha Moment Optimization

## Setup
- **Hypothesis**: Prompting Feature X usage → +20% Day 7 retention
- **Duration**: 7 days
- **Sample size**: 1,024 (Control), 1,015 (Variant)

## Results

### Primary Metric: Day 7 Retention
| Metric | Control | Variant | Lift | p-value |
|--------|---------|---------|------|---------|
| Day 7 Retention | 30.2% | 36.1% | +19.5% | 0.003 ✅ |

**Statistical Significance**: ✅ Yes (p = 0.003 < 0.05)
**Confidence Interval**: [+12%, +27%]
**Practical Significance**: ✅ Yes (+19.5% = huge impact)

### Secondary Metrics
| Metric | Control | Variant | Change |
|--------|---------|---------|--------|
| Feature X usage | 19% | 41% | +116% ⭐ |
| Time to activation | 4.2 days | 1.8 days | -57% ⭐ |
| Support tickets | 0.8/user | 0.6/user | -25% ⭐ |

### Segmentation Analysis
| Segment | Control Retention | Variant Retention | Lift |
|---------|------------------|-------------------|------|
| Mobile | 25% | 32% | +28% |
| Desktop | 33% | 38% | +15% |
| New users | 28% | 35% | +25% ⭐ Best |
| Returning | 35% | 40% | +14% |

## Insights
1. **Huge win**: +19.5% retention is massive
2. **Feature X = aha moment**: Confirmed hypothesis
3. **Fastest impact**: 1.8 days to activation vs 4.2 days
4. **Mobile especially**: +28% lift on mobile
5. **Reduced support**: Less confusion → fewer tickets

## Decision
🚀 **SHIP TO 100%**

## Next Steps
1. Scale to 100% of users (immediately)
2. Document as best practice for future products
3. Explore: Can we surface Feature X even earlier?
4. Experiment idea: What other "aha moments" can we accelerate?
```

**2. Weekly Metrics Review (30 min)**

```markdown
# Weekly Growth Metrics (Week of [Date])

## AARRR Funnel
```
📊 Acquisition: 4,200 signups (+5% WoW)
   ├─ Organic: 1,800 (43%)
   ├─ Paid: 1,500 (36%)
   └─ Referral: 900 (21%)

⚡ Activation: 2,520 reached aha moment (60%, ↑ from 55% last week)
   └─ 🎯 Experiment win contributed +5pp

🔄 Retention: 32% Day 7 retention (↑ from 30%)
   └─ 🎯 Aha moment experiment impact

💰 Revenue: $128K MRR (+$8K WoW, +6.7%)
   ├─ New: $12K
   ├─ Expansion: $3K
   └─ Churn: -$7K

📣 Referral: 8% referral rate (flat)
```

## North Star Metric
**Weekly Active Users (WAU)**: 12,500 (↑8% WoW) ⭐

## Key Insights
1. ✅ Activation improvement showing results
2. ✅ Retention curve trending up
3. ⚠️ Referral rate flat (opportunity)
4. ⚠️ Churn slightly elevated (investigate)
```

**3. Knowledge Base Update (30 min)**

```markdown
# Growth Learnings Database

## Entry #47: Feature X = Aha Moment

**Date**: [Date]
**Category**: Activation
**Hypothesis**: Prompting Feature X usage increases retention
**Result**: ✅ Win (+19.5% Day 7 retention)

**What We Learned**:
1. Feature X usage within first session = strongest retention predictor
2. Users don't discover Feature X organically (only 19% found it)
3. Modal prompt with guided walkthrough = effective intervention
4. Mobile users benefit most (+28% lift)

**Future Applications**:
- Apply "prompt aha moment" pattern to other products
- Identify aha moments early in product development
- Test guided walkthroughs for other complex features

**Cautions**:
- Don't overuse modals (tested just one, don't add 10)
- Ensure feature is actually valuable (not just pushing adoption)
- Monitor long-term retention (novelty effect risk)

**Related Experiments**:
- #23: Onboarding video (failed - passive content doesn't work)
- #34: Email activation campaign (moderate success +8%)

**Owner**: [Name]
**Tags**: #activation #retention #onboarding #mobile
```

**4. Next Week Planning (30 min)**

```markdown
# Next Week's Roadmap

## Experiments to Launch
1. **Referral program v1** (from backlog, ICE 6.3)
   - Design double-sided incentive
   - Build referral flow
   - Track viral coefficient

2. **Onboarding personalization** (new idea from this week)
   - Segment by use case
   - Customize onboarding flow
   - A/B test vs generic flow

## Experiments to Analyze
1. **Email re-engagement** (launched Wednesday)
   - Check resurrection rate
   - Analyze which email performed best
   - Scale if successful

## Research & Exploration
1. **Churn analysis** (elevated this week)
   - Interview 10 churned users
   - Identify common patterns
   - Generate retention experiments

## Capacity Planning
- Engineering: 12 hours available
- Design: 8 hours available
- Data: 6 hours available
- Marketing: 10 hours available
```

## Output Artifacts

Команда создает:

```
growth-sprint-[date]/
├── sprint-plan.md
├── experiments/
│   ├── experiment-001-aha-moment.md
│   ├── experiment-002-email-reengagement.md
│   └── experiment-003-referral-program.md
├── results/
│   ├── weekly-metrics-dashboard.md
│   ├── experiment-001-results.md
│   └── experiment-002-results.md
├── learnings/
│   ├── learning-047-aha-moment.md
│   └── learning-048-email-timing.md
└── next-week-plan.md
```

## Best Practices от Growth Leaders

### Netflix Growth Playbook
- **Test everything**: Even small UI changes
- **Long-term metrics**: Not just CTR, but retention impact
- **Personalization**: Segmented experiences by user type
- **Member experience first**: Don't sacrifice quality for growth

### Airbnb Experimentation
- **Peer review**: Other data scientists review designs
- **Pre-registration**: Log hypothesis before running
- **Guardrail metrics**: Protect core experience
- **Learning culture**: Document and share all results

### Dropbox Growth Tactics
- **Product-led growth**: Product as primary growth channel
- **Viral loops**: Built into product experience
- **Referral program**: Dropbox referral = 3900% growth
- **Simplicity focus**: Remove friction obsessively

### Slack Growth Strategy
- **Bottom-up adoption**: Team → Company wide
- **Collaboration virality**: Inviting teammates = distribution
- **2000 messages**: Magic number for stickiness
- **Network effects**: More users = more value

## Использование команды

**Запуск:**
```bash
/growth-sprint
```

**Interactive setup:**
1. Выберите focus area (Acquisition/Activation/Retention/Revenue/Referral)
2. Укажите current metrics baseline
3. Определите target improvement
4. Set team capacity

**Команда генерирует:**
- Sprint plan template
- Experiment briefs
- Tracking dashboards
- Learning documentation

**Все на русском в Markdown.**

## Metrics Dashboard Template

```markdown
# Growth Metrics Dashboard

## North Star Metric
**[Metric Name]**: [Current] ([% change] WoW)

## AARRR Metrics

### Acquisition
- New signups: [Number] ([% change])
- By channel:
  - Organic: [%]
  - Paid: [%]
  - Referral: [%]
- Cost per acquisition: $[Amount]

### Activation
- % reached aha moment: [%] ([change])
- Time to activation: [Hours/Days]
- Activation by cohort: [Trend]

### Retention
- Day 1: [%]
- Day 7: [%]
- Day 30: [%]
- Cohort trends: [Improving/Flat/Declining]

### Revenue
- MRR: $[Amount] ([% change])
- ARPU: $[Amount]
- LTV: $[Amount]
- LTV:CAC ratio: [Ratio]

### Referral
- Referral rate: [%]
- Viral coefficient: [K-factor]
- Invited users converted: [%]

## Active Experiments
| Experiment | Status | Early Signal | Decision Date |
|-----------|--------|--------------|---------------|
| [Name] | Running | [Signal] | [Date] |

## Key Insights This Week
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]
```

---

**Ready to run systematic growth experiments?**

Run `/growth-sprint` to start your first sprint.
