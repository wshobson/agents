# Agent Skills

Agent Skills are modular packages that extend Claude's capabilities with specialized domain knowledge, following Anthropic's [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md). This plugin ecosystem includes **55 specialized skills** across 15 plugins, enabling progressive disclosure and efficient token usage.

## Overview

Skills provide Claude with deep expertise in specific domains without loading everything into context upfront. Each skill includes:

- **YAML Frontmatter**: Name and activation criteria
- **Progressive Disclosure**: Metadata → Instructions → Resources
- **Activation Triggers**: Clear "Use when" clauses for automatic invocation

## Skills by Plugin

### Kubernetes Operations (4 skills)

| Skill | Description |
|-------|-------------|
| **k8s-manifest-generator** | Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices |
| **helm-chart-scaffolding** | Design, organize, and manage Helm charts for templating and packaging Kubernetes applications |
| **gitops-workflow** | Implement GitOps workflows with ArgoCD and Flux for automated, declarative deployments |
| **k8s-security-policies** | Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC |

### LLM Application Development (4 skills)

| Skill | Description |
|-------|-------------|
| **langchain-architecture** | Design LLM applications using LangChain framework with agents, memory, and tool integration |
| **prompt-engineering-patterns** | Master advanced prompt engineering techniques for LLM performance and reliability |
| **rag-implementation** | Build Retrieval-Augmented Generation systems with vector databases and semantic search |
| **llm-evaluation** | Implement comprehensive evaluation strategies with automated metrics and benchmarking |

### Backend Development (3 skills)

| Skill | Description |
|-------|-------------|
| **api-design-principles** | Master REST and GraphQL API design for intuitive, scalable, and maintainable APIs |
| **architecture-patterns** | Implement Clean Architecture, Hexagonal Architecture, and Domain-Driven Design |
| **microservices-patterns** | Design microservices with service boundaries, event-driven communication, and resilience |

### Developer Essentials (8 skills)

| Skill | Description |
|-------|-------------|
| **git-advanced-workflows** | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog |
| **sql-optimization-patterns** | Optimize SQL queries, indexing strategies, and EXPLAIN analysis for database performance |
| **error-handling-patterns** | Implement robust error handling with exceptions, Result types, and graceful degradation |
| **code-review-excellence** | Provide effective code reviews with constructive feedback and systematic analysis |
| **e2e-testing-patterns** | Build reliable E2E test suites with Playwright and Cypress for critical user workflows |
| **auth-implementation-patterns** | Implement authentication and authorization with JWT, OAuth2, sessions, and RBAC |
| **debugging-strategies** | Master systematic debugging techniques, profiling tools, and root cause analysis |
| **monorepo-management** | Manage monorepos with Turborepo, Nx, and pnpm workspaces for scalable multi-package projects |

### Blockchain & Web3 (4 skills)

| Skill | Description |
|-------|-------------|
| **defi-protocol-templates** | Implement DeFi protocols with templates for staking, AMMs, governance, and lending |
| **nft-standards** | Implement NFT standards (ERC-721, ERC-1155) with metadata and marketplace integration |
| **solidity-security** | Master smart contract security to prevent vulnerabilities and implement secure patterns |
| **web3-testing** | Test smart contracts using Hardhat and Foundry with unit tests and mainnet forking |

### CI/CD Automation (4 skills)

| Skill | Description |
|-------|-------------|
| **deployment-pipeline-design** | Design multi-stage CI/CD pipelines with approval gates and security checks |
| **github-actions-templates** | Create production-ready GitHub Actions workflows for testing, building, and deploying |
| **gitlab-ci-patterns** | Build GitLab CI/CD pipelines with multi-stage workflows and distributed runners |
| **secrets-management** | Implement secure secrets management using Vault, AWS Secrets Manager, or native solutions |

### Cloud Infrastructure (4 skills)

| Skill | Description |
|-------|-------------|
| **terraform-module-library** | Build reusable Terraform modules for AWS, Azure, and GCP infrastructure |
| **multi-cloud-architecture** | Design multi-cloud architectures avoiding vendor lock-in |
| **hybrid-cloud-networking** | Configure secure connectivity between on-premises and cloud platforms |
| **cost-optimization** | Optimize cloud costs through rightsizing, tagging, and reserved instances |

### Framework Migration (4 skills)

| Skill | Description |
|-------|-------------|
| **react-modernization** | Upgrade React apps, migrate to hooks, and adopt concurrent features |
| **angular-migration** | Migrate from AngularJS to Angular using hybrid mode and incremental rewriting |
| **database-migration** | Execute database migrations with zero-downtime strategies and transformations |
| **dependency-upgrade** | Manage major dependency upgrades with compatibility analysis and testing |

