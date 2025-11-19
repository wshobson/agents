---
name: aws-bedrock-deployment
description: AWS Bedrock production deployment - Provisioned Throughput, Knowledge Bases, Agents, Guardrails, fine-tuning, cross-region, multi-model orchestration. Use when deploying on AWS Bedrock, optimizing Bedrock costs, implementing Bedrock RAG.
---

# AWS Bedrock Production Deployment

Полное руководство по production deployment на Amazon Bedrock с best practices для enterprise workloads.

## Когда использовать этот скилл

- Deployment LLM на AWS Bedrock
- Настройка Provisioned Throughput
- Построение RAG с Bedrock Knowledge Bases
- Создание Bedrock Agents
- Fine-tuning моделей на Bedrock
- Cross-region deployment
- Cost optimization для Bedrock
- Guardrails configuration

## AWS Bedrock Overview

### Доступные модели (2024)

| Модель | Input ($/1M tokens) | Output ($/1M tokens) | Context | Notes |
|--------|---------------------|---------------------|---------|--------|
| **Claude 3.5 Sonnet v2** | $3 | $15 | 200k | Best quality/price |
| **Claude 3 Opus** | $15 | $75 | 200k | Highest capability |
| **Claude 3 Sonnet** | $3 | $15 | 200k | Balanced |
| **Claude 3 Haiku** | $0.25 | $1.25 | 200k | Fastest, cheapest |
| **Llama 3.1 405B** | $5.32 | $16 | 128k | Open source |
| **Llama 3.1 70B** | $0.99 | $0.99 | 128k | Cost-effective |
| **Llama 3.1 8B** | $0.22 | $0.22 | 128k | Very cheap |
| **Mistral Large 2** | $2 | $6 | 128k | Multilingual |
| **Mistral Small** | $0.2 | $0.6 | 32k | Fast inference |
| **Amazon Titan Text G1 - Premier** | $0.5 | $1.5 | 32k | AWS native |
| **Cohere Command R+** | $3 | $15 | 128k | Enterprise |

### Deployment Types

**On-Demand (Pay-as-you-go)**
- ✅ No upfront commitment
- ✅ Automatic scaling
- ⚠️ Higher per-token cost
- ⚠️ Shared capacity (throttling risk)

**Provisioned Throughput**
- ✅ Guaranteed capacity (Model Units)
- ✅ Lower per-token cost (with volume)
- ✅ Predictable performance
- ⚠️ Monthly commitment
- ⚠️ Upfront cost

## 1. Basic Bedrock Integration

### On-Demand Inference

```python
import boto3
import json
from typing import Dict, Any, Iterator

class BedrockClient:
    """
    Production-ready Bedrock client с error handling
    """

    def __init__(self, region: str = 'us-east-1'):
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=region
        )
        self.region = region

    def invoke_claude(
        self,
        prompt: str,
        model_id: str = 'anthropic.claude-3-5-sonnet-20241022-v2:0',
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Invoke Claude model на Bedrock
        """

        messages = [{"role": "user", "content": prompt}]

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system_prompt:
            body["system"] = system_prompt

        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )

            response_body = json.loads(response['body'].read())

            return {
                'text': response_body['content'][0]['text'],
                'usage': {
                    'input_tokens': response_body['usage']['input_tokens'],
                    'output_tokens': response_body['usage']['output_tokens']
                },
                'stop_reason': response_body['stop_reason']
            }

        except Exception as e:
            print(f"Error invoking Bedrock: {str(e)}")
            raise

    def invoke_claude_streaming(
        self,
        prompt: str,
        model_id: str = 'anthropic.claude-3-5-sonnet-20241022-v2:0',
        max_tokens: int = 2048
    ) -> Iterator[str]:
        """
        Streaming inference для real-time responses
        """

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = self.client.invoke_model_with_response_stream(
            modelId=model_id,
            body=json.dumps(body)
        )

        for event in response['body']:
            chunk = json.loads(event['chunk']['bytes'])

            if chunk['type'] == 'content_block_delta':
                if 'delta' in chunk and 'text' in chunk['delta']:
                    yield chunk['delta']['text']


# Usage
bedrock = BedrockClient(region='us-east-1')

# Regular inference
result = bedrock.invoke_claude(
    prompt="Explain quantum computing",
    system_prompt="You are a physics professor."
)

print(result['text'])
print(f"Tokens used: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")

# Streaming
print("Streaming response:")
for chunk in bedrock.invoke_claude_streaming("Write a short story"):
    print(chunk, end='', flush=True)
```

