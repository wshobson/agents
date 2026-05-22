---
name: context-driven-development
description: >-
  Creates and maintains project context artifacts (product.md, tech-stack.md, workflow.md, tracks.md)
  in a `conductor/` directory. Scaffolds new projects from scratch, extracts context from existing
  codebases, validates artifact consistency before implementation, and synchronizes documents as the
  project evolves. Use when setting up a project, creating or updating product docs, managing a tech
  stack file, defining development workflows, tracking work units, onboarding to an existing codebase,
  or running project scaffolding.
version: 1.0.0
---

# Context-Driven Development

Guide for implementing and maintaining context as a managed artifact alongside code, enabling consistent AI interactions and team alignment through structured project documentation.

## When to Use This Skill

- Setting up new projects with Conductor
- Understanding the relationship between context artifacts
- Maintaining consistency across AI-assisted development sessions
- Onboarding team members to an existing Conductor project
- Deciding when to update context documents
- Managing greenfield vs brownfield project contexts

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Read context first**: Always read relevant artifacts before starting work
2. **Small updates**: Make incremental context changes, not massive rewrites
3. **Link decisions**: Reference context when making implementation choices
4. **Version context**: Commit context changes alongside code changes
5. **Review context**: Include context artifact reviews in code reviews
6. **Validate regularly**: Run context validation checklist before major work
7. **Communicate changes**: Notify team when context artifacts change significantly
8. **Preserve history**: Use git to track context evolution over time
9. **Question staleness**: If context feels wrong, investigate and update
10. **Keep it actionable**: Every context item should inform a decision or behavior
