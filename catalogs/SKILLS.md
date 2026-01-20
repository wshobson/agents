# Skills Catalog

> **61 Modular Agent Skills** with progressive disclosure for efficient token usage.

## Overview

| Metric | Count |
|--------|-------|
| Total Skills | 61 |
| Skill Categories | 16 |

**Design Philosophy:**
- Skills load knowledge only when needed (progressive disclosure)
- Modular knowledge packages for specific domains
- Follows Anthropic Agent Skills Specification
- Minimal token usage through on-demand activation

---

## Python Development (5 skills)

### async-python-patterns
**Asyncio and concurrent programming patterns**

- **Plugin:** python-development
- **Location:** `plugins/python-development/skills/async-python-patterns/SKILL.md`
- **Topics:**
  - asyncio event loops
  - async/await patterns
  - Concurrency with asyncio.gather
  - Task management
  - Async context managers

---

### python-testing-patterns
**Pytest and testing frameworks**

- **Plugin:** python-development
- **Location:** `plugins/python-development/skills/python-testing-patterns/SKILL.md`
- **Topics:**
  - pytest fixtures and markers
  - Parameterized testing
  - Mocking strategies
  - Test organization
  - Coverage configuration

---

### python-packaging
**Package distribution and PyPI publishing**

- **Plugin:** python-development
- **Location:** `plugins/python-development/skills/python-packaging/SKILL.md`
- **Topics:**
  - pyproject.toml configuration
  - setuptools and build
  - PyPI publishing
  - Version management
  - Package structure

---

### python-performance-optimization
**Profiling and performance optimization**

- **Plugin:** python-development
- **Location:** `plugins/python-development/skills/python-performance-optimization/SKILL.md`
- **Topics:**
  - cProfile and line_profiler
  - Memory profiling
  - Cython integration
  - NumPy optimization
  - Multiprocessing

---

### uv-package-manager
**Fast Python dependency management with uv**

- **Plugin:** python-development
- **Location:** `plugins/python-development/skills/uv-package-manager/SKILL.md`
- **Topics:**
  - uv installation and setup
  - Virtual environment management
  - Dependency resolution
  - Lock file management
  - Performance benefits over pip

---

## JavaScript/TypeScript (4 skills)

### typescript-advanced-types
**Advanced TypeScript type system**

- **Plugin:** javascript-typescript
- **Location:** `plugins/javascript-typescript/skills/typescript-advanced-types/SKILL.md`
- **Topics:**
  - Conditional types
  - Mapped types
  - Template literal types
  - Type inference
  - Type guards and narrowing

---

### nodejs-backend-patterns
**Node.js production patterns**

- **Plugin:** javascript-typescript
- **Location:** `plugins/javascript-typescript/skills/nodejs-backend-patterns/SKILL.md`
- **Topics:**
  - Express/Fastify patterns
  - Error handling middleware
  - Logging strategies
  - Graceful shutdown
  - Cluster mode

---

### javascript-testing-patterns
**Jest and testing strategies**

- **Plugin:** javascript-typescript
- **Location:** `plugins/javascript-typescript/skills/javascript-testing-patterns/SKILL.md`
- **Topics:**
  - Jest configuration
  - Mocking modules
  - Snapshot testing
  - Integration testing
  - Test utilities

---

### modern-javascript-patterns
**ES6+ features and patterns**

- **Plugin:** javascript-typescript
- **Location:** `plugins/javascript-typescript/skills/modern-javascript-patterns/SKILL.md`
- **Topics:**
  - Destructuring and spread
  - Modules (ESM)
  - Iterators and generators
  - Proxies and Reflect
  - Optional chaining

---

## Kubernetes Operations (4 skills)

### k8s-manifest-generator
**Production Kubernetes manifests**

- **Plugin:** kubernetes-operations
- **Location:** `plugins/kubernetes-operations/skills/k8s-manifest-generator/SKILL.md`
- **Topics:**
  - Deployment configurations
  - Service definitions
  - ConfigMaps and Secrets
  - Resource limits
  - Probes and health checks

---

### helm-chart-scaffolding
**Helm chart design and development**

