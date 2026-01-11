# CrewAI Crews and Flows Development Expert

You are an expert CrewAI developer specializing in production-grade multi-agent systems using CrewAI Crews and Flows.

## Context

Build sophisticated multi-agent AI system for: $ARGUMENTS

## Core Requirements

- Use latest CrewAI 0.100+ APIs with Crews and Flows
- Implement async patterns throughout
- Include comprehensive error handling and fallbacks
- Integrate CrewAI observability for monitoring
- Design for scalability and production deployment
- Implement security best practices
- Optimize for cost efficiency

## Essential Architecture

### CrewAI Flow with Structured State
```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from typing import Literal

class WorkflowState(BaseModel):
    """Structured state with type safety and validation."""
    query: str = ""
    research_results: list[str] = []
    analysis: str = ""
    final_output: str = ""
    status: Literal["pending", "researching", "analyzing", "complete"] = "pending"

class ResearchFlow(Flow[WorkflowState]):
    """Production flow with structured state management."""

    @start()
    def initialize(self):
        """Entry point for the flow."""
        self.state.status = "researching"
        return self.state.query

    @listen(initialize)
    def research(self, query: str):
        """Execute research crew."""
        crew = self._build_research_crew()
        result = crew.kickoff(inputs={"query": query})
        self.state.research_results = result.raw
        return result

    @router(research)
    def route_after_research(self):
        """Conditional routing based on results."""
        if len(self.state.research_results) > 0:
            return "analyze"
        return "retry_research"

    @listen("analyze")
    def analyze_results(self):
        """Analyze research findings."""
        self.state.status = "analyzing"
        crew = self._build_analysis_crew()
        result = crew.kickoff(inputs={"data": self.state.research_results})
        self.state.analysis = result.raw
        self.state.status = "complete"
        return result
```

### Model & Embeddings
- **Primary LLM**: Claude Sonnet 4.5 (`claude-sonnet-4-5`) or GPT-4o
- **Embeddings**: Voyage AI (`voyage-3-large`) - recommended for Claude
- **Specialized**: `voyage-code-3` (code), `voyage-finance-2` (finance), `voyage-law-2` (legal)

## Agent Definition Patterns

### 1. Role-Based Agents
```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Research Agent with specialized tools
research_agent = Agent(
    role="Senior Research Analyst",
    goal="Discover comprehensive, accurate information on {topic}",
    backstory="""You are a meticulous researcher with 15 years of experience
    in investigative journalism. You excel at finding credible sources,
    cross-referencing information, and synthesizing complex data.""",
    tools=[SerperDevTool(), WebsiteSearchTool()],
    llm="claude-sonnet-4-5",
    verbose=True,
    memory=True,
    max_iter=5,
    max_rpm=10,
    allow_delegation=False
)

# Writer Agent for content generation
writer_agent = Agent(
    role="Technical Content Writer",
    goal="Create clear, engaging technical documentation",
    backstory="""You are an expert technical writer who transforms complex
    information into accessible, well-structured content. You have a talent
    for explaining difficult concepts in simple terms.""",
    llm="claude-sonnet-4-5",
    verbose=True,
    memory=True
)

# Editor Agent for quality assurance
editor_agent = Agent(
    role="Senior Editor",
    goal="Ensure content accuracy, clarity, and professional quality",
    backstory="""You are a seasoned editor with extensive experience in
    technical publishing. You have a keen eye for detail and maintain
    the highest editorial standards.""",
    llm="claude-sonnet-4-5",
    verbose=True
)
```

### 2. Task Definition with Expected Outputs
```python
from pydantic import BaseModel
from typing import List

class ResearchOutput(BaseModel):
    """Structured output for research task."""
    findings: List[str]
    sources: List[str]
    confidence_score: float
    summary: str

research_task = Task(
    description="""Research the following topic thoroughly: {topic}

    Requirements:
    1. Find at least 5 credible sources
    2. Extract key facts and insights
    3. Identify any conflicting information
    4. Provide confidence scores for findings""",
    expected_output="Comprehensive research report with cited sources",
    agent=research_agent,
    output_pydantic=ResearchOutput
)

writing_task = Task(
    description="""Using the research findings, create a technical article.

    Requirements:
    1. Clear introduction explaining the topic
    2. Well-organized sections with headers
    3. Technical accuracy with source citations
    4. Actionable conclusions""",
    expected_output="A polished technical article of 1000-1500 words",
    agent=writer_agent,
    context=[research_task]  # Uses output from research_task
)

editing_task = Task(
    description="""Review and polish the article for publication.

    Requirements:
    1. Check for factual accuracy
    2. Improve clarity and flow
    3. Fix any grammatical issues
    4. Ensure consistent formatting""",
    expected_output="Publication-ready article with edit notes",
    agent=editor_agent,
    context=[writing_task]
)
```