### Observability & Monitoring (4 skills)

| Skill | Description |
|-------|-------------|
| **prometheus-configuration** | Set up Prometheus for comprehensive metric collection and monitoring |
| **grafana-dashboards** | Create production Grafana dashboards for real-time system visualization |
| **distributed-tracing** | Implement distributed tracing with Jaeger and Tempo to track requests |
| **slo-implementation** | Define SLIs and SLOs with error budgets and alerting |

### Payment Processing (4 skills)

| Skill | Description |
|-------|-------------|
| **stripe-integration** | Implement Stripe payment processing for checkout, subscriptions, and webhooks |
| **paypal-integration** | Integrate PayPal payment processing with express checkout and subscriptions |
| **pci-compliance** | Implement PCI DSS compliance for secure payment card data handling |
| **billing-automation** | Build automated billing systems for recurring payments and invoicing |

### Python Development (5 skills)

| Skill | Description |
|-------|-------------|
| **async-python-patterns** | Master Python asyncio, concurrent programming, and async/await patterns |
| **python-testing-patterns** | Implement comprehensive testing with pytest, fixtures, and mocking |
| **python-packaging** | Create distributable Python packages with proper structure and PyPI publishing |
| **python-performance-optimization** | Profile and optimize Python code using cProfile and performance best practices |
| **uv-package-manager** | Master the uv package manager for fast dependency management and virtual environments |

### JavaScript/TypeScript (4 skills)

| Skill | Description |
|-------|-------------|
| **typescript-advanced-types** | Master TypeScript's advanced type system including generics and conditional types |
| **nodejs-backend-patterns** | Build production-ready Node.js services with Express/Fastify and best practices |
| **javascript-testing-patterns** | Implement comprehensive testing with Jest, Vitest, and Testing Library |
| **modern-javascript-patterns** | Master ES6+ features including async/await, destructuring, and functional programming |

### API Scaffolding (1 skill)

| Skill | Description |
|-------|-------------|
| **fastapi-templates** | Create production-ready FastAPI projects with async patterns and error handling |

### Machine Learning Operations (1 skill)

| Skill | Description |
|-------|-------------|
| **ml-pipeline-workflow** | Build end-to-end MLOps pipelines from data preparation through deployment |

### Security Scanning (1 skill)

| Skill | Description |
|-------|-------------|
| **sast-configuration** | Configure Static Application Security Testing tools for vulnerability detection |

## How Skills Work

### Activation

Skills are automatically activated when Claude detects matching patterns in your request:

```
User: "Set up Kubernetes deployment with Helm chart"
→ Activates: helm-chart-scaffolding, k8s-manifest-generator

User: "Build a RAG system for document Q&A"
→ Activates: rag-implementation, prompt-engineering-patterns

User: "Optimize Python async performance"
→ Activates: async-python-patterns, python-performance-optimization
```

### Progressive Disclosure

Skills use a three-tier architecture for token efficiency:

1. **Metadata** (Frontmatter): Name and activation criteria (always loaded)
2. **Instructions**: Core guidance and patterns (loaded when activated)
3. **Resources**: Examples and templates (loaded on demand)

### Integration with Agents

Skills work alongside agents to provide deep domain expertise:

- **Agents**: High-level reasoning and orchestration
- **Skills**: Specialized knowledge and implementation patterns

Example workflow:
```
backend-architect agent → Plans API architecture
  ↓
api-design-principles skill → Provides REST/GraphQL best practices
  ↓
fastapi-templates skill → Supplies production-ready templates
```

## Specification Compliance

All 55 skills follow the [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md):

- ✓ Required `name` field (hyphen-case)
- ✓ Required `description` field with "Use when" clause
- ✓ Descriptions under 1024 characters
- ✓ Complete, non-truncated descriptions
- ✓ Proper YAML frontmatter formatting

## Creating New Skills

To add a skill to a plugin:

1. Create `plugins/{plugin-name}/skills/{skill-name}/SKILL.md`
2. Add YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: What the skill does. Use when [activation trigger].
   ---
   ```
3. Write comprehensive skill content using progressive disclosure
4. Add skill path to `marketplace.json`:
   ```json
   {
     "name": "plugin-name",
     "skills": ["./skills/skill-name"]
   }
   ```

### Skill Structure

```
plugins/{plugin-name}/
└── skills/
    └── {skill-name}/
        └── SKILL.md        # Frontmatter + content
```

## Benefits

- **Token Efficiency**: Load only relevant knowledge when needed
- **Specialized Expertise**: Deep domain knowledge without bloat
- **Clear Activation**: Explicit triggers prevent unwanted invocation
- **Composability**: Mix and match skills across workflows
- **Maintainability**: Isolated updates don't affect other skills

## Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Agent Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
