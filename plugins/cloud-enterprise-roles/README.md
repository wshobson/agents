# Cloud Enterprise Roles Plugin

Профессиональные агенты, скиллы и команды для enterprise-ролей уровня senior специалистов из ведущих компаний (AWS, Azure, Google Cloud, Microsoft, SAP, Oracle, Stripe, MongoDB, OpenAI).

## Обзор

Этот плагин предоставляет экспертные возможности для трех ключевых enterprise-ролей:

### 🔍 **Systems Analyst** (Системный аналитик)
Экспертиза в сборе и анализе требований, проектировании процессов и data modeling для cloud-native систем.

**Основные возможности:**
- Requirements engineering (функциональные и нефункциональные требования)
- Business process modeling (BPMN 2.0, workflow automation)
- Enterprise data modeling (концептуальное, логическое, физическое)
- System integration design (API-first, event-driven)
- Gap analysis и technical feasibility assessment
- Requirements traceability matrix (RTM)

**Экспертиза:**
- Методологии: BABOK, IEEE 830, Lean Six Sigma
- Инструменты: Jira, Azure DevOps, Confluence
- Паттерны: Use cases, user stories (Given-When-Then), BPMN
- Платформы: AWS, Azure, GCP service integration

### 🏗️ **Systems Architect** (Системный архитектор)
Principal-level архитектор для проектирования cloud-native, distributed и secure enterprise систем.

**Основные возможности:**
- Cloud-native architecture (microservices, serverless, containers)
- Distributed systems design (CAP theorem, consensus algorithms, replication)
- Security architecture (zero trust, defense in depth, compliance)
- Multi-cloud и hybrid cloud strategies
- Performance optimization и cost optimization
- Architecture Decision Records (ADRs)

**Экспертиза:**
- Паттерны: Microservices, event-driven, CQRS, Saga pattern
- Платформы: AWS, Azure, GCP managed services
- Безопасность: GDPR, SOC 2, HIPAA, PCI-DSS compliance
- Frameworks: AWS Well-Architected, Azure Well-Architected Framework

### 📝 **Technical Writer** (Технический писатель)
Principal-level писатель для создания world-class API documentation и developer experience.