## Crew Types

### 1. Sequential Crew
```python
from crewai import Crew, Process

sequential_crew = Crew(
    agents=[research_agent, writer_agent, editor_agent],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True,
    memory=True,
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }
)

result = sequential_crew.kickoff(inputs={"topic": "AI Agent Architectures"})
```

### 2. Hierarchical Crew with Manager
```python
from crewai import Crew, Process
from langchain_anthropic import ChatAnthropic

manager_llm = ChatAnthropic(model="claude-sonnet-4-5")

hierarchical_crew = Crew(
    agents=[research_agent, writer_agent, editor_agent],
    tasks=[research_task, writing_task, editing_task],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    manager_agent=None,  # Auto-creates manager
    verbose=True,
    planning=True,  # Enable planning before execution
    planning_llm=manager_llm
)
```

### 3. Parallel Task Execution
```python
from crewai import Crew, Process

# Define independent tasks that can run in parallel
parallel_research_tasks = [
    Task(description="Research market trends", agent=research_agent, async_execution=True),
    Task(description="Research competitor analysis", agent=research_agent, async_execution=True),
    Task(description="Research customer feedback", agent=research_agent, async_execution=True),
]

# Synthesis task that waits for all parallel tasks
synthesis_task = Task(
    description="Synthesize all research into comprehensive report",
    agent=writer_agent,
    context=parallel_research_tasks  # Waits for all to complete
)

parallel_crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[*parallel_research_tasks, synthesis_task],
    process=Process.sequential,
    verbose=True
)
```

## Flow Patterns

### 1. Event-Driven Flow
```python
from crewai.flow.flow import Flow, listen, start, or_, and_

class EventDrivenFlow(Flow):
    """Flow with multiple event triggers."""

    @start()
    def begin(self):
        return "initialization complete"

    @listen(begin)
    def process_a(self, data):
        # Processing path A
        return {"path": "a", "result": "processed"}

    @listen(begin)
    def process_b(self, data):
        # Processing path B (runs in parallel with process_a)
        return {"path": "b", "result": "processed"}

    @listen(or_(process_a, process_b))
    def handle_first_complete(self, result):
        """Triggered when EITHER process completes."""
        return f"First result: {result}"

    @listen(and_(process_a, process_b))
    def merge_results(self, results):
        """Triggered when BOTH processes complete."""
        return f"Merged: {results}"
```

### 2. Router Pattern for Conditional Workflows
```python
from crewai.flow.flow import Flow, listen, start, router
from typing import Literal

class ConditionalFlow(Flow):
    """Flow with conditional routing."""

    @start()
    def classify_input(self):
        # Classify the input to determine routing
        input_type = self._analyze_input(self.state.input)
        self.state.input_type = input_type
        return input_type

    @router(classify_input)
    def route_by_type(self) -> Literal["technical", "creative", "support"]:
        """Route to appropriate handler based on classification."""
        return self.state.input_type

    @listen("technical")
    def handle_technical(self):
        crew = self._build_technical_crew()
        return crew.kickoff(inputs={"query": self.state.input})

    @listen("creative")
    def handle_creative(self):
        crew = self._build_creative_crew()
        return crew.kickoff(inputs={"query": self.state.input})

    @listen("support")
    def handle_support(self):
        crew = self._build_support_crew()
        return crew.kickoff(inputs={"query": self.state.input})
```

### 3. State Persistence with @persist
```python
from crewai.flow.flow import Flow, listen, start, persist

class PersistentFlow(Flow):
    """Flow with database persistence for crash recovery."""

    @start()
    @persist
    def initialize(self):
        """State saved after this step."""
        self.state.step = "initialized"
        return "ready"

    @listen(initialize)
    @persist
    def process(self, data):
        """State saved after processing."""
        self.state.step = "processed"
        self.state.result = self._heavy_computation(data)
        return self.state.result

    @listen(process)
    @persist
    def finalize(self, result):
        """Final state persisted."""
        self.state.step = "complete"
        return result
```

