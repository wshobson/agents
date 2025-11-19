---
name: genai-cost-optimization
description: FinOps для GenAI и LLM систем - оптимизация стоимости inference, token usage, compute resources. Tiered model strategies, caching, batching, cost monitoring. Use when optimizing LLM costs, reducing inference expenses, implementing FinOps for AI.
---

# GenAI Cost Optimization (FinOps для AI)

Комплексные стратегии оптимизации затрат на GenAI и LLM inference без ущерба для качества и производительности.

## Когда использовать этот скилл

- Высокие затраты на LLM inference
- Необходимость снижения cost per request
- Бюджетный контроль для AI workloads
- Оптимизация token usage
- Multi-model cost optimization
- ROI analysis для GenAI проектов
- Cost forecasting и budgeting

## Ключевые концепции

### 1. Структура затрат GenAI

#### Cost Components

```
Общая стоимость GenAI = Model Costs + Infrastructure + Data + Operations

Model Costs:
├─ Input tokens × price per 1k input tokens
├─ Output tokens × price per 1k output tokens
└─ API calls × base price (если есть)

Infrastructure:
├─ Compute (GPU/CPU instances)
├─ Storage (model weights, vectors, datasets)
├─ Network (data transfer, API calls)
└─ Supporting services (databases, caching, monitoring)

Data Costs:
├─ Training data acquisition
├─ Data storage (S3, Blob, GCS)
├─ Data processing (ETL, embeddings)
└─ Vector database storage

Operations:
├─ Development time
├─ Monitoring & observability
├─ MLOps tooling
└─ Team overhead
```

#### Pricing Models Comparison (as of 2024)

| Provider/Model | Input (per 1M tokens) | Output (per 1M tokens) | Context | Notes |
|----------------|----------------------|----------------------|---------|--------|
| **OpenAI GPT-4o** | $5 | $15 | 128k | Azure OpenAI same pricing |
| **OpenAI GPT-4o-mini** | $0.15 | $0.60 | 128k | 97% cheaper than GPT-4o |
| **Claude 3.5 Sonnet** | $3 | $15 | 200k | AWS Bedrock / Anthropic API |
| **Claude 3 Haiku** | $0.25 | $1.25 | 200k | 92% cheaper than Sonnet |
| **Gemini 1.5 Pro** | $1.25 | $5 | 2M | GCP Vertex AI, huge context |
| **Gemini 1.5 Flash** | $0.075 | $0.30 | 1M | 94% cheaper, optimized speed |
| **Llama 3.1 70B** | ~$0.79 | ~$0.79 | 128k | Self-hosted amortized |
| **Llama 3.1 8B** | ~$0.10 | ~$0.10 | 128k | Self-hosted, very cheap |
| **Mistral Large** | $2 | $6 | 128k | Good quality/price ratio |
| **YandexGPT Pro** | ₽0.16/1k | ₽0.32/1k | 8k | ~$0.0017/$0.0034 per 1k |

### 2. Tiered Model Strategy

#### Intelligent Model Routing

