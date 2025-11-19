# Marketing Suite Plugin

Комплексный enterprise marketing плагин с тремя senior-level AI агентами, 12 специализированными скиллами и 3 мощными командами для Product Marketing, Growth Marketing и Account-Based Marketing.

## Обзор

Marketing Suite предоставляет экспертизу уровня AWS, Microsoft, Stripe, Netflix, Salesforce и других лидеров индустрии для:

- **Product Marketing**: Positioning, messaging, go-to-market strategy, competitive intelligence
- **Growth Marketing**: Experimentation, funnel optimization, retention tactics, PLG strategies
- **Account-Based Marketing**: Enterprise account planning, buying committee mapping, intent orchestration

## Агенты (3)

### 1. Product Marketing Manager
**Модель**: Sonnet (complex reasoning)
**Экспертиза**: Product positioning, go-to-market launches, competitive strategy

**Используйте для:**
- Создания positioning statements и messaging frameworks
- Планирования product launches (tier 1/2/3)
- Разработки competitive battle cards
- Go-to-market strategy для новых продуктов
- Sales enablement materials

**Ключевые навыки:**
- Geoffrey Moore positioning framework
- Value proposition canvas (Strategyzer)
- Win/loss analysis
- Analyst relations
- Customer advisory boards

---

### 2. Growth Marketing Strategist
**Модель**: Sonnet (experiment design)
**Экспертиза**: Data-driven growth, A/B testing, retention optimization

**Используйте для:**
- Планирования growth experiments (ICE/PIE scoring)
- Оптимизации conversion funnels
- Designing viral loops и referral programs
- Retention campaigns и re-engagement
- PLG (Product-Led Growth) tactics

**Ключевые навыки:**
- AARRR pirate metrics
- North Star Metric framework
- Statistical significance testing
- Cohort analysis
- Growth loops vs funnels

---

### 3. ABM Architect
**Модель**: Sonnet (strategic orchestration)
**Экспертиза**: Enterprise ABM campaigns, account planning, intent-based orchestration

**Используйте для:**
- Strategic account planning (1:1, 1:Few, 1:Many)
- Buying committee mapping
- Multi-threaded engagement strategies
- Intent signal orchestration
- Sales-marketing alignment

**Ключевые навыки:**
- ICP scoring models
- MEDDIC qualification
- Multi-touch attribution
- Account engagement scoring
- Executive sponsorship programs

## Скиллы (12)

### Product Marketing Skills
1. **product-positioning**: Positioning statements, value props, messaging frameworks
2. **competitive-intelligence**: Battle cards, win/loss analysis, competitive positioning
3. **gtm-planning**: Go-to-market strategy, launch tiering, channel orchestration

### Growth Marketing Skills
4. **growth-experimentation**: A/B testing, hypothesis prioritization, ICE scoring
5. **funnel-optimization**: Conversion rate optimization, friction reduction
6. **retention-tactics**: Hook model, reactivation campaigns, cohort analysis
7. **plg-tactics**: Product-led growth, freemium models, viral loops

### ABM Skills
8. **account-planning**: Strategic account plans, ICP criteria, account scoring
9. **buying-committee**: Stakeholder mapping, multi-threading, MEDDIC
10. **intent-orchestration**: Intent signals, real-time triggers, strike zone playbooks

### Cross-Functional Skills
11. **customer-marketing**: Advocacy programs, case study development, reference management
12. **revenue-attribution**: Multi-touch attribution, pipeline analysis, ROI measurement

## Команды (3)

### 1. `/launch-product`
Комплексный product launch orchestrator от positioning до post-launch analysis.

**Создает:**
- Positioning brief & messaging framework
- GTM strategy & timeline (T-12 to T+4 weeks)
- Sales enablement materials (deck, battle cards, demo scripts)
- Marketing campaigns (email, social, paid, content)
- Launch readiness checklist
- Success metrics dashboard

**Использование:**
```bash
/launch-product
```

---

### 2. `/growth-sprint`
Еженедельный growth sprint framework с experiment planning, execution и analysis.

**Создает:**
- Hypothesis backlog & ICE prioritization
- Experiment design (A/B tests, MVT)
- Metrics tracking dashboard
- Learning documentation
- Next sprint plan

**Использование:**
```bash
/growth-sprint
```

---

### 3. `/abm-campaign`
Enterprise ABM campaign orchestrator с account selection, multi-channel execution и attribution.

**Создает:**
- Account selection & tiering (ICP scoring)
- Buying committee maps
- Campaign playbooks (1:1, 1:Few, 1:Many)
- Sales-marketing alignment plans
- Performance dashboards & attribution

**Использование:**
```bash
/abm-campaign
```

## Структура плагина

