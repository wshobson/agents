# Artifact Templates

Starter templates for each Conductor context artifact. Copy and fill in for new projects.

> Contributed by [@fernandezbaptiste](https://github.com/fernandezbaptiste) ([#437](https://github.com/wshobson/agents/pull/437))

## product.md

```markdown
# [Product Name]

> One-line description of what this product does.

## Problem

What problem does this solve and for whom?

## Solution

High-level approach to solving the problem.

## Target Users

| Persona | Needs | Pain Points |
|---|---|---|
| Persona 1 | What they need | What frustrates them |

## Core Features

| Feature | Status | Description |
|---|---|---|
| Feature A | planned | What it does |
| Feature B | implemented | What it does |

## Success Metrics

| Metric | Target | Current |
|---|---|---|
| Metric 1 | target value | - |

## Roadmap

- **Phase 1**: scope
- **Phase 2**: scope
```

## tech-stack.md

```markdown
# Tech Stack

## Languages & Frameworks

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12 | Backend API |
| React | 18.x | Frontend UI |

## Key Dependencies

| Package | Version | Rationale |
|---|---|---|
| FastAPI | 0.100+ | REST API framework |
| SQLAlchemy | 2.x | ORM and database access |

## Infrastructure

| Component | Choice | Notes |
|---|---|---|
| Hosting | AWS ECS | Production containers |
| Database | PostgreSQL 16 | Primary data store |
| CI/CD | GitHub Actions | Build and deploy |

## Dev Tools

| Tool | Purpose | Config |
|---|---|---|
| pytest | Testing (target: 80% coverage) | pyproject.toml |
| ruff | Linting + formatting | ruff.toml |
```

## workflow.md

```markdown
# Workflow

## Methodology

TDD with trunk-based development.

## Git Conventions

- **Branch naming**: `feature/<track-id>-description`
- **Commit format**: `type(scope): message`
- **PR requirements**: 1 approval, all checks green

## Quality Gates

| Gate | Requirement |
|---|---|
| Tests | All pass, coverage >= 80% |
| Lint | Zero errors |
| Review | At least 1 approval |
| Types | No type errors |

## Deployment

1. PR merged to main
2. CI runs tests + build
3. Auto-deploy to staging
4. Manual promotion to production
```

## tracks.md

```markdown
# Tracks

## Active

| ID | Title | Status | Priority | Assignee |
|---|---|---|---|---|
| TRACK-001 | Feature name | in-progress | high | @person |

## Completed

| ID | Title | Completed |
|---|---|---|
| TRACK-000 | Initial setup | 2024-01-15 |
```

## product-guidelines.md

```markdown
# Product Guidelines

## Voice & Tone

- Professional but approachable
- Direct and concise
- Technical where needed, plain language by default

## Terminology

| Term | Use | Don't Use |
|---|---|---|
| workspace | preferred | project, repo |
| track | preferred | ticket, issue |

## Error Messages

Format: `[Component] What happened. What to do next.`
Example: `[Auth] Session expired. Please sign in again.`
```
