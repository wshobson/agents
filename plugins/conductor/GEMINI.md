# Conductor

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `conductor-validator` | opus | Validates Conductor project artifacts for completeness, consistency, and correctness. Use after setup, when diagnosin... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/conductor:implement` `[track-id] [--task X.Y] [--phase N]` | Execute tasks from a track's implementation plan following TDD workflow |
| `/conductor:manage` `[--archive | --restore | --delete | --rename | --list | --cleanup]` | Manage track lifecycle: archive, restore, delete, rename, and cleanup |
| `/conductor:new-track` `<feature|bug|chore|refactor> <name>` | Create a new track with specification and phased implementation plan |
| `/conductor:revert` `[track-id | track-id:phase | track-id:task]` | Git-aware undo by logical work unit (track, phase, or task) |
| `/conductor:setup` `[--resume]` | Initialize project with Conductor artifacts (product definition, tech stack, workflow, style guides) |
| `/conductor:status` `[track-id] [--detailed]` | Display project status, active tracks, and next actions |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `context-driven-development` | >- Creates and maintains project context artifacts (product.md, tech-stack.md, workflow.md, tracks.md) in a `conductor/` directory. Scaff... |
| `track-management` | Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Appl... |
| `workflow-patterns` | Use this skill when implementing tasks according to Conductor's TDD workflow, handling phase checkpoints, managing git commits for tasks,... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Validates Conductor project artifacts for completeness, consistency, and correctness" → activates `conductor-validator`
- ">- Creates and maintains project context artifacts (product.md, tech-stack.md, workflow.md, tracks.md) in a `conductor/` directory" → activates `context-driven-development` skill
- In Claude Code: `/conductor:implement` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