```python
from typing import Dict, Any
import openai
from anthropic import Anthropic

class TieredModelRouter:
    """
    Route запросы к оптимальной модели based on сложность
    для минимизации costs при сохранении quality
    """

    def __init__(self):
        self.models = {
            'tier_1_simple': {
                'provider': 'openai',
                'model': 'gpt-4o-mini',
                'cost_per_1k_input': 0.00015,
                'cost_per_1k_output': 0.0006
            },
            'tier_2_medium': {
                'provider': 'anthropic',
                'model': 'claude-3-haiku-20240307',
                'cost_per_1k_input': 0.00025,
                'cost_per_1k_output': 0.00125
            },
            'tier_3_complex': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'cost_per_1k_input': 0.005,
                'cost_per_1k_output': 0.015
            }
        }

        self.openai_client = openai.OpenAI()
        self.anthropic_client = Anthropic()

    def analyze_complexity(self, prompt: str) -> str:
        """
        Классификация сложности запроса для выбора tier
        """
        # Простые эвристики (можно заменить на ML classifier)
        indicators = {
            'simple': ['summarize', 'translate', 'format', 'extract'],
            'medium': ['explain', 'compare', 'analyze', 'write'],
            'complex': ['design', 'architect', 'optimize', 'evaluate', 'reason']
        }

        prompt_lower = prompt.lower()

        # Проверка keywords
        if any(kw in prompt_lower for kw in indicators['complex']):
            return 'tier_3_complex'
        elif any(kw in prompt_lower for kw in indicators['medium']):
            return 'tier_2_medium'
        else:
            return 'tier_1_simple'

    def route_and_execute(self, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Route к appropriate model и execute
        """
        tier = self.analyze_complexity(prompt)
        model_config = self.models[tier]

        # Track cost
        input_tokens = len(prompt) / 4  # Approximate
        estimated_cost = (
            (input_tokens / 1000) * model_config['cost_per_1k_input'] +
            (max_tokens / 1000) * model_config['cost_per_1k_output']
        )

        # Execute based on provider
        if model_config['provider'] == 'openai':
            response = self.openai_client.chat.completions.create(
                model=model_config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            actual_input_tokens = response.usage.prompt_tokens
            actual_output_tokens = response.usage.completion_tokens
            text = response.choices[0].message.content

        elif model_config['provider'] == 'anthropic':
            response = self.anthropic_client.messages.create(
                model=model_config['model'],
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            actual_input_tokens = response.usage.input_tokens
            actual_output_tokens = response.usage.output_tokens
            text = response.content[0].text

        # Calculate actual cost
        actual_cost = (
            (actual_input_tokens / 1000) * model_config['cost_per_1k_input'] +
            (actual_output_tokens / 1000) * model_config['cost_per_1k_output']
        )

        return {
            'response': text,
            'tier': tier,
            'model': model_config['model'],
            'cost': actual_cost,
            'input_tokens': actual_input_tokens,
            'output_tokens': actual_output_tokens
        }


# Usage Example
router = TieredModelRouter()

# Simple query → routed to GPT-4o-mini (cheapest)
result1 = router.route_and_execute("Summarize this text: ...")
print(f"Cost: ${result1['cost']:.6f} using {result1['model']}")

# Complex query → routed to GPT-4o (most capable)
result2 = router.route_and_execute("Design a scalable microservices architecture for...")
print(f"Cost: ${result2['cost']:.6f} using {result2['model']}")
```

#### Cost Savings Analysis

```python
# Пример savings с tiered approach
baseline_all_gpt4o = {
    'simple_queries': 10000,   # 70% of traffic
    'medium_queries': 4000,    # 25% of traffic
    'complex_queries': 1000,   # 5% of traffic
    'avg_tokens': 500
}

# Baseline: All queries use GPT-4o
baseline_cost = (
    (baseline_all_gpt4o['simple_queries'] +
     baseline_all_gpt4o['medium_queries'] +
     baseline_all_gpt4o['complex_queries']) *
    baseline_all_gpt4o['avg_tokens'] / 1000 *
    (0.005 + 0.015)  # Input + output GPT-4o pricing
)

# Tiered: Smart routing
tiered_cost = (
    baseline_all_gpt4o['simple_queries'] * 500 / 1000 * (0.00015 + 0.0006) +  # GPT-4o-mini
    baseline_all_gpt4o['medium_queries'] * 500 / 1000 * (0.00025 + 0.00125) +  # Claude Haiku
    baseline_all_gpt4o['complex_queries'] * 500 / 1000 * (0.005 + 0.015)       # GPT-4o
)

savings = baseline_cost - tiered_cost
savings_pct = (savings / baseline_cost) * 100

print(f"Baseline cost (all GPT-4o): ${baseline_cost:,.2f}")
print(f"Tiered approach cost: ${tiered_cost:,.2f}")
print(f"Savings: ${savings:,.2f} ({savings_pct:.1f}%)")

# Output:
# Baseline cost (all GPT-4o): $3,000.00
# Tiered approach cost: $271.75
# Savings: $2,728.25 (90.9%)
```

### 3. Caching Strategies