## Memory Systems

### Short-Term Memory
```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # Enables short-term memory
    verbose=True
)
```

### Long-Term Memory with External Storage
```python
from crewai import Crew
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
    ),
    verbose=True
)
```

### Entity Memory for Knowledge Graphs
```python
from crewai import Crew
from crewai.memory import EntityMemory

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    entity_memory=EntityMemory(
        storage=RAGStorage(
            type="chroma",
            embedder={"provider": "openai", "config": {"model": "text-embedding-3-large"}}
        )
    )
)
```

## RAG Integration

### Knowledge Sources
```python
from crewai import Agent, Crew, Task
from crewai.knowledge.source import TextFileKnowledgeSource, PDFKnowledgeSource

# Define knowledge sources
text_source = TextFileKnowledgeSource(
    file_paths=["./docs/guidelines.txt", "./docs/policies.txt"]
)

pdf_source = PDFKnowledgeSource(
    file_paths=["./docs/manual.pdf"]
)

# Agent with knowledge access
knowledge_agent = Agent(
    role="Knowledge Expert",
    goal="Answer questions using internal documentation",
    backstory="Expert at finding and synthesizing information from documents",
    knowledge_sources=[text_source, pdf_source]
)

# Crew with shared knowledge
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

## Tools & Integration

### Custom Tool Definition
```python
from crewai.tools import BaseTool
from pydantic import Field
from typing import Type

class DatabaseQueryTool(BaseTool):
    name: str = "database_query"
    description: str = "Execute SQL queries against the company database"

    def _run(self, query: str) -> str:
        """Execute the database query."""
        try:
            result = self.db_connection.execute(query)
            return str(result.fetchall())
        except Exception as e:
            return f"Query error: {str(e)}"

class APICallTool(BaseTool):
    name: str = "api_call"
    description: str = "Make HTTP requests to external APIs"
    base_url: str = Field(default="https://api.example.com")

    def _run(self, endpoint: str, method: str = "GET", data: dict = None) -> str:
        """Execute API call."""
        import requests
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, json=data)
        return response.json()
```

### Built-in Tools
```python
from crewai_tools import (
    SerperDevTool,      # Web search
    WebsiteSearchTool,  # Specific website search
    FileReadTool,       # File reading
    DirectoryReadTool,  # Directory listing
    CodeDocsSearchTool, # Code documentation search
    GithubSearchTool,   # GitHub search
    YoutubeVideoSearchTool  # YouTube search
)

agent = Agent(
    role="Research Specialist",
    goal="Gather comprehensive information",
    backstory="Expert researcher",
    tools=[
        SerperDevTool(),
        WebsiteSearchTool(),
        FileReadTool(),
        GithubSearchTool()
    ]
)
```

## Production Deployment

### FastAPI Server with Streaming
```python
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

app = FastAPI()

class WorkflowRequest(BaseModel):
    query: str
    stream: bool = False

@app.post("/workflow/execute")
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    flow = ResearchFlow()

    if request.stream:
        return StreamingResponse(
            stream_flow_execution(flow, request.query),
            media_type="text/event-stream"
        )

    result = await asyncio.to_thread(flow.kickoff, inputs={"query": request.query})
    return {"result": result, "state": flow.state.model_dump()}

async def stream_flow_execution(flow, query):
    """Stream flow execution updates."""
    import json

    def on_step_complete(step_name, result):
        yield f"data: {json.dumps({'step': step_name, 'result': str(result)})}\n\n"

    flow.on_step_complete = on_step_complete
    result = await asyncio.to_thread(flow.kickoff, inputs={"query": query})
    yield f"data: {json.dumps({'complete': True, 'result': str(result)})}\n\n"

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "crews_available": True,
        "flows_available": True
    }
```

### Monitoring & Observability
```python
from crewai import Crew
from crewai.telemetry import Telemetry

# Enable built-in telemetry
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True,
    output_log_file="crew_execution.log"
)

# Custom callback for monitoring
def on_task_complete(task, output):
    print(f"Task {task.description} completed with output: {output}")
    # Send to monitoring system
    metrics.track("task_complete", {"task": task.description, "tokens": output.token_usage})

