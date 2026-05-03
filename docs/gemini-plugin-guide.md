# Gemini CLI Skill Discovery Guide

This guide is a quick reference for finding skills across 80 plugins using natural language triggers. In Gemini CLI, skills auto-activate when you describe your task — no slash commands needed.

For installation and setup instructions, please refer to the main [README.md](../README.md).

---

## Language Development (10 plugins)

**python-development** — Skills: async-python-patterns, python-background-jobs, python-code-style, python-design-patterns, python-error-handling, python-packaging, python-performance-optimization, python-project-structure, python-testing-patterns, python-type-safety, uv-package-manager
**Use when**: "Set up a FastAPI project with uv", "write async Python", "package my Python library"

**javascript-typescript** — Skills: javascript-testing-patterns, modern-javascript-patterns, nodejs-backend-patterns, typescript-advanced-types
**Use when**: "Create a Node.js server", "add TypeScript generics", "write Jest tests"

**systems-programming** — Skills: go-concurrency-patterns, memory-safety-patterns, rust-async-patterns
**Use when**: "Write a concurrent Go service", "implement Rust async", "avoid C++ memory bugs"

**dotnet-contribution** — Skills: dotnet-backend-patterns
**Use when**: "Build an ASP.NET Core API", "use Entity Framework with Dapper"

**shell-scripting** — Skills: bash-defensive-patterns, bats-testing-patterns, shellcheck-configuration
**Use when**: "Write a production Bash script", "test shell scripts with bats"

**jvm-languages** — **Use when**: "Build a Spring Boot app", "write Scala or Java enterprise code"

**web-scripting** — **Use when**: "Build a Rails app", "create a PHP Laravel backend"

**functional-programming** — **Use when**: "Scaffold an Elixir Phoenix app", "use OTP fault-tolerance patterns"

**julia-development** — **Use when**: "Write high-performance Julia numerical code"

**arm-cortex-microcontrollers** — **Use when**: "Write STM32 firmware", "implement nRF52 peripheral drivers"

---

## Full-Stack Development (7 plugins)

**backend-development** — Skills: api-design-principles, architecture-patterns, cqrs-implementation, event-store-design, microservices-patterns, saga-orchestration, temporal-python-testing, workflow-orchestration-patterns
**Use when**: "Design a REST API with TDD", "implement CQRS", "set up Temporal saga orchestration"

**frontend-mobile-development** — Skills: nextjs-app-router-patterns, react-native-architecture, react-state-management, tailwind-design-system
**Use when**: "Build a Next.js App Router project", "set up React Native", "create a Tailwind design system"

**ui-design** — Skills: accessibility-compliance, design-system-patterns, interaction-design, mobile-android-design, mobile-ios-design, react-native-design, responsive-design, visual-design-foundations, web-component-design
**Use when**: "Design a mobile UI for iOS", "build a design system", "make my app responsive"

**developer-essentials** — Skills: auth-implementation-patterns, code-review-excellence, debugging-strategies, e2e-testing-patterns, error-handling-patterns, git-advanced-workflows, monorepo-management, nx-workspace-patterns, sql-optimization-patterns, turborepo-caching
**Use when**: "Add JWT authentication", "set up a monorepo with Nx", "write Playwright end-to-end tests"

**api-scaffolding** — Skills: fastapi-templates
**Use when**: "Scaffold a REST or GraphQL API", "generate a FastAPI project"

**multi-platform-apps** — **Use when**: "Build an app for web, iOS, and Android simultaneously"

**api-testing-observability** — **Use when**: "Generate OpenAPI docs", "write API integration tests", "add API monitoring"

---

## Infrastructure & DevOps (5 plugins)

**cloud-infrastructure** — Skills: cost-optimization, hybrid-cloud-networking, istio-traffic-management, multi-cloud-architecture, service-mesh-observability, terraform-module-library
**Use when**: "Design AWS/Azure/GCP architecture", "write Terraform modules", "set up Istio service mesh"

**kubernetes-operations** — Skills: gitops-workflow, helm-chart-scaffolding, k8s-manifest-generator, k8s-security-policies
**Use when**: "Generate Kubernetes manifests", "set up GitOps with ArgoCD", "create a Helm chart"

