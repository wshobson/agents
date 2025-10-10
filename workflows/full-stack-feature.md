---
model: claude-sonnet-4-5-20250929
---

Implement a full-stack feature across multiple platforms with coordinated agent orchestration:

[Extended thinking: This workflow orchestrates a comprehensive feature implementation across backend, frontend, mobile, and API layers. Each agent builds upon the work of previous agents to create a cohesive multi-platform solution.]

## Phase 1: Architecture and API Design

### 1. Backend Architecture
- Use Task tool with subagent_type="backend-architect"
- Prompt: "Design backend architecture for: $ARGUMENTS. Include service boundaries, data models, and technology recommendations."
- Output: Service architecture, database schema, API structure

### 2. GraphQL API Design (if applicable)
- Use Task tool with subagent_type="graphql-architect"
- Prompt: "Design GraphQL schema and resolvers for: $ARGUMENTS. Build on the backend architecture from previous step. Include types, queries, mutations, and subscriptions."
- Output: GraphQL schema, resolver structure, federation strategy

## Phase 2: Implementation

### 3. Frontend Development
- Use Task tool with subagent_type="frontend-developer"
- Prompt: "Implement web frontend for: $ARGUMENTS. Use the API design from previous steps. Include responsive UI, state management, and API integration."
- Output: React/Vue/Angular components, state management, API client

### 4. Mobile Development
- Use Task tool with subagent_type="mobile-developer"
- Prompt: "Implement mobile app features for: $ARGUMENTS. Ensure consistency with web frontend and use the same API. Include offline support and native integrations."
- Output: React Native/Flutter implementation, offline sync, push notifications

## Phase 3: Quality Assurance

### 5. Comprehensive Testing
- Use Task tool with subagent_type="test-automator"
- Prompt: "Create test suites for: $ARGUMENTS. Cover backend APIs, frontend components, mobile app features, and integration tests across all platforms."
- Output: Unit tests, integration tests, e2e tests, test documentation

### 6. Security Review
- Use Task tool with subagent_type="security-auditor"
- Prompt: "Audit security across all implementations for: $ARGUMENTS. Check API security, frontend vulnerabilities, and mobile app security."
- Output: Security report, remediation steps

## Phase 4: Optimization and Deployment

### 7. Performance Optimization
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Optimize performance across all platforms for: $ARGUMENTS. Focus on API response times, frontend bundle size, and mobile app performance."
- Output: Performance improvements, caching strategies, optimization report

### 8. Deployment Preparation
- Use Task tool with subagent_type="deployment-engineer"
- Prompt: "Prepare deployment for all components of: $ARGUMENTS. Include CI/CD pipelines, containerization, and monitoring setup."
- Output: Deployment configurations, monitoring setup, rollout strategy

## Coordination Notes
- Each agent receives outputs from previous agents
- Maintain consistency across all platforms
- Ensure API contracts are honored by all clients
- Document integration points between components

Feature to implement: $ARGUMENTS