---
name: requirements-engineering
description: Advanced requirements engineering practices for enterprise systems including elicitation, analysis, specification, validation, and management. Use when gathering requirements, writing specifications, conducting stakeholder workshops, or creating requirements traceability.
---

# Requirements Engineering for Enterprise Systems

## When to Use This Skill

- Gathering and documenting business or technical requirements
- Conducting stakeholder workshops and interviews
- Creating functional and non-functional specifications
- Writing user stories with acceptance criteria
- Building requirements traceability matrices
- Validating requirements with stakeholders
- Managing requirements changes and versions
- Analyzing gaps between current and future state

## Core Concepts

### Requirements Elicitation Techniques

#### Stakeholder Interviews
**Структурированный подход к интервью:**

```
ПОДГОТОВКА:
1. Изучить бизнес-контекст и текущие системы
2. Определить цели интервью и ключевые вопросы
3. Подготовить шаблон для записи ответов
4. Запланировать 60-90 минут с каждым стейкхолдером

ВОПРОСЫ ДЛЯ БИЗНЕС-СТЕЙКХОЛДЕРОВ:
- Какие бизнес-цели должна достичь система?
- Какие метрики успеха вы определили?
- Какие процессы сегодня неэффективны?
- Какие ограничения по бюджету/срокам?
- Кто будет основными пользователями системы?

ВОПРОСЫ ДЛЯ ТЕХНИЧЕСКИХ СТЕЙКХОЛДЕРОВ:
- Какие технические ограничения существуют?
- С какими системами требуется интеграция?
- Какие нефункциональные требования критичны?
- Какие существуют стандарты и политики?
- Какова текущая архитектура и технический долг?

ФИКСАЦИЯ РЕЗУЛЬТАТОВ:
- Записывать дословные цитаты для критичных требований
- Фиксировать бизнес-обоснование (WHY, не только WHAT)
- Отмечать конфликты и неопределенности
- Определить приоритеты требований
```

#### Facilitated Workshops
**Формат проведения воркшопов:**

```
ТИПЫ ВОРКШОПОВ:

1. Discovery Workshop (2-4 часа)
   Цель: Определить границы системы и ключевые требования
   Участники: Бизнес-владельцы, архитекторы, ключевые пользователи
   Активности:
   - Определение целей и успешных исходов
   - Mapping пользовательских путей (user journeys)
   - Идентификация ключевых сценариев использования
   - Определение ограничений и рисков

2. Process Modeling Workshop (4-6 часов)
   Цель: Задокументировать AS-IS и спроектировать TO-BE процессы
   Участники: Process owners, пользователи, аналитики
   Активности:
   - Визуализация текущих процессов (BPMN)
   - Выявление pain points и bottlenecks
   - Проектирование оптимизированных процессов
   - Определение точек автоматизации

3. Requirements Prioritization Workshop (2-3 часа)
   Цель: Приоритизация требований и определение MVP
   Участники: Product owners, бизнес-стейкхолдеры, архитекторы
   Активности:
   - MoSCoW приоритизация (Must/Should/Could/Won't)
   - Weighted scoring по бизнес-ценности и сложности
   - Определение фаз внедрения
   - ROI анализ для ключевых функций

ИНСТРУМЕНТЫ ДЛЯ ВОРКШОПОВ:
- Виртуальные доски: Miro, Mural, FigJam
- Real-time collaboration: Google Docs, Confluence
- Диаграммы: Lucidchart, draw.io, PlantUML
- Голосования и опросы: Slido, Mentimeter
```

#### Document Analysis
**Анализ существующей документации:**

```
ИСТОЧНИКИ ДОКУМЕНТАЦИИ:
✓ Техническая документация текущих систем
✓ Бизнес-процессы и стандартные операционные процедуры (SOP)
✓ Отчеты об инцидентах и проблемах
✓ Аналитика использования систем
✓ Результаты пользовательских опросов
✓ Регуляторные требования и compliance документы

МЕТОД ИЗВЛЕЧЕНИЯ ТРЕБОВАНИЙ:
1. Cataloging: Создать инвентарь всех документов
2. Gap Analysis: Сравнить with желаемым состоянием
3. Implicit Requirements: Извлечь неявные требования
4. Validation: Подтвердить актуальность с стейкхолдерами
5. Traceability: Связать требования с источниками
```

