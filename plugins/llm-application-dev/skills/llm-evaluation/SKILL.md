---
name: llm-evaluation
description: Implement comprehensive evaluation strategies for LLM applications using automated metrics, human feedback, and benchmarking. Use when testing LLM performance, measuring AI application quality, or establishing evaluation frameworks.
---

# LLM Evaluation

Master comprehensive evaluation strategies for LLM applications, from automated metrics to human evaluation and A/B testing.

## When to Use This Skill

- Measuring LLM application performance systematically
- Comparing different models or prompts
- Detecting performance regressions before deployment
- Validating improvements from prompt changes
- Building confidence in production systems
- Establishing baselines and tracking progress over time
- Debugging unexpected model behavior

## Core Evaluation Types

### 1. Automated Metrics

Fast, repeatable, scalable evaluation using computed scores.

**Text Generation:**

- **BLEU**: N-gram overlap (translation)
- **ROUGE**: Recall-oriented (summarization)
- **METEOR**: Semantic similarity
- **BERTScore**: Embedding-based similarity
- **Perplexity**: Language model confidence

**Classification:**

- **Accuracy**: Percentage correct
- **Precision/Recall/F1**: Class-specific performance
- **Confusion Matrix**: Error patterns
- **AUC-ROC**: Ranking quality

**Retrieval (RAG):**

- **MRR**: Mean Reciprocal Rank
- **NDCG**: Normalized Discounted Cumulative Gain
- **Precision@K**: Relevant in top K
- **Recall@K**: Coverage in top K

### 2. Human Evaluation

Manual assessment for quality aspects difficult to automate.

**Dimensions:**

- **Accuracy**: Factual correctness
- **Coherence**: Logical flow
- **Relevance**: Answers the question
- **Fluency**: Natural language quality
- **Safety**: No harmful content
- **Helpfulness**: Useful to the user

### 3. LLM-as-Judge

Use stronger LLMs to evaluate weaker model outputs.

**Approaches:**

- **Pointwise**: Score individual responses
- **Pairwise**: Compare two responses
- **Reference-based**: Compare to gold standard
- **Reference-free**: Judge without ground truth

## Quick Start

```python
from dataclasses import dataclass
from typing import Callable
import numpy as np

@dataclass
class Metric:
    name: str
    fn: Callable

    @staticmethod
    def accuracy():
        return Metric("accuracy", calculate_accuracy)

    @staticmethod
    def bleu():
        return Metric("bleu", calculate_bleu)

    @staticmethod
    def bertscore():
        return Metric("bertscore", calculate_bertscore)

    @staticmethod
    def custom(name: str, fn: Callable):
        return Metric(name, fn)

class EvaluationSuite:
    def __init__(self, metrics: list[Metric]):
        self.metrics = metrics

    async def evaluate(self, model, test_cases: list[dict]) -> dict:
        results = {m.name: [] for m in self.metrics}

        for test in test_cases:
            prediction = await model.predict(test["input"])

            for metric in self.metrics:
                score = metric.fn(
                    prediction=prediction,
                    reference=test.get("expected"),
                    context=test.get("context")
                )
                results[metric.name].append(score)

        return {
            "metrics": {k: np.mean(v) for k, v in results.items()},
            "raw_scores": results
        }

# Usage
suite = EvaluationSuite([
    Metric.accuracy(),
    Metric.bleu(),
    Metric.bertscore(),
    Metric.custom("groundedness", check_groundedness)
])

test_cases = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe. Paris is its capital."
    },
]

results = await suite.evaluate(model=your_model, test_cases=test_cases)
```

## Automated Metrics Implementation

### BLEU Score

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference: str, hypothesis: str, **kwargs) -> float:
    """Calculate BLEU score between reference and hypothesis."""
    smoothie = SmoothingFunction().method4

    return sentence_bleu(
        [reference.split()],
        hypothesis.split(),
        smoothing_function=smoothie
    )
```

### ROUGE Score

```python
from rouge_score import rouge_scorer

