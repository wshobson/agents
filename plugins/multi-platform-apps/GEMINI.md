# Multi Platform Apps

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `backend-architect` | inherit | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. Ma... |
| `flutter-expert` | inherit | Master Flutter development with Dart 3, advanced widgets, and multi-platform deployment. Handles state management, an... |
| `frontend-developer` | inherit | Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next... |
| `ios-developer` | inherit | Develop native iOS applications with Swift/SwiftUI. Masters iOS 18, SwiftUI, UIKit integration, Core Data, networking... |
| `mobile-developer` | inherit | Develop React Native, Flutter, or native mobile apps with modern architecture patterns. Masters cross-platform develo... |
| `ui-ux-designer` | sonnet | Create interface designs, wireframes, and design systems. Masters user research, accessibility standards, and modern ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/multi-platform-apps:multi-platform` `<feature description> [--platforms web,ios,android,desktop] [--shared-code evaluate|kotlin-multiplatform|typescript]` | Orchestrate cross-platform feature development across web, mobile, and desktop with API-first architecture |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems" → activates `backend-architect`
- In Claude Code: `/multi-platform-apps:multi-platform` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