### Requirements Specification

#### Functional Requirements

**Формат User Story (Agile):**
```
Как <роль пользователя>
Я хочу <функциональность>
Чтобы <бизнес-ценность>

Acceptance Criteria (Given-When-Then):
GIVEN <начальное состояние>
WHEN <действие пользователя>
THEN <ожидаемый результат>

Пример:
Как менеджер по продажам
Я хочу фильтровать лиды по источнику и статусу
Чтобы фокусироваться на наиболее перспективных возможностях

Acceptance Criteria:
GIVEN я нахожусь на странице списка лидов
WHEN я выбираю источник "Web Form" и статус "Qualified"
THEN отображаются только лиды, соответствующие обоим фильтрам
AND счетчик показывает количество отфильтрованных результатов
AND я могу экспортировать отфильтрованный список в CSV

Non-functional Requirements:
- Фильтрация должна отрабатывать < 500ms для 10,000 лидов
- Поддерживать до 5 одновременных фильтров
- Сохранять последние использованные фильтры
```

**Формат Use Case (Traditional):**
```
UC-001: Создание нового заказа клиента

Primary Actor: Менеджер по продажам
Preconditions:
- Пользователь аутентифицирован
- Клиент существует в системе
- Доступны товары в каталоге

Main Success Scenario:
1. Менеджер выбирает "Создать заказ"
2. Система отображает форму создания заказа
3. Менеджер выбирает клиента из списка
4. Менеджер добавляет товары в заказ
5. Система рассчитывает итоговую сумму с учетом скидок
6. Менеджер подтверждает заказ
7. Система создает заказ и отправляет уведомление клиенту
8. Система отображает номер созданного заказа

Extensions (Alternative Flows):
3a. Клиент не найден в системе
    3a1. Менеджер создает нового клиента
    3a2. Система сохраняет клиента
    3a3. Continue from step 4

4a. Товар отсутствует на складе
    4a1. Система отображает предупреждение
    4a2. Система предлагает альтернативные товары
    4a3. Менеджер выбирает альтернативу или продолжает

Postconditions:
- Заказ создан в статусе "Pending"
- Клиент получил email с подтверждением
- Товары зарезервированы на складе
- Создана задача для отдела логистики

Business Rules:
- BR-001: Скидка применяется автоматически при заказе > $1000
- BR-002: Оплата требуется в течение 30 дней
- BR-003: Минимальная сумма заказа - $100

Frequency: 500-1000 раз в день
Performance: Создание заказа должно занимать < 3 секунд
```

#### Non-Functional Requirements (NFRs)

**Категории NFR с примерами:**