def calculate_rouge(reference: str, hypothesis: str, **kwargs) -> dict:
    """Calculate ROUGE scores."""
    scorer = rouge_scorer.RougeScorer(
        ['rouge1', 'rouge2', 'rougeL'],
        use_stemmer=True
    )
    scores = scorer.score(reference, hypothesis)

    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }
```

### BERTScore

```python
from bert_score import score

def calculate_bertscore(
    references: list[str],
    hypotheses: list[str],
    **kwargs
) -> dict:
    """Calculate BERTScore using pre-trained model."""
    P, R, F1 = score(
        hypotheses,
        references,
        lang='en',
        model_type='microsoft/deberta-xlarge-mnli'
    )

    return {
        'precision': P.mean().item(),
        'recall': R.mean().item(),
        'f1': F1.mean().item()
    }
```

### Custom Metrics

```python
def calculate_groundedness(response: str, context: str, **kwargs) -> float:
    """Check if response is grounded in provided context."""
    from transformers import pipeline

    nli = pipeline(
        "text-classification",
        model="microsoft/deberta-large-mnli"
    )

    result = nli(f"{context} [SEP] {response}")[0]

    # Return confidence that response is entailed by context
    return result['score'] if result['label'] == 'ENTAILMENT' else 0.0

def calculate_toxicity(text: str, **kwargs) -> float:
    """Measure toxicity in generated text."""
    from detoxify import Detoxify

    results = Detoxify('original').predict(text)
    return max(results.values())  # Return highest toxicity score

def calculate_factuality(claim: str, sources: list[str], **kwargs) -> float:
    """Verify factual claims against sources."""
    from transformers import pipeline

    nli = pipeline("text-classification", model="facebook/bart-large-mnli")

    scores = []
    for source in sources:
        result = nli(f"{source}</s></s>{claim}")[0]
        if result['label'] == 'entailment':
            scores.append(result['score'])

    return max(scores) if scores else 0.0
```

## LLM-as-Judge Patterns

### Single Output Evaluation

```python
from anthropic import Anthropic
from pydantic import BaseModel, Field
import json

class QualityRating(BaseModel):
    accuracy: int = Field(ge=1, le=10, description="Factual correctness")
    helpfulness: int = Field(ge=1, le=10, description="Answers the question")
    clarity: int = Field(ge=1, le=10, description="Well-written and understandable")
    reasoning: str = Field(description="Brief explanation")

async def llm_judge_quality(
    response: str,
    question: str,
    context: str = None
) -> QualityRating:
    """Use Claude to judge response quality."""
    client = Anthropic()

    system = """You are an expert evaluator of AI responses.
    Rate responses on accuracy, helpfulness, and clarity (1-10 scale).
    Provide brief reasoning for your ratings."""

    prompt = f"""Rate the following response:

Question: {question}
{f'Context: {context}' if context else ''}
Response: {response}

Provide ratings in JSON format:
{{
  "accuracy": <1-10>,
  "helpfulness": <1-10>,
  "clarity": <1-10>,
  "reasoning": "<brief explanation>"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    return QualityRating(**json.loads(message.content[0].text))
```

### Pairwise Comparison

```python
from pydantic import BaseModel, Field
from typing import Literal

class ComparisonResult(BaseModel):
    winner: Literal["A", "B", "tie"]
    reasoning: str
    confidence: int = Field(ge=1, le=10)

async def compare_responses(
    question: str,
    response_a: str,
    response_b: str
) -> ComparisonResult:
    """Compare two responses using LLM judge."""
    client = Anthropic()

    prompt = f"""Compare these two responses and determine which is better.

Question: {question}

Response A: {response_a}

Response B: {response_b}

Consider accuracy, helpfulness, and clarity.