**cicd-automation** — Skills: deployment-pipeline-design, github-actions-templates, gitlab-ci-patterns, secrets-management
**Use when**: "Set up a GitHub Actions pipeline", "create a GitLab CI workflow"

**deployment-strategies** — **Use when**: "Plan a blue-green or canary deployment", "automate rollback"

**deployment-validation** — **Use when**: "Run pre-deployment checks", "validate configuration before release"

---

## Security (6 plugins)

**security-scanning** — Skills: attack-tree-construction, sast-configuration, security-requirement-extraction, stride-analysis-patterns, threat-mitigation-mapping
**Use when**: "Scan code for vulnerabilities", "run STRIDE threat modeling", "find OWASP Top 10 issues"

**reverse-engineering** — Skills: anti-reversing-techniques, binary-analysis-patterns, memory-forensics, protocol-reverse-engineering
**Use when**: "Analyze a binary for CTF research", "investigate suspicious firmware", "reverse engineer a protocol"

**block-no-verify** — Skills: block-no-verify-hook
**Use when**: "Block agents from using --no-verify to bypass git hooks"

**security-compliance** — **Use when**: "Audit for SOC2/HIPAA/GDPR compliance"

**backend-api-security** — **Use when**: "Harden API auth", "add rate limiting and OAuth2"

**frontend-mobile-security** — **Use when**: "Prevent XSS and CSRF", "implement a Content Security Policy"

---

## Multi-Agent Workflows (5 plugins)

**conductor** — Skills: context-driven-development, track-management, workflow-patterns
**Use when**: "Plan and implement a feature end-to-end", "manage parallel work tracks with context"

**agent-teams** — Skills: multi-reviewer-patterns, parallel-debugging, parallel-feature-development, task-coordination-strategies, team-communication-protocols, team-composition-patterns
**Use when**: "Run parallel agents to review code from multiple angles", "coordinate agents to build a feature"

**full-stack-orchestration** — **Use when**: "Build a complete feature from backend through tests to deployment"

**agent-orchestration** — **Use when**: "Optimize how my agents coordinate", "manage long multi-agent sessions"

**tdd-workflows** — **Use when**: "Drive development with red-green-refactor TDD cycles"

---

## Testing & Quality (5 plugins)

**unit-testing** — **Use when**: "Generate pytest or Jest tests", "add edge-case coverage"

**qa-orchestra** — **Use when**: "Run a full QA cycle", "validate my app with a browser agent" *(external plugin)*

**comprehensive-review** — Skills: full-review — **Use when**: "Do a deep code review covering architecture, security, and performance"

**performance-testing-review** — **Use when**: "Review for performance bottlenecks", "assess test coverage quality"

**plugin-eval** — Skills: evaluation-methodology — **Use when**: "Score a plugin skill against the evaluation rubric"

---

## AI & ML (3 plugins)

**llm-application-dev** — Skills: embedding-strategies, hybrid-search-implementation, langchain-architecture, llm-evaluation, prompt-engineering-patterns, rag-implementation, similarity-search-patterns, vector-index-tuning
**Use when**: "Build a RAG system", "implement a LangGraph agent", "optimize prompts", "tune vector indexes"

**machine-learning-ops** — Skills: ml-pipeline-workflow — **Use when**: "Set up MLOps pipelines", "automate model training and deployment"

**context-management** — **Use when**: "Restore context from a previous session", "persist state across long workflows"

---

## Data & Databases (4 plugins)

**data-engineering** — Skills: airflow-dag-patterns, data-quality-frameworks, dbt-transformation-patterns, spark-optimization
**Use when**: "Build an Airflow ETL DAG", "transform data with dbt", "optimize a Spark job"

**database-design** — Skills: postgresql — **Use when**: "Design a PostgreSQL schema", "write complex SQL"

**data-validation-suite** — **Use when**: "Validate API data schemas", "add data quality checks to my pipeline"

**database-migrations** — **Use when**: "Automate database migrations", "migrate from MySQL to PostgreSQL"

---

## Operations, Observability & Governance (10 plugins)

**incident-response** — Skills: incident-runbook-templates, on-call-handoff-patterns, postmortem-writing
**Use when**: "Triage a production incident", "write a postmortem", "create on-call runbooks"

**observability-monitoring** — Skills: distributed-tracing, grafana-dashboards, prometheus-configuration, slo-implementation
**Use when**: "Set up Prometheus metrics", "create Grafana dashboards", "implement SLOs"

