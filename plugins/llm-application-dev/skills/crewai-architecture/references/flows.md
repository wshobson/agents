# CrewAI Flow Reference

Complete reference for CrewAI Flow orchestration, state management, decorators, and routing patterns.

## Flow Definition

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel

class WorkflowState(BaseModel):
    query: str = ""
    results: list = []
    status: str = "pending"

class MyFlow(Flow[WorkflowState]):

    @start()
    def initialize(self):
        self.state.status = "started"
        return "initialized"

    @listen(initialize)
    def process(self, data):
        self.state.status = "processing"
        # Do work
        return self.state

# Execute
flow = MyFlow()
result = flow.kickoff(inputs={"query": "test"})
```

## Core Decorators

### @start()

Marks the entry point of a flow. Every flow must have exactly one start method.

```python
from crewai.flow.flow import Flow, start

class MyFlow(Flow):

    @start()
    def begin(self):
        """Entry point - called first when flow starts."""
        self.state.initialized = True
        return "ready"
```

### @listen(event)

Triggers when the specified event completes. The event can be:
- A method reference
- A string event name
- Multiple events with `or_()` or `and_()`

```python
from crewai.flow.flow import Flow, listen, start

class MyFlow(Flow):

    @start()
    def step_one(self):
        return "step one done"

    @listen(step_one)
    def step_two(self, result):
        """Triggered when step_one completes."""
        print(f"Received: {result}")
        return "step two done"

    @listen("custom_event")
    def handle_custom(self):
        """Triggered by string event name."""
        return "handled"
```

### @router(event)

Conditional routing after an event. Must return a string that matches a `@listen()` event name.

```python
from crewai.flow.flow import Flow, listen, start, router
from typing import Literal

class MyFlow(Flow):

    @start()
    def classify(self):
        # Classify input
        self.state.category = self._analyze(self.state.input)
        return self.state.category

    @router(classify)
    def route(self) -> Literal["technical", "creative", "support"]:
        """Route to appropriate handler."""
        return self.state.category

    @listen("technical")
    def handle_technical(self):
        return "technical response"

    @listen("creative")
    def handle_creative(self):
        return "creative response"

    @listen("support")
    def handle_support(self):
        return "support response"
```

### @persist

Saves state to database after the decorated method completes. Enables crash recovery.

```python
from crewai.flow.flow import Flow, listen, start, persist

class MyFlow(Flow):

    @start()
    @persist
    def step_one(self):
        """State saved after this step."""
        self.state.checkpoint = "step_one"
        return "done"

    @listen(step_one)
    @persist
    def step_two(self, data):
        """State saved again - recoverable if crash."""
        self.state.checkpoint = "step_two"
        return "done"
```

## Event Combinators

### or_() - First to Complete

Triggers when ANY of the specified events complete.

```python
from crewai.flow.flow import Flow, listen, start, or_

class MyFlow(Flow):

    @start()
    def begin(self):
        return "started"

    @listen(begin)
    def path_a(self, data):
        # Processing path A
        return "a done"

    @listen(begin)
    def path_b(self, data):
        # Processing path B (parallel with path_a)
        return "b done"

    @listen(or_(path_a, path_b))
    def handle_first(self, result):
        """Triggered when EITHER path completes first."""
        return f"First result: {result}"
```

### and_() - All Complete

Triggers when ALL specified events complete.

```python
from crewai.flow.flow import Flow, listen, start, and_

class MyFlow(Flow):

    @start()
    def begin(self):
        return "started"

    @listen(begin)
    def path_a(self, data):
        return {"path": "a", "result": "done"}

    @listen(begin)
    def path_b(self, data):
        return {"path": "b", "result": "done"}

    @listen(and_(path_a, path_b))
    def merge_results(self, results):
        """Triggered when BOTH paths complete."""
        return f"Merged: {results}"
```

## State Management

### Unstructured State (Flexible)

Dynamic attributes added at runtime. Simple but no type safety.

```python
from crewai.flow.flow import Flow, start

class FlexibleFlow(Flow):
    """State attributes added dynamically."""

    @start()
    def begin(self):
        self.state.step = "started"
        self.state.data = []
        self.state.any_name = "any value"
        return "initialized"
```

### Structured State (Type-Safe)

Use Pydantic models for type safety and validation.

```python
from crewai.flow.flow import Flow, start
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class TypedState(BaseModel):
    """Type-safe state with validation."""
    query: str = ""
    results: List[str] = Field(default_factory=list)
    score: float = 0.0
    status: Literal["pending", "processing", "complete"] = "pending"
    metadata: Optional[dict] = None

class TypedFlow(Flow[TypedState]):
    """Flow with type checking and validation."""

    @start()
    def process(self):
        # IDE autocomplete works
        self.state.results.append("new result")
        self.state.score = 0.95
        self.state.status = "complete"
        return self.state
```

### State Access

```python
class MyFlow(Flow[MyState]):

    @start()
    def process(self):
        # Read state
        query = self.state.query

        # Write state
        self.state.results = ["result1", "result2"]

        # State is automatically persisted between steps
        return self.state