Answer with JSON:
{{
  "winner": "A" or "B" or "tie",
  "reasoning": "<explanation>",
  "confidence": <1-10>
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return ComparisonResult(**json.loads(message.content[0].text))
```

### Reference-Based Evaluation

```python
class ReferenceEvaluation(BaseModel):
    semantic_similarity: float = Field(ge=0, le=1)
    factual_accuracy: float = Field(ge=0, le=1)
    completeness: float = Field(ge=0, le=1)
    issues: list[str]

async def evaluate_against_reference(
    response: str,
    reference: str,
    question: str
) -> ReferenceEvaluation:
    """Evaluate response against gold standard reference."""
    client = Anthropic()

    prompt = f"""Compare the response to the reference answer.

Question: {question}
Reference Answer: {reference}
Response to Evaluate: {response}

Evaluate:
1. Semantic similarity (0-1): How similar is the meaning?
2. Factual accuracy (0-1): Are all facts correct?
3. Completeness (0-1): Does it cover all key points?
4. List any specific issues or errors.

Respond in JSON:
{{
  "semantic_similarity": <0-1>,
  "factual_accuracy": <0-1>,
  "completeness": <0-1>,
  "issues": ["issue1", "issue2"]
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return ReferenceEvaluation(**json.loads(message.content[0].text))
```

## Human Evaluation Frameworks

### Annotation Guidelines

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AnnotationTask:
    """Structure for human annotation task."""
    response: str
    question: str
    context: Optional[str] = None

    def get_annotation_form(self) -> dict:
        return {
            "question": self.question,
            "context": self.context,
            "response": self.response,
            "ratings": {
                "accuracy": {
                    "scale": "1-5",
                    "description": "Is the response factually correct?"
                },
                "relevance": {
                    "scale": "1-5",
                    "description": "Does it answer the question?"
                },
                "coherence": {
                    "scale": "1-5",
                    "description": "Is it logically consistent?"
                }
            },
            "issues": {
                "factual_error": False,
                "hallucination": False,
                "off_topic": False,
                "unsafe_content": False
            },
            "feedback": ""
        }
```

### Inter-Rater Agreement

```python
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(
    rater1_scores: list[int],
    rater2_scores: list[int]
) -> dict:
    """Calculate inter-rater agreement."""
    kappa = cohen_kappa_score(rater1_scores, rater2_scores)

    if kappa < 0:
        interpretation = "Poor"
    elif kappa < 0.2:
        interpretation = "Slight"
    elif kappa < 0.4:
        interpretation = "Fair"
    elif kappa < 0.6:
        interpretation = "Moderate"
    elif kappa < 0.8:
        interpretation = "Substantial"
    else:
        interpretation = "Almost Perfect"

    return {
        "kappa": kappa,
        "interpretation": interpretation
    }
```

## A/B Testing

### Statistical Testing Framework

```python
from scipy import stats
import numpy as np
from dataclasses import dataclass, field

@dataclass
class ABTest:
    variant_a_name: str = "A"
    variant_b_name: str = "B"
    variant_a_scores: list[float] = field(default_factory=list)
    variant_b_scores: list[float] = field(default_factory=list)

    def add_result(self, variant: str, score: float):
        """Add evaluation result for a variant."""
        if variant == "A":
            self.variant_a_scores.append(score)
        else:
            self.variant_b_scores.append(score)

    def analyze(self, alpha: float = 0.05) -> dict:
        """Perform statistical analysis."""
        a_scores = np.array(self.variant_a_scores)
        b_scores = np.array(self.variant_b_scores)

        # T-test
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(a_scores)**2 + np.std(b_scores)**2) / 2)
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            "variant_a_mean": np.mean(a_scores),
            "variant_b_mean": np.mean(b_scores),
            "difference": np.mean(b_scores) - np.mean(a_scores),
            "relative_improvement": (np.mean(b_scores) - np.mean(a_scores)) / np.mean(a_scores),
            "p_value": p_value,
            "statistically_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "effect_size": self._interpret_cohens_d(cohens_d),
            "winner": self.variant_b_name if np.mean(b_scores) > np.mean(a_scores) else self.variant_a_name
        }

    @staticmethod
    def _interpret_cohens_d(d: float) -> str:
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
```

## Regression Testing

### Regression Detection

```python
from dataclasses import dataclass

@dataclass
class RegressionResult:
    metric: str
    baseline: float
    current: float
    change: float
    is_regression: bool

class RegressionDetector:
    def __init__(self, baseline_results: dict, threshold: float = 0.05):
        self.baseline = baseline_results
        self.threshold = threshold

    def check_for_regression(self, new_results: dict) -> dict:
        """Detect if new results show regression."""
        regressions = []

        for metric in self.baseline.keys():
            baseline_score = self.baseline[metric]
            new_score = new_results.get(metric)

            if new_score is None:
                continue

            # Calculate relative change
            relative_change = (new_score - baseline_score) / baseline_score

            # Flag if significant decrease
            is_regression = relative_change < -self.threshold
            if is_regression:
                regressions.append(RegressionResult(
                    metric=metric,
                    baseline=baseline_score,
                    current=new_score,
                    change=relative_change,
                    is_regression=True
                ))

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions,
            "summary": f"{len(regressions)} metric(s) regressed"
        }
```

## LangSmith Evaluation Integration

```python
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator

# Initialize LangSmith client
client = Client()

# Create dataset
dataset = client.create_dataset("qa_test_cases")
client.create_examples(
    inputs=[{"question": q} for q in questions],
    outputs=[{"answer": a} for a in expected_answers],
    dataset_id=dataset.id
)

# Define evaluators
evaluators = [
    LangChainStringEvaluator("qa"),           # QA correctness
    LangChainStringEvaluator("context_qa"),   # Context-grounded QA
    LangChainStringEvaluator("cot_qa"),       # Chain-of-thought QA
]

# Run evaluation
async def target_function(inputs: dict) -> dict:
    result = await your_chain.ainvoke(inputs)
    return {"answer": result}

experiment_results = await evaluate(
    target_function,
    data=dataset.name,
    evaluators=evaluators,
    experiment_prefix="v1.0.0",
    metadata={"model": "claude-sonnet-4-5", "version": "1.0.0"}
)

print(f"Mean score: {experiment_results.aggregate_metrics['qa']['mean']}")
```

## Benchmarking

### Running Benchmarks

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class BenchmarkResult:
    metric: str
    mean: float
    std: float
    min: float
    max: float

class BenchmarkRunner:
    def __init__(self, benchmark_dataset: list[dict]):
        self.dataset = benchmark_dataset

    async def run_benchmark(
        self,
        model,
        metrics: list[Metric]
    ) -> dict[str, BenchmarkResult]:
        """Run model on benchmark and calculate metrics."""
        results = {metric.name: [] for metric in metrics}

        for example in self.dataset:
            # Generate prediction
            prediction = await model.predict(example["input"])

            # Calculate each metric
            for metric in metrics:
                score = metric.fn(
                    prediction=prediction,
                    reference=example["reference"],
                    context=example.get("context")
                )
                results[metric.name].append(score)

        # Aggregate results
        return {
            metric: BenchmarkResult(
                metric=metric,
                mean=np.mean(scores),
                std=np.std(scores),
                min=min(scores),
                max=max(scores)
            )
            for metric, scores in results.items()
        }
```

## Resources

- [LangSmith Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [RAGAS Framework](https://docs.ragas.io/)
- [DeepEval Library](https://docs.deepeval.com/)
- [Arize Phoenix](https://docs.arize.com/phoenix/)
- [HELM Benchmark](https://crfm.stanford.edu/helm/)

## Best Practices

1. **Multiple Metrics**: Use diverse metrics for comprehensive view
2. **Representative Data**: Test on real-world, diverse examples
3. **Baselines**: Always compare against baseline performance
4. **Statistical Rigor**: Use proper statistical tests for comparisons
5. **Continuous Evaluation**: Integrate into CI/CD pipeline
6. **Human Validation**: Combine automated metrics with human judgment
7. **Error Analysis**: Investigate failures to understand weaknesses
8. **Version Control**: Track evaluation results over time

## Common Pitfalls

- **Single Metric Obsession**: Optimizing for one metric at the expense of others
- **Small Sample Size**: Drawing conclusions from too few examples
- **Data Contamination**: Testing on training data
- **Ignoring Variance**: Not accounting for statistical uncertainty
- **Metric Mismatch**: Using metrics not aligned with business goals
- **Position Bias**: In pairwise evals, randomize order
- **Overfitting Prompts**: Optimizing for test set instead of real use