**protect-mcp** — Skills: protect-mcp-setup — **Use when**: "Enforce Cedar policies on every tool call", "create signed audit receipts"

**signed-audit-trails** — Skills: signed-audit-trails-recipe — **Use when**: "Set up Ed25519 signed audit trails for tool calls"

**review-agent-governance** — Skills: review-agent-setup — **Use when**: "Require human approval before AI posts a PR review or merges"

**error-diagnostics** — **Use when**: "Trace a production error to its root cause"

**distributed-debugging** — **Use when**: "Debug across microservices", "correlate logs across distributed services"

**error-debugging** — **Use when**: "Analyze an error trace", "diagnose a flaky test"

**application-performance** — **Use when**: "Profile my app for bottlenecks", "optimize backend response times"

**database-cloud-optimization** — **Use when**: "Optimize slow queries", "reduce cloud infrastructure costs"

---

## Documentation (4 plugins)

**documentation-generation** — Skills: architecture-decision-records, changelog-automation, openapi-spec-generation
**Use when**: "Generate an OpenAPI spec", "create a Mermaid diagram", "write an ADR", "automate changelog"

**documentation-standards** — Skills: hads — **Use when**: "Apply HADS semantic tagging to docs for AI consumption"

**code-documentation** — **Use when**: "Generate docs for this codebase", "explain what this code does"

**c4-architecture** — **Use when**: "Create C4 architecture diagrams from my codebase"

---

## Business, Marketing & Specialized (19 plugins)

**business-analytics** — Skills: data-storytelling, kpi-dashboard-design — **Use when**: "Build a KPI dashboard", "create a financial report"

**startup-business-analyst** — Skills: competitive-landscape, market-sizing-analysis, startup-financial-modeling, startup-metrics-framework, team-composition-analysis — **Use when**: "Calculate TAM/SAM/SOM", "build a fundraising model"

**hr-legal-compliance** — Skills: employment-contract-templates, gdpr-data-handling — **Use when**: "Draft an employment contract", "create GDPR documentation"

**customer-sales-automation** — **Use when**: "Automate support workflows", "manage a sales pipeline"

**seo-content-creation** — **Use when**: "Write SEO-optimized content", "create an E-E-A-T content plan"

**seo-technical-optimization** — **Use when**: "Optimize meta tags and schema markup"

**seo-analysis-monitoring** — **Use when**: "Detect keyword cannibalization", "check content freshness"

**content-marketing** — **Use when**: "Develop a content marketing strategy", "research blog topics"

**blockchain-web3** — Skills: defi-protocol-templates, nft-standards, solidity-security, web3-testing
**Use when**: "Write a Solidity smart contract", "build a DeFi protocol", "audit smart contract security"

**quantitative-trading** — Skills: backtesting-frameworks, risk-metrics-calculation — **Use when**: "Build an algorithmic trading strategy", "backtest a portfolio"

**payment-processing** — Skills: billing-automation, paypal-integration, pci-compliance, stripe-integration — **Use when**: "Integrate Stripe", "implement subscription billing", "check PCI compliance"

**game-development** — Skills: godot-gdscript-patterns, unity-ecs-patterns — **Use when**: "Write a Unity game script", "build a Godot game"

**accessibility-compliance** — Skills: screen-reader-testing, wcag-audit-patterns — **Use when**: "Audit for WCAG compliance", "test screen reader support"

**meigen-ai-design** — **Use when**: "Generate AI images with a creative workflow"

**framework-migration** — Skills: angular-migration, database-migration, dependency-upgrade, react-modernization — **Use when**: "Migrate from AngularJS to Angular", "modernize a React app", "upgrade dependencies safely"

**codebase-cleanup** — **Use when**: "Remove dead code", "reduce technical debt", "prep for a major version bump"

**dependency-management** — **Use when**: "Audit dependencies for vulnerabilities", "update packages safely"

**code-refactoring** — **Use when**: "Automate a refactoring pass", "clean up messy code"

**team-collaboration** — **Use when**: "Automate standup summaries", "manage GitHub issues", "improve team DX"

---

*80 plugins total: 79 local + 1 external (qa-orchestra via git-subdir). All skills auto-activate in Gemini CLI — describe your task naturally.*
