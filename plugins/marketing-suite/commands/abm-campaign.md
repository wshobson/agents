---
name: abm-campaign
description: Комплексный ABM campaign orchestrator для enterprise accounts с account selection, multi-threaded engagement, intent orchestration и revenue attribution.
---

# ABM Campaign Command

Автоматизирует создание и execution enterprise ABM campaigns от account selection до closed-won analysis.

## Цель

Orchestrate полный ABM campaign lifecycle:
- Account selection & tiering (ICP scoring)
- Buying committee mapping
- Intent-based prioritization
- Multi-channel campaign orchestration
- Sales-marketing alignment playbooks
- Performance tracking & attribution

## Входные параметры

```
Campaign Type: [Strategic 1:1 / ABM Lite 1:Few / Programmatic 1:Many]
Account count: [5-20 / 50-100 / 500-1000]
Industry focus: [Technology / Financial Services / Healthcare / etc.]
Target ACV: [$100K-500K / $500K-2M / $2M+]
Campaign duration: [Quarter / 6 months / Annual]
```

## Процесс выполнения

### Фаза 1: Account Selection (Week 1-2)

**Команда создает:**

1. **ICP Scoring Model**
```markdown
# ICP Criteria & Weights

## Firmographic (40%)
- Revenue: $500M+ (10 pts)
- Employees: 1,000+ (10 pts)
- Industry match: Target verticals (10 pts)
- Geography: Sales coverage areas (10 pts)

## Intent Signals (30%)
- Website engagement: Pricing/Enterprise pages (10 pts)
- Third-party intent: Bombora surges (10 pts)
- G2 research: Category comparison (10 pts)

## Strategic Value (30%)
- Revenue potential: Estimated ACV (15 pts)
- Reference value: Logo recognition (10 pts)
- Expansion opportunity: Multi-product fit (5 pts)

Scoring:
- A Accounts (80-100): Strategic ABM
- B Accounts (60-79): ABM Lite
- C Accounts (40-59): Programmatic
```

2. **Account List Generation**
```markdown
# Target Account List: Q[X] 2024 Campaign

## Tier A Accounts (Strategic 1:1)
| Company | Industry | Score | ACV Potential | Owner |
|---------|----------|-------|---------------|-------|
| [Name] | Tech | 92 | $2.5M | [AE] |
| [Name] | FinServ | 88 | $1.8M | [AE] |
...

## Tier B Accounts (ABM Lite)
| Company | Industry | Score | ACV Potential | Cluster |
|---------|----------|-------|---------------|---------|
| [Name] | Healthcare | 72 | $500K | Healthcare-1 |
...

## Tier C Accounts (Programmatic)
| Company | Industry | Score | ACV Potential | Segment |
|---------|----------|-------|---------------|---------|
| [Name] | Manufacturing | 54 | $150K | Mid-Market |
...
```

### Фаза 2: Buying Committee Research (Week 2-3)

**Для каждого Tier A Account:**

```markdown
# Account Plan: [Company Name]

## Company Intelligence
- **Strategic priorities**: [From annual report]
- **Technology initiatives**: [Cloud migration, digital transformation]
- **Recent news**: [Leadership changes, M&A, market expansion]
- **Competitors using us**: [Social proof in industry]

## Buying Committee Map

### Economic Buyer: [CFO Name]
- **LinkedIn**: [Profile URL]
- **Background**: [Previous companies, education]
- **Priorities**: [Cost optimization, ROI]
- **Recent activity**: [Posts, shares]
- **Our connections**: [Mutual LinkedIn connections]
- **Engagement status**: 🔴 Not contacted
- **Next action**: Executive dinner invitation

### Technical Buyer: [CTO Name]
[Same structure]

### Champion: [VP Engineering Name]
[Same structure]

### Influencers: [Architect Names]
[Same structure]

## Multi-Threading Score: 0/7 personas
```

### Фаза 3: Campaign Design (Week 3-4)

**Strategic ABM Playbook (Tier A):**

