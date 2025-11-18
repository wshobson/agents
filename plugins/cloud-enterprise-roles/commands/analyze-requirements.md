---
name: analyze-requirements
description: Автоматизированный анализ бизнес-требований с созданием BRD, функциональных спецификаций и user stories.
---

# Analyze Requirements

Эта команда помогает провести полный цикл анализа требований для enterprise-проекта.

## Что делает команда

1. Собирает информацию о проекте через интерактивные вопросы
2. Создает Business Requirements Document (BRD)
3. Генерирует функциональные спецификации
4. Создает user stories с acceptance criteria
5. Строит requirements traceability matrix

## Использование

```bash
/analyze-requirements
```

Команда запросит следующую информацию:

- **Название проекта**: Как называется проект?
- **Бизнес-цели**: Какие ключевые цели должна достичь система?
- **Stakeholders**: Кто основные stakeholders?
- **User personas**: Кто будут пользователи системы?
- **Key features**: Какие основные функции требуются?
- **NFRs**: Какие нефункциональные требования критичны?
- **Constraints**: Есть ли ограничения (бюджет, сроки, технологии)?

## Выходные документы

Команда создаст следующие файлы в директории `requirements/`:

```
requirements/
├── BRD.md                    # Business Requirements Document
├── FRD.md                    # Functional Requirements Document
├── user-stories/             # User stories по feature
│   ├── authentication.md
│   ├── orders.md
│   └── reporting.md
├── data-models/              # Концептуальные data models
│   └── erd.mmd              # Mermaid ER diagram
├── process-flows/            # BPMN диаграммы процессов
│   └── order-fulfillment.md
└── RTM.md                    # Requirements Traceability Matrix
```

## Пример вывода

### Business Requirements Document

```markdown
# Business Requirements Document: E-Commerce Platform

## Executive Summary

Разработка cloud-native e-commerce платформы для увеличения online продаж на 200% в течение 12 месяцев.

## Business Objectives

1. **Увеличить конверсию**: С 2% до 5% через improved UX
2. **Расширить рынок**: Поддержка multi-currency и internationalization
3. **Снизить операционные затраты**: Автоматизация 80% manual processes

## Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Monthly Orders | 10,000 | 30,000 | 12 months |
| Conversion Rate | 2% | 5% | 6 months |
| Cart Abandonment | 70% | 40% | 6 months |
| Customer Satisfaction | 3.5/5 | 4.5/5 | 12 months |

[...]
```

### User Stories

```markdown
# User Story: Guest Checkout

**As a** guest customer
**I want to** checkout without creating an account
**So that** I can complete my purchase quickly

## Acceptance Criteria

```gherkin
Given I have items in my cart
When I proceed to checkout
Then I should see an option to checkout as guest

Given I choose guest checkout
When I enter shipping and payment details
Then my order should be created successfully
And I should receive an order confirmation email
```

## Non-Functional Requirements

- Checkout flow должен занимать < 60 секунд
- Support для 99.9% uptime
- PCI-DSS compliance для payment processing

## Business Value

- Reduce cart abandonment by 15%
- Increase conversion rate by capturing impulse buyers
- Estimated revenue impact: $500K annually

[...]
```

## Интеграция с tools

Команда автоматически:
- Создает Jira epics и stories (если настроено)
- Генерирует диаграммы в Mermaid format
- Экспортирует в Confluence (опционально)

## Следующие шаги

После выполнения команды:

1. Review BRD с business stakeholders
2. Validate user stories с product owner
3. Technical review с architecture team
4. Prioritize requirements используя MoSCoW
5. Proceed to `/design-architecture` для технического дизайна
