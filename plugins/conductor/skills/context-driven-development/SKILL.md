---
name: context-driven-development
description: >-
  Creates and maintains project context artifacts (product.md, tech-stack.md, workflow.md, tracks.md)
  in a `conductor/` directory. Scaffolds new projects from scratch, extracts context from existing
  codebases, validates artifact consistency before implementation, and synchronizes documents as the
  project evolves. Use when setting up a project, creating or updating product docs, managing a tech
  stack file, defining development workflows, tracking work units, onboarding to an existing codebase,
  or running project scaffolding.
---

# Context-Driven Development

## Workflow

Follow **Context → Spec & Plan → Implement**:

1. **Context** — verify project artifacts exist and are current
2. **Spec** — define requirements and acceptance criteria for a work unit
3. **Plan** — break the spec into phased, actionable tasks
4. **Implement** — execute tasks following established workflow patterns

## Artifacts

| Artifact | Role | Update trigger |
|---|---|---|
| `product.md` | WHAT + WHY — vision, goals, users, features | Vision/goals change, features ship, audience shifts |
| `product-guidelines.md` | Voice, terminology, copy standards | Brand guidelines change, new terminology introduced |
| `tech-stack.md` | Languages, deps, infra, tools with versions | Deps added/upgraded, infra changes, new tools adopted |
| `workflow.md` | Methodology, git conventions, testing, quality gates | Practices evolve, standards change |
| `tracks.md` | Work-unit registry with status and assignees | Tracks created, status changes, tracks completed |

See [references/artifact-templates.md](references/artifact-templates.md) for copy-paste starter templates.

## Directory Structure

```
conductor/
├── index.md              # Navigation hub
├── product.md
├── product-guidelines.md
├── tech-stack.md
├── workflow.md
├── tracks.md
├── setup_state.json      # Resumable setup state
├── code_styleguides/     # Language-specific conventions
│   └── <language>.md
└── tracks/
    └── <track-id>/
        ├── spec.md
        ├── plan.md
        ├── metadata.json
        └── index.md
```

## Project Setup

| Scenario | Command | Behavior |
|---|---|---|
| **Greenfield** (new repo) | `/conductor:setup` | Interactively creates all artifacts, generates style guides, initializes empty tracks registry |
| **Brownfield** (existing repo) | `/conductor:setup` | Analyzes existing code, configs, and docs — pre-populates artifacts for review |

### Starting a New Track

```bash
# 1. validate context is current
cat conductor/tracks.md
cat conductor/tech-stack.md

# 2. create track directory and spec
mkdir -p conductor/tracks/TRACK-042
cat > conductor/tracks/TRACK-042/spec.md << 'EOF'
# Add Redis Caching
## Requirements
- Cache auth sessions in Redis
- TTL: 24 hours
## Acceptance Criteria
- [ ] Redis added to tech-stack.md with version and rationale
- [ ] Session lookup < 5ms p99
EOF

# 3. register the track
echo "| TRACK-042 | Add Redis caching | in-progress | high | @dev |" >> conductor/tracks.md

# 4. commit context before implementation
git add conductor/ && git commit -m "feat(conductor): add TRACK-042 redis caching spec"
```

## Pre-Implementation Validation

Before starting work on any track, confirm artifacts are current:

| Area | Check |
|---|---|
| Product | `product.md` reflects current vision, users, and feature list |
| Tech | `tech-stack.md` lists all deps with accurate versions |
| Workflow | `workflow.md` describes current practices and quality gates |
| Tracks | `tracks.md` shows all active work, no stale entries |

**On failure**: flag outdated items → propose specific updates → get confirmation before proceeding.

See [references/maintenance-principles.md](references/maintenance-principles.md) for artifact synchronization rules and dependency update procedures.

See [references/anti-patterns.md](references/anti-patterns.md) for common context management mistakes.

See [references/integration-patterns.md](references/integration-patterns.md) for IDE, git hook, and CI/CD integration guidance.

See [references/best-practices.md](references/best-practices.md) for session continuity and context management tips.