- **Plugin:** kubernetes-operations
- **Location:** `plugins/kubernetes-operations/skills/helm-chart-scaffolding/SKILL.md`
- **Topics:**
  - Chart structure
  - Values file design
  - Template functions
  - Dependencies
  - Chart testing

---

### gitops-workflow
**ArgoCD and Flux implementation**

- **Plugin:** kubernetes-operations
- **Location:** `plugins/kubernetes-operations/skills/gitops-workflow/SKILL.md`
- **Topics:**
  - ArgoCD setup
  - Application definitions
  - Sync policies
  - Rollback strategies
  - Multi-cluster GitOps

---

### k8s-security-policies
**NetworkPolicy, RBAC, and PodSecurity**

- **Plugin:** kubernetes-operations
- **Location:** `plugins/kubernetes-operations/skills/k8s-security-policies/SKILL.md`
- **Topics:**
  - NetworkPolicy rules
  - RBAC configuration
  - PodSecurityPolicies
  - Service accounts
  - Secrets management

---

## Cloud Infrastructure (4 skills)

### terraform-module-library
**Reusable Terraform modules**

- **Plugin:** cloud-infrastructure
- **Location:** `plugins/cloud-infrastructure/skills/terraform-module-library/SKILL.md`
- **Topics:**
  - Module structure
  - Input variables
  - Output values
  - Module composition
  - State management

---

### multi-cloud-architecture
**Multi-cloud design patterns**

- **Plugin:** cloud-infrastructure
- **Location:** `plugins/cloud-infrastructure/skills/multi-cloud-architecture/SKILL.md`
- **Topics:**
  - Cloud-agnostic design
  - Cross-cloud networking
  - Data residency
  - Vendor lock-in avoidance
  - Cost optimization

---

### hybrid-cloud-networking
**On-premises/cloud connectivity**

- **Plugin:** cloud-infrastructure
- **Location:** `plugins/cloud-infrastructure/skills/hybrid-cloud-networking/SKILL.md`
- **Topics:**
  - VPN configuration
  - Direct Connect/ExpressRoute
  - Network peering
  - DNS resolution
  - Security groups

---

### cost-optimization
**Cloud cost optimization strategies**

- **Plugin:** cloud-infrastructure
- **Location:** `plugins/cloud-infrastructure/skills/cost-optimization/SKILL.md`
- **Topics:**
  - Reserved instances
  - Spot instances
  - Right-sizing
  - Cost monitoring
  - Budget alerts

---

## CI/CD Automation (4 skills)

### deployment-pipeline-design
**Multi-stage CI/CD pipelines**

- **Plugin:** cicd-automation
- **Location:** `plugins/cicd-automation/skills/deployment-pipeline-design/SKILL.md`
- **Topics:**
  - Pipeline stages
  - Approval gates
  - Environment promotion
  - Rollback strategies
  - Pipeline as code

---

### github-actions-templates
**GitHub Actions workflows**

- **Plugin:** cicd-automation
- **Location:** `plugins/cicd-automation/skills/github-actions-templates/SKILL.md`
- **Topics:**
  - Workflow syntax
  - Reusable workflows
  - Matrix builds
  - Caching strategies
  - Secrets management

---

### gitlab-ci-patterns
**GitLab CI pipelines**

- **Plugin:** cicd-automation
- **Location:** `plugins/cicd-automation/skills/gitlab-ci-patterns/SKILL.md`
- **Topics:**
  - .gitlab-ci.yml structure
  - Pipeline stages
  - Runners configuration
  - Artifacts management
  - Environments

---

### secrets-management
**Vault and secrets handling**

- **Plugin:** cicd-automation
- **Location:** `plugins/cicd-automation/skills/secrets-management/SKILL.md`
- **Topics:**
  - HashiCorp Vault
  - Secret rotation
  - Dynamic secrets
  - Access policies
  - Encryption at rest

---

## LLM Application Development (4 skills)

### langchain-architecture
**LangChain framework design**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/skills/langchain-architecture/SKILL.md`
- **Topics:**
  - Chain composition
  - Memory systems
  - Tool integration
  - Agent patterns
  - Custom components

---

### llm-evaluation
**LLM evaluation and benchmarking**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/skills/llm-evaluation/SKILL.md`
- **Topics:**
  - Evaluation metrics
  - Benchmark design
  - A/B testing
  - Human evaluation
  - Automated testing

