# CrewAI Crew Reference

Complete reference for CrewAI Crew configuration, process types, and orchestration patterns.

## Crew Definition

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True,
    memory=True,
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }
)

result = crew.kickoff(inputs={"topic": "AI Agents"})
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `agents` | list | required | List of Agent instances |
| `tasks` | list | required | List of Task instances |
| `process` | Process | `sequential` | Execution process type |
| `verbose` | bool | `False` | Enable detailed logging |
| `memory` | bool | `False` | Enable crew memory |
| `embedder` | dict | `None` | Embedding configuration |
| `manager_llm` | LLM | `None` | LLM for hierarchical manager |
| `manager_agent` | Agent | `None` | Custom manager agent |
| `planning` | bool | `False` | Enable planning before execution |
| `planning_llm` | LLM | `None` | LLM for planning phase |
| `output_log_file` | str | `None` | Path to log file |
| `full_output` | bool | `False` | Return detailed output |

## Process Types

### 1. Sequential Process

Tasks execute in order, each building on the previous output.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True
)

# Execution order:
# 1. research_task (researcher)
# 2. writing_task (writer) - receives research output
# 3. editing_task (editor) - receives writing output
```

**Best for:**
- Linear workflows
- Tasks with clear dependencies
- Simple pipelines

### 2. Hierarchical Process

A manager agent coordinates and delegates tasks to team members.

```python
from crewai import Crew, Process
from crewai import LLM

manager_llm = LLM(model="anthropic/claude-sonnet-4-5")

crew = Crew(
    agents=[researcher, writer, editor, analyst],
    tasks=[task1, task2, task3, task4],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    planning=True,
    planning_llm=manager_llm,
    verbose=True
)

# Manager automatically:
# 1. Creates execution plan
# 2. Assigns tasks to appropriate agents
# 3. Coordinates between agents
# 4. Synthesizes final output
```

**Best for:**
- Complex projects
- Dynamic task assignment
- Teams with diverse skills

### 3. Parallel Execution

Independent tasks run simultaneously for faster execution.

```python
from crewai import Task, Crew, Process

# Define parallel tasks with async_execution=True
market_research = Task(
    description="Research market trends",
    agent=researcher,
    async_execution=True
)

competitor_analysis = Task(
    description="Analyze competitors",
    agent=researcher,
    async_execution=True
)

customer_feedback = Task(
    description="Analyze customer feedback",
    agent=researcher,
    async_execution=True
)

# Synthesis task waits for all parallel tasks
final_report = Task(
    description="Synthesize all research into report",
    agent=writer,
    context=[market_research, competitor_analysis, customer_feedback]
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[market_research, competitor_analysis, customer_feedback, final_report],
    process=Process.sequential,  # Sequential manages async tasks
    verbose=True
)
```

## Memory Configuration

### Short-Term Memory

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True  # Enables conversation memory
)
```

### Long-Term Memory

```python
from crewai.memory import LongTermMemory
from crewai.memory.storage import RAGStorage

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    long_term_memory=LongTermMemory(
        storage=RAGStorage(
            type="chroma",
            embedder={
                "provider": "openai",
                "config": {"model": "text-embedding-3-large"}
            }
        )
    )
)
```

### Entity Memory

```python
from crewai.memory import EntityMemory

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    entity_memory=EntityMemory(
        storage=RAGStorage(type="chroma", embedder=embedder_config)
    )
)
```

## Knowledge Sources (RAG)

```python
from crewai.knowledge.source import TextFileKnowledgeSource, PDFKnowledgeSource

text_source = TextFileKnowledgeSource(
    file_paths=["./docs/guidelines.txt", "./docs/policies.txt"]
)

pdf_source = PDFKnowledgeSource(
    file_paths=["./docs/manual.pdf"]
)

crew = Crew(
    agents=[knowledge_agent],
    tasks=[query_task],
    knowledge_sources=[text_source, pdf_source],
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }
)
```

## Embedding Providers

### OpenAI

