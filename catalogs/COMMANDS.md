# Commands Catalog

> **70 Slash Commands** for direct tool invocation in Claude Code.

## Overview

| Metric | Count |
|--------|-------|
| Total Commands | 70 |
| Command Categories | 18 |

**Usage:**
Commands are invoked using slash syntax: `/plugin-name:command-name`

Example: `/tdd-workflows:tdd-cycle` or `/security-scanning:security-sast`

---

## Development & Feature Building (5 commands)

### /backend-development:feature-development
**Backend feature implementation with TDD approach**

- **Plugin:** backend-development
- **Location:** `plugins/backend-development/commands/feature-development.md`
- **Description:** Implements backend features using test-driven development methodology with proper architecture patterns

---

### /full-stack-orchestration:full-stack-feature
**Full-stack feature orchestration**

- **Plugin:** full-stack-orchestration
- **Location:** `plugins/full-stack-orchestration/commands/full-stack-feature.md`
- **Description:** End-to-end feature development coordinating frontend, backend, testing, security, and deployment

---

### /multi-platform-apps:multi-platform
**Cross-platform application development**

- **Plugin:** multi-platform-apps
- **Location:** `plugins/multi-platform-apps/commands/multi-platform.md`
- **Description:** Coordinate development across web, iOS, Android, and desktop platforms

---

### /python-development:python-scaffold
**Python project scaffolding**

- **Plugin:** python-development
- **Location:** `plugins/python-development/commands/python-scaffold.md`
- **Description:** Scaffold new Python projects with modern best practices, testing, and tooling

---

### /javascript-typescript:typescript-scaffold
**TypeScript project scaffolding**

- **Plugin:** javascript-typescript
- **Location:** `plugins/javascript-typescript/commands/typescript-scaffold.md`
- **Description:** Scaffold TypeScript projects with proper configuration and tooling

---

## Testing & TDD (5 commands)

### /unit-testing:test-generate
**Generate unit tests**

- **Plugin:** unit-testing
- **Location:** `plugins/unit-testing/commands/test-generate.md`
- **Description:** Automatically generate unit tests for Python and JavaScript code

---

### /tdd-workflows:tdd-cycle
**Complete TDD cycle**

- **Plugin:** tdd-workflows
- **Location:** `plugins/tdd-workflows/commands/tdd-cycle.md`
- **Description:** Execute full red-green-refactor TDD cycle

---

### /tdd-workflows:tdd-red
**Write failing tests (Red phase)**

- **Plugin:** tdd-workflows
- **Location:** `plugins/tdd-workflows/commands/tdd-red.md`
- **Description:** Write failing tests before implementation

---

### /tdd-workflows:tdd-green
**Implement passing code (Green phase)**

- **Plugin:** tdd-workflows
- **Location:** `plugins/tdd-workflows/commands/tdd-green.md`
- **Description:** Implement minimum code to pass tests

---

### /tdd-workflows:tdd-refactor
**Refactor code (Refactor phase)**

- **Plugin:** tdd-workflows
- **Location:** `plugins/tdd-workflows/commands/tdd-refactor.md`
- **Description:** Refactor code while keeping tests green

---

## Code Review & Quality (6 commands)

### /code-review-ai:ai-review
**AI-powered code review**

- **Plugin:** code-review-ai
- **Location:** `plugins/code-review-ai/commands/ai-review.md`
- **Description:** Get AI-powered architectural and code quality analysis

---

### /comprehensive-review:full-review
**Multi-perspective code review**

- **Plugin:** comprehensive-review
- **Location:** `plugins/comprehensive-review/commands/full-review.md`
- **Description:** Comprehensive review covering architecture, security, and best practices

---

### /comprehensive-review:pr-enhance
**PR enhancement suggestions**

- **Plugin:** comprehensive-review
- **Location:** `plugins/comprehensive-review/commands/pr-enhance.md`
- **Description:** Enhance pull request with better description, tests, and documentation

---

### /performance-testing-review:ai-review
**Performance-focused review**

- **Plugin:** performance-testing-review
- **Location:** `plugins/performance-testing-review/commands/ai-review.md`
- **Description:** Code review focused on performance implications

---

### /performance-testing-review:multi-agent-review
**Multi-agent performance analysis**

- **Plugin:** performance-testing-review
- **Location:** `plugins/performance-testing-review/commands/multi-agent-review.md`
- **Description:** Multiple agents analyze code for performance issues

---

### /error-debugging:multi-agent-review
**Multi-agent error investigation**