## 2. Provisioned Throughput Deployment

### Model Units Calculation

```python
class ProvisionedThroughputCalculator:
    """
    Calculate required Model Units для Provisioned Throughput
    """

    # Model Unit costs (hourly)
    MODEL_UNIT_COSTS = {
        'anthropic.claude-3-5-sonnet-20241022-v2:0': {
            '1_month': 8.00,
            '6_month': 6.40
        },
        'anthropic.claude-3-haiku-20240307-v1:0': {
            '1_month': 1.00,
            '6_month': 0.80
        }
    }

    def calculate_required_units(
        self,
        requests_per_second: float,
        avg_input_tokens: int,
        avg_output_tokens: int,
        model_id: str
    ) -> int:
        """
        Estimate Model Units needed
        """

        # Базовая пропускная способность 1 Model Unit:
        # Claude 3.5 Sonnet: ~4000 input tokens/sec, ~4000 output tokens/sec

        base_input_throughput = 4000  # tokens/sec
        base_output_throughput = 4000

        # Total tokens per second
        total_input_tps = requests_per_second * avg_input_tokens
        total_output_tps = requests_per_second * avg_output_tokens

        # Required units (max of input or output requirements)
        units_for_input = total_input_tps / base_input_throughput
        units_for_output = total_output_tps / base_output_throughput

        required_units = max(units_for_input, units_for_output)

        # Round up и add 20% buffer
        return int(required_units * 1.2) + 1

    def calculate_monthly_cost(
        self,
        model_units: int,
        model_id: str,
        commitment: str = '1_month'
    ) -> float:
        """
        Calculate monthly cost для Provisioned Throughput
        """

        hourly_cost = self.MODEL_UNIT_COSTS[model_id][commitment]
        monthly_hours = 730  # avg hours per month

        return model_units * hourly_cost * monthly_hours

    def compare_ondemand_vs_provisioned(
        self,
        monthly_requests: int,
        avg_input_tokens: int,
        avg_output_tokens: int,
        model_id: str = 'anthropic.claude-3-5-sonnet-20241022-v2:0'
    ):
        """
        Cost comparison
        """

        # On-demand cost
        total_input_tokens = monthly_requests * avg_input_tokens
        total_output_tokens = monthly_requests * avg_output_tokens

        ondemand_cost = (
            (total_input_tokens / 1_000_000) * 3 +  # $3 per 1M input tokens
            (total_output_tokens / 1_000_000) * 15  # $15 per 1M output tokens
        )

        # Provisioned cost
        requests_per_second = monthly_requests / (30 * 24 * 3600)
        required_units = self.calculate_required_units(
            requests_per_second,
            avg_input_tokens,
            avg_output_tokens,
            model_id
        )

        provisioned_cost_1mo = self.calculate_monthly_cost(
            required_units, model_id, '1_month'
        )
        provisioned_cost_6mo = self.calculate_monthly_cost(
            required_units, model_id, '6_month'
        )

        return {
            'monthly_requests': monthly_requests,
            'required_model_units': required_units,
            'costs': {
                'on_demand': ondemand_cost,
                'provisioned_1_month': provisioned_cost_1mo,
                'provisioned_6_month': provisioned_cost_6mo
            },
            'savings': {
                'provisioned_1_month': ondemand_cost - provisioned_cost_1mo,
                'provisioned_6_month': ondemand_cost - provisioned_cost_6mo
            }
        }


# Usage
calculator = ProvisionedThroughputCalculator()

analysis = calculator.compare_ondemand_vs_provisioned(
    monthly_requests=1_000_000,
    avg_input_tokens=500,
    avg_output_tokens=300,
    model_id='anthropic.claude-3-5-sonnet-20241022-v2:0'
)

print(f"Required Model Units: {analysis['required_model_units']}")
print(f"\nCost Comparison:")
print(f"On-Demand: ${analysis['costs']['on_demand']:,.2f}")
print(f"Provisioned (1-month): ${analysis['costs']['provisioned_1_month']:,.2f}")
print(f"Provisioned (6-month): ${analysis['costs']['provisioned_6_month']:,.2f}")
print(f"\nSavings with 6-month commitment: ${analysis['savings']['provisioned_6_month']:,.2f}")
```

