# Agent Type Selection Guide

Decision matrix for choosing the right `subagent_type` when spawning teammates.

## Decision Matrix

```
Does the teammate need to modify files?
├── YES → Does it need a specialized role?
│         ├── YES → Which role?
│         │         ├── Code review → agent-teams:team-reviewer
│         │         ├── Bug investigation → agent-teams:team-debugger
│         │         ├── Feature building → agent-teams:team-implementer
│         │         └── Team coordination → agent-teams:team-lead
│         └── NO → general-purpose
└── NO → Does it need deep codebase exploration?
          ├── YES → Explore
          └── NO → Plan (for architecture/design tasks)
```

## Agent Type Comparison

| Agent Type                   | Can Read | Can Write | Can Edit | Can Bash | Specialized        |
| ---------------------------- | -------- | --------- | -------- | -------- | ------------------ |
| general-purpose              | Yes      | Yes       | Yes      | Yes      | No                 |
| Explore                      | Yes      | No        | No       | No       | Search/explore     |
| Plan                         | Yes      | No        | No       | No       | Architecture       |
| agent-teams:team-lead        | Yes      | Yes       | Yes      | Yes      | Team orchestration |
| agent-teams:team-reviewer    | Yes      | Yes       | Yes      | Yes      | Code review        |
| agent-teams:team-debugger    | Yes      | Yes       | Yes      | Yes      | Bug investigation  |
| agent-teams:team-implementer | Yes      | Yes       | Yes      | Yes      | Feature building   |

## Common Mistakes

| Mistake                               | Why It Fails                   | Correct Choice                          |
| ------------------------------------- | ------------------------------ | --------------------------------------- |
| Using `Explore` for implementation    | Cannot write/edit files        | `general-purpose` or `team-implementer` |
| Using `Plan` for coding tasks         | Cannot write/edit files        | `general-purpose` or `team-implementer` |
| Using `general-purpose` for reviews   | No review structure/checklists | `team-reviewer`                         |
| Using `team-implementer` for research | Has tools but wrong focus      | `Explore` or `Plan`                     |

## When to Use Each

### general-purpose

- One-off tasks that don't fit specialized roles
- Tasks requiring unique tool combinations
- Ad-hoc scripting or automation

### Explore

- Codebase research and analysis
- Finding files, patterns, or dependencies
- Understanding architecture before planning

### Plan

- Designing implementation approaches
- Creating task decompositions
- Architecture review (read-only)

### team-lead

- Coordinating multiple teammates
- Decomposing work and managing tasks
- Synthesizing results from parallel work

### team-reviewer

- Focused code review on a specific dimension
- Producing structured findings with severity ratings
- Following dimension-specific checklists

### team-debugger

- Investigating a specific hypothesis about a bug
- Gathering evidence with file:line citations
- Reporting confidence levels and causal chains

### team-implementer

- Building code within file ownership boundaries
- Following interface contracts
- Coordinating at integration points