- **Plugin:** error-debugging
- **Location:** `plugins/error-debugging/commands/multi-agent-review.md`
- **Description:** Multiple agents investigate error root causes

---

## Documentation (3 commands)

### /code-documentation:doc-generate
**Generate documentation**

- **Plugin:** code-documentation
- **Location:** `plugins/code-documentation/commands/doc-generate.md`
- **Description:** Generate comprehensive documentation for code

---

### /code-documentation:code-explain
**Explain code**

- **Plugin:** code-documentation
- **Location:** `plugins/code-documentation/commands/code-explain.md`
- **Description:** Get detailed explanation of code functionality

---

### /documentation-generation:doc-generate
**Full documentation generation**

- **Plugin:** documentation-generation
- **Location:** `plugins/documentation-generation/commands/doc-generate.md`
- **Description:** Generate OpenAPI specs, diagrams, tutorials, and API references

---

## Debugging & Troubleshooting (7 commands)

### /debugging-toolkit:smart-debug
**Smart debugging**

- **Plugin:** debugging-toolkit
- **Location:** `plugins/debugging-toolkit/commands/smart-debug.md`
- **Description:** Intelligent debugging with context-aware suggestions

---

### /error-debugging:error-analysis
**Error analysis**

- **Plugin:** error-debugging
- **Location:** `plugins/error-debugging/commands/error-analysis.md`
- **Description:** Analyze error messages and suggest fixes

---

### /error-debugging:error-trace
**Error tracing**

- **Plugin:** error-debugging
- **Location:** `plugins/error-debugging/commands/error-trace.md`
- **Description:** Trace error through the codebase

---

### /error-diagnostics:error-trace
**Production error tracing**

- **Plugin:** error-diagnostics
- **Location:** `plugins/error-diagnostics/commands/error-trace.md`
- **Description:** Trace errors in production systems

---

### /error-diagnostics:error-analysis
**Root cause analysis**

- **Plugin:** error-diagnostics
- **Location:** `plugins/error-diagnostics/commands/error-analysis.md`
- **Description:** Deep root cause analysis for errors

---

### /error-diagnostics:smart-debug
**Smart debugging for production**

- **Plugin:** error-diagnostics
- **Location:** `plugins/error-diagnostics/commands/smart-debug.md`
- **Description:** Production-aware smart debugging

---

### /distributed-debugging:debug-trace
**Distributed system debugging**

- **Plugin:** distributed-debugging
- **Location:** `plugins/distributed-debugging/commands/debug-trace.md`
- **Description:** Debug across distributed microservices

---

## Refactoring & Code Management (6 commands)

### /code-refactoring:refactor-clean
**Code refactoring**

- **Plugin:** code-refactoring
- **Location:** `plugins/code-refactoring/commands/refactor-clean.md`
- **Description:** Clean and refactor code with best practices

---

### /code-refactoring:tech-debt
**Technical debt management**

- **Plugin:** code-refactoring
- **Location:** `plugins/code-refactoring/commands/tech-debt.md`
- **Description:** Identify and manage technical debt

---

### /code-refactoring:context-restore
**Context restoration**

- **Plugin:** code-refactoring
- **Location:** `plugins/code-refactoring/commands/context-restore.md`
- **Description:** Restore context from previous sessions

---

### /codebase-cleanup:tech-debt
**Technical debt analysis**

- **Plugin:** codebase-cleanup
- **Location:** `plugins/codebase-cleanup/commands/tech-debt.md`
- **Description:** Analyze and prioritize technical debt

---

### /codebase-cleanup:refactor-clean
**Codebase cleanup**

- **Plugin:** codebase-cleanup
- **Location:** `plugins/codebase-cleanup/commands/refactor-clean.md`
- **Description:** Clean up codebase and reduce complexity

---

### /codebase-cleanup:deps-audit
**Dependency audit**

- **Plugin:** codebase-cleanup
- **Location:** `plugins/codebase-cleanup/commands/deps-audit.md`
- **Description:** Audit dependencies for security and updates

---

## Git & Workflows (5 commands)

### /git-pr-workflows:pr-enhance
**PR enhancement**

- **Plugin:** git-pr-workflows
- **Location:** `plugins/git-pr-workflows/commands/pr-enhance.md`
- **Description:** Enhance pull requests with better content

---

### /git-pr-workflows:onboard
**Team onboarding**

- **Plugin:** git-pr-workflows
- **Location:** `plugins/git-pr-workflows/commands/onboard.md`
- **Description:** Generate onboarding documentation for new team members