### Provisioned Throughput Deployment

```python
import boto3

bedrock = boto3.client('bedrock')

# Purchase Provisioned Throughput
response = bedrock.create_provisioned_model_throughput(
    modelUnits=5,  # Number of Model Units
    provisionedModelName='claude-sonnet-production',
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    commitmentDuration='OneMonth',  # or 'SixMonths'
    tags=[
        {'key': 'Environment', 'value': 'Production'},
        {'key': 'Team', 'value': 'AI-Engineering'}
    ]
)

provisioned_model_arn = response['provisionedModelArn']

# Use Provisioned Throughput
bedrock_runtime = boto3.client('bedrock-runtime')

response = bedrock_runtime.invoke_model(
    modelId=provisioned_model_arn,  # Use ARN instead of model ID
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Hello"}]
    })
)
```

## 3. Knowledge Bases (RAG на Bedrock)

### Создание Knowledge Base

```python
import boto3
from typing import List, Dict

class BedrockKnowledgeBase:
    """
    Managed RAG с Bedrock Knowledge Bases
    """

    def __init__(self):
        self.bedrock_agent = boto3.client('bedrock-agent')
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
        self.s3 = boto3.client('s3')

    def create_knowledge_base(
        self,
        name: str,
        description: str,
        s3_bucket: str,
        s3_prefix: str,
        embedding_model: str = 'amazon.titan-embed-text-v1',
        vector_store_type: str = 'OPENSEARCH_SERVERLESS'
    ) -> str:
        """
        Create Knowledge Base с vector store
        """

        # 1. Create OpenSearch Serverless collection (if using)
        if vector_store_type == 'OPENSEARCH_SERVERLESS':
            collection_arn = self._create_opensearch_collection(name)

        # 2. Create Knowledge Base
        response = self.bedrock_agent.create_knowledge_base(
            name=name,
            description=description,
            roleArn=f'arn:aws:iam::{self._get_account_id()}:role/BedrockKnowledgeBaseRole',
            knowledgeBaseConfiguration={
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': f'arn:aws:bedrock:us-east-1::foundation-model/{embedding_model}'
                }
            },
            storageConfiguration={
                'type': vector_store_type,
                'opensearchServerlessConfiguration': {
                    'collectionArn': collection_arn,
                    'vectorIndexName': f'{name}-index',
                    'fieldMapping': {
                        'vectorField': 'embedding',
                        'textField': 'text',
                        'metadataField': 'metadata'
                    }
                }
            }
        )

        kb_id = response['knowledgeBase']['knowledgeBaseId']

        # 3. Create Data Source (S3)
        ds_response = self.bedrock_agent.create_data_source(
            knowledgeBaseId=kb_id,
            name=f'{name}-s3-datasource',
            dataSourceConfiguration={
                'type': 'S3',
                's3Configuration': {
                    'bucketArn': f'arn:aws:s3:::{s3_bucket}',
                    'inclusionPrefixes': [s3_prefix]
                }
            }
        )

        return kb_id

    def ingest_documents(self, knowledge_base_id: str, data_source_id: str):
        """
        Trigger ingestion job
        """

        response = self.bedrock_agent.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id
        )

        return response['ingestionJob']['ingestionJobId']

    def query_knowledge_base(
        self,
        knowledge_base_id: str,
        query: str,
        num_results: int = 5
    ) -> List[Dict]:
        """
        Query Knowledge Base (retrieval only)
        """

        response = self.bedrock_agent_runtime.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={'text': query},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': num_results
                }
            }
        )

        return response['retrievalResults']

    def retrieve_and_generate(
        self,
        knowledge_base_id: str,
        query: str,
        model_arn: str = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0'
    ) -> Dict:
        """
        RAG: Retrieve + Generate в одном API call
        """

        response = self.bedrock_agent_runtime.retrieve_and_generate(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': 5
                        }
                    }
                }
            }
        )

        return {
            'answer': response['output']['text'],
            'citations': response.get('citations', [])
        }

    def _get_account_id(self) -> str:
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']

    def _create_opensearch_collection(self, name: str) -> str:
        # Simplified - в production используйте полную настройку
        import boto3
        aoss = boto3.client('opensearchserverless')

        response = aoss.create_collection(
            name=f'{name}-collection',
            type='VECTORSEARCH'
        )

        return response['createCollectionDetail']['arn']


# Usage
kb = BedrockKnowledgeBase()

# Create Knowledge Base
kb_id = kb.create_knowledge_base(
    name='company-docs-kb',
    description='Internal company documentation',
    s3_bucket='my-documents-bucket',
    s3_prefix='documents/'
)

# Query с RAG
result = kb.retrieve_and_generate(
    knowledge_base_id=kb_id,
    query='What is our API authentication policy?'
)

print("Answer:", result['answer'])
print("\nSources:")
for citation in result['citations']:
    print(f"- {citation['retrievedReferences'][0]['location']['s3Location']['uri']}")
```