```yaml
Performance Requirements:
  - id: NFR-PERF-001
    category: Response Time
    requirement: "API endpoints должны отвечать < 200ms для p95 запросов"
    measurement: "CloudWatch metrics, percentile aggregation"
    priority: Must Have

  - id: NFR-PERF-002
    category: Throughput
    requirement: "Система должна обрабатывать 10,000 RPS в пиковые часы"
    measurement: "Load testing с Gatling/JMeter, production metrics"
    priority: Must Have

  - id: NFR-PERF-003
    category: Database Query
    requirement: "Все database queries < 100ms execution time"
    measurement: "Query performance monitoring, slow query log"
    priority: Should Have

Scalability Requirements:
  - id: NFR-SCALE-001
    category: Horizontal Scaling
    requirement: "Поддержка auto-scaling от 2 до 50 instances"
    measurement: "Load testing, production monitoring"
    priority: Must Have

  - id: NFR-SCALE-002
    category: Data Volume
    requirement: "Поддержка до 100M записей в основных таблицах"
    measurement: "Database performance testing"
    priority: Must Have

Availability Requirements:
  - id: NFR-AVAIL-001
    category: Uptime SLA
    requirement: "99.95% uptime (≈22 минуты downtime в месяц)"
    measurement: "Uptime monitoring (Pingdom, StatusPage)"
    priority: Must Have

  - id: NFR-AVAIL-002
    category: Disaster Recovery
    requirement: "RTO = 4 часа, RPO = 15 минут"
    measurement: "DR testing quarterly"
    priority: Must Have

  - id: NFR-AVAIL-003
    category: Multi-Region
    requirement: "Active-passive deployment в 2 регионах"
    measurement: "Failover testing monthly"
    priority: Should Have

Security Requirements:
  - id: NFR-SEC-001
    category: Authentication
    requirement: "Multi-factor authentication для всех пользователей"
    measurement: "Security audit, penetration testing"
    priority: Must Have

  - id: NFR-SEC-002
    category: Authorization
    requirement: "Role-Based Access Control с принципом least privilege"
    measurement: "Access review quarterly"
    priority: Must Have

  - id: NFR-SEC-003
    category: Encryption
    requirement: "AES-256 encryption at rest, TLS 1.3 in transit"
    measurement: "Security scanning, compliance audit"
    priority: Must Have

  - id: NFR-SEC-004
    category: Audit Logging
    requirement: "Логирование всех изменений данных и доступа"
    measurement: "Log analysis, compliance reports"
    priority: Must Have

Compliance Requirements:
  - id: NFR-COMP-001
    category: GDPR
    requirement: "Данные EU пользователей хранятся в EU регионах"
    measurement: "Data residency audit"
    priority: Must Have

  - id: NFR-COMP-002
    category: SOC 2
    requirement: "Соответствие SOC 2 Type II controls"
    measurement: "Annual SOC 2 audit"
    priority: Must Have

  - id: NFR-COMP-003
    category: Data Retention
    requirement: "Хранение audit logs минимум 7 лет"
    measurement: "Retention policy enforcement"
    priority: Must Have

Usability Requirements:
  - id: NFR-USA-001
    category: Accessibility
    requirement: "WCAG 2.1 Level AA compliance"
    measurement: "Automated testing + manual audit"
    priority: Must Have

  - id: NFR-USA-002
    category: Browser Support
    requirement: "Поддержка Chrome, Firefox, Safari, Edge (последние 2 версии)"
    measurement: "Cross-browser testing"
    priority: Must Have

  - id: NFR-USA-003
    category: Mobile Support
    requirement: "Responsive design для tablets и mobile devices"
    measurement: "Device testing, responsive testing"
    priority: Should Have

Maintainability Requirements:
  - id: NFR-MAINT-001
    category: Code Quality
    requirement: "Test coverage ≥ 80% для критичного кода"
    measurement: "Code coverage tools (Istanbul, JaCoCo)"
    priority: Should Have

  - id: NFR-MAINT-002
    category: Documentation
    requirement: "API documentation с OpenAPI 3.0"
    measurement: "Documentation review"
    priority: Must Have

  - id: NFR-MAINT-003
    category: Deployment
    requirement: "Zero-downtime deployments с blue-green strategy"
    measurement: "Deployment process validation"
    priority: Should Have
```

### Requirements Traceability Matrix (RTM)

**Структура RTM:**

```
RTM связывает:
Business Need → Requirement → Design → Implementation → Test Case

Пример RTM в табличном формате:

| Req ID | Business Need | Requirement | Design Component | Implementation | Test Cases | Status |
|--------|---------------|-------------|------------------|----------------|------------|---------|
| BR-001 | Увеличить конверсию на 15% | Пользователь может сохранять фильтры | FilterService, UserPreferences API | PR#1234 | TC-001, TC-002 | ✅ Done |
| BR-002 | Сократить время обработки заказов на 30% | Автоматическая валидация заказов | OrderValidationEngine | PR#1256 | TC-010, TC-011, TC-012 | 🚧 In Progress |
| BR-003 | Compliance с GDPR | Пользователь может удалить свои данные | GDPR DataDeletionService | PR#1289 | TC-020, TC-021 | ⏳ Planned |

ИНСТРУМЕНТЫ ДЛЯ RTM:
- Jira: Requirements + Epics + Stories + Test Cases
- Azure DevOps: Work Items с traceability links
- Confluence: Documentation с таблицами и links
- Специализированные: IBM DOORS, Jama Connect, Modern Requirements
```

### Requirements Validation & Verification

