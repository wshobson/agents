# Retention Optimization Playbook

## Understanding Retention

### Retention Curve

```
100% ┤
     │╲
 80% │ ╲
     │  ╲___  ← Flattening = retention stabilizing
 60% │      ────
     │
 40% │
     └────────────────────
     D1  D7  D30 D90 D180
```

**Healthy Curves**:
- Consumer: Flatten at 20-40%
- B2B SaaS: Flatten at 60-80%
- Social: Flatten at 30-50%

---

## Retention Frameworks

### 1. Hook Model (Nir Eyal)

**Cycle**:
```
Trigger → Action → Variable Reward → Investment → (repeat)
```

**Example (Instagram)**:
- Trigger: Push notification (friend posted)
- Action: Open app, view post
- Reward: Interesting content, likes
- Investment: Post comment, like back
- Loop: More engagement → more notifications

---

### 2. Retention Drivers

**Core Value**:
- Does user experience "aha moment"?
- Time to first value < 24 hours?

**Habit Formation**:
- Daily use case?
- Trigger for re-engagement?
- Investment that brings user back?

**Switching Costs**:
- Data accumulated?
- Integrations connected?
- Team invited?

---

## Retention Tactics by Stage

### Day 1 (Activation)

**Goal**: Get to aha moment

**Tactics**:
- Onboarding checklist (progress bar)
- Quick wins (achieve something valuable immediately)
- Social proof (show what others achieved)
- Emails: Welcome series (value reminders)

**Metrics**:
- % completing onboarding
- Time to first value
- Key action completion

---

### Day 7 (Early Retention)

**Goal**: Form habit

**Tactics**:
- Re-engagement emails (you have X unread messages)
- Push notifications (personalized triggers)
- Weekly digest (recap of activity)
- Achievement unlocks (gamification)

**Metrics**:
- 7-day retention cohorts
- Session frequency (sessions/user/week)
- Feature adoption

---

### Day 30 (Medium-Term Retention)

**Goal**: Integrate into workflow

**Tactics**:
- Product updates (new features)
- User education (webinars, tutorials)
- Community engagement (user groups)
- Personal check-ins (customer success)

**Metrics**:
- 30-day retention cohorts
- WAU/MAU ratio
- Feature depth (# features used)

---

### Day 90+ (Long-Term Retention)

**Goal**: Make indispensable

**Tactics**:
- Account expansion (team growth)
- Advanced features (power user tools)
- Integration ecosystem (lock-in)
- Loyalty programs (rewards)

**Metrics**:
- 90-day+ cohorts
- Net dollar retention (NDR)
- Product qualified leads (expansion)

---

## Retention Formulas

### Cohort Retention
```
Retention(Day N) = Active Users(Day N) / New Users(Day 0)
```

### Retention by Feature
```
Retained users using Feature X
vs
Retained users not using Feature X

If Feature X group > 20pp higher retention → core feature
```

### Quick Ratio (Growth Quality)
```
Quick Ratio = (New + Resurrected) / Churned

>1.0 = Healthy growth
<1.0 = Leaky bucket
```

---

## Common Retention Issues

### Issue 1: Weak Aha Moment

**Symptom**: High sign-ups, low day-7 retention

**Diagnosis**:
- Compare retained vs churned users
- What did retained users do that churned didn't?

**Solution**:
- Make aha moment more obvious
- Reduce time to aha moment
- Guided onboarding to aha moment

---

### Issue 2: No Habit Loop

**Symptom**: Good activation, declining engagement over time

**Diagnosis**:
- No daily use case
- No triggers for re-engagement

**Solution**:
- Build re-engagement triggers (emails, notifications)
- Create daily value (new content, personalization)
- Gamification (streaks, achievements)

---

### Issue 3: Competition/Churn

**Symptom**: Users leave for competitors

**Diagnosis**:
- Feature gaps
- Poor performance
- Better pricing elsewhere

**Solution**:
- Competitive analysis → feature parity
- Performance optimization
- Pricing adjustments
- Switching costs (data export friction)

---

## Retention Case Studies

### Duolingo: Streaks

**Mechanic**: Daily login streak counter

**Impact**:
- 7-day retention: 37% → 55% (+18pp)
- DAU: 2x increase
- User motivation: Don't break the streak

---

### Facebook: 7 Friends in 10 Days

**Finding**: Users who add 7 friends in first 10 days have 90%+ retention

**Action**:
- Optimize friend suggestions
- Encourage invitations
- Show value of connections

---

### Slack: 2,000 Message Magic Number

**Finding**: Teams sending 2,000 messages have 93% retention

**Action**:
- Encourage team invitations
- Show progress to 2K messages
- Celebrate milestones

---

## Retention Metrics Dashboard

```
Metric                  Target      Current   Status
─────────────────────────────────────────────────────
D1 retention            50%         45%       ⚠️
D7 retention            40%         42%       ✅
D30 retention           25%         23%       ⚠️
DAU/MAU                 40%         38%       ⚠️
Weekly active users     60%         65%       ✅
Feature adoption        70%         68%       ⚠️
Aha moment rate         50%         48%       ⚠️
Time to aha             24h         18h       ✅
```

---

## References

- "Hooked" - Nir Eyal
- "The Retention Playbook" - Reforge
- Lenny's Newsletter (retention deep dives)
