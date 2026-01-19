# Conductor - Context-Driven Development Plugin for Claude Code

Conductor transforms Claude Code into a project management tool by implementing **Context-Driven Development**. It enforces a structured workflow: **Context → Spec & Plan → Implement**.

## Philosophy

By treating context as a managed artifact alongside code, teams establish a persistent, project-aware foundation for all AI interactions. The system maintains:

- **Product vision** as living documentation
- **Technical decisions** as structured artifacts
- **Work units (tracks)** with specifications and phased plans
- **TDD workflow** with verification checkpoints

## Features

- **Specification & Planning**: Generate detailed specs and actionable task plans before implementation
- **Context Management**: Maintain style guides, tech stack preferences, and product goals
- **Safe Iteration**: Review plans before code generation, keeping humans in control
- **Team Collaboration**: Project-level context documents become shared foundations
- **Project Intelligence**: Handles both greenfield (new) and brownfield (existing) projects
- **Semantic Reversion**: Git-aware revert by logical work units (tracks, phases, tasks)
- **State Persistence**: Resume setup across multiple sessions

## Commands

| Command                | Description                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `/conductor:setup`     | Initialize project with product definition, tech stack, workflow, and style guides |
| `/conductor:new-track` | Create a feature or bug track with spec.md and plan.md                             |
| `/conductor:implement` | Execute tasks from the plan following workflow rules                               |
| `/conductor:status`    | Display project progress overview                                                  |
| `/conductor:revert`    | Git-aware undo by track, phase, or task                                            |
| `/conductor:manage`    | Manage track lifecycle: archive, restore, delete, rename, and cleanup              |

## Generated Artifacts

```
conductor/
├── index.md              # Navigation hub
├── product.md            # Product vision & goals
├── product-guidelines.md # Standards & messaging
├── tech-stack.md         # Technology preferences
├── workflow.md           # Development practices (TDD, commits)
├── tracks.md             # Master track registry
├── setup_state.json      # Resumable setup state
├── code_styleguides/     # Language-specific conventions
└── tracks/
    ├── _archive/         # Archived tracks
    └── <track-id>/
        ├── spec.md       # Requirements specification
        ├── plan.md       # Phased task breakdown
        ├── metadata.json # Track metadata
        └── index.md      # Track navigation
```

## Workflow

### 1. Setup (`/conductor:setup`)

Interactive initialization that creates foundational project documentation:

- Detects greenfield vs brownfield projects
- Asks sequential questions about product, tech stack, workflow preferences
- Generates style guides for selected languages
- Creates tracks registry

### 2. Create Track (`/conductor:new-track`)

Start a new feature or bug fix:

- Interactive Q&A to gather requirements
- Generates detailed specification (spec.md)
- Creates phased implementation plan (plan.md)
- Registers track in tracks.md

### 3. Implement (`/conductor:implement`)

Execute the plan systematically:

- Follows TDD red-green-refactor cycle
- Updates task status markers
- Includes manual verification checkpoints
- Synchronizes documentation on completion

### 4. Monitor (`/conductor:status`)

View project progress:

- Current phase and task
- Completion percentage
- Identified blockers

### 5. Revert (`/conductor:revert`)

Undo work by logical unit:

- Select track, phase, or task to revert
- Git-aware: finds all associated commits
- Requires confirmation before execution

### 6. Manage (`/conductor:manage`)

Manage track lifecycle:

- Archive completed tracks with reason tracking
- Restore archived tracks to active state
- Delete tracks permanently (with safeguards)
- Rename track IDs with reference updates
- Cleanup orphaned artifacts and stale tracks

## Installation

```bash
/plugin install conductor
```

## Acknowledgments

This plugin is based on [Conductor](https://github.com/gemini-cli-extensions/conductor) by Google, originally developed for Gemini CLI.

Adapted for Claude Code by [@wshobson](https://github.com/wshobson).

## License

Apache License 2.0 - See the [original project](https://github.com/gemini-cli-extensions/conductor) for license details.