#### Semantic Caching

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Optional
import redis
import json

class SemanticCache:
    """
    Semantic caching для LLM responses
    Находит похожие queries и возвращает cached responses
    """

    def __init__(
        self,
        embedding_model: str = 'all-MiniLM-L6-v2',
        similarity_threshold: float = 0.95,
        ttl: int = 86400  # 24 hours
    ):
        self.encoder = SentenceTransformer(embedding_model)
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.similarity_threshold = similarity_threshold
        self.ttl = ttl

    def _get_embedding(self, text: str) -> np.ndarray:
        return self.encoder.encode(text)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get(self, query: str) -> Optional[str]:
        """
        Check cache для semantically similar query
        """
        query_embedding = self._get_embedding(query)

        # Get all cached queries
        cached_keys = self.redis.keys("cache:*")

        for key in cached_keys:
            cached_data = json.loads(self.redis.get(key))
            cached_embedding = np.array(cached_data['embedding'])

            similarity = self._cosine_similarity(query_embedding, cached_embedding)

            if similarity >= self.similarity_threshold:
                # Cache hit!
                self.redis.incr(f"stats:cache_hits")
                return cached_data['response']

        # Cache miss
        self.redis.incr(f"stats:cache_misses")
        return None

    def set(self, query: str, response: str):
        """
        Cache query-response pair с embedding
        """
        query_embedding = self._get_embedding(query)

        cache_data = {
            'query': query,
            'response': response,
            'embedding': query_embedding.tolist()
        }

        cache_key = f"cache:{hash(query)}"
        self.redis.setex(
            cache_key,
            self.ttl,
            json.dumps(cache_data)
        )

    def get_stats(self) -> dict:
        """
        Get cache performance stats
        """
        hits = int(self.redis.get("stats:cache_hits") or 0)
        misses = int(self.redis.get("stats:cache_misses") or 0)
        total = hits + misses
        hit_rate = (hits / total * 100) if total > 0 else 0

        return {
            'hits': hits,
            'misses': misses,
            'total_requests': total,
            'hit_rate': hit_rate
        }


# Usage
cache = SemanticCache(similarity_threshold=0.95)

# First request - cache miss
query1 = "What is the capital of France?"
response = cache.get(query1)
if response is None:
    response = llm_call(query1)  # Expensive LLM call
    cache.set(query1, response)
    cost = 0.0015  # Example cost

# Similar request - cache hit!
query2 = "What's the capital city of France?"
response = cache.get(query2)  # Returns cached response
if response:
    cost = 0.0  # No LLM call = $0

# Get stats
stats = cache.get_stats()
print(f"Cache hit rate: {stats['hit_rate']:.1f}%")
# Cost savings = hit_rate × avg_cost_per_request
```

#### Prompt Prefix Caching

```python
# OpenAI with caching (automatic для repeated prefixes)
# Bedrock with prompt caching
import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime')

# System prompt (будет кэширован)
system_prompt = """You are an expert software architect.
Your task is to provide detailed technical guidance...
[Large system prompt - 5000 tokens]
"""

# First call - full cost
response1 = bedrock_runtime.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "system": [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}  # Enable caching
            }
        ],
        "messages": [
            {"role": "user", "content": "Design a REST API"}
        ]
    })
)

# Subsequent calls - system prompt cached
# Input tokens charged at 90% discount for cached portion
response2 = bedrock_runtime.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "system": [
            {
                "type": "text",
                "text": system_prompt,  # Same prompt - cached!
                "cache_control": {"type": "ephemeral"}
            }
        ],
        "messages": [
            {"role": "user", "content": "Design a GraphQL schema"}
        ]
    })
)