**Техники валидации:**

```
1. PEER REVIEW
   - Технический review с архитекторами и инженерами
   - Бизнес review со stakeholders
   - Checklist: Полнота, корректность, реалистичность, тестируемость

2. PROTOTYPING
   - Low-fidelity: Wireframes (Figma, Sketch, Balsamiq)
   - High-fidelity: Interactive prototypes (InVision, Axure)
   - Code prototype для технически сложных решений

3. WALKTHROUGH С ПОЛЬЗОВАТЕЛЯМИ
   - Демонстрация прототипов end users
   - Сбор обратной связи по usability и completeness
   - Валидация user journeys

4. AUTOMATED VALIDATION
   - Consistency checking (терминология, naming)
   - Completeness checking (все use cases покрыты)
   - Conflict detection (противоречивые требования)

КРИТЕРИИ КАЧЕСТВА ТРЕБОВАНИЙ (SMART):
✓ Specific: Конкретное и недвусмысленное
✓ Measurable: Измеримое и тестируемое
✓ Achievable: Технически реализуемое
✓ Relevant: Связано с бизнес-целями
✓ Time-bound: С определенными сроками
```

### Requirements Management

**Управление изменениями:**

```
ПРОЦЕСС CHANGE MANAGEMENT:

1. Change Request Submission
   - Источник: Stakeholder, User Feedback, Technical Discovery
   - Форма: Change Request Form с обоснованием
   - Информация: Impact analysis, affected components, effort estimate

2. Impact Analysis
   - Анализ влияния на:
     * Другие requirements
     * Архитектуру и дизайн
     * Существующий код
     * Тестовые сценарии
     * Документацию
     * Сроки и бюджет

3. Change Approval
   - Review board: Product Owner, Architect, Tech Lead
   - Критерии решения: Business value, Technical feasibility, Cost vs Benefit
   - Результаты: Approved / Rejected / Deferred

4. Requirements Update
   - Обновить спецификацию requirements
   - Обновить RTM
   - Коммуницировать изменения всей команде
   - Версионирование документов

5. Implementation Tracking
   - Связать с implementation tasks (Jira tickets)
   - Отслеживать прогресс
   - Валидировать через testing

ВЕРСИОНИРОВАНИЕ REQUIREMENTS:
- Major version (1.0 → 2.0): Significant scope change
- Minor version (1.0 → 1.1): New requirements added
- Patch version (1.0.0 → 1.0.1): Clarifications, typo fixes
- Использовать Git для version control документации
```

## Advanced Patterns

### API Contract Requirements

**Спецификация API требований:**

```yaml
# OpenAPI-based Requirements Specification
/orders:
  post:
    summary: "Create new customer order"
    operationId: createOrder

    # Functional Requirements
    requirements:
      - id: FR-API-001
        description: "Accept order with customer ID, line items, shipping address"
        priority: Must Have
      - id: FR-API-002
        description: "Validate customer exists before order creation"
        priority: Must Have
      - id: FR-API-003
        description: "Calculate total including taxes and discounts"
        priority: Must Have

    # Non-Functional Requirements
    performance:
      - responseTime: "< 500ms for p95"
      - throughput: "1000 requests/second"

    security:
      - authentication: "OAuth 2.0 Bearer token"
      - authorization: "roles: [sales_manager, customer_service]"
      - rateLimiting: "100 requests/minute per API key"

    errorHandling:
      - 400: "Invalid request body (validation errors)"
      - 401: "Unauthorized (missing/invalid token)"
      - 403: "Forbidden (insufficient permissions)"
      - 404: "Customer not found"
      - 409: "Duplicate order (idempotency conflict)"
      - 422: "Business rule violation (e.g., items out of stock)"
      - 500: "Internal server error"
      - 503: "Service temporarily unavailable"

    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateOrderRequest'
          examples:
            standardOrder:
              summary: "Standard order example"
              value:
                customerId: "cust_123456"
                lineItems:
                  - productId: "prod_789"
                    quantity: 2
                    unitPrice: 99.99
                shippingAddress:
                  street: "123 Main St"
                  city: "San Francisco"
                  state: "CA"
                  zipCode: "94105"
                  country: "US"

    responses:
      '201':
        description: "Order created successfully"
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
        headers:
          Location:
            description: "URL of created order"
            schema:
              type: string
              format: uri
```

