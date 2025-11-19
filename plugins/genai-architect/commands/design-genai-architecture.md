---
name: design-genai-architecture
description: Интерактивная команда для проектирования GenAI/LLM архитектуры с выбором платформы, cost estimation, и production-ready deployment plan.
---

# Design GenAI Architecture

Эта команда помогает спроектировать complete GenAI/LLM архитектуру от требований до deployment plan.

## Процесс

### Шаг 1: Сбор требований

Ответьте на следующие вопросы:

**Функциональные требования:**
1. Какой тип GenAI системы вы строите?
   - [ ] Document Q&A / RAG system
   - [ ] Chatbot / Conversational AI
   - [ ] Content generation
   - [ ] Code assistant
   - [ ] Multi-modal AI (vision, audio)
   - [ ] Custom use case: ___________

2. Какие модели вам нужны?
   - [ ] GPT-4o / GPT-4 (OpenAI)
   - [ ] Claude 3.5 / Claude 3 (Anthropic)
   - [ ] Gemini Pro / Gemini Ultra (Google)
   - [ ] Open-source (Llama, Mistral, etc.)
   - [ ] Custom fine-tuned models

3. Специфические возможности:
   - [ ] RAG с векторным поиском
   - [ ] Multi-agent orchestration
   - [ ] Function calling / Tool use
   - [ ] Streaming responses
   - [ ] Multi-turn conversations
   - [ ] Context caching

**Нефункциональные требования:**

4. Ожидаемая нагрузка:
   - Requests per day: ___________
   - Concurrent users: ___________
   - Average tokens per request: ___________
   - Peak multiplier: ___________x

5. Performance требования:
   - Target latency (p95): _________ ms
   - Required throughput: _________ req/sec
   - Availability SLA: _________ %

6. Budget constraints:
   - Monthly budget: $ ___________
   - Cost per request target: $ ___________

7. Compliance & Security:
   - [ ] Data residency (specify region): ___________
   - [ ] GDPR compliance
   - [ ] HIPAA compliance
   - [ ] SOC2 compliance
   - [ ] PII handling requirements
   - [ ] Custom security requirements: ___________

### Шаг 2: Platform Selection

На основе ваших требований, я рекомендую:

**Recommended Platform:** [AWS Bedrock / Azure OpenAI / GCP Vertex AI / Self-hosted / Hybrid]

**Reasoning:**
- [Обоснование выбора]
- [Cost-benefit analysis]
- [Compliance match]

**Alternative Options:**
1. [Alternative 1]: [Pros/Cons]
2. [Alternative 2]: [Pros/Cons]

### Шаг 3: Architecture Design

```
[Архитектурная диаграмма в ASCII или Mermaid]
```

**Components:**
1. **API Gateway**: [Выбранное решение]
2. **LLM Service**: [Bedrock/Azure OpenAI/Vertex AI/etc.]
3. **Vector Database**: [Pinecone/Qdrant/pgvector/etc.]
4. **Caching Layer**: [Redis/Momento/etc.]
5. **Monitoring**: [CloudWatch/Azure Monitor/GCP Monitoring]
6. **Load Balancer**: [ALB/Azure Load Balancer/Cloud Load Balancing]

**Data Flow:**
1. [Step by step data flow description]

### Шаг 4: Cost Estimation

**Monthly Cost Breakdown:**

| Component | Configuration | Monthly Cost |
|-----------|--------------|--------------|
| LLM API calls | [X requests @ $Y/1k tokens] | $_____ |
| Vector Database | [Storage + queries] | $_____ |
| Compute | [Instances/containers] | $_____ |
| Caching | [Redis cluster] | $_____ |
| Storage | [S3/Blob/GCS] | $_____ |
| Network | [Data transfer] | $_____ |
| Monitoring | [Logs + metrics] | $_____ |
| **Total** | | **$_____** |

**Cost Optimization Opportunities:**
- [Optimization 1]: Potential saving $___/mo
- [Optimization 2]: Potential saving $___/mo
- [Optimization 3]: Potential saving $___/mo

### Шаг 5: Security Architecture

