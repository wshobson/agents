---
name: llm-inference-infrastructure
description: Проектирование и развертывание production-ready LLM Inference инфраструктуры на AWS, Azure, GCP, Nebius, NVIDIA, Oracle. Use when designing LLM serving infrastructure, choosing inference platforms, optimizing inference costs.
---

# LLM Inference Infrastructure

Комплексный гайд по проектированию и развертыванию enterprise-grade инфраструктуры для LLM inference на всех major cloud платформах.

## Когда использовать этот скилл

- Проектирование новой LLM inference платформы
- Выбор оптимального cloud провайдера для GenAI workload
- Миграция между inference platforms
- Оптимизация существующей infrastructure
- Multi-cloud deployment strategy
- Cost optimization для LLM serving
- Scaling strategy для production traffic

## Ключевые концепции

### 1. Выбор платформы: Decision Framework

#### Критерии выбора

| Критерий | AWS | Azure | GCP | NVIDIA | Nebius | Oracle |
|----------|-----|-------|-----|---------|---------|---------|
| **Модели** | Bedrock: Claude, Llama, Mistral, Titan | Azure OpenAI: GPT-4o, GPT-3.5 | Vertex AI: Gemini, PaLM, Claude, Llama | NIM: Optimized containers | YandexGPT, custom | Cohere, Llama |
| **Managed Service** | ✅ Bedrock | ✅ Azure OpenAI | ✅ Vertex AI | ❌ Self-managed | ✅ YandexGPT | ✅ OCI GenAI |
| **Custom Models** | ✅ SageMaker | ✅ Azure ML | ✅ Vertex AI | ✅ Triton | ✅ DataSphere | ✅ Data Science |
| **GPU Options** | P4d, P5 (A100, H100) | NDv4, NCv4 (A100) | A2, G2 (A100, L4) | All NVIDIA | A100 | A100 Bare Metal |
| **Data Residency** | Global regions | Global + Gov cloud | Global regions | Any (self-hosted) | Russia-based | Global regions |
| **Pricing Model** | Pay-per-token + provisioned | Pay-per-token + PTU | Pay-per-token + provisioned | Self-managed cost | Pay-per-request | Pay-per-token |
| **SLA** | 99.9% | 99.9% | 99.9% | Custom | 99.95% | 99.95% |

#### Decision Tree

```
Нужен ли GPT-4o/GPT-4?
├─ Да → Azure OpenAI Service
│   └─ + Enterprise agreement → Provisioned PTU
│   └─ + Variable traffic → Standard (pay-per-token)
│
└─ Нет → Какие модели нужны?
    ├─ Claude 3.5 Sonnet → AWS Bedrock или GCP Vertex AI
    │   └─ + Существующая AWS инфра → AWS Bedrock
    │   └─ + GCP ecosystem → Vertex AI
    │
    ├─ Gemini Pro/Ultra → GCP Vertex AI
    │
    ├─ Open-source (Llama, Mistral) → Несколько опций
    │   ├─ Managed service → AWS Bedrock / GCP Vertex AI / Azure ML
    │   ├─ Max performance → NVIDIA NIM + self-hosted
    │   ├─ Cost optimization → Self-hosted на spot instances
    │   └─ Russia data residency → Nebius AI
    │
    └─ Custom fine-tuned → Self-hosted infrastructure
        ├─ Best tools → AWS SageMaker
        ├─ ML platform → GCP Vertex AI
        └─ Cost-effective → NVIDIA Triton на Kubernetes
```

### 2. AWS Infrastructure для LLM

#### Amazon Bedrock Architecture

```python
# Bedrock с Provisioned Throughput
import boto3

bedrock = boto3.client('bedrock-runtime')

# On-demand inference
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Hello!"}
        ]
    })
)

# Provisioned Throughput для guaranteed capacity
response = bedrock.invoke_model(
    modelId='arn:aws:bedrock:us-east-1:123456789:provisioned-model/abc123',
    body=json.dumps({...})
)
```

#### Bedrock с RAG (Knowledge Bases)