### Data Requirements Specification

**Спецификация требований к данным:**

```yaml
Entity: Customer

Business Rules:
  - BR-CUST-001: "Email должен быть уникальным в системе"
  - BR-CUST-002: "Клиент может иметь несколько shipping addresses"
  - BR-CUST-003: "После создания 10 заказов клиент получает статус 'Premium'"
  - BR-CUST-004: "Данные клиента должны храниться 7 лет после последней транзакции"

Attributes:
  id:
    type: UUID
    constraints: Primary Key, Auto-generated
    description: "Уникальный идентификатор клиента"

  email:
    type: String (255)
    constraints: Unique, Not Null, Email Format
    description: "Email адрес для логина и коммуникации"
    requirements:
      - "Валидация по RFC 5322"
      - "Case-insensitive уникальность"
      - "Маскирование в логах (GDPR)"

  firstName:
    type: String (100)
    constraints: Not Null
    description: "Имя клиента"
    requirements:
      - "Поддержка Unicode (международные имена)"
      - "Trim whitespace"

  lastName:
    type: String (100)
    constraints: Not Null
    description: "Фамилия клиента"

  phone:
    type: String (20)
    constraints: Nullable
    format: "E.164 international format"
    description: "Контактный телефон"
    requirements:
      - "Валидация по E.164"
      - "Маскирование в UI (показывать последние 4 цифры)"

  status:
    type: Enum
    values: [Active, Inactive, Suspended, Premium]
    default: Active
    description: "Текущий статус клиента"

  createdAt:
    type: Timestamp
    constraints: Not Null, Auto-generated
    description: "Дата и время создания записи"

  updatedAt:
    type: Timestamp
    constraints: Auto-updated on change
    description: "Дата и время последнего обновления"

Relationships:
  - name: addresses
    type: One-to-Many
    target: Address
    cascadeDelete: true
    description: "Shipping и billing addresses клиента"

  - name: orders
    type: One-to-Many
    target: Order
    cascadeDelete: false
    description: "История заказов клиента"

Indexes:
  - name: idx_customer_email
    fields: [email]
    type: Unique
    description: "Для быстрого поиска по email при логине"

  - name: idx_customer_status
    fields: [status]
    type: Non-unique
    description: "Для фильтрации клиентов по статусу"

  - name: idx_customer_created
    fields: [createdAt]
    type: Non-unique
    description: "Для отчетов по датам регистрации"

Data Quality Requirements:
  - "Дедупликация клиентов по email + phone"
  - "Automated data validation при создании/обновлении"
  - "Data cleansing: trim whitespace, normalize phone numbers"
  - "Monitoring для data integrity (orphaned records)"

Privacy & Compliance:
  - GDPR:
      - "Право на удаление (Right to Erasure)"
      - "Право на портабельность данных (Data Portability)"
      - "Маскирование PII в логах и backups"
      - "Encryption at rest (AES-256)"

  - Audit:
      - "Логирование всех изменений в audit log"
      - "Retention: 7 лет"
      - "Включать: user, timestamp, old value, new value"
```

## References

### Requirements Documentation Templates
- Business Requirements Document (BRD)
- Functional Specification Document (FSD)
- System Requirements Specification (SRS)
- Use Case Templates
- User Story Templates
- NFR Specification Templates
- API Requirements Templates

### Industry Standards
- IEEE 830: Software Requirements Specification
- IIBA BABOK: Business Analysis Body of Knowledge
- ISO/IEC 25010: Software Quality Requirements and Evaluation
- IREB: International Requirements Engineering Board

### Tools & Techniques
- BABOK Techniques Guide
- Requirements Elicitation Techniques
- MoSCoW Prioritization Guide
- Weighted Scoring Models
- Kano Model for Feature Prioritization

---

**Примечание**: Все примеры и шаблоны адаптированы под практики ведущих компаний (AWS, Azure, Google Cloud, Stripe, MongoDB, SAP, Oracle, Microsoft) и готовы к использованию в enterprise-проектах.
