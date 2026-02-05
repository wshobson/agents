# Preset Team Definitions

Detailed preset team configurations with task templates for common workflows.

## Review Team Preset

**Command**: `/team-spawn review`

### Configuration

- **Team Size**: 3
- **Agent Type**: `agent-teams:team-reviewer`
- **Display Mode**: tmux recommended

### Members

| Name                  | Dimension    | Focus Areas                                       |
| --------------------- | ------------ | ------------------------------------------------- |
| security-reviewer     | Security     | Input validation, auth, injection, secrets, CVEs  |
| performance-reviewer  | Performance  | Query efficiency, memory, caching, async patterns |
| architecture-reviewer | Architecture | SOLID, coupling, patterns, error handling         |

### Task Template

```
Subject: Review {target} for {dimension} issues
Description:
  Dimension: {dimension}
  Target: {file list or diff}
  Checklist: {dimension-specific checklist}
  Output format: Structured findings with file:line, severity, evidence, fix
```

### Variations

- **Security-focused**: `--reviewers security,testing` (2 members)
- **Full review**: `--reviewers security,performance,architecture,testing,accessibility` (5 members)
- **Frontend review**: `--reviewers architecture,testing,accessibility` (3 members)

## Debug Team Preset

**Command**: `/team-spawn debug`

### Configuration

- **Team Size**: 3 (default) or N with `--hypotheses N`
- **Agent Type**: `agent-teams:team-debugger`
- **Display Mode**: tmux recommended

### Members

| Name           | Role                      |
| -------------- | ------------------------- |
| investigator-1 | Investigates hypothesis 1 |
| investigator-2 | Investigates hypothesis 2 |
| investigator-3 | Investigates hypothesis 3 |

### Task Template

```
Subject: Investigate hypothesis: {hypothesis summary}
Description:
  Hypothesis: {full hypothesis statement}
  Scope: {files/module/project}
  Evidence criteria:
    Confirming: {what would confirm}
    Falsifying: {what would falsify}
  Report format: confidence level, evidence with file:line, causal chain
```

## Feature Team Preset

**Command**: `/team-spawn feature`

### Configuration

- **Team Size**: 3 (1 lead + 2 implementers)
- **Agent Types**: `agent-teams:team-lead` + `agent-teams:team-implementer`
- **Display Mode**: tmux recommended

### Members

| Name          | Role             | Responsibility                           |
| ------------- | ---------------- | ---------------------------------------- |
| feature-lead  | team-lead        | Decomposition, coordination, integration |
| implementer-1 | team-implementer | Work stream 1 (assigned files)           |
| implementer-2 | team-implementer | Work stream 2 (assigned files)           |

### Task Template

```
Subject: Implement {work stream name}
Description:
  Owned files: {explicit file list}
  Requirements: {specific deliverables}
  Interface contract: {shared types/APIs}
  Acceptance criteria: {verification steps}
  Blocked by: {dependency task IDs if any}
```

## Fullstack Team Preset

**Command**: `/team-spawn fullstack`

### Configuration

- **Team Size**: 4 (1 lead + 3 implementers)
- **Agent Types**: `agent-teams:team-lead` + 3x `agent-teams:team-implementer`
- **Display Mode**: tmux recommended

### Members

| Name           | Role             | Layer                            |
| -------------- | ---------------- | -------------------------------- |
| fullstack-lead | team-lead        | Coordination, integration        |
| frontend-dev   | team-implementer | UI components, client-side logic |
| backend-dev    | team-implementer | API endpoints, business logic    |
| test-dev       | team-implementer | Unit, integration, e2e tests     |

### Dependency Pattern

```
frontend-dev ──┐
               ├──→ test-dev (blocked by both)
backend-dev  ──┘
```

## Research Team Preset

**Command**: `/team-spawn research`

### Configuration

- **Team Size**: 3
- **Agent Type**: `general-purpose`
- **Display Mode**: tmux recommended

### Members

| Name         | Role            | Focus                                            |
| ------------ | --------------- | ------------------------------------------------ |
| researcher-1 | general-purpose | Research area 1 (e.g., codebase architecture)    |
| researcher-2 | general-purpose | Research area 2 (e.g., library documentation)    |
| researcher-3 | general-purpose | Research area 3 (e.g., web resources & examples) |

### Available Research Tools

Each researcher has access to:

- **Codebase**: `Grep`, `Glob`, `Read` — search and read local files
- **Web**: `WebSearch`, `WebFetch` — search the web and fetch page content
- **Deep Exploration**: `Task` with `subagent_type: Explore` — spawn sub-explorers for deep dives

### Task Template

```
Subject: Research {topic or question}
Description:
  Question: {specific research question}
  Scope: {codebase files, web resources, library docs, or all}
  Tools to prioritize:
    - Codebase: Grep/Glob/Read for local code analysis
    - Web: WebSearch/WebFetch for articles, examples, best practices
  Deliverable: Summary with citations (file:line for code, URLs for web)
  Output format: Structured report with sections, evidence, and recommendations
```

### Variations

- **Codebase-only**: 3 researchers exploring different modules or patterns locally
- **Web research**: 3 researchers using WebSearch to survey approaches, benchmarks, or best practices
- **Mixed**: 1 codebase researcher + 1 docs researcher + 1 web researcher (recommended for evaluating new libraries)

### Example Research Assignments

```
Researcher 1 (codebase): "How does our current auth system work? Trace the flow from login to token validation."
Researcher 2 (web): "Search for comparisons between NextAuth, Clerk, and Auth0 for Next.js apps. Focus on pricing, DX, and migration effort."
Researcher 3 (docs): "Look up the latest NextAuth.js v5 API docs. How does it handle JWT and session management?"
```

## Security Team Preset

**Command**: `/team-spawn security`

### Configuration

- **Team Size**: 4
- **Agent Type**: `agent-teams:team-reviewer`
- **Display Mode**: tmux recommended

### Members

| Name            | Dimension      | Focus Areas                                          |
| --------------- | -------------- | ---------------------------------------------------- |
| vuln-reviewer   | OWASP/Vulns    | Injection, XSS, CSRF, deserialization, SSRF          |
| auth-reviewer   | Auth/Access    | Authentication, authorization, session management    |
| deps-reviewer   | Dependencies   | CVEs, supply chain, outdated packages, license risks |
| config-reviewer | Secrets/Config | Hardcoded secrets, env vars, debug endpoints, CORS   |

### Task Template

```
Subject: Security audit {target} for {dimension}
Description:
  Dimension: {security sub-dimension}
  Target: {file list, directory, or entire project}
  Checklist: {dimension-specific security checklist}
  Output format: Structured findings with file:line, CVSS-like severity, evidence, remediation
  Standards: OWASP Top 10, CWE references where applicable
```

### Variations

- **Quick scan**: `--reviewers owasp,secrets` (2 members for fast audit)
- **Full audit**: All 4 dimensions (default)
- **CI/CD focused**: Add a 5th reviewer for pipeline security and deployment configuration

## Migration Team Preset

**Command**: `/team-spawn migration`

### Configuration

- **Team Size**: 4 (1 lead + 2 implementers + 1 reviewer)
- **Agent Types**: `agent-teams:team-lead` + 2x `agent-teams:team-implementer` + `agent-teams:team-reviewer`
- **Display Mode**: tmux recommended

### Members

| Name             | Role             | Responsibility                                  |
| ---------------- | ---------------- | ----------------------------------------------- |
| migration-lead   | team-lead        | Migration plan, coordination, conflict handling |
| migrator-1       | team-implementer | Migration stream 1 (assigned files/modules)     |
| migrator-2       | team-implementer | Migration stream 2 (assigned files/modules)     |
| migration-verify | team-reviewer    | Verify migrated code correctness and patterns   |

### Task Template

```
Subject: Migrate {module/files} from {old} to {new}
Description:
  Owned files: {explicit file list}
  Migration rules: {specific transformation patterns}
  Old pattern: {what to change from}
  New pattern: {what to change to}
  Acceptance criteria: {tests pass, no regressions, new patterns used}
  Blocked by: {dependency task IDs if any}
```

### Dependency Pattern

```
migration-lead (plan) → migrator-1 ──┐
                      → migrator-2 ──┼→ migration-verify
                                     ┘
```

### Use Cases

- Framework upgrades (React class → hooks, Vue 2 → Vue 3, Angular version bumps)
- Language migrations (JavaScript → TypeScript, Python 2 → 3)
- API version bumps (REST v1 → v2, GraphQL schema changes)
- Database migrations (ORM changes, schema restructuring)
- Build system changes (Webpack → Vite, CRA → Next.js)