```python
# Создание Knowledge Base
bedrock_agent = boto3.client('bedrock-agent')

kb = bedrock_agent.create_knowledge_base(
    name='product-docs-kb',
    roleArn='arn:aws:iam::123456789:role/BedrockKBRole',
    knowledgeBaseConfiguration={
        'type': 'VECTOR',
        'vectorKnowledgeBaseConfiguration': {
            'embeddingModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1'
        }
    },
    storageConfiguration={
        'type': 'OPENSEARCH_SERVERLESS',
        'opensearchServerlessConfiguration': {
            'collectionArn': 'arn:aws:aoss:us-east-1:123456789:collection/abc',
            'vectorIndexName': 'bedrock-knowledge-base-index',
            'fieldMapping': {
                'vectorField': 'embedding',
                'textField': 'text',
                'metadataField': 'metadata'
            }
        }
    }
)

# Query с RAG
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

response = bedrock_agent_runtime.retrieve_and_generate(
    input={'text': 'What are the product features?'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': kb['knowledgeBase']['knowledgeBaseId'],
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
        }
    }
)
```

#### SageMaker для Custom Models

```python
from sagemaker.huggingface import HuggingFaceModel
from sagemaker.serverless import ServerlessInferenceConfig

# Serverless deployment
serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=6144,
    max_concurrency=10
)

huggingface_model = HuggingFaceModel(
    model_data='s3://my-bucket/model.tar.gz',
    role='arn:aws:iam::123456789:role/SageMakerRole',
    transformers_version='4.28',
    pytorch_version='2.0',
    py_version='py310'
)

predictor = huggingface_model.deploy(
    serverless_inference_config=serverless_config
)

# Real-time endpoint с auto-scaling
predictor = huggingface_model.deploy(
    initial_instance_count=2,
    instance_type='ml.g5.2xlarge',
    endpoint_name='llama-2-7b-production'
)

# Auto-scaling policy
client = boto3.client('application-autoscaling')

client.register_scalable_target(
    ServiceNamespace='sagemaker',
    ResourceId=f'endpoint/{predictor.endpoint_name}/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    MinCapacity=2,
    MaxCapacity=10
)

client.put_scaling_policy(
    PolicyName='TargetTrackingScaling',
    ServiceNamespace='sagemaker',
    ResourceId=f'endpoint/{predictor.endpoint_name}/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    PolicyType='TargetTrackingScaling',
    TargetTrackingScalingPolicyConfiguration={
        'TargetValue': 1000.0,
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
        }
    }
)
```

### 3. Azure Infrastructure для LLM

#### Azure OpenAI Service

```python
from openai import AzureOpenAI

# Standard deployment
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint="https://myresource.openai.azure.com"
)

response = client.chat.completions.create(
    model="gpt-4o",  # deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=1000,
    temperature=0.7
)

# Provisioned Throughput Units (PTU)
# Создание через Azure Portal или CLI
# az cognitiveservices account deployment create \
#   --name myresource \
#   --resource-group mygroup \
#   --deployment-name gpt-4o-ptu \
#   --model-name gpt-4o \
#   --model-version "2024-05-13" \
#   --model-format OpenAI \
#   --sku-capacity 100 \
#   --sku-name ProvisionedManaged
```

#### Azure ML для Custom Models

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration
)

# Создание endpoint
endpoint = ManagedOnlineEndpoint(
    name="llama-2-endpoint",
    description="Llama 2 7B inference endpoint",
    auth_mode="key"
)

ml_client.online_endpoints.begin_create_or_update(endpoint)

# Deployment
model = Model(path="./model")

deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name="llama-2-endpoint",
    model=model,
    environment=Environment(
        image="mcr.microsoft.com/azureml/pytorch-2.0-cuda11.7-cudnn8:latest",
        conda_file="conda.yml"
    ),
    code_configuration=CodeConfiguration(
        code="./src",
        scoring_script="score.py"
    ),
    instance_type="Standard_NC6s_v3",
    instance_count=2,
    request_settings={
        "request_timeout_ms": 90000,
        "max_concurrent_requests_per_instance": 1
    },
    liveness_probe={
        "initial_delay": 600,
        "period": 10,
        "timeout": 2,
        "failure_threshold": 30
    }
)

ml_client.online_deployments.begin_create_or_update(deployment)
```

### 4. GCP Infrastructure для LLM

#### Vertex AI Generative AI

```python
from vertexai.preview.generative_models import GenerativeModel

# Gemini Pro
model = GenerativeModel("gemini-1.5-pro")

response = model.generate_content(
    "What is the meaning of life?",
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.95,
    }
)

# Claude на Vertex AI
from vertexai.preview.language_models import ChatModel

chat_model = ChatModel.from_pretrained("claude-3-sonnet@20240229")

chat = chat_model.start_chat()
response = chat.send_message("Hello!")
```

#### Vertex AI Prediction Endpoints

```python
from google.cloud import aiplatform