## 4. Bedrock Agents

### Agent Creation

```python
class BedrockAgent:
    """
    Bedrock Agent с tools/functions
    """

    def __init__(self):
        self.bedrock_agent = boto3.client('bedrock-agent')
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

    def create_agent(
        self,
        name: str,
        description: str,
        model_id: str = 'anthropic.claude-3-5-sonnet-20241022-v2:0',
        instructions: str = None
    ) -> str:
        """
        Create Agent
        """

        response = self.bedrock_agent.create_agent(
            agentName=name,
            description=description,
            agentResourceRoleArn=f'arn:aws:iam::{self._get_account_id()}:role/BedrockAgentRole',
            foundationModel=model_id,
            instruction=instructions or "You are a helpful assistant."
        )

        return response['agent']['agentId']

    def create_action_group(
        self,
        agent_id: str,
        action_group_name: str,
        lambda_arn: str,
        api_schema: Dict
    ):
        """
        Add action group (tools) к agent
        """

        response = self.bedrock_agent.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName=action_group_name,
            actionGroupExecutor={
                'lambda': lambda_arn
            },
            apiSchema={
                'payload': json.dumps(api_schema)
            }
        )

        return response['agentActionGroup']['actionGroupId']

    def prepare_agent(self, agent_id: str):
        """
        Prepare agent (build)
        """

        response = self.bedrock_agent.prepare_agent(
            agentId=agent_id
        )

        return response['agentStatus']

    def create_alias(
        self,
        agent_id: str,
        alias_name: str = 'production'
    ) -> str:
        """
        Create agent alias для versioning
        """

        response = self.bedrock_agent.create_agent_alias(
            agentId=agent_id,
            agentAliasName=alias_name
        )

        return response['agentAlias']['agentAliasId']

    def invoke_agent(
        self,
        agent_id: str,
        agent_alias_id: str,
        session_id: str,
        input_text: str
    ) -> str:
        """
        Invoke agent
        """

        response = self.bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text
        )

        # Stream response
        completion = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    completion += chunk['bytes'].decode('utf-8')

        return completion


# Usage
agent = BedrockAgent()

# Create agent
agent_id = agent.create_agent(
    name='customer-support-agent',
    description='Customer support automation',
    instructions="""You are a customer support agent.
You can search our knowledge base and create support tickets.
Always be helpful and professional."""
)

# Add action группу (Lambda function для tools)
action_group_id = agent.create_action_group(
    agent_id=agent_id,
    action_group_name='support-tools',
    lambda_arn='arn:aws:lambda:us-east-1:123456789:function:support-tools',
    api_schema={
        "openapi": "3.0.0",
        "info": {"title": "Support Tools API", "version": "1.0.0"},
        "paths": {
            "/create-ticket": {
                "post": {
                    "description": "Create a support ticket",
                    "parameters": [
                        {"name": "title", "in": "query", "required": True, "schema": {"type": "string"}},
                        {"name": "description", "in": "query", "required": True, "schema": {"type": "string"}}
                    ]
                }
            }
        }
    }
)

# Prepare и create alias
agent.prepare_agent(agent_id)
alias_id = agent.create_alias(agent_id, 'production')

# Invoke
response = agent.invoke_agent(
    agent_id=agent_id,
    agent_alias_id=alias_id,
    session_id='user-123-session',
    input_text='I need help with my order #12345'
)

print(response)
```

