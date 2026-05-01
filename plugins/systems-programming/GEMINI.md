# Systems Programming

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `c-pro` | opus | Write efficient C code with proper memory management, pointer arithmetic, and system calls. Handles embedded systems,... |
| `cpp-pro` | opus | Write idiomatic C++ code with modern features, RAII, smart pointers, and STL algorithms. Handles templates, move sema... |
| `golang-pro` | opus | Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservi... |
| `rust-pro` | opus | Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems programming... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/systems-programming:rust-project` | Rust Project Scaffolding |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `go-concurrency-patterns` | Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing... |
| `memory-safety-patterns` | Implement memory-safe programming with RAII, ownership, smart pointers, and resource management across Rust, C++, and C. Use when writing... |
| `rust-async-patterns` | Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust application... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Write efficient C code with proper memory management, pointer arithmetic, and system calls" → activates `c-pro`
- "Master Go concurrency with goroutines, channels, sync primitives, and context" → activates `go-concurrency-patterns` skill
- In Claude Code: `/systems-programming:rust-project` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
