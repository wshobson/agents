# Agent Teams Plugin

Orchestrate multi-agent teams for parallel code review, hypothesis-driven debugging, and coordinated feature development using Claude Code's experimental [Agent Teams](https://code.claude.com/docs/en/agent-teams) feature.

## Setup

### Prerequisites

1. Enable the experimental Agent Teams feature:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

2. Configure teammate display mode in your `~/.claude/settings.json`:

```json
{
  "teammateMode": "tmux"
}
```

Available display modes:

- `"tmux"` — Each teammate runs in a tmux pane (recommended)
- `"iterm2"` — Each teammate gets an iTerm2 tab (macOS only)
- `"in-process"` — Teammates run in the same process (default)

### Installation

First, add the marketplace (if you haven't already):

```
/plugin marketplace add wshobson/agents
```

Then install the plugin:

```
/plugin install agent-teams@claude-code-workflows
```

## Features

- **Preset Teams** — Spawn pre-configured teams for common workflows (review, debug, feature, fullstack, research, security, migration)
- **Multi-Reviewer Code Review** — Parallel review across security, performance, architecture, testing, and accessibility dimensions
- **Hypothesis-Driven Debugging** — Competing hypothesis investigation with evidence-based root cause analysis
- **Parallel Feature Development** — Coordinated multi-agent implementation with file ownership boundaries
- **Parallel Research** — Multiple Explore agents investigating different questions or codebase areas simultaneously
- **Security Audit** — Comprehensive parallel security review across OWASP, auth, dependencies, and configuration
- **Migration Support** — Coordinated codebase migration with parallel implementation streams and correctness verification
- **Task Coordination** — Dependency-aware task management with workload balancing
- **Team Communication** — Structured messaging protocols for efficient agent collaboration

## Commands

| Command          | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `/team-spawn`    | Spawn a team using presets or custom composition           |
| `/team-status`   | Display team members, tasks, and progress                  |
| `/team-shutdown` | Gracefully shut down a team and clean up resources         |
| `/team-review`   | Multi-reviewer parallel code review                        |
| `/team-debug`    | Competing hypotheses debugging with parallel investigation |
| `/team-feature`  | Parallel feature development with file ownership           |
| `/team-delegate` | Task delegation dashboard and workload management          |

## Agents

| Agent              | Role                                                                              | Color  |
| ------------------ | --------------------------------------------------------------------------------- | ------ |
| `team-lead`        | Team orchestrator — decomposes work, manages lifecycle, synthesizes results       | Blue   |
| `team-reviewer`    | Multi-dimensional code reviewer — operates on assigned review dimension           | Green  |
| `team-debugger`    | Hypothesis investigator — gathers evidence to confirm/falsify assigned hypothesis | Red    |
| `team-implementer` | Parallel builder — implements within strict file ownership boundaries             | Yellow |

## Skills

| Skill                          | Description                                                              |
| ------------------------------ | ------------------------------------------------------------------------ |
| `team-composition-patterns`    | Team sizing heuristics, preset compositions, agent type selection        |
| `task-coordination-strategies` | Task decomposition, dependency graphs, workload monitoring               |
| `parallel-debugging`           | Hypothesis generation, evidence collection, result arbitration           |
| `multi-reviewer-patterns`      | Review dimension allocation, finding deduplication, severity calibration |
| `parallel-feature-development` | File ownership strategies, conflict avoidance, integration patterns      |
| `team-communication-protocols` | Message type selection, plan approval workflow, shutdown protocol        |

## Quick Start

### Multi-Reviewer Code Review

```
/team-review src/ --reviewers security,performance,architecture
```

Spawns 3 reviewers, each analyzing the codebase from their assigned dimension, then consolidates findings into a prioritized report.

### Hypothesis-Driven Debugging

```
/team-debug "API returns 500 on POST /users with valid payload" --hypotheses 3
```

Generates 3 competing hypotheses, spawns investigators for each, collects evidence, and presents the most likely root cause with a fix.

### Parallel Feature Development

```
/team-feature "Add user authentication with OAuth2" --team-size 3 --plan-first
```

Decomposes the feature into work streams with file ownership boundaries, gets your approval, then spawns implementers to build in parallel.

### Parallel Research

```
/team-spawn research --name codebase-research
```

Spawns 3 researchers to investigate different aspects in parallel — across your codebase (Grep/Read) and the web (WebSearch/WebFetch). Each reports findings with citations.

### Security Audit

```
/team-spawn security
```

Spawns 4 security reviewers covering OWASP vulnerabilities, auth/access control, dependency supply chain, and secrets/configuration. Produces a consolidated security report.

### Codebase Migration

```
/team-spawn migration --name react-hooks-migration
```

Spawns a lead to plan the migration, 2 implementers to migrate code in parallel streams, and a reviewer to verify correctness of the migrated code.

### Custom Team

```
/team-spawn custom --name my-team --members 4
```

Interactively configure team composition with custom roles and agent types.

## Best Practices

1. **Start with presets** — Use `/team-spawn review`, `/team-spawn debug`, or `/team-spawn feature` before building custom teams
2. **Use `--plan-first`** — For feature development, always review the decomposition before spawning implementers
3. **File ownership is critical** — Never assign the same file to multiple implementers; use interface contracts at boundaries
4. **Monitor with `/team-status`** — Check progress regularly and use `/team-delegate --rebalance` if work is uneven
5. **Graceful shutdown** — Always use `/team-shutdown` rather than killing processes manually
6. **Keep teams small** — 2-4 teammates is optimal; larger teams increase coordination overhead
7. **Use Shift+Tab** — Claude Code's built-in delegate mode (Shift+Tab) complements these commands for ad-hoc delegation
