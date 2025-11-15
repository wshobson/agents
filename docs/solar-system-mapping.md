# Solar System Agent Mapping

This document maps all 65 existing plugins to the new solar system architecture.

## ☀️ The Sun

**Plugin:** `solar-core`
**Location:** `plugins/solar-core/`
**Agent:** `solar-orchestrator.md`
**Purpose:** Central task analysis and routing to appropriate planets

---

## ☿ Mercury (Speed & CLI)

**Orbital Distance:** 1 (closest, fastest)
**Model:** Haiku (speed optimized)
**Core Function:** Fast operations, shell scripting, quick debugging

### Plugins (3)
1. `shell-scripting`
2. `debugging-toolkit`
3. `error-debugging`

### Agents (7)
- bash-pro
- posix-shell-pro
- debugger (2 uses)
- dx-optimizer
- error-detective (2 uses)

### Skills (3)
- bash-defensive-patterns
- shellcheck-configuration
- bats-testing-patterns

---

## ♀ Venus (Frontend & Beauty)

**Orbital Distance:** 2
**Model:** Sonnet (complex UI reasoning)
**Core Function:** User interfaces, mobile apps, accessibility

### Plugins (3)
1. `frontend-mobile-development`
2. `multi-platform-apps`
3. `accessibility-compliance`

### Agents (7)
- frontend-developer (5 uses)
- mobile-developer (2 uses)
- flutter-expert
- ios-developer
- ui-ux-designer
- ui-visual-validator
- frontend-security-coder

### Skills (0)
- (Could add UI/UX patterns)

---

## 🌍 Earth (Full-Stack & Integration)

**Orbital Distance:** 3 (balanced, most versatile)
**Model:** Hybrid (Sonnet → Haiku → Sonnet)
**Core Function:** Full-stack coordination, TDD, Git workflows

### Plugins (5)
1. `full-stack-orchestration`
2. `tdd-workflows`
3. `git-pr-workflows`
4. `unit-testing`
5. `developer-essentials`

### Agents (5)
- test-automator (4 uses)
- tdd-orchestrator (2 uses)
- code-reviewer (7 uses - MOST USED)
- security-auditor (5 uses)
- deployment-engineer (4 uses)
- performance-engineer (5 uses)

### Skills (8)
- git-advanced-workflows
- sql-optimization-patterns
- error-handling-patterns
- code-review-excellence
- e2e-testing-patterns
- auth-implementation-patterns
- debugging-strategies
- monorepo-management

---

## ♂ Mars (Backend & APIs)

**Orbital Distance:** 4
**Model:** Sonnet (architecture decisions)
**Core Function:** Backend APIs, GraphQL, server-side logic

### Plugins (4)
1. `backend-development`
2. `api-scaffolding`
3. `api-testing-observability`
4. `backend-api-security`

### Agents (7)
- backend-architect (8 uses - MOST POPULAR!)
- graphql-architect (2 uses)
- fastapi-pro (2 uses)
- django-pro (2 uses)
- backend-security-coder (2 uses)
- api-documenter (2 uses)

### Skills (4)
- api-design-principles
- architecture-patterns
- microservices-patterns
- fastapi-templates

---

## ♃ Jupiter (Infrastructure & Cloud)

**Orbital Distance:** 5 (largest, most complex)
**Model:** Hybrid (planning + execution)
**Core Function:** Cloud, Kubernetes, CI/CD, deployment

### Plugins (5)
1. `cloud-infrastructure`
2. `kubernetes-operations`
3. `cicd-automation`
4. `deployment-strategies`
5. `deployment-validation`

### Agents (11)
- cloud-architect (4 uses)
- kubernetes-architect (3 uses)
- terraform-specialist (3 uses)
- deployment-engineer (4 uses)
- network-engineer (2 uses)
- hybrid-cloud-architect
- devops-troubleshooter (2 uses)

### Skills (12)
- terraform-module-library
- cost-optimization
- hybrid-cloud-networking
- multi-cloud-architecture
- k8s-manifest-generator
- helm-chart-scaffolding
- gitops-workflow
- k8s-security-policies
- deployment-pipeline-design
- github-actions-templates
- gitlab-ci-patterns
- secrets-management

---

## ♄ Saturn (Data, AI & ML)

**Orbital Distance:** 6
**Model:** Sonnet (complex data patterns)
**Core Function:** Machine learning, data engineering, LLMs, databases

### Plugins (6)
1. `machine-learning-ops`
2. `data-engineering`
3. `llm-application-dev`
4. `database-design`
5. `database-migrations`
6. `agent-orchestration`

### Agents (12)
- data-scientist
- ml-engineer
- mlops-engineer
- data-engineer (2 uses)
- ai-engineer
- prompt-engineer
- context-manager (2 uses)
- database-architect (3 uses)
- sql-pro
- database-optimizer (3 uses)
- database-admin

### Skills (6)
- ml-pipeline-workflow
- langchain-architecture
- llm-evaluation
- prompt-engineering-patterns
- rag-implementation
- postgresql

---

## ♅ Uranus (Security & Compliance)

**Orbital Distance:** 7
**Model:** Sonnet (careful security analysis)
**Core Function:** Security scanning, compliance, vulnerability detection

### Plugins (4)
1. `security-scanning`
2. `security-compliance`
3. `backend-api-security`
4. `frontend-mobile-security`