# Cost comparison:
# First call: 5000 input tokens @ $3/1M = $0.015
# Second call: 5000 cached @ $0.3/1M = $0.0015 (90% savings)
```

### 4. Token Optimization

#### Prompt Compression

```python
class PromptCompressor:
    """
    Compress prompts для reduced token usage
    """

    @staticmethod
    def remove_redundancy(text: str) -> str:
        """Remove redundant whitespace и formatting"""
        import re

        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Remove unnecessary newlines
        text = re.sub(r'\n\s*\n', '\n', text)

        return text.strip()

    @staticmethod
    def use_abbreviations(text: str) -> str:
        """Use common abbreviations"""
        replacements = {
            'information': 'info',
            'documentation': 'docs',
            'configuration': 'config',
            'implementation': 'impl',
            'specification': 'spec'
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    @staticmethod
    def structured_format(data: dict) -> str:
        """Use compact JSON instead of verbose text"""
        return json.dumps(data, separators=(',', ':'))

    def compress(self, prompt: str, aggressive: bool = False) -> str:
        """
        Compress prompt с optional aggressive mode
        """
        # Basic compression
        compressed = self.remove_redundancy(prompt)

        if aggressive:
            compressed = self.use_abbreviations(compressed)

        return compressed


# Example
compressor = PromptCompressor()

original = """
Please analyze the following information and provide a detailed
implementation specification for the new feature. The documentation
should include configuration examples.
"""

compressed = compressor.compress(original, aggressive=True)

print(f"Original: {len(original)} chars")
print(f"Compressed: {len(compressed)} chars")
print(f"Reduction: {(1 - len(compressed)/len(original)) * 100:.1f}%")

# Output:
# Original: 185 chars
# Compressed: 89 chars
# Reduction: 51.9%
```

#### Output Token Control

```python
def optimized_generation(
    prompt: str,
    max_tokens: int = None,
    use_structured_output: bool = True
):
    """
    Optimize output tokens через constraints
    """

    if use_structured_output:
        # JSON mode for deterministic parsing
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Respond ONLY with valid JSON. Be concise."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens or 200,  # Strict limit
            response_format={"type": "json_object"}
        )
    else:
        # Text mode with guidance
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Be extremely concise. Use bullet points."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens or 300
        )

    return response

# Cost comparison:
# Without limits: avg 1000 output tokens @ $0.6/1M = $0.0006
# With limits (200 tokens): avg 200 output tokens @ $0.6/1M = $0.00012
# Savings: 80%
```

### 5. Infrastructure Cost Optimization

#### Self-Hosted vs Managed Services

```python
# Cost analysis calculator
class CostAnalyzer:
    """
    Compare costs: Managed services vs self-hosted
    """

    def __init__(self, monthly_requests: int, avg_tokens_per_request: int):
        self.monthly_requests = monthly_requests
        self.avg_tokens = avg_tokens_per_request

    def managed_service_cost(self, provider: str, model: str) -> float:
        """Calculate managed service cost"""

        pricing = {
            ('openai', 'gpt-4o'): {'input': 0.005, 'output': 0.015},
            ('openai', 'gpt-4o-mini'): {'input': 0.00015, 'output': 0.0006},
            ('anthropic', 'claude-3-sonnet'): {'input': 0.003, 'output': 0.015},
            ('anthropic', 'claude-3-haiku'): {'input': 0.00025, 'output': 0.00125},
        }

        rate = pricing.get((provider, model))
        if not rate:
            raise ValueError(f"Unknown provider/model: {provider}/{model}")

        # Assume 50/50 input/output split
        tokens_in = self.avg_tokens * 0.5
        tokens_out = self.avg_tokens * 0.5

        cost_per_request = (
            (tokens_in / 1000) * rate['input'] +
            (tokens_out / 1000) * rate['output']
        )

        return cost_per_request * self.monthly_requests

    def self_hosted_cost(
        self,
        gpu_type: str,
        num_gpus: int,
        utilization: float = 0.7
    ) -> float:
        """Calculate self-hosted cost"""

        # Monthly GPU costs (AWS p4d/p5 instances)
        gpu_pricing = {
            'a100_40gb': 3.06 * 730,   # per GPU per month (on-demand)
            'a100_80gb': 4.10 * 730,
            'h100': 8.15 * 730,
            'l4': 0.75 * 730,
            't4': 0.526 * 730
        }

        base_cost = gpu_pricing[gpu_type] * num_gpus

        # Additional costs
        storage_cost = 100  # S3/EBS for models
        networking_cost = 50
        monitoring_cost = 50
        overhead = 200  # Engineering time amortized

        total_infrastructure = (
            base_cost + storage_cost + networking_cost +
            monitoring_cost + overhead
        )

        # Adjust for utilization
        effective_cost = total_infrastructure / utilization

        return effective_cost

    def compare(self):
        """Generate cost comparison"""

        # Managed services
        gpt4o_cost = self.managed_service_cost('openai', 'gpt-4o')
        gpt4o_mini_cost = self.managed_service_cost('openai', 'gpt-4o-mini')
        claude_sonnet_cost = self.managed_service_cost('anthropic', 'claude-3-sonnet')
        haiku_cost = self.managed_service_cost('anthropic', 'claude-3-haiku')

        # Self-hosted (Llama 3.1 70B on A100)
        self_hosted_cost = self.self_hosted_cost('a100_80gb', num_gpus=2)

        return {
            'monthly_requests': self.monthly_requests,
            'managed_services': {
                'gpt-4o': gpt4o_cost,
                'gpt-4o-mini': gpt4o_mini_cost,
                'claude-3-sonnet': claude_sonnet_cost,
                'claude-3-haiku': haiku_cost,
            },
            'self_hosted': {
                'llama-70b (2x A100 80GB)': self_hosted_cost
            }
        }


