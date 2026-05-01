# Functional Programming

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `elixir-pro` | inherit | Write idiomatic Elixir code with OTP patterns, supervision trees, and Phoenix LiveView. Masters concurrency, fault to... |
| `haskell-pro` | sonnet | Expert Haskell engineer specializing in advanced type systems, pure functional design, and high-reliability software.... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Write idiomatic Elixir code with OTP patterns, supervision trees, and Phoenix LiveView" → activates `elixir-pro`

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