---

### /git-pr-workflows:git-workflow
**Git automation**

- **Plugin:** git-pr-workflows
- **Location:** `plugins/git-pr-workflows/commands/git-workflow.md`
- **Description:** Automate common git workflows

---

### /framework-migration:code-migrate
**Code migration**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/commands/code-migrate.md`
- **Description:** Migrate code between frameworks or versions

---

### /framework-migration:legacy-modernize
**Legacy modernization**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/commands/legacy-modernize.md`
- **Description:** Modernize legacy code patterns

---

## Dependency Management (2 commands)

### /dependency-management:deps-audit
**Dependency audit**

- **Plugin:** dependency-management
- **Location:** `plugins/dependency-management/commands/deps-audit.md`
- **Description:** Audit and analyze project dependencies

---

### /framework-migration:deps-upgrade
**Dependency upgrade**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/commands/deps-upgrade.md`
- **Description:** Upgrade dependencies with compatibility checks

---

## Security & Compliance (5 commands)

### /security-scanning:security-hardening
**Security hardening**

- **Plugin:** security-scanning
- **Location:** `plugins/security-scanning/commands/security-hardening.md`
- **Description:** Apply security hardening measures

---

### /security-scanning:security-sast
**SAST analysis**

- **Plugin:** security-scanning
- **Location:** `plugins/security-scanning/commands/security-sast.md`
- **Description:** Run static application security testing

---

### /security-scanning:security-dependencies
**Dependency security scanning**

- **Plugin:** security-scanning
- **Location:** `plugins/security-scanning/commands/security-dependencies.md`
- **Description:** Scan dependencies for vulnerabilities

---

### /security-compliance:compliance-check
**Compliance validation**

- **Plugin:** security-compliance
- **Location:** `plugins/security-compliance/commands/compliance-check.md`
- **Description:** Validate SOC2, HIPAA, GDPR compliance

---

### /frontend-mobile-security:xss-scan
**XSS vulnerability scanning**

- **Plugin:** frontend-mobile-security
- **Location:** `plugins/frontend-mobile-security/commands/xss-scan.md`
- **Description:** Scan for XSS vulnerabilities

---

## Infrastructure & Deployment (4 commands)

### /deployment-validation:config-validate
**Configuration validation**

- **Plugin:** deployment-validation
- **Location:** `plugins/deployment-validation/commands/config-validate.md`
- **Description:** Validate deployment configurations

---

### /cicd-automation:workflow-automate
**CI/CD workflow automation**

- **Plugin:** cicd-automation
- **Location:** `plugins/cicd-automation/commands/workflow-automate.md`
- **Description:** Automate CI/CD pipeline workflows

---

### /systems-programming:rust-project
**Rust project scaffolding**

- **Plugin:** systems-programming
- **Location:** `plugins/systems-programming/commands/rust-project.md`
- **Description:** Scaffold new Rust projects

---

### /frontend-mobile-development:component-scaffold
**Component scaffolding**

- **Plugin:** frontend-mobile-development
- **Location:** `plugins/frontend-mobile-development/commands/component-scaffold.md`
- **Description:** Scaffold frontend components

---

## Observability & Monitoring (2 commands)

### /observability-monitoring:monitor-setup
**Monitoring setup**

- **Plugin:** observability-monitoring
- **Location:** `plugins/observability-monitoring/commands/monitor-setup.md`
- **Description:** Set up monitoring infrastructure

---

### /observability-monitoring:slo-implement
**SLO implementation**

- **Plugin:** observability-monitoring
- **Location:** `plugins/observability-monitoring/commands/slo-implement.md`
- **Description:** Implement SLOs and alerting

---

## Data & ML (3 commands)

### /data-engineering:data-driven-feature
**Data-driven features**

- **Plugin:** data-engineering
- **Location:** `plugins/data-engineering/commands/data-driven-feature.md`
- **Description:** Build data-driven features

---

### /data-engineering:data-pipeline
**Data pipeline creation**

- **Plugin:** data-engineering
- **Location:** `plugins/data-engineering/commands/data-pipeline.md`
- **Description:** Create ETL data pipelines

---

### /machine-learning-ops:ml-pipeline
**ML pipeline orchestration**

- **Plugin:** machine-learning-ops
- **Location:** `plugins/machine-learning-ops/commands/ml-pipeline.md`
- **Description:** Orchestrate ML training and deployment pipelines

---

## Database (2 commands)

### /database-migrations:sql-migrations
**SQL migration management**

- **Plugin:** database-migrations
- **Location:** `plugins/database-migrations/commands/sql-migrations.md`
- **Description:** Manage SQL database migrations

---

### /database-migrations:migration-observability
**Migration monitoring**

- **Plugin:** database-migrations
- **Location:** `plugins/database-migrations/commands/migration-observability.md`
- **Description:** Monitor database migration health

---

## API Development (1 command)

### /api-testing-observability:api-mock
**API mocking**

- **Plugin:** api-testing-observability
- **Location:** `plugins/api-testing-observability/commands/api-mock.md`
- **Description:** Create API mocks for testing

---

## Performance & Optimization (2 commands)

### /application-performance:performance-optimization
**Performance tuning**

- **Plugin:** application-performance
- **Location:** `plugins/application-performance/commands/performance-optimization.md`
- **Description:** Optimize application performance

---

### /database-cloud-optimization:cost-optimize
**Cost optimization**

- **Plugin:** database-cloud-optimization
- **Location:** `plugins/database-cloud-optimization/commands/cost-optimize.md`
- **Description:** Optimize cloud and database costs

---

## AI & LLM Applications (3 commands)

### /llm-application-dev:langchain-agent
**LangChain agents**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/commands/langchain-agent.md`
- **Description:** Create LangChain-based agents

