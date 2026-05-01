# Llm Application Dev

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `ai-engineer` | inherit | Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Implements vector search, mult... |
| `prompt-engineer` | inherit | Expert prompt engineer specializing in advanced prompting techniques, LLM optimization, and AI system design. Masters... |
| `vector-database-engineer` | inherit | Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdr... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/llm-application-dev:ai-assistant` `<assistant-type> [options]` | Build AI assistant application with NLU, dialog management, and integrations |
| `/llm-application-dev:langchain-agent` `<agent-type> [options]` | Create LangGraph-based agent with modern patterns |
| `/llm-application-dev:prompt-optimize` `<prompt-text-or-file>` | Optimize prompts for production with CoT, few-shot, and constitutional AI patterns |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `embedding-strategies` | Select and optimize embedding models for semantic search and RAG applications. Use when choosing embedding models, implementing chunking ... |
| `hybrid-search-implementation` | Combine vector and keyword search for improved retrieval. Use when implementing RAG systems, building search engines, or when neither app... |
| `langchain-architecture` | Design LLM applications using LangChain 1.x and LangGraph for agents, memory, and tool integration. Use when building LangChain applicati... |
| `llm-evaluation` | Implement comprehensive evaluation strategies for LLM applications using automated metrics, human feedback, and benchmarking. Use when te... |
| `prompt-engineering-patterns` | Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability in production. Use when optim... |
| `rag-implementation` | Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Use when implementing ... |
| `similarity-search-patterns` | Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or... |
| `vector-index-tuning` | Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Build production-ready LLM applications, advanced RAG systems, and intelligent agents" → activates `ai-engineer`
- "Select and optimize embedding models for semantic search and RAG applications" → activates `embedding-strategies` skill
- In Claude Code: `/llm-application-dev:ai-assistant` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