```markdown
# 90-Day Strategic ABM Play: [Account]

## Week 1-2: Research & Warm-Up
- [ ] Deep account research completed
- [ ] Buying committee identified (7 personas)
- [ ] Account-specific value prop created
- [ ] LinkedIn engagement begins (like/comment posts)
- [ ] Intent monitoring activated

## Week 3-4: Initial Outreach
- [ ] Personalized direct mail (custom package $200)
- [ ] AE email to Economic Buyer (custom ROI deck)
- [ ] SDR multi-touch to Champion (email/phone/LinkedIn)
- [ ] Display ads activated (IP targeting)
- [ ] Custom industry report delivered

## Week 5-6: Relationship Building
- [ ] Executive dinner invitation (8-person intimate)
- [ ] Technical deep-dive webinar (for Technical Buyer)
- [ ] Customer reference call arranged (similar company)
- [ ] LinkedIn InMail from our C-level to their C-level
- [ ] Custom demo video (their use case)

## Week 7-8: Acceleration
- [ ] Discovery meeting scheduled
- [ ] Custom ROI analysis (their numbers)
- [ ] Security & compliance docs delivered
- [ ] POC proposal presented
- [ ] Buying committee expansion (reach 5+ contacts)

## Week 9-12: Close Support
- [ ] Executive sponsorship activated
- [ ] Proposal customization
- [ ] Contract negotiation support
- [ ] Implementation planning
- [ ] Success metrics agreed
```

**ABM Lite Playbook (Tier B - Industry Cluster):**

```markdown
# Healthcare Provider Cluster Campaign

## Accounts: 20 healthcare organizations

## Shared Characteristics
- 500-bed hospitals
- Electronic Health Record (EHR) modernization
- HIPAA compliance critical
- Budget cycles: Q1 planning

## Cluster Campaign Assets
- [ ] Healthcare industry brief (white paper)
- [ ] HIPAA compliance guide (technical doc)
- [ ] Hospital CIO webinar series (4 sessions)
- [ ] Healthcare customer case studies (3 customers)
- [ ] ROI calculator (hospital-specific)

## Multi-Channel Execution
**Week 1-2**: LinkedIn campaign (Healthcare IT personas)
**Week 3-4**: Industry webinar (invite all 20 accounts)
**Week 5-6**: Email nurture (HIPAA focus)
**Week 7-8**: Direct mail (compliance guide)
**Week 9-12**: Sales follow-up (meeting requests)

## Success Metrics
- 15+ accounts engaged (website visit + content download)
- 10+ webinar attendees
- 5+ discovery meetings
- 2+ opportunities created
```

### Фаза 4: Campaign Execution (Ongoing)

**Weekly Account Reviews:**

```markdown
# Weekly ABM Status Report

## Account Engagement Summary

### Hot Accounts (High Intent + Engaged)
| Account | Intent Score | Engagement | Stage | Next Action |
|---------|--------------|------------|-------|-------------|
| [Name] | 92 | 🔥 Very High | Discovery | Demo scheduled Fri |
| [Name] | 87 | 🔥 Very High | Evaluation | POC proposal ready |

### Warming Accounts (Increasing Intent)
| Account | Intent Score | Engagement | Stage | Next Action |
|---------|--------------|------------|-------|-------------|
| [Name] | 68 | 🟡 Medium | Awareness | Webinar invite sent |

### Cool Accounts (Low Engagement)
| Account | Intent Score | Engagement | Stage | Next Action |
|---------|--------------|------------|-------|-------------|
| [Name] | 42 | ❄️ Low | Target | Direct mail next week |

## Key Activities This Week
- 12 emails sent (4 replied)
- 8 LinkedIn connections made
- 3 webinar attendees
- 2 discovery meetings held
- 1 demo delivered
- 5 intent spikes detected

## Blockers & Escalations
- [ ] [Account X]: Need C-level sponsorship → Escalate to VP Sales
- [ ] [Account Y]: Security questions → Need Legal review
```

### Фаза 5: Sales-Marketing Orchestration

**Coordinated Plays:**

```markdown
# Sales-Marketing Sync: [Account Name]

## Trigger: High intent spike detected

### Marketing Actions (Hour 0-24)
- [ ] Retargeting ads activated (LinkedIn + Display)
- [ ] Personalized email sequence triggered
- [ ] Account alert sent to SDR & AE
- [ ] Custom content identified (relevant to research topic)

### SDR Actions (Hour 24-48)
- [ ] Account research completed
- [ ] Buying committee contacts identified
- [ ] LinkedIn connection requests sent
- [ ] Personalized email (reference their research)
- [ ] Phone attempts (3x over 2 days)

### AE Actions (Day 3-5)
- [ ] Review SDR research
- [ ] Personalized outreach (higher level contacts)
- [ ] Custom value prop prepared
- [ ] Demo environment ready (their use case)

### Success Path
- [ ] Meeting booked
- [ ] Discovery call completed
- [ ] Opportunity created in CRM
- [ ] POC/evaluation stage

### If No Response
- [ ] Continue nurture (marketing automation)
- [ ] Add to next webinar invite
- [ ] Queue for direct mail
- [ ] Retry outreach in 30 days
```

### Фаза 6: Performance Tracking

**Campaign Dashboard:**

