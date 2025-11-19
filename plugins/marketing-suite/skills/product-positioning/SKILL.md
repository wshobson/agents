---
name: product-positioning
description: Экспертные навыки создания product positioning statements, value propositions и messaging frameworks уровня AWS, Microsoft, Stripe. Use when creating positioning, defining value props, or building messaging hierarchy.
---

# Product Positioning

## Когда использовать этот навык

- Создание positioning statement для нового продукта или feature
- Разработка messaging framework для marketing campaigns
- Дифференциация от конкурентов на переполненном рынке
- Адаптация позиционирования для разных segments
- Validation и refinement существующего positioning

## Ключевые концепции

### Geoffrey Moore Positioning Statement

**Формула:**
```
For [целевой клиент]
Who [описание потребности или opportunity]
Our [название продукта/категория]
That [ключевая выгода, reason to buy]
Unlike [primary competitive alternative]
Our product [statement of primary differentiation]
```

**Пример - Stripe:**
```
For internet businesses
Who need to accept payments online
Stripe is a payment infrastructure platform
That makes it easy to start accepting payments in minutes
Unlike legacy payment processors with complex onboarding
Stripe provides a developer-first API and instant activation
```

### Value Proposition Canvas (Strategyzer)

**Customer Profile:**
- **Jobs to be Done**: Функциональные, социальные, эмоциональные
- **Pains**: Препятствия, риски, нежелательные outcomes
- **Gains**: Ожидаемые, желаемые, неожиданные benefits

**Value Map:**
- **Products & Services**: Что вы предлагаете
- **Pain Relievers**: Как вы устраняете боли
- **Gain Creators**: Как вы создаете value

**Fit = Pain Relievers + Gain Creators решают главные Jobs/Pains/Gains**

### Messaging Hierarchy

**Уровень 1: Core Positioning (1 предложение)**
- Самое важное утверждение о продукте
- Пример (AWS): "The world's most comprehensive and broadly adopted cloud platform"

**Уровень 2: Value Pillars (3-5 преимуществ)**
- Ключевые reasons to believe
- Пример (AWS): Breadth of services, Global infrastructure, Security, Innovation speed, Partner ecosystem

**Уровень 3: Proof Points (данные и факты)**
- Конкретные метрики, кейсы, testimonials
- Пример (AWS): 200+ services, 25+ regions, 99.99% SLA, Fortune 500 customers

**Уровень 4: Use Cases & Stories**
- Конкретные сценарии применения
- Индустриальные examples
- Customer success stories

### Аудиторная адаптация

**Technical Buyer (CTO, VP Engineering):**
```
Focus: Архитектура, масштабируемость, интеграции
Language: Technical depth, API-first, performance metrics
Proof: Technical docs, architecture diagrams, benchmarks
```

**Business Buyer (CEO, CFO):**
```
Focus: ROI, risk mitigation, strategic value
Language: Business outcomes, cost savings, competitive advantage
Proof: ROI calculators, analyst reports, business cases
```

**Champion (Director, Manager):**
```
Focus: Team productivity, ease of adoption, career impact
Language: Time savings, best practices, industry leadership
Proof: Peer testimonials, implementation guides, success metrics
```

## Шаблоны и примеры

### Шаблон 1: Positioning Brief

```markdown
# Product Positioning Brief: [Product Name]

## Executive Summary
[2-3 предложения о позиционировании]

## Target Customer
- **Primary**: [Role, industry, company size]
- **Secondary**: [Additional segments]

## Problem Statement
[Какую проблему решаем? Почему это важно сейчас?]

## Positioning Statement
For [target]
Who [need]
[Product] is [category]
That [benefit]
Unlike [alternatives]
Our product [differentiation]

## Value Pillars
1. **[Pillar 1]**: [Описание]
   - Proof point: [Данные]
2. **[Pillar 2]**: [Описание]
   - Proof point: [Данные]
3. **[Pillar 3]**: [Описание]
   - Proof point: [Данные]

## Competitive Differentiation
| Criteria | Us | Competitor A | Competitor B |
|----------|----|--------------| -------------|
| [Factor] | ✓  | ✗            | ✓            |

## Key Messages by Audience
- **Technical**: [Message]
- **Business**: [Message]
- **Champion**: [Message]

## Supporting Evidence
- Customer quotes
- Case studies
- Analyst validation
```

### Шаблон 2: Messaging Framework

