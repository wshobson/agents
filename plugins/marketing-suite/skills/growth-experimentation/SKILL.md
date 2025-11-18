---
name: growth-experimentation
description: Методология проведения data-driven экспериментов роста, A/B testing, experimentation frameworks уровня Netflix, Airbnb, Stripe. Use when designing growth experiments, prioritizing tests, or analyzing experiment results.
---

# Growth Experimentation

## Когда использовать этот навык

- Разработка growth experiment roadmap
- Приоритизация hypothesis для тестирования
- Дизайн A/B tests с statistical rigor
- Анализ experiment results и принятие решений
- Building experimentation culture в команде

## Ключевые концепции

### Experiment Framework

**Hypothesis Structure:**
```
We believe that [making this change]
For [these users]
Will result in [this outcome]
We'll know we're right when [measurable result]
```

**Example (Dropbox):**
```
We believe that adding referral incentives (500MB free space)
For both referrer and referee
Will increase viral coefficient from 0.5 to 1.0
We'll know we're right when signups from referrals increase by 60%
```

### ICE Scoring для Prioritization

**Formula:**
```
ICE Score = (Impact × Confidence × Ease) / 3

Impact (1-10): Potential magnitude of effect
Confidence (1-10): How sure are we it will work
Ease (1-10): How easy to implement
```

**Example Scoring:**
| Hypothesis | Impact | Confidence | Ease | ICE Score |
|-----------|--------|------------|------|-----------|
| Email subject line test | 7 | 8 | 10 | 8.3 |
| Redesign onboarding | 9 | 5 | 3 | 5.7 |
| Add social proof | 8 | 7 | 8 | 7.7 |

### Statistical Significance

**Key Concepts:**

**Sample Size Calculation:**
```
Minimum users per variant = 16 × (σ²) / (δ²)

где:
σ = standard deviation
δ = minimum detectable effect (MDE)

Правило большого пальца: 1000+ users per variant
```

**P-Value & Confidence:**
- **p < 0.05**: 95% confidence (стандарт)
- **p < 0.01**: 99% confidence (более строгий)
- **p-hacking**: ❌ Не останавливайте тест рано!

**Statistical Power:**
- Target: 80% power
- Означает: 80% вероятность detect эффект, если он есть

## Типы Experiments

### 1. A/B Tests (Split Testing)

**Простейший формат:**
- Control (A): Current experience
- Variant (B): New experience
- 50/50 traffic split
- Measure difference в key metric

**Example (LinkedIn):**
```
Control: "View profile" button
Variant: "Send message" button
Metric: Connection rate
Result: 20% increase → Ship variant
```

### 2. Multivariate Tests (MVT)

**Тестирование multiple elements:**
- Element 1: Headline (A1, A2)
- Element 2: CTA (B1, B2)
- Element 3: Image (C1, C2)
- Total combinations: 2×2×2 = 8 variants

**Требование:** Нужно больше traffic (минимум 1000+ users per variant)

### 3. Sequential Testing

**Iterative approach:**
```
Week 1: Test A vs B → B wins
Week 2: Test B vs C → C wins
Week 3: Test C vs D → C still wins
Result: Ship C
```

### 4. Multi-Armed Bandit

**Dynamic allocation:**
- Start 50/50 split
- Algorithm shifts traffic к better performer
- Maximizes overall conversion during test
- Reduces "opportunity cost" of testing

**Good for:**
- Content recommendations (Netflix)
- Ad creative optimization
- Email subject lines

## Experimentation Process

### Phase 1: Hypothesis Generation

**Sources of Ideas:**

**Data Analysis:**
- Funnel drop-offs (где users leave)
- Heatmaps & session recordings (confusion points)
- Cohort analysis (what distinguishes high-value users)
- User surveys (direct feedback)

**Best Practices Research:**
- Competitor analysis
- Industry case studies
- Behavioral psychology (Cialdini principles)
- UX patterns that work

**Team Brainstorming:**
- Product, Marketing, Design, Engineering input
- Customer support insights
- Sales objections

### Phase 2: Prioritization

**ICE/PIE Scoring:**

**PIE Framework (Alternative):**
```
Potential (1-10): Max possible improvement
Importance (1-10): Impact на business goals
Ease (1-10): Resources needed

PIE Score = (Potential + Importance + Ease) / 3
```

