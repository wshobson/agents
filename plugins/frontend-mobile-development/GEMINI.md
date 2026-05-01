# Frontend Mobile Development

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `frontend-developer` | inherit | Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next... |
| `mobile-developer` | inherit | Develop React Native, Flutter, or native mobile apps with modern architecture patterns. Masters cross-platform develo... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/frontend-mobile-development:component-scaffold` | React/React Native Component Scaffolding |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `nextjs-app-router-patterns` | Master Next.js 14+ App Router with Server Components, streaming, parallel routes, and advanced data fetching. Use when building Next.js a... |
| `react-native-architecture` | Build production React Native apps with Expo, navigation, native modules, offline sync, and cross-platform patterns. Use when developing ... |
| `react-state-management` | Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing serv... |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating compon... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Build React components, implement responsive layouts, and handle client-side state management" → activates `frontend-developer`
- "Master Next.js 14+ App Router with Server Components, streaming, parallel routes, and advanced data fetching" → activates `nextjs-app-router-patterns` skill
- In Claude Code: `/frontend-mobile-development:component-scaffold` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