---

### prompt-engineering-patterns
**Advanced prompt techniques**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/skills/prompt-engineering-patterns/SKILL.md`
- **Topics:**
  - Few-shot prompting
  - Chain-of-thought
  - Self-consistency
  - Prompt templates
  - Output parsing

---

### rag-implementation
**Retrieval-Augmented Generation**

- **Plugin:** llm-application-dev
- **Location:** `plugins/llm-application-dev/skills/rag-implementation/SKILL.md`
- **Topics:**
  - Vector databases
  - Embedding models
  - Chunking strategies
  - Retrieval optimization
  - Context management

---

## Backend Development (5 skills)

### api-design-principles
**REST and GraphQL design**

- **Plugin:** backend-development
- **Location:** `plugins/backend-development/skills/api-design-principles/SKILL.md`
- **Topics:**
  - RESTful conventions
  - Resource modeling
  - Versioning strategies
  - Error handling
  - Pagination patterns

---

### architecture-patterns
**Clean/Hexagonal/DDD patterns**

- **Plugin:** backend-development
- **Location:** `plugins/backend-development/skills/architecture-patterns/SKILL.md`
- **Topics:**
  - Clean Architecture
  - Hexagonal Architecture
  - Domain-Driven Design
  - CQRS
  - Event Sourcing

---

### microservices-patterns
**Microservice boundaries and communication**

- **Plugin:** backend-development
- **Location:** `plugins/backend-development/skills/microservices-patterns/SKILL.md`
- **Topics:**
  - Service boundaries
  - Communication patterns
  - Data consistency
  - Service discovery
  - Circuit breakers

---

### workflow-orchestration-patterns
**Durable workflows with Temporal**

- **Plugin:** backend-development
- **Location:** `plugins/backend-development/skills/workflow-orchestration-patterns/SKILL.md`
- **Topics:**
  - Temporal concepts
  - Workflow design
  - Activity implementation
  - Error handling
  - Worker configuration

---

### temporal-python-testing
**Temporal testing strategies**

- **Plugin:** backend-development
- **Location:** `plugins/backend-development/skills/temporal-python-testing/SKILL.md`
- **Topics:**
  - Workflow testing
  - Activity testing
  - Mock activities
  - Time manipulation
  - End-to-end testing

---

## Observability & Monitoring (4 skills)

### distributed-tracing
**Jaeger and Tempo tracing**

- **Plugin:** observability-monitoring
- **Location:** `plugins/observability-monitoring/skills/distributed-tracing/SKILL.md`
- **Topics:**
  - OpenTelemetry
  - Trace context
  - Span attributes
  - Sampling strategies
  - Trace visualization

---

### grafana-dashboards
**Dashboard creation and design**

- **Plugin:** observability-monitoring
- **Location:** `plugins/observability-monitoring/skills/grafana-dashboards/SKILL.md`
- **Topics:**
  - Dashboard design
  - Panel types
  - Variables and templating
  - Alerting
  - Dashboard as code

---

### prometheus-configuration
**Prometheus setup and configuration**

- **Plugin:** observability-monitoring
- **Location:** `plugins/observability-monitoring/skills/prometheus-configuration/SKILL.md`
- **Topics:**
  - Prometheus setup
  - Scrape configuration
  - Recording rules
  - Alert rules
  - Federation

---

### slo-implementation
**SLO definition and alerting**

- **Plugin:** observability-monitoring
- **Location:** `plugins/observability-monitoring/skills/slo-implementation/SKILL.md`
- **Topics:**
  - SLI definition
  - SLO calculation
  - Error budgets
  - Multi-window alerting
  - SLO dashboards

---

## Framework Migration (4 skills)

### react-modernization
**React upgrade strategies**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/skills/react-modernization/SKILL.md`
- **Topics:**
  - Class to hooks migration
  - State management updates
  - React 18 features
  - Concurrent mode
  - Performance improvements

---

### angular-migration
**AngularJS to Angular migration**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/skills/angular-migration/SKILL.md`
- **Topics:**
  - Migration strategies
  - ngUpgrade
  - Component architecture
  - RxJS patterns
  - Lazy loading

---

### database-migration
**Zero-downtime migrations**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/skills/database-migration/SKILL.md`
- **Topics:**
  - Schema migrations
  - Data migrations
  - Rollback strategies
  - Blue-green deployments
  - Feature flags