## 5. Guardrails

### Guardrails Configuration

```python
class BedrockGuardrails:
    """
    Content filtering и safety controls
    """

    def __init__(self):
        self.bedrock = boto3.client('bedrock')

    def create_guardrail(
        self,
        name: str,
        blocked_input_messaging: str,
        blocked_output_messaging: str
    ) -> str:
        """
        Create guardrail с filters
        """

        response = self.bedrock.create_guardrail(
            name=name,
            description='Content safety guardrail',
            # Content filters
            contentPolicyConfig={
                'filtersConfig': [
                    {
                        'type': 'SEXUAL',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH'
                    },
                    {
                        'type': 'VIOLENCE',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH'
                    },
                    {
                        'type': 'HATE',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH'
                    },
                    {
                        'type': 'INSULTS',
                        'inputStrength': 'MEDIUM',
                        'outputStrength': 'MEDIUM'
                    },
                    {
                        'type': 'MISCONDUCT',
                        'inputStrength': 'MEDIUM',
                        'outputStrength': 'MEDIUM'
                    }
                ]
            },
            # Topic filters
            topicPolicyConfig={
                'topicsConfig': [
                    {
                        'name': 'Financial Advice',
                        'definition': 'Requests for specific investment or financial advice',
                        'examples': [
                            'Should I invest in Bitcoin?',
                            'Which stocks should I buy?'
                        ],
                        'type': 'DENY'
                    }
                ]
            },
            # PII filters
            sensitiveInformationPolicyConfig={
                'piiEntitiesConfig': [
                    {'type': 'EMAIL', 'action': 'ANONYMIZE'},
                    {'type': 'PHONE', 'action': 'ANONYMIZE'},
                    {'type': 'CREDIT_DEBIT_CARD_NUMBER', 'action': 'BLOCK'},
                    {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'}
                ]
            },
            blockedInputMessaging=blocked_input_messaging,
            blockedOutputsMessaging=blocked_output_messaging
        )

        return response['guardrailId']

    def invoke_with_guardrail(
        self,
        prompt: str,
        guardrail_id: str,
        guardrail_version: str = 'DRAFT',
        model_id: str = 'anthropic.claude-3-5-sonnet-20241022-v2:0'
    ):
        """
        Invoke model с guardrails
        """

        bedrock_runtime = boto3.client('bedrock-runtime')

        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            guardrailIdentifier=guardrail_id,
            guardrailVersion=guardrail_version,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        return json.loads(response['body'].read())


# Usage
guardrails = BedrockGuardrails()

guardrail_id = guardrails.create_guardrail(
    name='content-safety-guardrail',
    blocked_input_messaging='Your request was blocked due to content policy.',
    blocked_output_messaging='I cannot provide that information due to content policy.'
)

# Invoke с guardrails
result = guardrails.invoke_with_guardrail(
    prompt="Tell me a joke",
    guardrail_id=guardrail_id
)
```

## Best Practices

### 1. Cost Optimization
- Provisioned Throughput для predictable high-volume (>500k requests/mo)
- On-demand для variable/low-volume workloads
- Haiku для simple tasks, Sonnet для complex
- Prompt caching для repeated system prompts

### 2. Performance
- Cross-region deployment для low latency
- Streaming для better UX
- Batch processing для high throughput
- Monitor token usage constantly

### 3. Security
- VPC endpoints для private access
- Guardrails для content safety
- IAM roles с least privilege
- Encrypt data at rest и in transit
- CloudTrail logging enabled

### 4. Reliability
- Multi-AZ knowledge bases
- Exponential backoff retries
- Circuit breakers
- Health checks

## References

- **references/bedrock-pricing.md** - Детальный pricing guide
- **references/model-comparison.md** - Сравнение моделей
- **references/knowledge-bases-guide.md** - RAG best practices
- **assets/terraform/bedrock.tf** - IaC templates
- **assets/cloudformation/bedrock-stack.yaml** - CFN templates
