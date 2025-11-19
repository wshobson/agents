---
name: launch-product
description: Комплексный go-to-market launch плагин для запуска продуктов с positioning, messaging, enablement и campaign orchestration уровня AWS/Microsoft.
---

# Product Launch Command

Этот command orchestrates полный цикл запуска продукта, от positioning до post-launch analysis.

## Цель

Автоматизировать создание всех необходимых артефактов для tier-1 product launch:
- Positioning & messaging framework
- Go-to-market strategy & timeline
- Sales enablement materials
- Marketing campaign assets
- Launch readiness checklist
- Success metrics dashboard

## Входные параметры

При запуске команды вас попросят предоставить:

### 1. Информация о продукте
```
Название продукта: [Name]
Категория продукта: [Category - new product/major feature/enhancement]
Launch tier: [Tier 1/2/3]
Target launch date: [Date]
```

### 2. Целевая аудитория
```
Primary persona: [Role, industry, company size]
Secondary personas: [Additional segments]
Key pain points: [Top 3 problems being solved]
```

### 3. Конкурентный контекст
```
Primary competitors: [List top 3]
Current alternatives: [How customers solve today]
Key differentiators: [Why choose us]
```

### 4. Бизнес-цели
```
Revenue target: [$XXX in first quarter]
Adoption target: [XXX users/accounts]
Pipeline target: [$XXX influenced pipeline]
```

## Процесс выполнения

### Фаза 1: Discovery & Research (T-12 weeks)

**Команда проводит:**

1. **Customer research analysis**
   - Анализирует существующие customer interviews
   - Выявляет Jobs-to-be-Done patterns
   - Определяет ключевые pain points

2. **Competitive intelligence**
   - Создает battle cards для топ-3 конкурентов
   - Строит competitive positioning map
   - Определяет key differentiators

3. **Win/loss analysis**
   - Анализирует последние 20-30 deals
   - Выявляет patterns успехов и failures
   - Определяет critical success factors

**Выходные артефакты:**
```
outputs/discovery/
├── customer-insights-summary.md
├── competitive-landscape-analysis.md
├── win-loss-patterns.md
└── market-opportunity-sizing.md
```

### Фаза 2: Positioning & Messaging (T-10 weeks)

**Команда создает:**

1. **Core positioning statement**
   - Geoffrey Moore positioning format
   - Value proposition canvas
   - Elevator pitch (30 sec, 1 min, 5 min versions)

2. **Messaging framework**
   - Core positioning (1 sentence)
   - Value pillars (3-5 key benefits)
   - Proof points (metrics, testimonials, case studies)
   - Audience-specific messaging (technical/business/champion)

3. **Message testing**
   - Рекомендации для Wynter/UserTesting validation
   - A/B testing plan для landing pages
   - Sales validation approach

**Выходные артефакты:**
```
outputs/positioning/
├── positioning-brief.md
├── messaging-framework.md
├── value-proposition-canvas.md
├── elevator-pitches.md
└── message-testing-plan.md
```

### Фаза 3: GTM Strategy & Planning (T-8 weeks)

**Команда разрабатывает:**

1. **Go-to-market strategy**
   - Target segments & ICP
   - Channel strategy (organic/paid/field/sales)
   - Pricing & packaging recommendations
   - Partner strategy

2. **Launch timeline**
   - T-12 weeks to T+4 weeks detailed plan
   - Key milestones и dependencies
   - Team responsibilities (RACI matrix)
   - Risk mitigation plans

3. **Budget allocation**
   - Paid media budget по channels
   - Content production costs
   - Events & field marketing
   - Tools & technology

**Выходные артефакты:**
```
outputs/gtm-strategy/
├── gtm-strategy-document.md
├── launch-timeline-gantt.md
├── channel-strategy-mix.md
├── budget-allocation-plan.md
└── risk-mitigation-matrix.md
```

### Фаза 4: Content & Creative (T-6 weeks)

**Команда создает briefs для:**

1. **Website assets**
   - Product page wireframe & copy
   - Landing page variations (by persona)
   - SEO optimization plan

2. **Sales collateral**
   - Product overview deck (10 slides)
   - One-pager (technical & business versions)
   - Demo script & talking points
   - FAQ document
   - Objection handling guide

