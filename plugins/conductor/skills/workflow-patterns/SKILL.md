---
name: workflow-patterns
description: Use this skill when implementing tasks according to Conductor's TDD workflow, handling phase checkpoints, managing git commits for tasks, or understanding the verification protocol.
version: 1.0.0
---

# Workflow Patterns

Guide for implementing tasks using Conductor's TDD workflow, managing phase checkpoints, handling git commits, and executing the verification protocol that ensures quality throughout implementation.

## When to Use This Skill

- Implementing tasks from a track's plan.md
- Following TDD red-green-refactor cycle
- Completing phase checkpoints
- Managing git commits and notes
- Understanding quality assurance gates
- Handling verification protocols
- Recording progress in plan files

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Never skip RED**: Always write failing tests first
2. **Small commits**: One logical change per commit
3. **Immediate updates**: Update plan.md right after task completion
4. **Wait for approval**: Never skip checkpoint verification
5. **Rich git notes**: Include context that helps future understanding
6. **Coverage discipline**: Don't accept coverage below target
7. **Quality gates**: Check all gates before marking complete
8. **Sequential phases**: Complete phases in order
9. **Document deviations**: Note any changes from original plan
10. **Clean state**: Each commit should leave code in working state
11. **Fast feedback**: Run relevant tests frequently during development
12. **Clear blockers**: Address blockers promptly, don't work around them