**Portfolio Approach:**
- 70% High-confidence, incremental tests
- 20% Medium-confidence, bigger bets
- 10% Wild ideas, breakthrough potential

### Phase 3: Design & Setup

**Experiment Design Checklist:**
- ☑ Hypothesis clearly stated
- ☑ Primary metric defined
- ☑ Secondary metrics identified
- ☑ Sample size calculated
- ☑ Duration determined (min 1-2 weeks)
- ☑ Randomization method chosen
- ☑ Success criteria defined upfront
- ☑ Instrumentation/tracking implemented

**Common Pitfalls:**
- ❌ Testing too many things at once
- ❌ Insufficient sample size
- ❌ Not running long enough
- ❌ Selection bias in segmentation
- ❌ Not considering weekly/monthly patterns

### Phase 4: Analysis

**Results Interpretation:**

**Statistical Significance:**
```
if p-value < 0.05 AND
   confidence interval doesn't include 0 AND
   test ran for planned duration:
   → Result is statistically significant
```

**Practical Significance:**
```
Lift × Volume = Impact

Example:
+5% conversion (lift)
× 10,000 weekly visitors (volume)
= 500 additional conversions/week
× $100 LTV
= $50,000/week revenue impact
```

**Check for:**
- **Novelty effect**: Temporary boost from newness
- **Segment differences**: Works for mobile but not desktop
- **Time patterns**: Weekday vs weekend differences
- **Secondary metrics**: Did we hurt something else?

### Phase 5: Decision & Learning

**Decision Tree:**
```
Is result significant?
├─ Yes: Did it hit success criteria?
│  ├─ Yes: SHIP IT
│  └─ No: ITERATE or KILL
└─ No: Insufficient data
   ├─ Run longer
   └─ Or KILL and move on
```

**Document Learnings:**
- What we tested
- Why we tested it
- Results (with data)
- Decision made
- Key insights for future
- Share with team (build knowledge base)

## Experimentation Best Practices

### Netflix Experimentation Culture

**Principles:**
- **Test everything**: UI changes, algorithms, content
- **Parallel experiments**: Run 100s simultaneously
- **Long-term metrics**: Not just CTR, but retention
- **Member experience > short-term gains**

**Example:**
- Tested: Autoplay next episode
- Measured: Watch time, retention
- Result: Massive lift → became standard

### Airbnb Experimentation Rigor

**Standards:**
- **Pre-registration**: Log hypothesis before test
- **Peer review**: Other data scientists review design
- **Guardrail metrics**: Don't break core experience
- **Segmentation**: Mobile vs web, new vs returning

**Example:**
- Tested: Professional photography for listings
- Result: 2-3x bookings → $3M+ investment in photographer network

### Stripe Developer-First Testing

**Approach:**
- **API changes**: Heavily tested with beta users
- **Documentation**: A/B test docs structure
- **Onboarding**: Iterate на time-to-first-transaction

**Example:**
- Tested: Stripe Checkout vs custom integration
- Measured: Implementation time, conversion
- Result: 50% faster implementation → push Checkout

## Advanced Techniques

### 1. Bayesian Testing

**vs Frequentist (traditional):**
- Updates probability as data comes in
- Can stop early with confidence
- Answers "What's probability B is better than A?"

**Good for:**
- Lower traffic scenarios
- When need faster decisions
- E-commerce (Dynamic Yield, Optimizely use this)

### 2. Holdout Groups

**Long-term impact measurement:**
```
Launch experiment → 95% get new experience
                  → 5% stay on control (holdout)

Measure after 3, 6, 12 months:
Did the effect persist? Increase? Fade?
```

**Example (Facebook):**
- Tested News Feed algorithm change
- Measured short-term: Engagement up 5%
- Measured long-term: Retention actually down
- Decision: Don't ship

### 3. Interaction Effects

**Testing combined changes:**

Problem: Test A wins (+10%), Test B wins (+15%)
         But A+B together = +18% (not 25%)

**Why?** Interaction effects (A and B overlap or conflict)

**Solution:** Test combinations explicitly

### 4. Personalization & Segmentation

**Not one-size-fits-all:**
```
Overall: Variant loses -2%
  ├─ New users: Variant wins +15%
  └─ Returning users: Variant loses -8%

Decision: Ship to new users only
```

