# CrewAI Agent Reference

Complete reference for CrewAI Agent configuration, optimization, and best practices.

## Agent Definition

```python
from crewai import Agent, LLM

agent = Agent(
    role="Senior Research Analyst",
    goal="Discover comprehensive, accurate information on {topic}",
    backstory="""You are a meticulous researcher with 15 years of experience
    in investigative journalism. You excel at finding credible sources,
    cross-referencing information, and synthesizing complex data.""",
    tools=[search_tool, scrape_tool],
    llm=LLM(model="anthropic/claude-sonnet-4-5"),
    verbose=True,
    memory=True,
    max_iter=5,
    max_rpm=10,
    allow_delegation=False
)
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `role` | str | required | The agent's job title or function |
| `goal` | str | required | What the agent aims to achieve |
| `backstory` | str | required | Context that shapes agent behavior |
| `tools` | list | `[]` | External capabilities the agent can use |
| `llm` | LLM/str | default | The language model powering the agent |
| `verbose` | bool | `False` | Enable detailed logging |
| `memory` | bool | `False` | Enable short-term memory |
| `max_iter` | int | `25` | Maximum reasoning iterations |
| `max_rpm` | int | `None` | Rate limiting for API calls |
| `allow_delegation` | bool | `False` | Whether agent can delegate to others |
| `cache` | bool | `True` | Enable response caching |
| `step_callback` | callable | `None` | Callback after each step |

## LLM Configuration

### Using Anthropic Claude

```python
from crewai import LLM

# Claude Sonnet 4.5
llm = LLM(model="anthropic/claude-sonnet-4-5")

# Claude Haiku (faster, cheaper)
llm = LLM(model="anthropic/claude-haiku-3-5")

# With custom parameters
llm = LLM(
    model="anthropic/claude-sonnet-4-5",
    temperature=0.7,
    max_tokens=4096
)
```

### Using OpenAI GPT

```python
# GPT-4o
llm = LLM(model="openai/gpt-4o")

# GPT-4o Mini (faster, cheaper)
llm = LLM(model="openai/gpt-4o-mini")
```

### Using Local Models (Ollama)

```python
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)
```

## Role Design Best Practices

### 1. Be Specific About Expertise

**Bad:**
```python
role="Assistant"
goal="Help with tasks"
```

**Good:**
```python
role="Senior Financial Analyst"
goal="Analyze quarterly earnings reports and identify key trends"
```

### 2. Write Detailed Backstories

**Bad:**
```python
backstory="You are helpful."
```

**Good:**
```python
backstory="""You are a CFA-certified financial analyst with 10 years of
experience at top investment banks. You specialize in tech sector analysis
and have a track record of accurate earnings predictions. You approach
each analysis methodically, cross-referencing multiple data sources."""
```

### 3. Match Tools to Role

```python
# Research Agent - search and scraping tools
research_agent = Agent(
    role="Research Specialist",
    goal="Find comprehensive information",
    backstory="Expert researcher with attention to detail",
    tools=[SerperDevTool(), WebsiteSearchTool(), FileReadTool()]
)

# Code Agent - code execution tools
code_agent = Agent(
    role="Senior Developer",
    goal="Write clean, tested code",
    backstory="Expert programmer with 15 years experience",
    tools=[CodeInterpreterTool(), GitHubSearchTool()]
)
```

## Memory Configuration

### Short-Term Memory

```python
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    memory=True  # Enables conversation memory
)
```

### Custom Memory Provider

```python
from crewai.memory import MemoryConfig

agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    memory_config=MemoryConfig(
        provider="chroma",
        embedding_model="text-embedding-3-large"
    )
)
```

## Rate Limiting

```python
# Limit to 10 requests per minute
agent = Agent(
    role="Researcher",
    goal="Search for information",
    backstory="Expert researcher",
    max_rpm=10,  # Rate limit
    max_iter=5   # Max reasoning iterations
)
```

## Delegation

### Enable Delegation

```python
manager = Agent(
    role="Project Manager",
    goal="Coordinate team efforts",
    backstory="Experienced PM",
    allow_delegation=True  # Can delegate to other agents
)

worker = Agent(
    role="Developer",
    goal="Implement features",
    backstory="Senior developer",
    allow_delegation=False  # Cannot delegate
)
```

### Delegation Flow

When `allow_delegation=True`:
1. Agent receives task
2. Agent can ask other agents for help
3. Results are synthesized by delegating agent

## Callbacks and Hooks

```python
def on_step(step_output):
    """Called after each agent step."""
    print(f"Step completed: {step_output}")
    # Log to monitoring system
    metrics.track("agent_step", {"output": str(step_output)})

agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    step_callback=on_step
)
```

## Common Patterns

### 1. Specialized Research Agent

```python
research_agent = Agent(
    role="Senior Research Analyst",
    goal="Discover comprehensive, accurate information on {topic}",
    backstory="""Meticulous researcher with 15 years of experience.
    Expert at finding credible sources and synthesizing complex data.""",
    tools=[SerperDevTool(), WebsiteSearchTool()],
    llm=LLM(model="anthropic/claude-sonnet-4-5"),
    verbose=True,
    memory=True,
    max_iter=5,
    max_rpm=10
)
```

### 2. Code Generation Agent

```python
developer_agent = Agent(
    role="Senior Software Engineer",
    goal="Write clean, efficient, well-tested code for {task}",
    backstory="""Expert programmer with 15 years of experience in
    Python, JavaScript, and cloud architectures. Strong believer in
    TDD and clean code principles.""",
    tools=[CodeInterpreterTool(), FileReadTool(), FileWriteTool()],
    llm=LLM(model="anthropic/claude-sonnet-4-5"),
    verbose=True,
    max_iter=10
)
```

### 3. Quality Assurance Agent

```python
qa_agent = Agent(
    role="Quality Assurance Engineer",
    goal="Verify code quality and identify bugs in {code}",
    backstory="""Expert QA engineer with a keen eye for edge cases
    and potential issues. Thorough and methodical in testing.""",
    tools=[CodeInterpreterTool(), run_tests],
    llm=LLM(model="anthropic/claude-sonnet-4-5"),
    verbose=True
)
```

## Troubleshooting

### Agent Not Using Tools

```python
# Ensure tools are properly configured
from crewai_tools import SerperDevTool

tool = SerperDevTool()  # Must be instantiated
agent = Agent(
    role="Researcher",
    goal="Search for information",
    backstory="Expert researcher",
    tools=[tool]  # Pass instance, not class
)
```

### Agent Stuck in Loop

```python
# Set max iterations to prevent infinite loops
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    max_iter=5  # Stop after 5 iterations
)
```

### Rate Limit Errors

```python
# Add rate limiting
agent = Agent(
    role="Researcher",
    goal="Search extensively",
    backstory="Thorough researcher",
    max_rpm=5  # Maximum 5 requests per minute
)
```
