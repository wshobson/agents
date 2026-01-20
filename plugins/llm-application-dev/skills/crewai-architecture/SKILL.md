---
name: crewai-architecture
description: Design multi-agent AI applications using the CrewAI framework with Crews, Flows, and orchestration patterns. Use when building multi-agent systems, implementing AI workflows, or creating complex agent collaborations.
---

# CrewAI Architecture

Master the CrewAI framework for building sophisticated multi-agent AI applications with Crews, Flows, state management, and agent orchestration.

## When to Use This Skill

- Building multi-agent collaborative AI systems
- Implementing complex multi-step AI workflows
- Managing agent state and workflow orchestration
- Creating role-based AI teams that work together
- Building production-grade agentic applications
- Implementing hierarchical agent management
- Creating event-driven AI workflows
- Designing AI systems with specialized agent roles

## Core Concepts

### 1. Agents
Autonomous entities with specific roles, goals, and capabilities.

**Agent Components:**
- **Role**: The agent's job title or function (e.g., "Senior Research Analyst")
- **Goal**: What the agent aims to achieve
- **Backstory**: Context that shapes agent behavior and expertise
- **Tools**: External capabilities the agent can use
- **LLM**: The language model powering the agent

**Agent Configuration:**
- `verbose`: Enable detailed logging
- `memory`: Enable short-term memory
- `max_iter`: Maximum reasoning iterations
- `max_rpm`: Rate limiting for API calls
- `allow_delegation`: Whether agent can delegate to others

### 2. Tasks
Discrete units of work assigned to agents.

**Task Components:**
- **Description**: Detailed instructions for the task
- **Expected Output**: What the completed task should produce
- **Agent**: The agent responsible for execution
- **Context**: Previous tasks whose outputs inform this task
- **Output Schema**: Pydantic model for structured outputs

**Task Execution Modes:**
- Synchronous execution (default)
- `async_execution=True` for parallel processing

### 3. Crews
Teams of agents working together on tasks.

**Process Types:**
- **Sequential**: Tasks executed in order, each building on previous
- **Hierarchical**: Manager agent coordinates and delegates
- **Parallel**: Independent tasks run simultaneously

**Crew Features:**
- Shared memory across agents
- Knowledge sources for RAG
- Configurable embedding providers
- Planning mode for complex tasks

### 4. Flows
Orchestration layer for complex multi-step workflows.

**Flow Features:**
- Event-driven architecture with decorators
- Structured and unstructured state management
- Conditional routing between steps
- State persistence for crash recovery
- Parallel execution paths

**Key Decorators:**
- `@start()`: Entry point of the flow
- `@listen(event)`: Triggered when event completes
- `@router(event)`: Conditional routing after event
- `@persist`: Save state to database after step

## Quick Start

```python
from crewai import Agent, Task, Crew, Process

# Define an agent
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate information on {topic}",
    backstory="Expert researcher with attention to detail",
    verbose=True
)

# Define a task
research_task = Task(
    description="Research the following topic: {topic}",
    expected_output="Comprehensive summary with key findings",
    agent=researcher
)

# Create and run a crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI Agent Architectures"})
print(result.raw)
```

## Architecture Patterns

### Pattern 1: Sequential Multi-Agent Pipeline
```python
from crewai import Agent, Task, Crew, Process

# Research -> Write -> Edit pipeline
researcher = Agent(
    role="Researcher",
    goal="Gather comprehensive information",
    backstory="Expert at finding credible sources"
)

writer = Agent(
    role="Writer",
    goal="Create clear, engaging content",
    backstory="Skilled technical writer"
)

editor = Agent(
    role="Editor",
    goal="Polish content to publication quality",
    backstory="Meticulous editor with high standards"
)

research_task = Task(
    description="Research {topic}",
    expected_output="Research findings with sources",
    agent=researcher
)

writing_task = Task(
    description="Write article based on research",
    expected_output="Draft article",
    agent=writer,
    context=[research_task]
)

editing_task = Task(
    description="Edit and polish the article",
    expected_output="Final article",
    agent=editor,
    context=[writing_task]
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential
)
```

### Pattern 2: Hierarchical Crew with Manager
```python
from crewai import Crew, Process
from langchain_anthropic import ChatAnthropic

manager_llm = ChatAnthropic(model="claude-sonnet-4-5")

hierarchical_crew = Crew(
    agents=[researcher, writer, editor, analyst],
    tasks=[task1, task2, task3, task4],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    planning=True,
    planning_llm=manager_llm,
    verbose=True
)

# Manager automatically coordinates agents and delegates tasks
result = hierarchical_crew.kickoff(inputs={"project": "market analysis"})
```

### Pattern 3: Flow with Structured State
```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from typing import Literal

class AnalysisState(BaseModel):
    query: str = ""
    data: list = []
    analysis: str = ""
    status: Literal["pending", "processing", "complete"] = "pending"

class AnalysisFlow(Flow[AnalysisState]):

    @start()
    def gather_data(self):
        self.state.status = "processing"
        crew = self._build_data_crew()
        result = crew.kickoff(inputs={"query": self.state.query})
        self.state.data = result.raw
        return result

    @listen(gather_data)
    def analyze(self, data):
        crew = self._build_analysis_crew()
        result = crew.kickoff(inputs={"data": self.state.data})
        self.state.analysis = result.raw
        self.state.status = "complete"
        return result

# Execute flow
flow = AnalysisFlow()
result = flow.kickoff(inputs={"query": "market trends 2024"})
print(flow.state.analysis)
```

