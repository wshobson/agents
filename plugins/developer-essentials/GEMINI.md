# Developer Essentials

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `monorepo-architect` | opus | Expert in monorepo architecture, build systems, and dependency management at scale. Masters Nx, Turborepo, Bazel, and... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `auth-implementation-patterns` | Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC to build secure, scalable access con... |
| `bazel-build-optimization` | Optimize Bazel builds for large-scale monorepos. Use when configuring Bazel, implementing remote execution, or optimizing build performan... |
| `code-review-excellence` | Master effective code review practices to provide constructive feedback, catch bugs early, and foster knowledge sharing while maintaining... |
| `debugging-strategies` | Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track down bugs across any codebase or te... |
| `e2e-testing-patterns` | Master end-to-end testing with Playwright and Cypress to build reliable test suites that catch bugs, improve confidence, and enable fast ... |
| `error-handling-patterns` | Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build ... |
| `git-advanced-workflows` | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover fro... |
| `monorepo-management` | Master monorepo management with Turborepo, Nx, and pnpm workspaces to build efficient, scalable multi-package repositories with optimized... |
| `nx-workspace-patterns` | Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or imple... |
| `sql-optimization-patterns` | Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow ... |
| `turborepo-caching` | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipeline... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert in monorepo architecture, build systems, and dependency management at scale" → activates `monorepo-architect`
- "Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC to build secure, scalable access control systems" → activates `auth-implementation-patterns` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