### Agents (4)
- security-auditor (5 uses)
- backend-security-coder (2 uses)
- frontend-security-coder
- mobile-security-coder

### Skills (1)
- sast-configuration

---

## ♆ Neptune (Operations & Monitoring)

**Orbital Distance:** 8 (furthest, deepest)
**Model:** Hybrid (fast response + deep analysis)
**Core Function:** Observability, incident response, performance

### Plugins (5)
1. `observability-monitoring`
2. `incident-response`
3. `error-diagnostics`
4. `distributed-debugging`
5. `application-performance`
6. `database-cloud-optimization`

### Agents (6)
- observability-engineer (2 uses)
- incident-responder
- devops-troubleshooter (2 uses)
- performance-engineer (5 uses)
- database-optimizer (3 uses)

### Skills (4)
- distributed-tracing
- grafana-dashboards
- prometheus-configuration
- slo-implementation

---

## ☄️ Asteroid Belt (Documentation & Quality)

**Location:** Between Mars and Jupiter
**Model:** Mixed
**Core Function:** Documentation, code quality, refactoring

### Plugins (10)
1. `code-documentation`
2. `documentation-generation`
3. `code-review-ai`
4. `code-refactoring`
5. `comprehensive-review`
6. `performance-testing-review`
7. `framework-migration`
8. `codebase-cleanup`
9. `dependency-management`
10. `context-management`

### Agents (11)
- docs-architect (2 uses)
- tutorial-engineer (2 uses)
- api-documenter (2 uses)
- mermaid-expert
- reference-builder
- architect-review (2 uses)
- legacy-modernizer (3 uses)

### Skills (4)
- angular-migration
- database-migration
- dependency-upgrade
- react-modernization

---

## 🌌 Kuiper Belt (Specialized Domains)

**Location:** Beyond Neptune
**Model:** Specialized per domain
**Core Function:** Domain-specific expertise

### Language Planets (7 plugins)
1. `python-development` (3 agents, 5 skills)
2. `javascript-typescript` (2 agents, 4 skills)
3. `systems-programming` (4 agents: Rust, Go, C, C++)
4. `jvm-languages` (3 agents: Java, Scala, C#)
5. `web-scripting` (2 agents: PHP, Ruby)
6. `functional-programming` (1 agent: Elixir)
7. `julia-development` (1 agent)
8. `arm-cortex-microcontrollers` (1 agent)

### Business & Marketing (7 plugins)
1. `business-analytics`
2. `hr-legal-compliance`
3. `customer-sales-automation`
4. `content-marketing`
5. `seo-content-creation`
6. `seo-technical-optimization`
7. `seo-analysis-monitoring`

### Specialized Industries (5 plugins)
1. `blockchain-web3` (1 agent, 4 skills)
2. `quantitative-trading` (2 agents)
3. `payment-processing` (1 agent, 4 skills)
4. `game-development` (2 agents)
5. `data-validation-suite` (1 agent)

### Team Utilities (2 plugins)
1. `team-collaboration`
2. `error-debugging`

---

## Summary Statistics

### By Planet
- **Mercury:** 3 plugins, 7 agents, 3 skills
- **Venus:** 3 plugins, 7 agents, 0 skills
- **Earth:** 5 plugins, 6 core agents (highly reused), 8 skills
- **Mars:** 4 plugins, 7 agents, 4 skills
- **Jupiter:** 5 plugins, 11 agents, 12 skills
- **Saturn:** 6 plugins, 12 agents, 6 skills
- **Uranus:** 4 plugins, 4 agents, 1 skill
- **Neptune:** 6 plugins, 6 agents, 4 skills
- **Asteroid Belt:** 10 plugins, 11 agents, 4 skills
- **Kuiper Belt:** 24 plugins, 50+ agents, 13+ skills

### Total
- **65 plugins** mapped
- **~100 unique agents**
- **47 skills**

---

## Gravitational Relationships

### Most Influential Agents (High Gravity)
1. **backend-architect** (8 uses) → Mars core
2. **code-reviewer** (7 uses) → Earth core
3. **security-auditor** (5 uses) → Uranus core, Earth moon
4. **performance-engineer** (5 uses) → Neptune core, Earth moon
5. **frontend-developer** (5 uses) → Venus core

### Common Multi-Planet Workflows

**Full-Stack Feature:**
```
Sun → Earth (tdd-orchestrator) →
      Mars (backend-architect) →
      Venus (frontend-developer) →
      Jupiter (deployment-engineer) →
      Neptune (observability-engineer)
```

**Security Hardening:**
```
Sun → Uranus (security-auditor) →
      Mars (backend-security-coder) →
      Venus (frontend-security-coder) →
      Neptune (observability-engineer)
```

**ML Pipeline:**
```
Sun → Saturn (mlops-engineer) →
      Saturn/data-engineer →
      Jupiter (cloud-architect) →
      Neptune (observability-engineer)
```

---

## Migration Strategy

1. **Phase 1:** Create solar-core plugin with Sun orchestrator
2. **Phase 2:** Create planet directories (mercury, venus, earth, mars, jupiter, saturn, uranus, neptune)
3. **Phase 3:** Create asteroid-belt and kuiper-belt directories
4. **Phase 4:** Move existing plugins to appropriate planet directories
5. **Phase 5:** Update marketplace.json with new structure
6. **Phase 6:** Create planet-specific orchestrator agents
7. **Phase 7:** Update documentation and README

---

Generated: 2025-11-15
