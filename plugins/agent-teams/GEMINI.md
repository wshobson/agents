# Agent Teams

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `team-debugger` | opus | Hypothesis-driven debugging investigator that investigates one assigned hypothesis, gathering evidence to confirm or ... |
| `team-implementer` | opus | Parallel feature builder that implements components within strict file ownership boundaries, coordinating at integrat... |
| `team-lead` | opus | Team orchestrator that decomposes work into parallel tasks with file ownership boundaries, manages team lifecycle, an... |
| `team-reviewer` | opus | Multi-dimensional code reviewer that operates on one assigned review dimension (security, performance, architecture, ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/agent-teams:team-debug` `<error-description-or-file> [--hypotheses N] [--scope files|module|project]` | Debug issues using competing hypotheses with parallel investigation by multiple agents |
| `/agent-teams:team-delegate` `[team-name] [--assign task-id=member-name] [--message member-name 'content'] [--rebalance]` | Task delegation dashboard for managing team workload, assignments, and rebalancing |
| `/agent-teams:team-feature` `<feature-description> [--team-size N] [--branch feature/name] [--plan-first]` | Develop features in parallel with multiple agents using file ownership boundaries and dependency management |
| `/agent-teams:team-review` `<target> [--reviewers security,performance,architecture,testing,accessibility] [--base-branch main]` | Launch a multi-reviewer parallel code review with specialized review dimensions |
| `/agent-teams:team-shutdown` `[team-name] [--force] [--keep-tasks]` | Gracefully shut down an agent team, collect final results, and clean up resources |
| `/agent-teams:team-spawn` `<preset|custom> [--name team-name] [--members N] [--delegate]` | Spawn an agent team using presets (review, debug, feature, fullstack, research, security, migration) or custom compos... |
| `/agent-teams:team-status` `[team-name] [--tasks] [--members] [--json]` | Display team members, task status, and progress for an active agent team |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `multi-reviewer-patterns` | Coordinate parallel code reviews across multiple quality dimensions with finding deduplication, severity calibration, and consolidated re... |
| `parallel-debugging` | Debug complex issues using competing hypotheses with parallel investigation, evidence collection, and root cause arbitration. Use this sk... |
| `parallel-feature-development` | Coordinate parallel feature development with file ownership strategies, conflict avoidance rules, and integration patterns for multi-agen... |
| `task-coordination-strategies` | Decompose complex tasks, design dependency graphs, and coordinate multi-agent work with proper task descriptions and workload balancing. ... |
| `team-communication-protocols` | Structured messaging protocols for agent team communication including message type selection, plan approval, shutdown procedures, and ant... |
| `team-composition-patterns` | Design optimal agent team compositions with sizing heuristics, preset configurations, and agent type selection. Use this skill when decid... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Hypothesis-driven debugging investigator that investigates one assigned hypothesis, gathering evidence to confirm or falsify it with file:line citations and confidence levels" → activates `team-debugger`
- "Coordinate parallel code reviews across multiple quality dimensions with finding deduplication, severity calibration, and consolidated reporting" → activates `multi-reviewer-patterns` skill
- In Claude Code: `/agent-teams:team-debug` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