3. **Marketing content**
   - Blog post series (announcement, deep-dives, use cases)
   - Email nurture sequence (6-8 emails)
   - Social media toolkit (posts, images, videos)
   - Video scripts (product overview, customer testimonials)

4. **Analyst & PR**
   - Analyst briefing deck
   - Press release draft
   - Media pitch angles
   - Spokesperson talking points

**Выходные артефакты:**
```
outputs/content-creative/
├── website/
│   ├── product-page-brief.md
│   └── landing-page-variations.md
├── sales-collateral/
│   ├── product-deck-outline.md
│   ├── one-pager-brief.md
│   └── demo-script.md
├── marketing-content/
│   ├── blog-post-series.md
│   ├── email-sequence.md
│   └── social-toolkit.md
└── analyst-pr/
    ├── analyst-briefing-deck.md
    └── press-release-draft.md
```

### Фаза 5: Sales Enablement (T-4 weeks)

**Команда готовит:**

1. **Training materials**
   - Product training deck (45 min session)
   - Demo certification program
   - Competitive battle cards
   - Use case scenarios по industry

2. **Sales plays**
   - Discovery question guide
   - Qualification criteria (BANT/MEDDIC)
   - Objection handling scripts
   - Closing techniques

3. **Tools & resources**
   - Salesforce updates (new fields, reports)
   - Sales portal resources
   - Email templates
   - Call scripts

4. **Enablement rollout**
   - Training session schedule
   - Office hours для questions
   - Certification quiz
   - Feedback collection mechanism

**Выходные артефакты:**
```
outputs/sales-enablement/
├── training-deck.md
├── certification-program.md
├── battle-cards.md
├── discovery-guide.md
├── objection-handling.md
└── enablement-rollout-plan.md
```

### Фаза 6: Launch Execution (T-0 / Launch Day)

**Launch day orchestration:**

1. **Internal launch (T-1 day)**
   - All-hands announcement
   - Sales team rally
   - Support team briefing
   - Partner notification

2. **External launch (T-0)**
   ```
   9:00 AM: Press release goes live
   9:30 AM: Website updates published
   10:00 AM: Social media posts (coordinated)
   10:30 AM: Email announcement to customers
   11:00 AM: Blog post published
   2:00 PM: Webinar (product demo + Q&A)
   All day: Sales outreach to hot accounts
   ```

3. **Launch day monitoring**
   - Website traffic & conversion
   - Social media engagement
   - Press pickup tracking
   - Sales activity monitoring
   - Support ticket volume

**Выходные артефакты:**
```
outputs/launch-execution/
├── launch-day-runbook.md
├── communication-schedule.md
├── monitoring-dashboard.md
└── escalation-procedures.md
```

### Фаза 7: Post-Launch Analysis (T+2 weeks, T+4 weeks)

**Команда анализирует:**

1. **Launch metrics**
   - Awareness: Press mentions, social reach, website traffic
   - Engagement: Content downloads, webinar attendance, demo requests
   - Pipeline: MQLs, SQLs, opportunities created
   - Revenue: Deals closed, ARR impact

2. **Feedback synthesis**
   - Sales team feedback
   - Customer reactions (surveys, support tickets)
   - Analyst commentary
   - Competitive response

3. **Iteration recommendations**
   - Messaging refinements
   - Content gaps to fill
   - Sales enablement improvements
   - Campaign optimizations

**Выходные артефакты:**
```
outputs/post-launch/
├── launch-metrics-dashboard.md
├── feedback-synthesis.md
├── lessons-learned.md
└── iteration-recommendations.md
```

## Launch Readiness Checklist

