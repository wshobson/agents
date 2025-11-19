---
name: design-architecture
description: Проектирование cloud-native архитектуры с созданием architecture diagrams, ADRs и technology stack recommendations.
---

# Design Architecture

Автоматизированное проектирование системной архитектуры для cloud-native applications.

## Использование

```bash
/design-architecture
```

## Входные данные

Команда запросит:

- **System type**: Web app, API, microservices, data pipeline, etc.
- **Scale requirements**: Expected users, transactions, data volume
- **Cloud provider**: AWS, Azure, GCP, multi-cloud
- **Key NFRs**: Performance, availability, security priorities
- **Existing systems**: Integration requirements
- **Team skills**: Technology constraints based on team expertise

## Выходные артефакты

```
architecture/
├── overview.md                 # High-level architecture overview
├── diagrams/
│   ├── context.mmd            # C4 Context diagram
│   ├── container.mmd          # C4 Container diagram
│   ├── component.mmd          # C4 Component diagram
│   └── deployment.mmd         # Deployment architecture
├── adrs/                      # Architecture Decision Records
│   ├── 001-database-selection.md
│   ├── 002-api-gateway-choice.md
│   └── 003-authentication-strategy.md
├── technology-stack.md        # Recommended technologies
├── scalability-plan.md        # Scaling strategies
├── security-architecture.md   # Security controls
└── cost-estimate.md           # TCO analysis
```

## Пример вывода

### Architecture Decision Record

```markdown
# ADR-001: Database Selection

## Status

Accepted

## Context

Система требует хранение:
- Customer data (structured, relational)
- Product catalog (semi-structured, search-heavy)
- Session state (key-value, high throughput)
- Analytics events (time-series, write-heavy)

Требования:
- 99.95% availability
- < 100ms read latency (p95)
- Support для 10K writes/second
- Global distribution (US, EU, APAC)

## Decision

Используем **polyglot persistence** подход:

1. **PostgreSQL (Aurora)** для customer data
   - ACID transactions required
   - Complex queries и joins
   - Proven reliability

2. **Elasticsearch** для product catalog
   - Full-text search capabilities
   - Faceted search и filters
   - Real-time indexing

3. **Redis (ElastiCache)** для session state
   - In-memory performance (< 1ms)
   - TTL support
   - Pub/Sub для real-time features

4. **TimescaleDB** для analytics
   - Time-series optimized
   - PostgreSQL compatibility
   - Automatic data retention

## Consequences

### Positive
- Optimal performance для каждого use case
- Specialized databases для specialized needs
- Independent scaling по workload type

### Negative
- Increased operational complexity
- Multiple databases to manage
- Data synchronization challenges
- Higher learning curve для team

## Alternatives Considered

**Single database (PostgreSQL)**: Rejected из-за suboptimal performance для search и caching use cases.

**NoSQL only (DynamoDB)**: Rejected из-за lack of complex query support и transaction guarantees.

## Implementation

1. Phase 1: PostgreSQL и Redis (core functionality)
2. Phase 2: Add Elasticsearch (search features)
3. Phase 3: Add TimescaleDB (analytics)

Cost estimate: ~$2,500/month для expected scale
```

### Technology Stack

```markdown
# Technology Stack Recommendations

## Backend Services

### API Layer
- **Framework**: Node.js с Express / Python FastAPI / Go Gin
- **API Gateway**: AWS API Gateway / Azure API Management
- **Authentication**: Auth0 / AWS Cognito с OAuth 2.0
- **Rate Limiting**: Redis с sliding window algorithm

### Business Logic
- **Microservices**: Containerized services (Docker)
- **Orchestration**: Kubernetes (EKS, AKS, или GKE)
- **Service Mesh**: Istio для service-to-service communication
- **Message Queue**: Amazon SQS / Azure Service Bus

### Data Layer
- **Primary Database**: PostgreSQL 15 (Aurora Serverless v2)
- **Cache**: Redis 7 (ElastiCache)
- **Search**: Elasticsearch 8
- **Object Storage**: S3 / Azure Blob Storage

## Frontend
- **Framework**: React 18 / Next.js 14
- **State Management**: Redux Toolkit / Zustand
- **UI Components**: Material-UI / Tailwind CSS
- **Mobile**: React Native / Flutter

## Infrastructure
- **IaC**: Terraform / AWS CDK
- **CI/CD**: GitHub Actions / GitLab CI
- **Monitoring**: Datadog / New Relic / Prometheus + Grafana
- **Logging**: ELK Stack / CloudWatch Logs
- **APM**: New Relic / Datadog APM

## Security
- **WAF**: AWS WAF / Cloudflare
- **DDoS Protection**: AWS Shield / Cloudflare
- **Secrets Management**: AWS Secrets Manager / HashiCorp Vault
- **Vulnerability Scanning**: Snyk / Dependabot

## Rationale

Каждая технология выбрана based on:
- ✅ Production-proven at scale
- ✅ Strong community support
- ✅ Cloud-native architecture alignment
- ✅ Team skill alignment
- ✅ Cost-effectiveness

[Detailed justification для each technology...]
```

## Автоматическая генерация

Команда автоматически:
- Создает Mermaid diagrams на основе requirements
- Генерирует ADRs для key decisions
- Рассчитывает cost estimates
- Создает security threat model
- Предлагает scaling strategies

## Следующие шаги

1. Review architecture с technical team
2. Validate с security и compliance teams
3. Conduct architecture review session
4. Create proof-of-concept для high-risk components
5. Proceed to `/create-api-docs` для API documentation