```markdown
# ABM Campaign Performance: Q[X] 2024

## Account Coverage
- Total target accounts: 75
- Engaged accounts: 52 (69%) ✅
- Hot accounts (high intent): 12 (16%)
- Opportunities created: 8 (11%)

## Buying Committee Coverage
- Average contacts per account: 3.4
- Accounts with 5+ contacts: 18 (34%)
- C-level engagement: 22 accounts (29%)

## Pipeline Impact
- Pipeline generated: $4.2M
- Average deal size: $525K (vs $400K baseline)
- Win rate: 38% (vs 25% non-ABM)
- Sales cycle: 87 days (vs 120 days non-ABM)

## Channel Performance
| Channel | Accounts Engaged | Cost | Cost per Engagement |
|---------|------------------|------|---------------------|
| LinkedIn Ads | 42 | $12K | $286 |
| Direct Mail | 35 | $8K | $229 |
| Webinars | 28 | $5K | $179 |
| Email | 52 | $2K | $38 |
| Field Events | 15 | $25K | $1,667 |

## Content Performance
| Asset | Downloads | Accounts | Opportunity Influence |
|-------|-----------|----------|----------------------|
| Industry Report | 34 | 28 | 5 opps |
| ROI Calculator | 22 | 18 | 4 opps |
| Case Study | 18 | 15 | 3 opps |
| Webinar Replay | 26 | 22 | 2 opps |

## Attribution Analysis
- First-touch: Webinar (40%), LinkedIn (30%), Direct Mail (20%)
- Multi-touch: Avg 7.2 touchpoints before opportunity
- Most influential: Executive dinner → 80% conversion to opp
```

## Output Artifacts

```
abm-campaign-[name]/
├── strategy/
│   ├── account-selection-criteria.md
│   ├── target-account-list.md
│   ├── campaign-strategy.md
│   └── budget-allocation.md
├── accounts/
│   ├── tier-a-accounts/
│   │   ├── account-plan-company1.md
│   │   ├── buying-committee-map-company1.md
│   │   └── engagement-playbook-company1.md
│   ├── tier-b-clusters/
│   │   └── healthcare-cluster-plan.md
│   └── tier-c-segments/
│       └── mid-market-segment-plan.md
├── campaigns/
│   ├── linkedin-campaign-brief.md
│   ├── email-sequences.md
│   ├── direct-mail-plan.md
│   ├── event-strategy.md
│   └── content-calendar.md
├── tracking/
│   ├── weekly-status-reports/
│   ├── account-engagement-dashboard.md
│   ├── pipeline-attribution.md
│   └── roi-analysis.md
└── enablement/
    ├── sales-playbooks.md
    ├── talk-tracks.md
    ├── battle-cards.md
    └── objection-handling.md
```

## Best Practices от ABM Leaders

### Salesforce ABM Approach
```
- Dedicated account teams (AE + SE + CSM)
- Quarterly business reviews (even pre-sale)
- Customer Advisory Boards (strategic input)
- Multi-year relationship building
```

### Oracle Strategic Accounts
```
- C-level to C-level engagement (CEO involvement)
- Industry expertise (vertical-specific teams)
- Long-term investment (3-5 year relationships)
- Business consulting (not just vendor)
```

### Microsoft Enterprise ABM
```
- Partner ecosystem (co-sell with SIs)
- Digital transformation positioning (strategic)
- Technology roadmap alignment (CTO-level)
- Executive sponsorship programs
```

### AWS Enterprise Flywheel
```
- TAM assignment (Technical Account Manager)
- Well-Architected Review (free consulting)
- Executive briefings (immersive experiences)
- Concierge support (white-glove service)
```

## Success Metrics

### Account Engagement (Leading)
- Target: 70%+ accounts engaged
- Definition: 3+ touches, 1+ content download

### Pipeline Generation (Primary)
- Target: $5M+ pipeline from ABM accounts
- Average deal size: 50%+ larger than non-ABM

### Revenue Attribution (Ultimate)
- Target: 30-50% of enterprise revenue
- Win rate: 2-3x higher than non-ABM
- Sales cycle: 20-30% shorter

### Program ROI (Overall)
- Target: 5:1 ROI minimum
- Calculation: (Revenue - ABM Costs) / ABM Costs

## Usage

```bash
/abm-campaign
```

**Interactive setup:**
1. Define campaign type & account count
2. Set ICP criteria & scoring weights
3. Review generated account list
4. Approve playbooks & budget
5. Launch campaign & monitoring

**Все артефакты на русском в Markdown.**

---

**Ready to launch enterprise ABM campaigns?**

Run `/abm-campaign` to begin.
