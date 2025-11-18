---
name: business-process-analysis
description: Анализ и оптимизация бизнес-процессов используя BPMN 2.0, Lean Six Sigma, value stream mapping и workflow automation. Используйте когда моделируете процессы, проводите анализ эффективности, проектируете автоматизацию или оптимизируете workflows.
---

# Business Process Analysis

## Когда использовать этот скилл

- Моделирование текущих (AS-IS) бизнес-процессов
- Проектирование оптимизированных (TO-BE) процессов
- Проведение gap analysis между текущим и желаемым состоянием
- Идентификация bottlenecks и inefficiencies
- Проектирование workflow automation
- Расчет метрик эффективности процессов (cycle time, throughput)
- Применение Lean Six Sigma для устранения waste
- Проектирование event-driven process orchestration

## Основные концепции

### BPMN 2.0 Моделирование

**Базовые элементы BPMN:**

```
СОБЫТИЯ (Events):
○ Start Event (начало процесса)
◎ End Event (завершение процесса)
⊗ Intermediate Event (событие в процессе)

АКТИВНОСТИ (Activities):
┌──────────┐
│  Task    │ Атомарная работа
└──────────┘

┌──────────┐
│    +     │ Subprocess (свернутый)
└──────────┘

ШЛЮЗЫ (Gateways):
◇  Exclusive Gateway (XOR) - один путь
◇+ Parallel Gateway (AND) - все пути параллельно
◇○ Inclusive Gateway (OR) - один или несколько путей
◇× Event-based Gateway - ожидание события

ПОТОКИ (Flows):
──→ Sequence Flow (последовательность)
- -→ Message Flow (между участниками)
⋯→ Association (комментарии, данные)

LANES (Дорожки):
┌────────────────────────┐
│  Sales Department      │  Участник процесса
├────────────────────────┤
│  Logistics Department  │
└────────────────────────┘
```

**Пример процесса Order Fulfillment:**

```
        ┌─────────────────────────────────────────────────────────────────┐
        │                    SALES DEPARTMENT                              │
        ├─────────────────────────────────────────────────────────────────┤
        │                                                                  │
Start   │   ┌────────────┐    ┌───────────┐    ┌────────────────┐        │
○──────────→│ Receive    │───→│ Validate  │───→│ Check Stock   │──┐     │
        │   │ Order      │    │ Order     │    │ Availability  │  │     │
        │   └────────────┘    └───────────┘    └────────────────┘  │     │
        │                                              │             │     │
        └──────────────────────────────────────────────┼─────────────┼─────┘
                                                       │             │
                                                  In Stock?         │
                                                    ◇──────────────┘
                                                    │ Yes      │ No
                                                    │          ↓
        ┌───────────────────────────────────────────┼─────────────────────┐
        │                    WAREHOUSE                │                    │
        ├─────────────────────────────────────────────┼─────────────────────┤
        │                                             ↓                     │
        │   ┌────────────┐    ┌───────────┐    ┌────────────┐             │
        │   │ Pick Items │───→│ Pack      │───→│ Create     │────────┐    │
        │   │            │    │ Order     │    │ Shipment   │        │    │
        │   └────────────┘    └───────────┘    └────────────┘        │    │
        │                                                              │    │
        └──────────────────────────────────────────────────────────────┼────┘
                                                                       │
        ┌──────────────────────────────────────────────────────────────┼────┐
        │                    LOGISTICS                                 │    │
        ├──────────────────────────────────────────────────────────────┼────┤
        │                                                               ↓    │
        │   ┌────────────┐    ┌───────────┐    ┌────────────┐   ○ End     │
        │   │ Schedule   │───→│ Ship      │───→│ Deliver to │───────→     │
        │   │ Delivery   │    │ Order     │    │ Customer   │             │
        │   └────────────┘    └───────────┘    └────────────┘             │
        │                                                                   │
        └───────────────────────────────────────────────────────────────────┘

МЕТРИКИ ПРОЦЕССА:
- Cycle Time: 2-5 дней (от заказа до доставки)
- Throughput: 500 заказов в день
- In-Stock Rate: 95%
- On-Time Delivery: 98%
```

