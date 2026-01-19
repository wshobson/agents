# LLM Application Development Plugin for Claude Code

Build production-ready LLM applications, advanced RAG systems, and intelligent agents with modern AI patterns.

## Version 2.0.0 Highlights

- **LangGraph Integration**: Updated from deprecated LangChain patterns to LangGraph StateGraph workflows
- **Modern Model Support**: Claude Opus/Sonnet/Haiku 4.5 and GPT-5.2/GPT-5.2-mini
- **Voyage AI Embeddings**: Recommended embedding models for Claude applications
- **Structured Outputs**: Pydantic-based structured output patterns

## Features

### Core Capabilities

- **RAG Systems**: Production retrieval-augmented generation with hybrid search
- **Vector Search**: Pinecone, Qdrant, Weaviate, Milvus, pgvector optimization
- **Agent Architectures**: LangGraph-based agents with memory and tool use
- **Prompt Engineering**: Advanced prompting techniques with model-specific optimization

### Key Technologies

- LangChain 1.x / LangGraph for agent workflows
- Voyage AI, OpenAI, and open-source embedding models
- HNSW, IVF, and Product Quantization index strategies
- Async patterns with checkpointers for durable execution

## Agents

| Agent                      | Description                                                                |
| -------------------------- | -------------------------------------------------------------------------- |
| `ai-engineer`              | Production-grade LLM applications, RAG systems, and agent architectures    |
| `prompt-engineer`          | Advanced prompting techniques, constitutional AI, and model optimization   |
| `vector-database-engineer` | Vector search implementation, embedding strategies, and semantic retrieval |

## Skills

| Skill                          | Description                                                 |
| ------------------------------ | ----------------------------------------------------------- |
| `langchain-architecture`       | LangGraph StateGraph patterns, memory, and tool integration |
| `rag-implementation`           | RAG systems with hybrid search and reranking                |
| `llm-evaluation`               | Evaluation frameworks for LLM applications                  |
| `prompt-engineering-patterns`  | Chain-of-thought, few-shot, and structured outputs          |
| `embedding-strategies`         | Embedding model selection and optimization                  |
| `similarity-search-patterns`   | Vector similarity search implementation                     |
| `vector-index-tuning`          | HNSW, IVF, and quantization optimization                    |
| `hybrid-search-implementation` | Vector + keyword search fusion                              |

## Commands

| Command                                | Description                     |
| -------------------------------------- | ------------------------------- |
| `/llm-application-dev:langchain-agent` | Create LangGraph-based agent    |
| `/llm-application-dev:ai-assistant`    | Build AI assistant application  |
| `/llm-application-dev:prompt-optimize` | Optimize prompts for production |

## Installation

```bash
/plugin install llm-application-dev
```

## Requirements

- LangChain >= 1.2.0
- LangGraph >= 0.3.0
- Python 3.11+

## Changelog

### 2.0.0 (January 2026)

- **Breaking**: Migrated from LangChain 0.x to LangChain 1.x/LangGraph
- **Breaking**: Updated model references to Claude 4.5 and GPT-5.2
- Added Voyage AI as primary embedding recommendation for Claude apps
- Added LangGraph StateGraph patterns replacing deprecated `initialize_agent()`
- Added structured outputs with Pydantic
- Added async patterns with checkpointers
- Fixed security issue: replaced unsafe code execution with AST-based safe math evaluation
- Updated hybrid search with modern Pinecone client API

### 1.2.2

- Minor bug fixes and documentation updates

## License

MIT License - See the plugin configuration for details.