**Основные возможности:**
- API documentation excellence (REST, GraphQL, gRPC)
- OpenAPI/Swagger specifications
- Docs-as-code workflows (CI/CD, static site generators)
- Developer experience optimization (interactive docs, code playgrounds)
- Multi-language code examples (Python, JavaScript, Go, Java, C#)
- Documentation analytics и continuous improvement

**Экспертиза:**
- Инструменты: Docusaurus, MkDocs, Hugo, Swagger UI, Redoc
- Паттерны: Getting started guides, tutorials, API references
- Качество: Vale style guide enforcement, link validation, spell checking
- DX: Interactive API explorers, code examples testing

## Структура плагина

```
cloud-enterprise-roles/
├── agents/                           # 3 специализированных агента
│   ├── systems-analyst.md           # Requirements, processes, data models
│   ├── systems-architect.md         # Architecture, distributed systems, security
│   └── technical-writer.md          # API docs, tutorials, developer experience
│
├── skills/                           # 9 продвинутых скиллов
│   ├── requirements-engineering/     # Requirements elicitation, validation, RTM
│   ├── enterprise-data-modeling/     # Conceptual, logical, physical modeling
│   ├── business-process-analysis/    # BPMN, Lean Six Sigma, automation
│   ├── cloud-architecture-patterns/  # Microservices, serverless, containers
│   ├── distributed-systems-design/   # CAP, consensus, replication
│   ├── security-architecture/        # Zero trust, compliance, threat modeling
│   ├── api-documentation-excellence/ # OpenAPI, code examples, error docs
│   ├── docs-as-code-workflows/       # CI/CD, static site generators
│   └── developer-experience-optimization/ # Interactive docs, DX optimization
│
└── commands/                         # 3 автоматизированные команды
    ├── analyze-requirements.md       # BRD, FRD, user stories generation
    ├── design-architecture.md        # Architecture diagrams, ADRs, tech stack
    └── create-api-docs.md            # OpenAPI specs, code examples, guides
```

## Агенты

### systems-analyst
```yaml
model: sonnet
description: Senior systems analyst специализирующийся на requirements engineering,
  business process modeling, и system integration design для cloud-native архитектур.
```

**Используйте проактивно когда:**
- Анализируете бизнес-требования или проводите stakeholder interviews
- Создаете data models или проектируете интеграции
- Проводите gap analysis или оцениваете technical feasibility
- Документируете процессы или создаете user stories

### systems-architect
```yaml
model: sonnet
description: Principal-level architect специализирующийся на cloud-native architecture,
  distributed systems design, security patterns, и multi-cloud strategies.
```

**Используйте проактивно когда:**
- Проектируете system architecture или выбираете technology stack
- Создаете Architecture Decision Records (ADRs)
- Планируете migrations или оптимизируете performance/cost
- Решаете trade-offs между consistency, availability, partition tolerance

### technical-writer
```yaml
model: sonnet
description: Principal-level technical writer специализирующийся на API documentation,
  developer experience, architecture documentation, и docs-as-code workflows.
```

**Используйте проактивно когда:**
- Создаете technical documentation или API references
- Внедряете docs-as-code pipelines
- Улучшаете developer experience или создаете tutorials
- Документируете errors, troubleshooting guides

## Скиллы

Все скиллы следуют Anthropic Agent Skills Specification с progressive disclosure:
- **Metadata** (always loaded): name, description с "Use when" trigger
- **Instructions** (on activation): Core concepts, patterns, best practices
- **Resources** (on demand): Templates, examples, reference materials

### Для Systems Analyst
1. **requirements-engineering** - Elicitation, validation, traceability
2. **enterprise-data-modeling** - Conceptual, logical, physical models
3. **business-process-analysis** - BPMN, Lean Six Sigma, workflow automation

### Для Systems Architect
4. **cloud-architecture-patterns** - Microservices, serverless, event-driven
5. **distributed-systems-design** - CAP theorem, consensus, replication
6. **security-architecture** - Zero trust, compliance (GDPR, SOC 2, HIPAA)

### Для Technical Writer
7. **api-documentation-excellence** - OpenAPI, code examples, error handling
8. **docs-as-code-workflows** - CI/CD, static site generators, quality checks
9. **developer-experience-optimization** - Interactive docs, getting started guides

## Команды

### /analyze-requirements
Автоматизированный анализ бизнес-требований с созданием:
- Business Requirements Document (BRD)
- Functional Requirements Document (FRD)
- User stories с acceptance criteria
- Data models (ERD)
- Process flows (BPMN)
- Requirements Traceability Matrix (RTM)

**Использование:**
```bash
/analyze-requirements
```

### /design-architecture
Проектирование cloud-native архитектуры с созданием:
- Architecture diagrams (C4 model: Context, Container, Component)
- Architecture Decision Records (ADRs)
- Technology stack recommendations
- Security architecture documentation
- Scalability и cost optimization plans
- Deployment architecture

**Использование:**
```bash
/design-architecture
```

### /create-api-docs
Генерация comprehensive API documentation:
- OpenAPI 3.1 specifications
- Getting started guides
- Multi-language code examples (Python, JS, Go, Java, C#)
- Error documentation
- Interactive API explorer setup
- Docs-as-code CI/CD pipeline

**Использование:**
```bash
/create-api-docs
```

## Примеры использования

### Пример 1: Анализ требований для e-commerce платформы

```markdown
Пользователь: Нужно проанализировать требования для новой e-commerce платформы

Systems Analyst (используется проактивно):
1. Проводит structured requirements gathering
2. Создает BRD с business objectives и success metrics
3. Генерирует user stories для key features (checkout, cart, products)
4. Проектирует data models (Customer, Order, Product, Payment)
5. Создает BPMN diagrams для order fulfillment process
6. Строит RTM для traceability

Результат:
- requirements/BRD.md
- requirements/FRD.md
- requirements/user-stories/*.md
- requirements/data-models/erd.mmd
- requirements/process-flows/order-fulfillment.md
- requirements/RTM.md
```

### Пример 2: Проектирование архитектуры

```markdown
Пользователь: Спроектируй cloud-native архитектуру для этих требований

Systems Architect (используется проактивно):
1. Анализирует NFRs (performance, availability, security)
2. Выбирает architecture patterns (microservices, event-driven)
3. Рекомендует technology stack (AWS services, databases)
4. Создает ADRs для key decisions (database selection, API gateway)
5. Проектирует security architecture (zero trust, encryption)
6. Рассчитывает cost estimates и scaling strategies

Результат:
- architecture/overview.md
- architecture/diagrams/*.mmd (Context, Container, Component, Deployment)
- architecture/adrs/*.md
- architecture/technology-stack.md
- architecture/security-architecture.md
- architecture/cost-estimate.md
```

### Пример 3: Создание API документации

```markdown
Пользователь: Создай documentation для REST API

Technical Writer (используется проактивно):
1. Генерирует OpenAPI 3.1 specification
2. Создает getting started guide (< 5 минут до first API call)
3. Пишет multi-language code examples
4. Документирует error codes и troubleshooting
5. Настраивает docs-as-code pipeline (CI/CD)
6. Создает interactive API explorer (Swagger UI)

Результат:
- docs/getting-started.md
- docs/api-reference/*.md
- docs/code-examples/{python,javascript,go,java}/*
- docs/errors.md
- docs/openapi.yaml
- .github/workflows/docs-ci.yml
```

## Интеграции

### Claude Agent SDK
Все агенты оптимизированы для использования в Claude Agent SDK workflows:

```python
from anthropic import Anthropic

client = Anthropic()

# Use systems-analyst для requirements
response = client.messages.create(
    model="claude-sonnet-4",
    messages=[{
        "role": "user",
        "content": "Analyze requirements for payment processing system"
    }],
    tools=[...],  # systems-analyst agent
)

# Use systems-architect для architecture design
response = client.messages.create(
    model="claude-sonnet-4",
    messages=[{
        "role": "user",
        "content": "Design cloud-native architecture for high-traffic system"
    }],
    tools=[...],  # systems-architect agent
)
```

### Workflow Orchestration
Агенты могут работать в sequential или parallel workflows:

```
User Request: "Build e-commerce platform"
    ↓
systems-analyst: Analyze requirements
    ↓
systems-architect: Design architecture
    ↓
technical-writer: Create API docs
    ↓
Final deliverables: BRD, Architecture, API Docs
```

## Best Practices

### Когда использовать каждого агента:

**systems-analyst:**
- ✅ Gathering и documenting requirements
- ✅ Business process modeling и optimization
- ✅ Data modeling и integration design
- ✅ Gap analysis и feasibility assessment

**systems-architect:**
- ✅ Designing system architecture
- ✅ Technology stack selection
- ✅ Security и compliance planning
- ✅ Performance и cost optimization

**technical-writer:**
- ✅ Creating API documentation
- ✅ Writing developer guides
- ✅ Setting up docs-as-code pipelines
- ✅ Optimizing developer experience

### Последовательность работы:

1. **Requirements Phase**: systems-analyst → BRD, FRD, user stories, data models
2. **Design Phase**: systems-architect → Architecture, ADRs, tech stack, security
3. **Documentation Phase**: technical-writer → API docs, guides, tutorials

## Версии и обновления

**Версия**: 1.0.0

**Changelog:**
- ✨ Initial release с 3 агентами
- ✨ 9 comprehensive скиллов
- ✨ 3 автоматизированные команды
- ✨ Full enterprise-level expertise

## Лицензия

MIT License - см. LICENSE файл для деталей.

## Автор

**Dmitry Lazarenko**
- GitHub: [@lazarenkod](https://github.com/lazarenkod)
- Email: lazarenkod@gmail.com

## Вклад

Contributions welcome! Пожалуйста следуйте стандартам проекта:
- Agents: Frontmatter YAML + Markdown system prompt
- Skills: SKILL.md в директории с subdirectories для references/assets
- Commands: Markdown с clear usage instructions

## Поддержка

Для вопросов и поддержки:
- GitHub Issues: [lazarenkod/agents](https://github.com/lazarenkod/agents/issues)
- Email: lazarenkod@gmail.com

---

**Примечание**: Все агенты, скиллы и команды основаны на best practices от ведущих компаний (AWS, Azure, Google Cloud, Microsoft, SAP, Oracle, Stripe, MongoDB, OpenAI) и готовы к использованию в production enterprise-проектах.