### Process Metrics & KPIs

**Ключевые метрики эффективности:**

```yaml
Operational Metrics:

Cycle Time (Lead Time):
  definition: "Время от начала до конца процесса"
  formula: "End Time - Start Time"
  example: "Order fulfillment: 3 дня"
  target: "< 2 дня"
  measurement: "Process mining tools, workflow logs"

Processing Time (Touch Time):
  definition: "Фактическое время активной работы"
  formula: "Σ(Task Duration) excluding wait times"
  example: "Actual work: 4 часа из 3 дней"
  efficiency: "Processing Time / Cycle Time = 4h / 72h = 5.5%"

Wait Time:
  definition: "Время ожидания между задачами"
  formula: "Cycle Time - Processing Time"
  example: "Wait time: 68 часов"
  reduction: "Цель Lean - минимизировать wait time"

Throughput:
  definition: "Количество завершенных процессов за период"
  formula: "Completed Items / Time Period"
  example: "500 orders per day"
  target: "Increase to 750 orders per day"

Work in Progress (WIP):
  definition: "Количество активных процессов"
  formula: "Count of in-progress items"
  example: "200 orders in progress"
  constraint: "Limit WIP to improve flow (Kanban)"

Bottleneck Analysis:
  definition: "Шаг с наибольшим wait time"
  identification:
    - "Measure time at each step"
    - "Identify longest queues"
    - "Analyze resource utilization"
  example: "Quality Check - 60% of total wait time"
  solution: "Add resources or automate bottleneck"

First Time Right (FTR):
  definition: "Процент процессов без переделок"
  formula: "(Completed without rework) / Total * 100%"
  example: "85% FTR rate"
  target: "≥ 95%"
  cost_of_poor_quality: "15% rework rate = significant waste"

Process Cost:
  definition: "Общая стоимость выполнения процесса"
  components:
    labor: "Employee time * hourly rate"
    systems: "Software licenses, infrastructure"
    materials: "Physical materials consumed"
    overhead: "Facilities, management"
  example: "$45 per order processed"
  target: "Reduce to $30 per order through automation"

Automation Rate:
  definition: "Процент автоматизированных шагов"
  formula: "(Automated steps) / (Total steps) * 100%"
  example: "40% automation rate"
  target: "80% automation rate"
  roi: "Automation reduces cost and errors"
```

### Value Stream Mapping

**Создание Value Stream Map:**

```
VALUE STREAM MAP - Order Processing

┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│ Customer │      │ Sales    │      │Warehouse │      │Logistics │
│          │      │          │      │          │      │          │
└────┬─────┘      └────┬─────┘      └────┬─────┘      └────┬─────┘
     │                 │                  │                  │
Order│                 │                  │                  │
     ↓                 │                  │                  │
┌─────────────┐        │                  │                  │
│Place Order  │        │                  │                  │
│ PT: 5 min   │────────┤                  │                  │
│ WT: 0       │        │                  │                  │
└─────────────┘        │                  │                  │
                       ↓                  │                  │
                  ┌─────────────┐         │                  │
                  │Validate     │         │                  │
                  │Order        │         │                  │
                  │ PT: 10 min  │─────────┤                  │
                  │ WT: 2 hours │         │                  │
                  └─────────────┘         │                  │
                                          ↓                  │
                                    ┌─────────────┐          │
                                    │Pick & Pack  │          │
                                    │ PT: 30 min  │──────────┤
                                    │ WT: 12 hours│          │
                                    └─────────────┘          │
                                                             ↓
                                                       ┌─────────────┐
                                                       │Ship Order   │
                                                       │ PT: 15 min  │
                                                       │ WT: 24 hours│
                                                       └─────────────┘
                                                             │
                                                             ↓
                                                       Delivery

SUMMARY:
Total Processing Time (PT): 1 hour
Total Wait Time (WT): 38 hours
Total Lead Time: 39 hours

Value-Adding Time: 1 hour (2.5%)
Non-Value-Adding Time: 38 hours (97.5%)

АНАЛИЗ:
🔴 Problem: 97.5% времени = ожидание
🎯 Opportunity: Сократить wait time через:
   - Автоматизация валидации заказов
   - Real-time inventory updates
   - Batch processing для picking
   - Automated shipping label generation

УЛУЧШЕННОЕ СОСТОЯНИЕ (TO-BE):
Total Processing Time: 45 min (automation)
Total Wait Time: 4 hours (parallel processing)
Total Lead Time: 4.75 hours (87% improvement)
```