**Security Controls:**
1. **Authentication & Authorization**
   - [IAM roles, API keys, OAuth]

2. **Network Security**
   - [VPC, private endpoints, security groups]

3. **Data Protection**
   - [Encryption at rest/in transit]
   - [PII detection/redaction]

4. **Content Safety**
   - [Guardrails, content filtering]

5. **Audit & Compliance**
   - [Logging strategy]
   - [Compliance certifications]

### Шаг 6: Monitoring & Observability

**Key Metrics:**
- Latency (p50, p95, p99)
- Throughput (req/sec)
- Error rate
- Token usage
- Cost per request
- Cache hit rate
- Model quality scores

**Dashboards:**
1. Real-time operations dashboard
2. Cost analytics dashboard
3. Quality metrics dashboard

**Alerts:**
- High latency (p95 > threshold)
- Error rate spike
- Budget threshold breach
- Model quality degradation

### Шаг 7: Implementation Roadmap

**Phase 1: MVP (Weeks 1-2)**
- [ ] Setup cloud infrastructure (IaC)
- [ ] Deploy basic LLM integration
- [ ] Implement simple RAG pipeline
- [ ] Basic monitoring setup
- [ ] Initial testing

**Phase 2: Production (Weeks 3-4)**
- [ ] Add caching layer
- [ ] Implement hybrid search
- [ ] Setup auto-scaling
- [ ] Enhanced monitoring
- [ ] Security hardening
- [ ] Load testing

**Phase 3: Optimization (Weeks 5-6)**
- [ ] Cost optimization (tiered models, caching)
- [ ] Performance tuning
- [ ] A/B testing framework
- [ ] Advanced analytics
- [ ] Documentation

**Phase 4: Scale (Ongoing)**
- [ ] Multi-region deployment
- [ ] Advanced RAG techniques
- [ ] Continuous evaluation
- [ ] Model fine-tuning

### Шаг 8: Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|---------|------------|
| High latency | Medium | High | [Mitigation strategy] |
| Cost overrun | Medium | High | [Mitigation strategy] |
| Model quality issues | Low | High | [Mitigation strategy] |
| Compliance violation | Low | Critical | [Mitigation strategy] |
| Service outage | Low | High | [Mitigation strategy] |

### Шаг 9: Infrastructure as Code

**Terraform Example** (выбранная платформа):

```hcl
# [IaC code snippet для вашей архитектуры]
```

**Deployment Commands:**
```bash
# [Deployment instructions]
```

### Шаг 10: Documentation & Handoff

**Deliverables:**
1. ✅ Architecture Decision Record (ADR)
2. ✅ Cost estimation spreadsheet
3. ✅ Infrastructure as Code (Terraform/CDK)
4. ✅ Security documentation
5. ✅ Monitoring setup guide
6. ✅ Deployment runbook
7. ✅ Troubleshooting guide

**Next Steps:**
1. Review и approval от stakeholders
2. Setup development environment
3. Begin Phase 1 implementation
4. Schedule weekly review meetings

---

## Output

Вся архитектура сохраняется в файл:

**`genai-architecture-{project-name}-{date}.md`**

Со следующей структурой:

```markdown
# GenAI Architecture: {Project Name}

## Executive Summary
[Краткое описание, ключевые решения, timeline]

## Requirements
[Полный список требований]

## Architecture
[Диаграмма и описание компонентов]

## Platform Selection
[Выбор и обоснование]

## Cost Estimation
[Детальная стоимость]

## Security & Compliance
[Security controls и compliance mapping]

## Monitoring
[Metrics, dashboards, alerts]

## Implementation Roadmap
[Поэтапный план]

## Risks & Mitigation
[Risk matrix и strategies]

## Infrastructure as Code
[Полный IaC код]

## Appendices
- ADR (Architecture Decision Records)
- Detailed cost breakdown
- Alternative options considered
```

---

## Interactive Mode

Эта команда работает интерактивно. После запуска `/design-genai-architecture`, я задам вам вопросы и на основе ваших ответов создам полную архитектуру.

**Начнем?** Опишите ваш use case или ответьте на вопросы из Шага 1.