```
marketing-suite/
├── agents/
│   ├── product-marketing-manager.md
│   ├── growth-marketing-strategist.md
│   └── abm-architect.md
├── commands/
│   ├── launch-product.md
│   ├── growth-sprint.md
│   └── abm-campaign.md
├── skills/
│   ├── product-positioning/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── positioning-templates.md
│   │   └── assets/
│   │       └── example-aws-positioning.md
│   ├── competitive-intelligence/
│   ├── gtm-planning/
│   ├── growth-experimentation/
│   ├── funnel-optimization/
│   ├── retention-tactics/
│   ├── plg-tactics/
│   ├── account-planning/
│   ├── buying-committee/
│   ├── intent-orchestration/
│   ├── customer-marketing/
│   └── revenue-attribution/
└── README.md (this file)
```

## Best Practices от Industry Leaders

### Product Marketing (AWS, Microsoft, Stripe)
- **AWS**: Customer obsession, backward working, six-page narratives
- **Microsoft**: Enterprise trust, ecosystem integration, vertical solutions
- **Stripe**: Developer-first, documentation as marketing, transparent pricing
- **OpenAI**: Capability-first messaging, responsible AI positioning

### Growth Marketing (Netflix, Airbnb, Dropbox)
- **Netflix**: A/B test everything, personalization, long-term metrics
- **Airbnb**: Rigorous experimentation, peer review, guardrail metrics
- **Dropbox**: Referral program (3900% growth), viral loops
- **Slack**: Bottom-up adoption, 2000 messages magic number

### ABM (Salesforce, Oracle, SAP)
- **Salesforce**: Dedicated account teams, Customer Advisory Boards
- **Oracle**: C-level engagement, long-term relationships, industry expertise
- **SAP**: Vertical specialization, partner ecosystem, strategic consulting
- **AWS**: TAM programs, Well-Architected Reviews, executive briefings

## Примеры использования

### Сценарий 1: Запуск нового SaaS продукта
```
1. Используйте Product Marketing Manager для:
   - Создания positioning & messaging
   - Разработки GTM strategy

2. Запустите /launch-product для:
   - Полного launch plan (T-12 weeks)
   - Sales enablement materials
   - Campaign orchestration

3. После запуска используйте Growth Marketing Strategist для:
   - Optimization experiments
   - Funnel analysis
   - Retention campaigns
```

### Сценарий 2: Масштабирование роста
```
1. Используйте Growth Marketing Strategist для:
   - North Star Metric определения
   - Funnel analysis и bottleneck identification

2. Запустите /growth-sprint для:
   - Weekly experimentation cadence
   - Hypothesis prioritization (ICE)
   - Results tracking & learning

3. Для enterprise accounts используйте ABM Architect для:
   - PLG to sales handoff
   - Account-based expansion
```

### Сценарий 3: Enterprise ABM program
```
1. Используйте ABM Architect для:
   - ICP definition & account scoring
   - Buying committee mapping

2. Запустите /abm-campaign для:
   - Strategic account plans
   - Multi-channel orchestration
   - Sales-marketing alignment

3. Используйте Product Marketing Manager для:
   - Account-specific messaging
   - Custom collateral (ROI analysis, case studies)
```

## Ключевые метрики

### Product Marketing Metrics
- Brand awareness (search volume, share of voice)
- Content engagement (downloads, webinar attendance)
- Pipeline influence (MQL→SQL conversion)
- Win rate & deal size impact
- Sales cycle reduction

### Growth Marketing Metrics
- North Star Metric (product-specific)
- AARRR metrics (Acquisition, Activation, Retention, Revenue, Referral)
- Experiment velocity (tests per week)
- Funnel conversion rates
- Viral coefficient (K-factor)

### ABM Metrics
- Account engagement (% of target accounts engaged)
- Buying committee coverage (multi-threading score)
- Pipeline generation ($, deal size)
- Win rate (ABM vs non-ABM)
- ROI (5:1 target)

## Требования

- **Claude Model**: Sonnet 4.5 (для всех трех агентов)
- **Token Budget**: ~5K-15K tokens per agent session
- **Output**: Все артефакты в Markdown на русском языке
- **Dependencies**: Никаких внешних зависимостей (self-contained)

## Версия

**Current Version**: 1.0.0

**Changelog:**
- v1.0.0 (2024): Initial release с 3 агентами, 12 скиллами, 3 командами

## Поддержка

При создании плагина использовались best practices от:
- AWS (Product Marketing Excellence)
- Microsoft (Enterprise GTM)
- Stripe (Developer Marketing)
- Netflix (Growth Experimentation)
- Salesforce (ABM Leadership)
- Airbnb (Data-Driven Growth)
- Slack (Product-Led Growth)
- Dropbox (Viral Growth Loops)

## Лицензия

Part of Claude Code Plugins Marketplace.

---

**Готовы создавать маркетинг мирового класса?**

Установите Marketing Suite и активируйте агентов для ваших marketing задач.