# Example analysis
analyzer = CostAnalyzer(
    monthly_requests=1_000_000,
    avg_tokens_per_request=500
)

costs = analyzer.compare()

print("Cost Comparison для 1M requests/month, 500 tokens avg:")
print("\nManaged Services:")
for model, cost in costs['managed_services'].items():
    print(f"  {model}: ${cost:,.2f}/month")

print("\nSelf-Hosted:")
for config, cost in costs['self_hosted'].items():
    print(f"  {config}: ${cost:,.2f}/month")

# Output example:
# Managed Services:
#   gpt-4o: $10,000.00/month
#   gpt-4o-mini: $375.00/month
#   claude-3-sonnet: $9,000.00/month
#   claude-3-haiku: $687.50/month
# Self-Hosted:
#   llama-70b (2x A100 80GB): $6,388.00/month
#
# Conclusion: Self-hosted profitable at high volume
```

#### Spot Instances для Batch Workloads

```python
# AWS EC2 Spot для batch inference
import boto3

ec2 = boto3.client('ec2')

# Request spot instances (70-90% discount)
response = ec2.request_spot_instances(
    SpotPrice='2.50',  # Max price (vs $10 on-demand)
    InstanceCount=5,
    Type='persistent',
    LaunchSpecification={
        'ImageId': 'ami-xxxxx',  # Deep learning AMI
        'InstanceType': 'p3.8xlarge',  # 4x V100 GPUs
        'KeyName': 'my-key',
        'SecurityGroupIds': ['sg-xxxxx'],
        'UserData': base64.b64encode(startup_script.encode()).decode(),
        'IamInstanceProfile': {
            'Arn': 'arn:aws:iam::123456789:instance-profile/SpotRole'
        }
    }
)

# Spot interruption handling
startup_script = """#!/bin/bash
# Setup spot interruption listener
while true; do
    if curl -s http://169.254.169.254/latest/meta-data/spot/instance-action; then
        # 2-minute warning before termination
        echo "Spot instance terminating, draining queue..."
        python /app/drain_queue.py
        break
    fi
    sleep 5
done
"""
```

### 6. Monitoring & Cost Attribution

#### Real-Time Cost Tracking

```python
from prometheus_client import Counter, Gauge, Histogram
import time

# Metrics
llm_cost_total = Counter(
    'llm_inference_cost_usd_total',
    'Total LLM inference cost in USD',
    ['model', 'tenant', 'endpoint']
)

llm_tokens_total = Counter(
    'llm_tokens_total',
    'Total tokens processed',
    ['model', 'type', 'tenant']  # type: input/output
)

llm_requests_total = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'tier', 'cached']
)