---

### dependency-upgrade
**Dependency compatibility management**

- **Plugin:** framework-migration
- **Location:** `plugins/framework-migration/skills/dependency-upgrade/SKILL.md`
- **Topics:**
  - Version compatibility
  - Breaking change analysis
  - Upgrade paths
  - Testing strategies
  - Lock file management

---

## Payment Processing (4 skills)

### stripe-integration
**Stripe payment processing**

- **Plugin:** payment-processing
- **Location:** `plugins/payment-processing/skills/stripe-integration/SKILL.md`
- **Topics:**
  - Stripe API integration
  - Payment intents
  - Subscriptions
  - Webhooks
  - Testing and sandbox

---

### paypal-integration
**PayPal payment integration**

- **Plugin:** payment-processing
- **Location:** `plugins/payment-processing/skills/paypal-integration/SKILL.md`
- **Topics:**
  - PayPal REST API
  - Checkout integration
  - Subscription billing
  - Dispute handling
  - Testing environment

---

### pci-compliance
**PCI DSS compliance**

- **Plugin:** payment-processing
- **Location:** `plugins/payment-processing/skills/pci-compliance/SKILL.md`
- **Topics:**
  - PCI DSS requirements
  - Cardholder data
  - Network security
  - Access control
  - Security testing

---

### billing-automation
**Recurring billing systems**

- **Plugin:** payment-processing
- **Location:** `plugins/payment-processing/skills/billing-automation/SKILL.md`
- **Topics:**
  - Subscription management
  - Invoice generation
  - Payment retry logic
  - Dunning management
  - Usage-based billing

---

## Blockchain & Web3 (4 skills)

### defi-protocol-templates
**DeFi protocol implementation**

- **Plugin:** blockchain-web3
- **Location:** `plugins/blockchain-web3/skills/defi-protocol-templates/SKILL.md`
- **Topics:**
  - Lending protocols
  - AMM design
  - Yield farming
  - Governance tokens
  - Flash loans

---

### nft-standards
**ERC-721/1155 standards**

- **Plugin:** blockchain-web3
- **Location:** `plugins/blockchain-web3/skills/nft-standards/SKILL.md`
- **Topics:**
  - ERC-721 implementation
  - ERC-1155 multi-token
  - Metadata standards
  - Royalties (EIP-2981)
  - Marketplace integration

---

### solidity-security
**Smart contract security**

- **Plugin:** blockchain-web3
- **Location:** `plugins/blockchain-web3/skills/solidity-security/SKILL.md`
- **Topics:**
  - Reentrancy prevention
  - Access control
  - Integer overflow
  - Oracle manipulation
  - Audit preparation

---

### web3-testing
**Hardhat and Foundry testing**

- **Plugin:** blockchain-web3
- **Location:** `plugins/blockchain-web3/skills/web3-testing/SKILL.md`
- **Topics:**
  - Hardhat testing
  - Foundry tests
  - Forking mainnet
  - Gas optimization
  - Coverage reports

---

## Database Design (1 skill)

### postgresql
**PostgreSQL optimization and design**

- **Plugin:** database-design
- **Location:** `plugins/database-design/skills/postgresql/SKILL.md`
- **Topics:**
  - Query optimization
  - Index strategies
  - Partitioning
  - JSONB operations
  - Performance tuning

---

## API Scaffolding (1 skill)

### fastapi-templates
**Production-ready FastAPI projects**

- **Plugin:** api-scaffolding
- **Location:** `plugins/api-scaffolding/skills/fastapi-templates/SKILL.md`
- **Topics:**
  - Project structure
  - Dependency injection
  - Authentication
  - Database integration
  - Testing patterns

---

## Machine Learning Operations (1 skill)

### ml-pipeline-workflow
**MLOps pipeline construction**

- **Plugin:** machine-learning-ops
- **Location:** `plugins/machine-learning-ops/skills/ml-pipeline-workflow/SKILL.md`
- **Topics:**
  - Pipeline design
  - Feature stores
  - Model registry
  - Experiment tracking
  - Model serving