# Deploy custom model
aiplatform.init(project="my-project", location="us-central1")

model = aiplatform.Model.upload(
    display_name="llama-2-7b",
    artifact_uri="gs://my-bucket/model/",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/pytorch-gpu.2-0:latest"
)

endpoint = model.deploy(
    deployed_model_display_name="llama-2-7b-v1",
    machine_type="n1-standard-8",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
    min_replica_count=1,
    max_replica_count=5,
    traffic_percentage=100
)

# Prediction
response = endpoint.predict(
    instances=[{"prompt": "Hello, how are you?"}]
)
```

### 5. NVIDIA Infrastructure

#### NVIDIA NIM Deployment

```bash
# Pull NIM container
docker pull nvcr.io/nim/meta/llama-2-70b-chat:latest

# Run with optimizations
docker run -d \
  --gpus all \
  --shm-size=16g \
  -p 8000:8000 \
  -e NIM_MODEL_PROFILE=throughput \
  -v $HOME/.cache/nim:/opt/nim/.cache \
  nvcr.io/nim/meta/llama-2-70b-chat:latest
```

#### Triton Inference Server

```python
# model_repository/llama2/config.pbtxt
name: "llama2"
backend: "python"
max_batch_size: 32

input [
  {
    name: "INPUT_TEXT"
    data_type: TYPE_STRING
    dims: [-1]
  }
]

output [
  {
    name: "OUTPUT_TEXT"
    data_type: TYPE_STRING
    dims: [-1]
  }
]

instance_group [
  {
    count: 2
    kind: KIND_GPU
    gpus: [0, 1]
  }
]

dynamic_batching {
  preferred_batch_size: [8, 16, 32]
  max_queue_delay_microseconds: 5000
}
```

```python
# Client code
import tritonclient.http as httpclient

triton_client = httpclient.InferenceServerClient(url="localhost:8000")

inputs = httpclient.InferInput("INPUT_TEXT", [1], "BYTES")
inputs.set_data_from_numpy(np.array(["Hello!"], dtype=object))

outputs = httpclient.InferRequestedOutput("OUTPUT_TEXT")

response = triton_client.infer(
    model_name="llama2",
    inputs=[inputs],
    outputs=[outputs]
)
```

### 6. Multi-Cloud Architecture Patterns

#### Pattern 1: Regional Failover

```
┌──────────────────────────────────────────────────────┐
│                 Global Load Balancer                  │
│              (CloudFlare / Route53 / Traffic Manager)│
└──────────────────┬───────────────────────────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
   │  AWS  │   │ Azure │   │  GCP  │
   │US-East│   │US-West│   │EU-West│
   └───┬───┘   └───┬───┘   └───┬───┘
       │           │           │
   ┌───▼─────┐ ┌───▼─────┐ ┌───▼─────┐
   │Bedrock  │ │Azure OAI│ │Vertex AI│
   │Claude   │ │GPT-4o   │ │Gemini   │
   └─────────┘ └─────────┘ └─────────┘
```

**Terraform Example:**

```hcl
# Global routing
resource "cloudflare_load_balancer" "llm_global" {
  zone_id = var.zone_id
  name    = "llm-api.example.com"

  default_pool_ids = [
    cloudflare_load_balancer_pool.aws_primary.id,
    cloudflare_load_balancer_pool.azure_secondary.id,
    cloudflare_load_balancer_pool.gcp_tertiary.id
  ]

  fallback_pool_id = cloudflare_load_balancer_pool.azure_secondary.id

  steering_policy = "geo"

  region_pools {
    region   = "WNAM"  # Western North America
    pool_ids = [cloudflare_load_balancer_pool.aws_primary.id]
  }

  region_pools {
    region   = "ENAM"  # Eastern North America
    pool_ids = [cloudflare_load_balancer_pool.azure_secondary.id]
  }

  region_pools {
    region   = "EU"
    pool_ids = [cloudflare_load_balancer_pool.gcp_tertiary.id]
  }
}
```

#### Pattern 2: Cost-Optimized Routing

```python
class CostOptimizedRouter:
    """Route requests to cheapest available provider"""

    PRICING = {
        'aws_bedrock_claude': 0.003,  # per 1k tokens
        'azure_gpt4o': 0.005,
        'gcp_gemini': 0.00025,
        'self_hosted_llama': 0.0001   # amortized GPU cost
    }

    def route(self, request):
        # Classify request complexity
        complexity = self.analyze_complexity(request)

        if complexity > 0.8:
            # Complex: use best model (GPT-4o)
            return 'azure_gpt4o'
        elif complexity > 0.5:
            # Medium: use Claude
            return 'aws_bedrock_claude'
        elif complexity > 0.2:
            # Simple: use Gemini
            return 'gcp_gemini'
        else:
            # Very simple: use self-hosted
            return 'self_hosted_llama'

    def analyze_complexity(self, request):
        # ML model для классификации сложности
        prompt_length = len(request['prompt'])
        has_code = 'python' in request['prompt'].lower()
        needs_reasoning = any(kw in request['prompt'].lower()
                             for kw in ['analyze', 'explain', 'why'])

        score = 0
        if prompt_length > 1000: score += 0.3
        if has_code: score += 0.3
        if needs_reasoning: score += 0.4

        return min(1.0, score)