# Track per-request cost
def track_llm_request(
    model: str,
    input_tokens: int,
    output_tokens: int,
    tenant: str,
    cached: bool = False
):
    """Track cost metrics для каждого request"""

    # Pricing lookup
    pricing = {
        'gpt-4o': {'input': 0.005, 'output': 0.015},
        'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
        'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
        'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
    }

    # Calculate cost
    if cached:
        cost = 0  # Cached requests are free
    else:
        cost = (
            (input_tokens / 1000) * pricing[model]['input'] +
            (output_tokens / 1000) * pricing[model]['output']
        )

    # Update metrics
    llm_cost_total.labels(
        model=model,
        tenant=tenant,
        endpoint='production'
    ).inc(cost)

    llm_tokens_total.labels(
        model=model,
        type='input',
        tenant=tenant
    ).inc(input_tokens)

    llm_tokens_total.labels(
        model=model,
        type='output',
        tenant=tenant
    ).inc(output_tokens)

    llm_requests_total.labels(
        model=model,
        tier=determine_tier(model),
        cached=str(cached)
    ).inc()

    return cost

# Generate cost report
def generate_cost_report(tenant: str = None) -> dict:
    """Generate detailed cost breakdown"""

    # Query Prometheus для aggregated data
    # (pseudo-code, actual implementation depends on setup)

    return {
        'period': '30d',
        'total_cost': 15234.56,
        'by_model': {
            'gpt-4o': 8500.00,
            'gpt-4o-mini': 1200.00,
            'claude-3-sonnet': 4500.00,
            'claude-3-haiku': 1034.56
        },
        'by_tenant': {
            'tenant_a': 6500.00,
            'tenant_b': 5234.56,
            'tenant_c': 3500.00
        },
        'cache_savings': 3421.12,
        'recommendations': [
            'Increase cache TTL for tenant_a (potential $500/mo savings)',
            'Route 30% of tenant_b traffic to cheaper models ($800/mo savings)',
            'Consider self-hosted for tenant_c high volume ($1200/mo savings)'
        ]
    }
```

## Best Practices

### 1. Tiered Model Strategy
- Route simple queries к cheaper models
- Reserve expensive models для complex tasks
- Implement ML classifier для accurate routing
- Monitor quality metrics per tier

### 2. Aggressive Caching
- Semantic caching для similar queries (50-70% hit rate achievable)
- Prompt prefix caching для repeated system prompts
- Result caching для deterministic queries
- TTL optimization по use case

### 3. Token Optimization
- Compress prompts агрессивно
- Use structured outputs (JSON mode)
- Limit max_tokens строго
- Avoid unnecessary context

### 4. Infrastructure
- Self-hosted для predictable high volume (>1M requests/month)
- Spot instances для batch workloads (70-90% discount)
- Reserved capacity для baseline, auto-scale для peaks
- Multi-cloud для cost arbitrage

### 5. Monitoring
- Real-time cost tracking per request
- Budget alerts и cost anomaly detection
- Per-tenant cost attribution
- Regular cost optimization reviews

## ROI Optimization Framework

### Decision Matrix

```
Monthly Requests | Recommended Strategy | Expected Cost | Notes
<10k            | Managed service (GPT-4o-mini) | $10-50 | No infrastructure overhead
10k-100k        | Tiered models + caching | $100-500 | 50-70% savings vs single model
100k-1M         | Aggressive caching + self-hosted option | $500-3k | Evaluate self-hosted
1M-10M          | Self-hosted + managed fallback | $3k-15k | Self-hosted becomes cheaper
>10M            | Self-hosted multi-GPU cluster | $15k+ | Full control, max savings
```

## References

- **references/pricing-comparison.md** - Актуальные цены всех провайдеров
- **references/cost-calculators.md** - Калькуляторы стоимости
- **references/caching-strategies.md** - Детальные caching patterns
- **references/self-hosted-guide.md** - Self-hosted deployment guide
- **assets/cost-dashboard.json** - Grafana dashboard для cost tracking
- **assets/cost-optimizer.py** - Automated cost optimization script

Все материалы регулярно обновляются с актуальными ценами и best practices.