```markdown
# Messaging Framework: [Product/Campaign]

## Core Positioning
[Одно предложение - elevator pitch]

## Value Proposition
[2-3 предложения о ключевой ценности]

## Messaging Pillars

### Pillar 1: [Name]
**Headline**: [Customer-facing message]
**Benefit**: [What customer gets]
**Features**: [Supporting capabilities]
**Proof**: [Data, testimonials, case studies]

### Pillar 2: [Name]
[Same structure]

### Pillar 3: [Name]
[Same structure]

## Audience-Specific Messages

### For Technical Buyers
**Message**: [Technical value prop]
**Talk Track**: [Detailed explanation]
**Objection Handling**: [Common concerns + responses]

### For Business Buyers
**Message**: [Business value prop]
**Talk Track**: [ROI-focused explanation]
**Objection Handling**: [Budget/risk concerns + responses]

## Competitive Positioning
**vs [Competitor A]**: [Differentiation message]
**vs [Competitor B]**: [Differentiation message]

## Proof Points & Social Proof
- [Customer logo/testimonial]
- [Metric/achievement]
- [Award/recognition]
```

## Best Practices от лидеров

### AWS Positioning Approach
- **Customer obsession**: Start with customer problem
- **Backwards working**: Begin with press release, work backwards
- **Six-page narratives**: Deep context over PowerPoint
- **Leadership principles**: Embed в messaging

### Stripe Positioning Approach
- **Developer-first**: Technical audience as primary
- **Simplicity**: "Payments infrastructure for the internet"
- **Time-to-value**: "Accept payments in minutes"
- **Innovation showcase**: Highlight cutting-edge use cases

### Microsoft Enterprise Positioning
- **Trust & security**: Enterprise-grade compliance
- **Integration ecosystem**: Works with existing tools
- **Digital transformation**: Strategic business outcomes
- **Vertical solutions**: Industry-specific messaging

### Salesforce Positioning Tactics
- **Trailblazer narrative**: Customer success stories
- **Platform approach**: Ecosystem > product
- **Innovation leadership**: AI-first messaging (Einstein)
- **Community building**: Ohana culture в messaging

## Процесс создания Positioning

### Фаза 1: Исследование (2 недели)
1. **Customer interviews** (5-10 глубинных)
   - Jobs to be Done questions
   - Current alternatives
   - Decision criteria

2. **Win/Loss analysis** (20-30 deals)
   - Why did we win?
   - Why did we lose?
   - Competitor positioning

3. **Market research**
   - Gartner/Forrester reports
   - G2/Capterra reviews
   - Competitor messaging audit

### Фаза 2: Synthesis (1 неделя)
1. **Identify patterns**: Common themes в customer feedback
2. **Draft positioning**: Multiple versions
3. **Stakeholder input**: Product, Sales, CS feedback
4. **Refinement**: Iterate на основе input

### Фаза 3: Validation (1-2 недели)
1. **Message testing**: Wynter, UserTesting с target audience
2. **A/B test messaging**: Landing pages, emails
3. **Sales validation**: Use в real conversations
4. **Customer advisory board**: Present для feedback

### Фаза 4: Rollout (2 недели)
1. **Sales enablement**: Training sessions, talk tracks
2. **Marketing alignment**: Update всех materials
3. **Website updates**: New messaging live
4. **Content strategy**: Plan supporting content

## Метрики успеха Positioning

**Awareness Metrics:**
- Brand search volume change
- Share of voice vs competitors
- Message recall in surveys

**Consideration Metrics:**
- Website engagement (time on site, pages viewed)
- Content download rate
- Demo/trial request rate

**Conversion Metrics:**
- Win rate improvement
- Sales cycle reduction
- Average deal size increase

**Adoption Metrics:**
- Feature adoption rate
- Customer satisfaction (NPS)
- Renewal/retention rate

## Распространенные ошибки

❌ **Ошибка**: Feature-focused positioning ("We have X, Y, Z features")
✅ **Правильно**: Benefit-focused ("You can achieve A, B, C outcomes")

❌ **Ошибка**: Универсальное positioning для всех
✅ **Правильно**: Segmented messaging для разных audiences

❌ **Ошибка**: "Best" или "leading" без доказательств
✅ **Правильно**: Конкретные differentiators с proof points

❌ **Ошибка**: Игнорирование конкурентов
✅ **Правильно**: Explicit differentiation от alternatives

❌ **Ошибка**: Positioning "set and forget"
✅ **Правильно**: Continuous iteration на основе feedback

## Дополнительные ресурсы

См. `references/` для:
- Positioning templates от топ-компаний
- Message testing questionnaires
- Win/loss interview scripts
- Competitive positioning maps

См. `assets/` для:
- Positioning brief examples (AWS, Stripe, Microsoft)
- Messaging framework templates
- Value proposition canvas worksheets