### Lean Six Sigma применение

**8 видов Waste (DOWNTIME):**

```
1. DEFECTS (Дефекты)
   Примеры:
   - Ошибки в заказах требующие переделки
   - Incorrect shipping addresses
   - Поврежденные товары
   Решение:
   - Automated validation
   - Quality checks
   - Root cause analysis (5 Whys, Fishbone)

2. OVERPRODUCTION (Перепроизводство)
   Примеры:
   - Создание отчетов, которые никто не читает
   - Избыточная документация
   Решение:
   - Pull systems (produce только по запросу)
   - Kanban для WIP limits

3. WAITING (Ожидание)
   Примеры:
   - Ожидание approval
   - Ожидание данных из другой системы
   - Queue times между шагами
   Решение:
   - Автоматизация approvals
   - Asynchronous processing
   - Real-time data integration

4. NON-UTILIZED TALENT (Неиспользованные навыки)
   Примеры:
   - Высококвалифицированные сотрудники на рутинных задачах
   - Отсутствие возможности для инноваций
   Решение:
   - Автоматизация рутины
   - Делегирование решений
   - Innovation time

5. TRANSPORTATION (Транспортировка)
   Примеры:
   - Ручная передача данных между системами
   - Email attachments вместо shared storage
   Решение:
   - System integrations (APIs)
   - Centralized data storage
   - Workflow automation

6. INVENTORY (Запасы)
   Примеры:
   - Backlog невыполненных заказов
   - Накопление незавершенной работы
   Решение:
   - Just-in-time processing
   - WIP limits
   - Flow optimization

7. MOTION (Движение)
   Примеры:
   - Переключение между множеством систем
   - Поиск информации в разных местах
   Решение:
   - Unified interfaces
   - Single source of truth
   - Process simplification

8. EXTRA PROCESSING (Избыточная обработка)
   Примеры:
   - Дублирование ввода данных
   - Излишние согласования
   - Ненужные шаги в процессе
   Решение:
   - Streamline approvals
   - Eliminate redundant steps
   - Automation

DMAIC МЕТОДОЛОГИЯ (Six Sigma):

Define (Определить):
  - Определить проблему и цели
  - Voice of Customer (VOC)
  - Project charter
  - SIPOC diagram

Measure (Измерить):
  - Собрать текущие метрики
  - Baseline performance
  - Data collection plan
  - Process capability

Analyze (Анализировать):
  - Root cause analysis
  - Fishbone diagram
  - 5 Whys
  - Pareto analysis (80/20)

Improve (Улучшить):
  - Разработать решения
  - Pilot testing
  - Risk analysis
  - Implementation plan

Control (Контролировать):
  - Monitor performance
  - Control charts
  - Standard operating procedures
  - Continuous improvement
```

### Workflow Automation Design

**Event-Driven Process Automation:**