---

## Security Scanning (1 skill)

### sast-configuration
**SAST tool configuration**

- **Plugin:** security-scanning
- **Location:** `plugins/security-scanning/skills/sast-configuration/SKILL.md`
- **Topics:**
  - Tool selection
  - Rule configuration
  - CI/CD integration
  - False positive management
  - Custom rules

---

## Developer Essentials (8 skills)

### git-advanced-workflows
**Git rebasing, cherry-picking, and bisect**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/git-advanced-workflows/SKILL.md`
- **Topics:**
  - Interactive rebase
  - Cherry-picking
  - Git bisect
  - Reflog recovery
  - Worktrees

---

### sql-optimization-patterns
**SQL tuning and indexing**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/sql-optimization-patterns/SKILL.md`
- **Topics:**
  - Query analysis
  - Index optimization
  - Execution plans
  - Query rewriting
  - Denormalization

---

### error-handling-patterns
**Robust error handling**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/error-handling-patterns/SKILL.md`
- **Topics:**
  - Error types
  - Exception handling
  - Error boundaries
  - Retry patterns
  - Graceful degradation

---

### code-review-excellence
**Effective code reviews**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/code-review-excellence/SKILL.md`
- **Topics:**
  - Review checklist
  - Constructive feedback
  - Automated checks
  - Review workflow
  - Knowledge sharing

---

### e2e-testing-patterns
**Playwright and Cypress testing**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/e2e-testing-patterns/SKILL.md`
- **Topics:**
  - Playwright setup
  - Cypress configuration
  - Page objects
  - Test data
  - CI integration

---

### auth-implementation-patterns
**JWT, OAuth2, sessions, and RBAC**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/auth-implementation-patterns/SKILL.md`
- **Topics:**
  - JWT implementation
  - OAuth2 flows
  - Session management
  - RBAC patterns
  - Security best practices

---

### debugging-strategies
**Systematic debugging techniques**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/debugging-strategies/SKILL.md`
- **Topics:**
  - Debugging methodology
  - Logging strategies
  - Breakpoint techniques
  - Performance debugging
  - Remote debugging

---

### monorepo-management
**Turborepo, Nx, and pnpm workspaces**

- **Plugin:** developer-essentials
- **Location:** `plugins/developer-essentials/skills/monorepo-management/SKILL.md`
- **Topics:**
  - Monorepo setup
  - Turborepo configuration
  - Nx workspace
  - pnpm workspaces
  - Build caching

---

## Shell Scripting (3 skills)

### bash-defensive-patterns
**Defensive Bash programming**

- **Plugin:** shell-scripting
- **Location:** `plugins/shell-scripting/skills/bash-defensive-patterns/SKILL.md`
- **Topics:**
  - set -euo pipefail
  - Error handling
  - Input validation
  - Quoting rules
  - Portable patterns

---

### shellcheck-configuration
**ShellCheck tool setup**

- **Plugin:** shell-scripting
- **Location:** `plugins/shell-scripting/skills/shellcheck-configuration/SKILL.md`
- **Topics:**
  - ShellCheck installation
  - Configuration options
  - Rule customization
  - CI integration
  - Editor plugins

---

### bats-testing-patterns
**BATS shell testing framework**

- **Plugin:** shell-scripting
- **Location:** `plugins/shell-scripting/skills/bats-testing-patterns/SKILL.md`
- **Topics:**
  - BATS setup
  - Test writing
  - Assertions
  - Setup/teardown
  - CI integration

---

## Skills by Category Summary

| Category | Skill Count |
|----------|------------|
| Developer Essentials | 8 |
| Python Development | 5 |
| Backend Development | 5 |
| JavaScript/TypeScript | 4 |
| Kubernetes Operations | 4 |
| Cloud Infrastructure | 4 |
| CI/CD Automation | 4 |
| LLM Application Development | 4 |
| Observability & Monitoring | 4 |
| Framework Migration | 4 |
| Payment Processing | 4 |
| Blockchain & Web3 | 4 |
| Shell Scripting | 3 |
| Database Design | 1 |
| API Scaffolding | 1 |
| Machine Learning Operations | 1 |
| Security Scanning | 1 |