```markdown
# Launch Readiness Checklist

## T-12 Weeks: Strategy & Planning
- [ ] Customer research completed
- [ ] Competitive analysis done
- [ ] Positioning statement finalized
- [ ] GTM strategy approved
- [ ] Budget allocated
- [ ] Timeline published

## T-8 Weeks: Content & Enablement
- [ ] Messaging framework approved
- [ ] Website copy written
- [ ] Sales deck created
- [ ] Demo script ready
- [ ] Battle cards completed
- [ ] FAQ document finalized

## T-4 Weeks: Internal Prep
- [ ] Sales training completed
- [ ] Support team briefed
- [ ] Partner communications sent
- [ ] Legal/compliance approval
- [ ] PR plan activated
- [ ] Analyst briefings scheduled

## T-2 Weeks: Final Checks
- [ ] Website staged & QA'd
- [ ] Email campaigns scheduled
- [ ] Social posts queued
- [ ] Press release approved
- [ ] Launch day runbook reviewed
- [ ] Monitoring dashboards set up

## T-0 (Launch Day)
- [ ] Press release published
- [ ] Website live
- [ ] Social media posted
- [ ] Emails sent
- [ ] Sales team activated
- [ ] Webinar delivered

## T+2 Weeks: Early Assessment
- [ ] Metrics collected
- [ ] Feedback gathered
- [ ] Quick wins documented
- [ ] Issues identified & resolved

## T+4 Weeks: Full Review
- [ ] Comprehensive analysis completed
- [ ] Lessons learned documented
- [ ] Iteration plan created
- [ ] Next phase planning started
```

## Success Metrics

### Awareness Metrics
- **Press mentions**: Target 50+ tier-1/tier-2 publications
- **Social reach**: 1M+ impressions in first week
- **Website traffic**: 50% increase in product page visits
- **Brand search**: 100% increase in branded searches

### Engagement Metrics
- **Content downloads**: 500+ in first month
- **Webinar attendance**: 200+ attendees
- **Demo requests**: 100+ in first month
- **Trial signups**: 50+ (if applicable)

### Pipeline Metrics
- **MQLs generated**: 500+ in first quarter
- **SQL conversion**: 20% MQL → SQL
- **Opportunities**: $5M+ pipeline created
- **Win rate**: Maintain or improve vs baseline

### Revenue Metrics
- **Deals closed**: $500K+ in first quarter
- **Average deal size**: 20% increase vs previous quarter
- **Sales cycle**: No increase (maintain velocity)
- **Expansion revenue**: 10% of existing customers adopt

## Использование команды

**Простой запуск:**
```bash
/launch-product
```

**Вы будете guided через интерактивный процесс:**

1. **Product context**: Ответьте на вопросы о продукте
2. **Audience definition**: Определите target personas
3. **Competitive landscape**: Укажите конкурентов
4. **Business goals**: Установите targets

**Команда затем:**
- Создаст все необходимые документы
- Сохранит их в `marketing-artifacts/launch-[product-name]/`
- Предоставит launch timeline с датами
- Создаст чеклист для tracking

**Все артефакты на русском языке в Markdown формате.**

## Примеры output

### Positioning Brief Example
```markdown
# Positioning Brief: CloudSync Pro

## Executive Summary
CloudSync Pro — enterprise-grade data synchronization platform для multi-cloud environments, позиционируемый как the fastest и most reliable solution для mission-critical data workflows.

## Target Customer
**Primary**: VP Engineering / CTO в enterprise SaaS companies (500+ employees)
**Secondary**: Data Engineering teams в финансовых сервисах

## Problem Statement
Enterprise компании struggle с real-time data consistency across multiple cloud providers (AWS, Azure, GCP), приводя к data quality issues, compliance risks, и delayed business decisions.

## Positioning Statement
For VP Engineering в enterprise companies
Who need reliable multi-cloud data synchronization
CloudSync Pro is a data orchestration platform
That guarantees sub-second data consistency across clouds
Unlike point-to-point integration tools
CloudSync Pro provides unified control plane с built-in conflict resolution

[... полный документ продолжается ...]
```

## Best Practices

### От AWS
- **Customer obsession**: Backward working от customer needs
- **Narrative-driven**: Six-page narratives before decks
- **Data-informed**: Metric-driven decision making
- **Bias for action**: Start small, iterate fast

### От Microsoft
- **Demo-driven**: Product experience > slides
- **Partner ecosystem**: Co-launch с partners
- **Enterprise focus**: Security, compliance, trust
- **Platform thinking**: How it fits broader ecosystem

### От Stripe
- **Developer-first**: Technical documentation = marketing
- **Speed to value**: "Accept payments in 7 minutes"
- **Transparent pricing**: No hidden fees
- **Quality bar**: Best-in-class execution

### От Netflix
- **Consumer obsession**: Every detail matters
- **A/B test everything**: Data-driven optimization
- **Global from day 1**: Localization built in
- **Content marketing**: Show, don't tell

---

**Команда готова помочь вам запустить продукт мирового класса.**

Run `/launch-product` чтобы начать.