---

### /llm-application-dev:ai-assistant
**AI assistant creation**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/commands/ai-assistant.md`
- **Description:** Build AI assistant applications

---

### /llm-application-dev:prompt-optimize
**Prompt optimization**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/commands/prompt-optimize.md`
- **Description:** Optimize prompts for better results

---

## Agent Orchestration (2 commands)

### /agent-orchestration:multi-agent-optimize
**Multi-agent optimization**

- **Plugin:** agent-orchestration
- **Location:** `plugins/agent-orchestration/commands/multi-agent-optimize.md`
- **Description:** Optimize multi-agent system performance

---

### /agent-orchestration:improve-agent
**Agent improvement**

- **Plugin:** agent-orchestration
- **Location:** `plugins/agent-orchestration/commands/improve-agent.md`
- **Description:** Improve agent capabilities and performance

---

## Context Management (2 commands)

### /context-management:context-save
**Save context**

- **Plugin:** context-management
- **Location:** `plugins/context-management/commands/context-save.md`
- **Description:** Save current context for later restoration

---

### /context-management:context-restore
**Restore context**

- **Plugin:** context-management
- **Location:** `plugins/context-management/commands/context-restore.md`
- **Description:** Restore previously saved context

---

## Team & Collaboration (2 commands)

### /team-collaboration:issue
**Issue management**

- **Plugin:** team-collaboration
- **Location:** `plugins/team-collaboration/commands/issue.md`
- **Description:** Manage project issues and tasks

---

### /team-collaboration:standup-notes
**Standup notes**

- **Plugin:** team-collaboration
- **Location:** `plugins/team-collaboration/commands/standup-notes.md`
- **Description:** Generate standup meeting notes

---

## Accessibility (1 command)

### /accessibility-compliance:accessibility-audit
**WCAG accessibility audit**

- **Plugin:** accessibility-compliance
- **Location:** `plugins/accessibility-compliance/commands/accessibility-audit.md`
- **Description:** Audit for WCAG accessibility compliance

---

## Incident Management (2 commands)

### /incident-response:incident-response
**Incident response**

- **Plugin:** incident-response
- **Location:** `plugins/incident-response/commands/incident-response.md`
- **Description:** Coordinate incident response activities

---

### /incident-response:smart-fix
**Smart fix implementation**

- **Plugin:** incident-response
- **Location:** `plugins/incident-response/commands/smart-fix.md`
- **Description:** Implement smart fixes for incidents

---

## Commands by Category Summary

| Category | Command Count |
|----------|--------------|
| Debugging & Troubleshooting | 7 |
| Refactoring & Code Management | 6 |
| Code Review & Quality | 6 |
| Development & Feature Building | 5 |
| Testing & TDD | 5 |
| Git & Workflows | 5 |
| Security & Compliance | 5 |
| Infrastructure & Deployment | 4 |
| Documentation | 3 |
| Data & ML | 3 |
| AI & LLM Applications | 3 |
| Observability & Monitoring | 2 |
| Database | 2 |
| Performance & Optimization | 2 |
| Dependency Management | 2 |
| Agent Orchestration | 2 |
| Context Management | 2 |
| Team & Collaboration | 2 |
| Incident Management | 2 |
| API Development | 1 |
| Accessibility | 1 |