## Experimentation Anti-Patterns

### ❌ HiPPO (Highest Paid Person's Opinion)
**Wrong:** "CEO wants this, ship without testing"
**Right:** "Let's test CEO's idea vs alternatives"

### ❌ Vanity Metrics Optimization
**Wrong:** Optimize for clicks (doesn't mean revenue)
**Right:** Optimize for meaningful outcomes (retention, LTV)

### ❌ P-Hacking
**Wrong:** Stop test as soon as p < 0.05 even if sample size not met
**Right:** Run for pre-determined duration/sample size

### ❌ Local Maximum Trap
**Wrong:** Only incremental tests (green button to blue button)
**Right:** Also test bold redesigns (10x thinking)

### ❌ Ignoring Negative Results
**Wrong:** Only share winning tests
**Right:** Document failures (avoid repeating mistakes)

## Experimentation Metrics

### North Star Metric (NSM)

**Definition:** The one metric that best captures core value delivered

**Examples:**
| Company | North Star Metric |
|---------|-------------------|
| Spotify | Time Spent Listening |
| Slack | Messages Sent |
| Netflix | Watch Time |
| Airbnb | Nights Booked |
| Uber | Rides per Week |

### Supporting Metrics

**Engagement:**
- Daily Active Users (DAU)
- Monthly Active Users (MAU)
- DAU/MAU ratio (stickiness)
- Session frequency & duration

**Conversion:**
- Trial-to-paid rate
- Signup completion rate
- Feature adoption rate
- Activation rate (reaching aha moment)

**Retention:**
- Day 1, 7, 30 retention
- Cohort retention curves
- Churn rate
- Resurrection rate (bringing back churned)

**Revenue:**
- ARPU (Average Revenue Per User)
- LTV (Lifetime Value)
- MRR/ARR
- Net Revenue Retention

## Tools & Platforms

### Experimentation Platforms

**Enterprise:**
- Optimizely ($$$$)
- VWO (Visual Website Optimizer) ($$$)
- Adobe Target ($$$$)
- Google Optimize ($ - Free tier)

**Product Analytics + Experiments:**
- Amplitude Experiment ($$$)
- Mixpanel ($$)
- Statsig ($$)
- LaunchDarkly (feature flags) ($$$)

**Custom Stack:**
- Feature flags: LaunchDarkly, Split.io
- Analytics: Amplitude, Mixpanel, Heap
- Statistics: Python (scipy), R
- Data warehouse: Snowflake, BigQuery

### Statistical Calculators

**Sample Size:**
- Evan Miller's calculator (free online)
- Optimizely sample size calculator

**Significance:**
- Chi-square test (categorical data)
- T-test (continuous data)
- Bayesian calculators

## Шаблоны документации

### Experiment Brief Template

```markdown
# Experiment: [Name]

## Hypothesis
We believe that [change]
For [users]
Will result in [outcome]
We'll know when [metric] changes by [%]

## Rationale
[Why do we think this will work? Data/research supporting]

## Design
- **Variants**: Control (A), Variant (B)
- **Traffic allocation**: 50/50
- **Target audience**: [All users / Specific segment]
- **Duration**: [2 weeks / until 1000 conversions per variant]

## Metrics
- **Primary**: [Main metric we're trying to move]
- **Secondary**: [Supporting metrics]
- **Guardrail**: [Metrics we must not hurt]

## Success Criteria
- Primary metric improves by [%] with p < 0.05
- No degradation in guardrail metrics

## Implementation
- **Engineering effort**: [Hours/days]
- **Dependencies**: [Other teams/systems]
- **QA plan**: [How to verify correct implementation]

## Analysis Plan
- **Instrumentation**: [Events tracked]
- **Segmentation**: [Any subgroup analysis]
- **Timeline**: Review after [date]

---
**Owner**: [Name]
**Reviewers**: [Team members]
**Status**: [Draft / In Review / Running / Completed]
```

## Дополнительные ресурсы

См. `references/` для:
- Experimentation playbooks от Netflix, Airbnb
- Statistical significance calculators
- Sample size tables
- Experiment tracking spreadsheets

См. `assets/` для:
- ICE scoring templates
- Experiment brief templates
- Results analysis frameworks
- Learning documentation examples