```python
embedder = {
    "provider": "openai",
    "config": {"model": "text-embedding-3-large"}
}
```

### Voyage AI

```python
embedder = {
    "provider": "voyage",
    "config": {"model": "voyage-3-large"}
}
```

### Cohere

```python
embedder = {
    "provider": "cohere",
    "config": {"model": "embed-english-v3.0"}
}
```

## Task Context

Tasks can reference outputs from previous tasks:

```python
research_task = Task(
    description="Research {topic}",
    expected_output="Research findings",
    agent=researcher
)

writing_task = Task(
    description="Write article based on research",
    expected_output="Draft article",
    agent=writer,
    context=[research_task]  # Receives research output
)

editing_task = Task(
    description="Edit the article",
    expected_output="Final article",
    agent=editor,
    context=[writing_task]  # Receives writing output
)
```

## Structured Outputs

```python
from pydantic import BaseModel
from typing import List

class ResearchOutput(BaseModel):
    findings: List[str]
    sources: List[str]
    confidence: float

research_task = Task(
    description="Research {topic}",
    expected_output="Research findings",
    agent=researcher,
    output_pydantic=ResearchOutput
)

crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential
)

result = crew.kickoff(inputs={"topic": "AI"})
# result.pydantic contains structured ResearchOutput
```

## Callbacks

```python
def on_task_complete(task, output):
    """Called when a task completes."""
    print(f"Task completed: {task.description}")
    print(f"Output: {output}")

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential
)

crew.on_task_complete = on_task_complete
result = crew.kickoff(inputs={"topic": "AI"})
```

## Planning Mode

```python
from crewai import LLM

planning_llm = LLM(model="anthropic/claude-sonnet-4-5")

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    planning=True,
    planning_llm=planning_llm,
    verbose=True
)

# Before execution, crew creates a plan:
# 1. Analyzes all tasks and dependencies
# 2. Creates optimal execution strategy
# 3. Follows plan during execution
```

## Error Handling

```python
try:
    result = crew.kickoff(inputs={"topic": "AI"})
except Exception as e:
    print(f"Crew execution failed: {e}")
    # Handle failure (retry, fallback, etc.)
```

### With Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def execute_crew_with_retry(crew, inputs):
    return crew.kickoff(inputs=inputs)

result = execute_crew_with_retry(crew, {"topic": "AI"})
```

## Common Patterns

### Research Pipeline

```python
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[
        Task(description="Research {topic}", agent=researcher),
        Task(description="Analyze findings", agent=analyst, context=[research_task]),
        Task(description="Write report", agent=writer, context=[analysis_task])
    ],
    process=Process.sequential,
    memory=True
)
```

### Code Review Pipeline

```python
crew = Crew(
    agents=[reviewer, security_analyst, qa_engineer],
    tasks=[
        Task(description="Review code quality", agent=reviewer),
        Task(description="Check security issues", agent=security_analyst),
        Task(description="Verify test coverage", agent=qa_engineer)
    ],
    process=Process.sequential
)
```

### Content Creation Pipeline

```python
crew = Crew(
    agents=[researcher, writer, editor, designer],
    tasks=[
        Task(description="Research topic", agent=researcher),
        Task(description="Write content", agent=writer),
        Task(description="Edit content", agent=editor),
        Task(description="Create visuals", agent=designer)
    ],
    process=Process.sequential,
    memory=True
)
```

## Troubleshooting

### Crew Hangs

```python
# Set timeouts on agents
agent = Agent(
    role="Researcher",
    goal="Research topic",
    backstory="Expert",
    max_iter=5  # Prevent infinite loops
)
```

### Memory Errors

```python
# Use external storage for large memory
from crewai.memory.storage import RAGStorage

storage = RAGStorage(
    type="chroma",
    persist_directory="./crew_memory"
)
```

### Rate Limiting

```python
# Set rate limits on agents
agent = Agent(
    role="Researcher",
    goal="Research",
    backstory="Expert",
    max_rpm=10  # Max 10 requests per minute
)
```