```

### 7. Monitoring & Observability

#### CloudWatch Dashboards (AWS)

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Put custom metrics
cloudwatch.put_metric_data(
    Namespace='LLM/Inference',
    MetricData=[
        {
            'MetricName': 'TokenCount',
            'Value': 150,
            'Unit': 'Count',
            'Dimensions': [
                {'Name': 'Model', 'Value': 'claude-3-sonnet'},
                {'Name': 'Endpoint', 'Value': 'production'}
            ]
        },
        {
            'MetricName': 'InferenceCost',
            'Value': 0.00045,
            'Unit': 'None',
            'Dimensions': [
                {'Name': 'Model', 'Value': 'claude-3-sonnet'}
            ]
        }
    ]
)

# Create dashboard
dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["LLM/Inference", "TokenCount", {"stat": "Sum"}],
                    [".", "InferenceCost", {"stat": "Sum"}]
                ],
                "period": 300,
                "stat": "Average",
                "region": "us-east-1",
                "title": "LLM Usage & Cost"
            }
        }
    ]
}

cloudwatch.put_dashboard(
    DashboardName='LLM-Production',
    DashboardBody=json.dumps(dashboard_body)
)
```

## Best Practices

### 1. Security
- **API Key Management**: AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
- **VPC/VNet Isolation**: Private endpoints для всех LLM сервисов
- **IAM Policies**: Least privilege access
- **Content Filtering**: Встроенные guardrails (Bedrock Guardrails, Azure Content Safety)
- **Audit Logging**: CloudTrail, Azure Monitor Logs, Cloud Audit Logs

### 2. Cost Optimization
- **Caching**: Semantic caching для repeated queries
- **Batching**: Group requests для higher throughput
- **Model Selection**: Router для выбора optimal model по сложности
- **Reserved Capacity**: Provisioned throughput для predictable workloads
- **Spot Instances**: Для non-critical или batch workloads

### 3. Performance
- **Latency**: Target p95 < 2s для good UX
- **Throughput**: Scale horizontally с auto-scaling
- **Caching**: Multi-layer (prompt prefix, semantic, full response)
- **Load Balancing**: Geographic routing для reduced latency

### 4. Reliability
- **Multi-AZ**: Deploy across availability zones
- **Health Checks**: Automated endpoint monitoring
- **Circuit Breakers**: Prevent cascade failures
- **Fallback Models**: Graceful degradation
- **DR Strategy**: Cross-region failover

## References

См. дополнительные материалы:
- **references/aws-bedrock-guide.md** - Детальный гайд по AWS Bedrock
- **references/azure-openai-guide.md** - Azure OpenAI Service best practices
- **references/gcp-vertex-guide.md** - GCP Vertex AI deployment
- **references/nvidia-nim-guide.md** - NVIDIA NIM optimization
- **references/cost-comparison.md** - Сравнение стоимости провайдеров
- **assets/terraform-templates/** - IaC templates для всех платформ
- **assets/monitoring-dashboards/** - Dashboard configurations

## Troubleshooting

### Частые проблемы

| Проблема | Причина | Решение |
|----------|---------|---------|
| High latency | Cold start, large model | Warm pools, smaller model, caching |
| Throttling | Rate limits exceeded | Provisioned capacity, request queuing |
| High cost | Inefficient caching, wrong model | Implement caching, use tiered models |
| Quality issues | Wrong model for task | Model selection strategy, fine-tuning |
| Errors | Timeout, quota | Increase timeout, request quota increase |

Все deployment scripts и configurations доступны в директории `assets/`.