### Pattern 4: Conditional Routing in Flows
```python
from crewai.flow.flow import Flow, listen, start, router
from typing import Literal

class RoutingFlow(Flow):

    @start()
    def classify(self):
        # Classify input to determine routing
        classification = self._classify_input(self.state.input)
        self.state.classification = classification
        return classification

    @router(classify)
    def route(self) -> Literal["technical", "creative", "support"]:
        return self.state.classification

    @listen("technical")
    def handle_technical(self):
        return self._technical_crew().kickoff(inputs=self.state.dict())

    @listen("creative")
    def handle_creative(self):
        return self._creative_crew().kickoff(inputs=self.state.dict())

    @listen("support")
    def handle_support(self):
        return self._support_crew().kickoff(inputs=self.state.dict())
```

## State Management Best Practices

### Unstructured State (Flexible)
```python
from crewai.flow.flow import Flow, listen, start

class FlexibleFlow(Flow):
    """State attributes added dynamically."""

    @start()
    def begin(self):
        self.state.step = "started"
        self.state.data = []
        return "initialized"

    @listen(begin)
    def process(self, result):
        self.state.processed = True
        self.state.custom_field = "any value"
        return self.state
```

### Structured State (Type-Safe)
```python
from crewai.flow.flow import Flow
from pydantic import BaseModel, Field
from typing import List, Optional

class TypedState(BaseModel):
    """Type-safe state with validation."""
    query: str
    results: List[str] = Field(default_factory=list)
    score: float = 0.0
    metadata: Optional[dict] = None

class TypedFlow(Flow[TypedState]):
    """Flow with type checking and validation."""

    @start()
    def process(self):
        # IDE autocomplete and type checking work
        self.state.results.append("new result")
        self.state.score = 0.95
        return self.state
```

### State Persistence
```python
from crewai.flow.flow import Flow, persist

class PersistentFlow(Flow):
    """Flow with database persistence."""

    @start()
    @persist
    def step_one(self):
        """State saved after execution."""
        self.state.checkpoint = "step_one_complete"
        return "done"

    @listen(step_one)
    @persist
    def step_two(self, data):
        """Recoverable if crash occurs."""
        self.state.checkpoint = "step_two_complete"
        return "done"
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

## Tool Integration

### Custom Tools
```python
from crewai.tools import BaseTool

class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search for information"

    def _run(self, query: str) -> str:
        # Implementation
        return f"Results for: {query}"

agent = Agent(
    role="Researcher",
    goal="Find information",
    tools=[SearchTool()]
)
```

### Built-in Tools
```python
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    FileReadTool,
    DirectoryReadTool
)

agent = Agent(
    role="Analyst",
    goal="Analyze data",
    tools=[
        SerperDevTool(),
        FileReadTool()
    ]
)
```

## Testing Strategies

```python
import pytest
from unittest.mock import Mock, patch

def test_crew_execution():
    crew = build_test_crew()
    result = crew.kickoff(inputs={"topic": "test"})
    assert result is not None
    assert len(result.raw) > 0

def test_flow_state():
    flow = TestFlow()
    flow.kickoff(inputs={"query": "test"})
    assert flow.state.status == "complete"

@pytest.mark.integration
def test_full_pipeline():
    flow = ProductionFlow()
    result = flow.kickoff(inputs={"data": sample_data})
    assert flow.state.processed is True
```

## Performance Optimization

1. **Rate Limiting**: Set `max_rpm` on agents
2. **Iteration Limits**: Use `max_iter` to prevent loops
3. **Caching**: Enable response caching for repeated queries
4. **Parallel Tasks**: Use `async_execution=True` for independent tasks
5. **Streaming**: Enable streaming for real-time output

## Resources

- **references/agents.md**: Deep dive on agent configuration
- **references/crews.md**: Crew composition patterns
- **references/flows.md**: Flow orchestration guide
- **references/memory.md**: Memory system patterns
- **assets/crew-template.py**: Production crew template
- **assets/flow-template.py**: Production flow template

## Common Pitfalls

1. **Vague Agent Roles**: Unclear goals lead to poor performance
2. **Missing Context**: Tasks without context lose information
3. **No Error Handling**: Unhandled failures crash workflows
4. **Memory Overflow**: Not managing conversation length
5. **Over-delegation**: Too much delegation slows execution
6. **Unstructured State**: Dynamic state causes type errors
7. **No Persistence**: Long workflows lost on crash
8. **Missing Rate Limits**: API quotas exceeded

## Production Checklist

- [ ] Define clear agent roles and goals
- [ ] Use structured outputs with Pydantic
- [ ] Configure appropriate process type
- [ ] Implement Flows for complex workflows
- [ ] Enable memory for context retention
- [ ] Add state persistence for reliability
- [ ] Set rate limits and iteration caps
- [ ] Implement error handling and retries
- [ ] Add monitoring and logging
- [ ] Write comprehensive tests