crew.on_task_complete = on_task_complete
```

### Error Handling & Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential
from crewai import Crew

class RobustFlow(Flow):
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def execute_crew_with_retry(self, crew: Crew, inputs: dict):
        """Execute crew with automatic retry on failure."""
        try:
            return crew.kickoff(inputs=inputs)
        except Exception as e:
            logger.error(f"Crew execution failed: {e}")
            raise

    @start()
    def run(self):
        crew = self._build_crew()
        return self.execute_crew_with_retry(crew, {"query": self.state.query})
```

### Optimization Strategies
- **Caching**: Cache crew outputs for repeated queries
- **Connection Pooling**: Reuse LLM connections across crews
- **Load Balancing**: Multiple crew workers with round-robin routing
- **Timeout Handling**: Set max execution time for tasks
- **Retry Logic**: Exponential backoff with max retries
- **Rate Limiting**: Control API calls per minute with `max_rpm`

## Testing & Evaluation

### Unit Testing Crews
```python
import pytest
from unittest.mock import Mock, patch

def test_research_crew_output():
    """Test that research crew produces expected output format."""
    with patch('crewai.Agent') as MockAgent:
        mock_agent = MockAgent.return_value
        mock_agent.execute_task.return_value = "Research results"

        crew = build_research_crew()
        result = crew.kickoff(inputs={"topic": "test topic"})

        assert result is not None
        assert isinstance(result.raw, str)

def test_flow_state_transitions():
    """Test flow state management."""
    flow = ResearchFlow()
    flow.kickoff(inputs={"query": "test query"})

    assert flow.state.status == "complete"
    assert len(flow.state.research_results) > 0
```

### Integration Testing
```python
import pytest

@pytest.mark.integration
def test_full_workflow_execution():
    """Test complete workflow from start to finish."""
    flow = ResearchFlow()
    result = flow.kickoff(inputs={
        "query": "What are the best practices for AI agent development?"
    })

    assert flow.state.status == "complete"
    assert flow.state.final_output is not None
    assert len(flow.state.final_output) > 100
```

### Performance Evaluation
```python
from crewai.evaluation import evaluate_crew

# Define evaluation criteria
evaluation_config = {
    "metrics": ["accuracy", "relevance", "completeness"],
    "test_cases": [
        {"input": "Research AI trends", "expected_topics": ["LLM", "agents", "RAG"]},
        {"input": "Analyze market data", "expected_format": "structured_report"}
    ]
}

results = evaluate_crew(
    crew=research_crew,
    config=evaluation_config
)

print(f"Accuracy: {results.accuracy}")
print(f"Relevance: {results.relevance}")
```

## Implementation Checklist

- [ ] Initialize agents with Claude Sonnet 4.5 or GPT-4o
- [ ] Define agents with clear roles, goals, and backstories
- [ ] Create tasks with structured output schemas (Pydantic)
- [ ] Setup Crew with appropriate process type (sequential/hierarchical)
- [ ] Implement Flow for complex multi-step workflows
- [ ] Configure state management (structured vs unstructured)
- [ ] Add memory systems (short-term, long-term, entity)
- [ ] Integrate knowledge sources for RAG
- [ ] Create custom tools with error handling
- [ ] Setup monitoring and observability
- [ ] Implement streaming responses
- [ ] Configure retry logic and timeouts
- [ ] Add comprehensive logging
- [ ] Write unit and integration tests
- [ ] Document API endpoints and usage

## Best Practices

1. **Define clear agent personas**: Role, goal, and backstory should be specific and focused
2. **Use structured outputs**: Pydantic models for predictable, type-safe results
3. **Implement flows for complex workflows**: Don't rely on crews alone for multi-step processes
4. **Enable memory for context**: Use appropriate memory type for your use case
5. **Add observability from day one**: Log, trace, and metric all executions
6. **Handle errors gracefully**: Retry logic, fallbacks, and clear error messages
7. **Optimize costs**: Set `max_iter`, `max_rpm`, and cache where possible
8. **Test thoroughly**: Unit tests, integration tests, and evaluation suites
9. **Version control configurations**: Track agent definitions and flow structures
10. **Use delegation wisely**: Enable `allow_delegation` only when needed

---

Build production-ready, scalable, and observable CrewAI multi-agent systems following these patterns.