```

## Integrating Crews in Flows

```python
from crewai import Crew, Task, Agent
from crewai.flow.flow import Flow, listen, start

class ResearchFlow(Flow[ResearchState]):

    def __init__(self):
        super().__init__()
        self.researcher = Agent(
            role="Researcher",
            goal="Find information",
            backstory="Expert researcher"
        )
        self.writer = Agent(
            role="Writer",
            goal="Create content",
            backstory="Expert writer"
        )

    @start()
    def research(self):
        crew = Crew(
            agents=[self.researcher],
            tasks=[Task(
                description=f"Research: {self.state.query}",
                agent=self.researcher
            )]
        )
        result = crew.kickoff()
        self.state.research = result.raw
        return result

    @listen(research)
    def write(self, research_result):
        crew = Crew(
            agents=[self.writer],
            tasks=[Task(
                description=f"Write about: {self.state.research}",
                agent=self.writer
            )]
        )
        result = crew.kickoff()
        self.state.article = result.raw
        return result
```

## Common Flow Patterns

### 1. Linear Pipeline

```python
class PipelineFlow(Flow):

    @start()
    def step1(self):
        return "step1 output"

    @listen(step1)
    def step2(self, data):
        return "step2 output"

    @listen(step2)
    def step3(self, data):
        return "step3 output"
```

### 2. Conditional Routing

```python
class ConditionalFlow(Flow):

    @start()
    def analyze(self):
        self.state.type = self._classify()
        return self.state.type

    @router(analyze)
    def route(self):
        return self.state.type

    @listen("type_a")
    def handle_a(self):
        return "handled type a"

    @listen("type_b")
    def handle_b(self):
        return "handled type b"
```

### 3. Parallel Processing

```python
class ParallelFlow(Flow):

    @start()
    def begin(self):
        return "start"

    @listen(begin)
    def process_a(self, data):
        # Runs in parallel
        return "a result"

    @listen(begin)
    def process_b(self, data):
        # Runs in parallel with process_a
        return "b result"

    @listen(and_(process_a, process_b))
    def merge(self, results):
        return f"merged: {results}"
```

### 4. Loop with Condition

```python
class LoopFlow(Flow):

    @start()
    def initialize(self):
        self.state.iteration = 0
        return "initialized"

    @listen(initialize)
    def process(self, data):
        self.state.iteration += 1
        # Do processing
        return self.state.iteration

    @router(process)
    def check_done(self):
        if self.state.iteration >= 5:
            return "complete"
        return "process"  # Loop back

    @listen("complete")
    def finish(self):
        return f"Done after {self.state.iteration} iterations"
```

### 5. Error Handling Flow

```python
class RobustFlow(Flow):

    @start()
    def process(self):
        try:
            result = self._do_work()
            self.state.success = True
            return result
        except Exception as e:
            self.state.error = str(e)
            self.state.success = False
            return "error"

    @router(process)
    def route(self):
        if self.state.success:
            return "success"
        return "handle_error"

    @listen("success")
    def on_success(self):
        return "completed successfully"

    @listen("handle_error")
    def on_error(self):
        return f"failed: {self.state.error}"
```

## Flow Execution

### Basic Execution

```python
flow = MyFlow()
result = flow.kickoff(inputs={"query": "test"})
print(result)
print(flow.state)
```

### Async Execution

```python
import asyncio

flow = MyFlow()
result = await flow.kickoff_async(inputs={"query": "test"})
```

### With Timeout

```python
import asyncio

async def run_with_timeout():
    flow = MyFlow()
    try:
        result = await asyncio.wait_for(
            flow.kickoff_async(inputs={"query": "test"}),
            timeout=60.0
        )
        return result
    except asyncio.TimeoutError:
        return "Flow timed out"
```

## State Persistence

### Enable Persistence

```python
class PersistentFlow(Flow):

    @start()
    @persist
    def step1(self):
        self.state.step = 1
        return "done"

    @listen(step1)
    @persist
    def step2(self, data):
        self.state.step = 2
        return "done"
```

### Recovery from Crash

```python
# If flow crashes, it can be resumed from last persisted state
flow = PersistentFlow()

# Check if there's a saved state
if flow.has_saved_state():
    flow.resume()
else:
    flow.kickoff(inputs={"query": "test"})
```

## Debugging Flows

### Verbose Mode

```python
class DebugFlow(Flow):

    @start()
    def process(self):
        print(f"Current state: {self.state}")
        return "done"
```

### Step Callbacks

```python
def on_step(step_name, result):
    print(f"Step {step_name} completed: {result}")

flow = MyFlow()
flow.on_step_complete = on_step
flow.kickoff(inputs={"query": "test"})
```

## Best Practices

1. **Use Structured State**: Pydantic models catch errors early
2. **Add Persistence**: Use `@persist` for long-running flows
3. **Handle Errors**: Use routers to handle failure cases
4. **Keep Steps Small**: Each step should do one thing
5. **Use Meaningful Names**: Method names become event names
6. **Test Independently**: Test each step in isolation
7. **Monitor State**: Log state changes for debugging