```yaml
# AWS Step Functions State Machine для Order Processing

StateMachine: OrderFulfillment
Description: "Automated order processing workflow"

States:
  ValidateOrder:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:ValidateOrder"
    Next: CheckInventory
    Catch:
      - ErrorEquals: ["ValidationError"]
        Next: NotifyCustomerError
        ResultPath: "$.error"

  CheckInventory:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:CheckInventory"
    Next: InventoryDecision
    ResultPath: "$.inventory"

  InventoryDecision:
    Type: Choice
    Choices:
      - Variable: "$.inventory.available"
        BooleanEquals: true
        Next: ParallelProcessing
      - Variable: "$.inventory.available"
        BooleanEquals: false
        Next: BackorderProcess
    Default: NotifyCustomerError

  ParallelProcessing:
    Type: Parallel
    Branches:
      - StartAt: ProcessPayment
        States:
          ProcessPayment:
            Type: Task
            Resource: "arn:aws:lambda:us-east-1:123456:function:ProcessPayment"
            End: true

      - StartAt: ReserveInventory
        States:
          ReserveInventory:
            Type: Task
            Resource: "arn:aws:lambda:us-east-1:123456:function:ReserveInventory"
            End: true

      - StartAt: CalculateShipping
        States:
          CalculateShipping:
            Type: Task
            Resource: "arn:aws:lambda:us-east-1:123456:function:CalculateShipping"
            End: true
    Next: CreateShipment
    Catch:
      - ErrorEquals: ["PaymentFailed"]
        Next: RefundProcess

  CreateShipment:
    Type: Task
    Resource: "arn:aws:states:::sqs:sendMessage.waitForTaskToken"
    Parameters:
      QueueUrl: "https://sqs.us-east-1.amazonaws.com/123456/warehouse-queue"
      MessageBody:
        orderId.$: "$.orderId"
        taskToken.$: "$$.Task.Token"
    Next: NotifyCustomerShipped

  NotifyCustomerShipped:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:SendEmail"
    Parameters:
      template: "order-shipped"
      recipient.$: "$.customer.email"
    Next: WaitForDelivery

  WaitForDelivery:
    Type: Wait
    Seconds: 86400  # 24 часа
    Next: CheckDeliveryStatus

  CheckDeliveryStatus:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:TrackDelivery"
    Next: DeliveryDecision

  DeliveryDecision:
    Type: Choice
    Choices:
      - Variable: "$.delivery.status"
        StringEquals: "DELIVERED"
        Next: CompleteOrder
      - Variable: "$.delivery.status"
        StringEquals: "IN_TRANSIT"
        Next: WaitForDelivery
    Default: EscalateToSupport

  CompleteOrder:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:CompleteOrder"
    End: true

  BackorderProcess:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:CreateBackorder"
    Next: NotifyCustomerBackorder

  NotifyCustomerBackorder:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:SendEmail"
    Parameters:
      template: "backorder"
      recipient.$: "$.customer.email"
    End: true

  EscalateToSupport:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:CreateSupportTicket"
    End: true

  NotifyCustomerError:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:SendEmail"
    Parameters:
      template: "order-error"
      recipient.$: "$.customer.email"
    End: true

  RefundProcess:
    Type: Task
    Resource: "arn:aws:lambda:us-east-1:123456:function:ProcessRefund"
    Next: NotifyCustomerError

ПРЕИМУЩЕСТВА АВТОМАТИЗАЦИИ:
✅ Cycle time: с 39 часов → 4 часа
✅ Error rate: с 15% → 2%
✅ Cost per order: с $45 → $12
✅ Throughput: с 500 → 2000 orders/day
✅ 24/7 processing без human intervention
```

**Process Automation Patterns:**

```
1. SEQUENTIAL WORKFLOW
   A → B → C → D
   Каждый шаг ждет завершения предыдущего

2. PARALLEL WORKFLOW
        ┌→ B1 ┐
   A →  ├→ B2 ├→ D
        └→ B3 ┘
   Несколько шагов выполняются одновременно

3. CONDITIONAL WORKFLOW
        ┌→ B1 → D
   A → ◇
        └→ B2 → D
   Выбор пути на основе условий

4. EVENT-DRIVEN WORKFLOW
   A → [Wait for Event] → B → C
   Процесс ожидает внешнее событие

5. SAGA PATTERN (Distributed Transactions)
   A → B → C
   ↓   ↓   ↓
   A⁻¹ B⁻¹ C⁻¹  (Compensating transactions при failure)

6. HUMAN-IN-THE-LOOP
   A → [Manual Review] → B → C
   Критичные решения требуют human approval
```

## Справочные материалы

Для детальных примеров см. директорию `references/`:
- BPMN 2.0 templates
- Value stream mapping examples
- Lean Six Sigma toolkits
- Process automation patterns
- Workflow state machine examples
- KPI dashboards

---

**Примечание**: Методологии и паттерны основаны на практиках ведущих компаний и Lean Six Sigma стандартах.
