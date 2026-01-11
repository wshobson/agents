# CrewAI Memory Reference

Complete reference for CrewAI memory systems including short-term, long-term, and entity memory.

## Memory Overview

CrewAI provides three types of memory:

| Type | Purpose | Persistence | Use Case |
|------|---------|-------------|----------|
| **Short-Term** | Current conversation context | Session | Task continuity |
| **Long-Term** | Historical knowledge | Persistent | Learning from past |
| **Entity** | Named entity relationships | Persistent | Knowledge graphs |

## Short-Term Memory

Enables agents to remember context within the current execution.

### Enable Short-Term Memory

```python
from crewai import Agent, Crew

# On Agent
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    memory=True  # Enable short-term memory
)

# On Crew
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True  # Enable for all agents
)
```

### How It Works

1. Agent receives task
2. Previous interactions stored in context
3. Context provided with each new prompt
4. Memory cleared after crew execution

## Long-Term Memory

Persists knowledge across executions for learning and improvement.

### Basic Configuration

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
    )
)
```

### Storage Backends

#### ChromaDB (Default)

```python
from crewai.memory.storage import RAGStorage

storage = RAGStorage(
    type="chroma",
    persist_directory="./memory_store",
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }
)
```

#### Pinecone

```python
storage = RAGStorage(
    type="pinecone",
    api_key="your-api-key",
    environment="us-west1-gcp",
    index_name="crew-memory",
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }
)
```

#### Qdrant

```python
storage = RAGStorage(
    type="qdrant",
    url="http://localhost:6333",
    collection_name="crew_memory",
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }
)
```

### Embedding Providers

#### OpenAI

```python
embedder = {
    "provider": "openai",
    "config": {
        "model": "text-embedding-3-large"
        # or "text-embedding-3-small" for faster/cheaper
    }
}
```

#### Voyage AI

```python
embedder = {
    "provider": "voyage",
    "config": {
        "model": "voyage-3-large"
        # Specialized: voyage-code-3, voyage-finance-2, voyage-law-2
    }
}
```

#### Cohere

```python
embedder = {
    "provider": "cohere",
    "config": {
        "model": "embed-english-v3.0"
    }
}
```

#### Ollama (Local)

```python
embedder = {
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text",
        "url": "http://localhost:11434"
    }
}
```

## Entity Memory

Tracks named entities and their relationships for knowledge graph functionality.

### Configuration

```python
from crewai import Crew
from crewai.memory import EntityMemory
from crewai.memory.storage import RAGStorage

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    entity_memory=EntityMemory(
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

### How It Works

1. Agents extract entities from conversations
2. Entities stored with relationships
3. Future queries retrieve relevant entities
4. Agents can reference known entities

### Use Cases

- Customer relationship tracking
- Knowledge base building
- Research paper connections
- Project dependency mapping

## Combined Memory Configuration

```python
from crewai import Crew
from crewai.memory import LongTermMemory, EntityMemory
from crewai.memory.storage import RAGStorage

# Shared embedding configuration
embedder_config = {
    "provider": "openai",
    "config": {"model": "text-embedding-3-large"}
}

# Storage for both memory types
storage = RAGStorage(
    type="chroma",
    persist_directory="./crew_memory",
    embedder=embedder_config
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    memory=True,  # Short-term
    long_term_memory=LongTermMemory(storage=storage),
    entity_memory=EntityMemory(storage=storage),
    embedder=embedder_config
)
```

## Memory in Flows

### Flow State as Memory

```python
from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel
from typing import List

class FlowMemory(BaseModel):
    """Flow state persists across steps."""
    conversation_history: List[str] = []
    learned_facts: List[str] = []
    entities: dict = {}

class MemoryFlow(Flow[FlowMemory]):

    @start()
    def process_input(self):
        # Store in flow memory
        self.state.conversation_history.append(f"User: {self.state.input}")
        return self.state.input

    @listen(process_input)
    def analyze(self, data):
        # Access previous history
        context = "\n".join(self.state.conversation_history[-5:])

        # Process with context
        result = self._process_with_context(data, context)

        # Store learned facts
        self.state.learned_facts.extend(result.facts)
        return result
```

### Persistent Flow Memory

```python
from crewai.flow.flow import Flow, start, listen, persist

class PersistentMemoryFlow(Flow):

    @start()
    @persist
    def step1(self):
        """State saved to database."""
        self.state.step1_complete = True
        return "done"

    @listen(step1)
    @persist
    def step2(self, data):
        """Recoverable if crash."""
        self.state.step2_complete = True
        return "done"
```

## Memory Best Practices

### 1. Choose Appropriate Memory Type

| Scenario | Memory Type |
|----------|-------------|
| Single conversation | Short-term |
| Learning from history | Long-term |
| Entity tracking | Entity |
| Complex workflows | All three |

### 2. Optimize Embedding Selection

```python
# For general text
embedder = {"provider": "openai", "config": {"model": "text-embedding-3-large"}}

# For code-heavy content
embedder = {"provider": "voyage", "config": {"model": "voyage-code-3"}}

# For financial/legal
embedder = {"provider": "voyage", "config": {"model": "voyage-finance-2"}}
```

### 3. Manage Memory Size

```python
# Set limits on memory retrieval
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    long_term_memory=LongTermMemory(
        storage=RAGStorage(
            type="chroma",
            embedder=embedder_config
        ),
        max_results=10  # Limit retrieved memories
    )
)
```

### 4. Clear Stale Memory

```python
from crewai.memory.storage import RAGStorage

storage = RAGStorage(
    type="chroma",
    persist_directory="./crew_memory",
    embedder=embedder_config
)

# Clear all memories
storage.clear()

# Or create fresh storage
import shutil
shutil.rmtree("./crew_memory")
```

## Troubleshooting

### Memory Not Working

```python
# Ensure memory is enabled on both agent and crew
agent = Agent(
    role="Analyst",
    goal="Analyze",
    backstory="Expert",
    memory=True  # Required
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True  # Also required
)
```

### Slow Memory Retrieval

```python
# Use faster embedding model
embedder = {
    "provider": "openai",
    "config": {"model": "text-embedding-3-small"}  # Faster than large
}

# Or reduce retrieval count
long_term_memory = LongTermMemory(
    storage=storage,
    max_results=5  # Fewer results
)
```

### Out of Memory

```python
# Use external storage
storage = RAGStorage(
    type="qdrant",  # External vector DB
    url="http://localhost:6333",
    collection_name="crew_memory",
    embedder=embedder_config
)
```

### Inconsistent Results

```python
# Use consistent embedding model
# Don't mix embedding models in same storage

# Clear and rebuild if embedding model changed
storage.clear()
```
