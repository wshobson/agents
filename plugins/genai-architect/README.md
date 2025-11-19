# GenAI Architect Plugin

Комплексный плагин для системных архитекторов GenAI, LLM и LLM Inference as a Service. Соответствует навыкам senior ролей в AWS, Azure, Google Cloud, OpenAI, Nebius, NVIDIA, Oracle.

## Обзор

Этот плагин предоставляет экспертизу в:
- Проектирование enterprise-grade GenAI платформ
- LLM Inference as a Service архитектура
- Multi-cloud AI deployment (AWS, Azure, GCP, Nebius, NVIDIA, Oracle)
- Production RAG системы
- Cost optimization для GenAI workloads
- MLOps для LLM
- Security & Governance для AI систем

## Компоненты

### Агенты (3)

1. **genai-system-architect** - Системный архитектор GenAI/LLM платформ
   - Проектирование enterprise GenAI архитектуры
   - Выбор платформ (AWS Bedrock, Azure OpenAI, GCP Vertex AI, etc.)
   - Cost estimation и optimization
   - Multi-cloud strategies

2. **llm-inference-optimizer** - Специалист по оптимизации LLM inference
   - Quantization (INT8, INT4, GPTQ, AWQ)
   - Model serving optimization (vLLM, TensorRT-LLM, TGI)
   - Latency optimization
   - GPU utilization maximization

3. **genai-mlops-engineer** - MLOps инженер для GenAI
   - CI/CD для моделей
   - A/B testing и canary deployments
   - Model versioning и registry
   - Continuous evaluation

### Скиллы (5)

1. **llm-inference-infrastructure** - Инфраструктура для LLM inference
   - AWS (Bedrock, SageMaker)
   - Azure (OpenAI Service, Azure ML)
   - GCP (Vertex AI)
   - NVIDIA (NIM, Triton)
   - Nebius AI, Oracle Cloud

2. **genai-cost-optimization** - FinOps для GenAI
   - Tiered model strategies
   - Caching (semantic, prefix)
   - Token optimization
   - Self-hosted vs managed cost analysis

3. **production-rag-systems** - Production RAG архитектура
   - Hybrid search (vector + keyword)
   - Reranking strategies
   - Context assembly
   - Evaluation metrics

4. **aws-bedrock-deployment** - AWS Bedrock специфика
   - Provisioned Throughput
   - Knowledge Bases
   - Bedrock Agents
   - Guardrails

5. **llm-security-governance** - Безопасность LLM
   - Prompt injection defense
   - PII protection
   - Content moderation
   - Access control
   - Audit logging

### Команды (1)

1. **design-genai-architecture** - Интерактивное проектирование GenAI архитектуры
   - Сбор требований
   - Platform selection
   - Cost estimation
   - Security design
   - Implementation roadmap

## Использование

### Пример 1: Проектирование GenAI архитектуры

```
/design-genai-architecture

# Ответьте на вопросы и получите полную архитектуру с:
# - Выбором платформы
# - Cost estimation
# - Security controls
# - IaC код
# - Deployment plan
```

### Пример 2: Оптимизация существующей системы

```
Используйте агента llm-inference-optimizer для:
- Анализа bottlenecks
- Применения quantization
- Настройки vLLM/TensorRT
- Снижения latency
```

### Пример 3: Production RAG система

```
Используйте скилл production-rag-systems для:
- Hybrid search setup
- Reranking configuration
- Evaluation framework
- Performance optimization
```

## Особенности

### ✅ Русскоязычные агенты
Все агенты **по умолчанию отвечают на русском** языке и **сохраняют результаты в markdown-файлы**.

### ✅ Production-ready
Все решения ориентированы на production с учетом:
- Масштабируемости
- Надежности
- Cost efficiency
- Security best practices

### ✅ Multi-cloud
Глубокая экспертиза во всех major cloud провайдерах:
- AWS (Bedrock, SageMaker)
- Azure (OpenAI Service)
- GCP (Vertex AI)
- NVIDIA (NIM)
- Nebius AI
- Oracle Cloud

### ✅ Comprehensive
Покрывает весь lifecycle от проектирования до monitoring:
- Architecture design
- Cost optimization
- Security & compliance
- Deployment automation
- Monitoring & observability

## Целевая аудитория

- Senior/Principal GenAI Architects
- LLM Platform Engineers
- AI Infrastructure Engineers
- MLOps Engineers
- Cloud Architects работающие с AI workloads

## Версия

1.0.0 - Initial release

## Лицензия

См. корневую лицензию проекта.
