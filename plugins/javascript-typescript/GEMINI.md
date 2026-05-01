# Javascript Typescript

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `javascript-pro` | inherit | Master modern JavaScript with ES6+, async patterns, and Node.js APIs. Handles promises, event loops, and browser/Node... |
| `typescript-pro` | opus | Master TypeScript with advanced types, generics, and strict type safety. Handles complex type systems, decorators, an... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/javascript-typescript:typescript-scaffold` | TypeScript Project Scaffolding |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `javascript-testing-patterns` | Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end test... |
| `modern-javascript-patterns` | Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, a... |
| `nodejs-backend-patterns` | Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, d... |
| `typescript-advanced-types` | Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types for bu... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master modern JavaScript with ES6+, async patterns, and Node.js APIs" → activates `javascript-pro`
- "Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development" → activates `javascript-testing-patterns` skill
- In Claude Code: `/javascript-typescript:typescript-scaffold` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
