---
name: team-composition-patterns
description: Design optimal agent team compositions with sizing heuristics, preset configurations, and agent type selection. Use this skill when deciding team size, selecting agent types, or configuring team presets for multi-agent workflows.
version: 1.0.2
---

# Team Composition Patterns

Best practices for composing multi-agent teams, selecting team sizes, choosing agent types, and configuring display modes for Claude Code's Agent Teams feature.

## When to Use This Skill

- Deciding how many teammates to spawn for a task
- Choosing between preset team configurations
- Selecting the right agent type (subagent_type) for each role
- Configuring teammate display modes (tmux, iTerm2, in-process)
- Building custom team compositions for non-standard workflows

## Team Sizing Heuristics

| Complexity   | Team Size | When to Use                                                 |
| ------------ | --------- | ----------------------------------------------------------- |
| Simple       | 1-2       | Single-dimension review, isolated bug, small feature        |
| Moderate     | 2-3       | Multi-file changes, 2-3 concerns, medium features           |
| Complex      | 3-4       | Cross-cutting concerns, large features, deep debugging      |
| Very Complex | 4-5       | Full-stack features, comprehensive reviews, systemic issues |

**Rule of thumb**: Start with the smallest team that covers all required dimensions. Adding teammates increases coordination overhead.

## Preset Team Compositions

### Review Team

- **Size**: 3 reviewers
- **Agents**: 3x `team-reviewer`
- **Default dimensions**: security, performance, architecture
- **Use when**: Code changes need multi-dimensional quality assessment

### Debug Team

- **Size**: 3 investigators
- **Agents**: 3x `team-debugger`
- **Default hypotheses**: 3 competing hypotheses
- **Use when**: Bug has multiple plausible root causes

### Feature Team

- **Size**: 3 (1 lead + 2 implementers)
- **Agents**: 1x `team-lead` + 2x `team-implementer`
- **Use when**: Feature can be decomposed into parallel work streams

### Fullstack Team

- **Size**: 4 (1 lead + 3 implementers)
- **Agents**: 1x `team-lead` + 1x frontend `team-implementer` + 1x backend `team-implementer` + 1x test `team-implementer`
- **Use when**: Feature spans frontend, backend, and test layers

### Research Team

- **Size**: 3 researchers
- **Agents**: 3x `general-purpose`
- **Default areas**: Each assigned a different research question, module, or topic
- **Capabilities**: Codebase search (Grep, Glob, Read), web search (WebSearch, WebFetch)
- **Use when**: Need to understand a codebase, research libraries, compare approaches, or gather information from code and web sources in parallel

### Security Team

- **Size**: 4 reviewers
- **Agents**: 4x `team-reviewer`
- **Default dimensions**: OWASP/vulnerabilities, auth/access control, dependencies/supply chain, secrets/configuration
- **Use when**: Comprehensive security audit covering multiple attack surfaces

### Migration Team

- **Size**: 4 (1 lead + 2 implementers + 1 reviewer)
- **Agents**: 1x `team-lead` + 2x `team-implementer` + 1x `team-reviewer`
- **Use when**: Large codebase migration (framework upgrade, language port, API version bump) requiring parallel work with correctness verification

## Agent Type Selection

When spawning teammates with the Task tool, choose `subagent_type` based on what tools the teammate needs:

| Agent Type                     | Tools Available                           | Use For                                                    |
| ------------------------------ | ----------------------------------------- | ---------------------------------------------------------- |
| `general-purpose`              | All tools (Read, Write, Edit, Bash, etc.) | Implementation, debugging, any task requiring file changes |
| `Explore`                      | Read-only tools (Read, Grep, Glob)        | Research, code exploration, analysis                       |
| `Plan`                         | Read-only tools                           | Architecture planning, task decomposition                  |
| `agent-teams:team-reviewer`    | All tools                                 | Code review with structured findings                       |
| `agent-teams:team-debugger`    | All tools                                 | Hypothesis-driven investigation                            |
| `agent-teams:team-implementer` | All tools                                 | Building features within file ownership boundaries         |
| `agent-teams:team-lead`        | All tools                                 | Team orchestration and coordination                        |

**Key distinction**: Read-only agents (Explore, Plan) cannot modify files. Never assign implementation tasks to read-only agents.

## Display Mode Configuration

Configure in `~/.claude/settings.json`:

```json
{
  "teammateMode": "tmux"
}
```

| Mode           | Behavior                       | Best For                                          |
| -------------- | ------------------------------ | ------------------------------------------------- |
| `"tmux"`       | Each teammate in a tmux pane   | Development workflows, monitoring multiple agents |
| `"iterm2"`     | Each teammate in an iTerm2 tab | macOS users who prefer iTerm2                     |
| `"in-process"` | All teammates in same process  | Simple tasks, CI/CD environments                  |

## Custom Team Guidelines

When building custom teams:

1. **Every team needs a coordinator** — Either designate a `team-lead` or have the user coordinate directly
2. **Match roles to agent types** — Use specialized agents (reviewer, debugger, implementer) when available
3. **Avoid duplicate roles** — Two agents doing the same thing wastes resources
4. **Define boundaries upfront** — Each teammate needs clear ownership of files or responsibilities
5. **Keep it small** — 2-4 teammates is the sweet spot; 5+ requires significant coordination overhead
