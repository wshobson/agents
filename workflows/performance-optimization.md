---
model: claude-sonnet-4-5-20250929
---

Optimize application performance end-to-end using specialized performance and optimization agents:

[Extended thinking: This workflow coordinates multiple agents to identify and fix performance bottlenecks across the entire stack. From database queries to frontend rendering, each agent contributes their expertise to create a highly optimized application.]

## Phase 1: Performance Analysis

### 1. Application Profiling
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Profile application performance for: $ARGUMENTS. Identify CPU, memory, and I/O bottlenecks. Include flame graphs, memory profiles, and resource utilization metrics."
- Output: Performance profile, bottleneck analysis, optimization priorities

### 2. Database Performance Analysis
- Use Task tool with subagent_type="database-optimizer"
- Prompt: "Analyze database performance for: $ARGUMENTS. Review query execution plans, identify slow queries, check indexing, and analyze connection pooling."
- Output: Query optimization report, index recommendations, schema improvements

## Phase 2: Backend Optimization

### 3. Backend Code Optimization
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Optimize backend code for: $ARGUMENTS based on profiling results. Focus on algorithm efficiency, caching strategies, and async operations."
- Output: Optimized code, caching implementation, performance improvements

### 4. API Optimization
- Use Task tool with subagent_type="backend-architect"
- Prompt: "Optimize API design and implementation for: $ARGUMENTS. Consider pagination, response compression, field filtering, and batch operations."
- Output: Optimized API endpoints, GraphQL query optimization, response time improvements

## Phase 3: Frontend Optimization

### 5. Frontend Performance
- Use Task tool with subagent_type="frontend-developer"
- Prompt: "Optimize frontend performance for: $ARGUMENTS. Focus on bundle size, lazy loading, code splitting, and rendering performance. Implement Core Web Vitals improvements."
- Output: Optimized bundles, lazy loading implementation, performance metrics

### 6. Mobile App Optimization
- Use Task tool with subagent_type="mobile-developer"
- Prompt: "Optimize mobile app performance for: $ARGUMENTS. Focus on startup time, memory usage, battery efficiency, and offline performance."
- Output: Optimized mobile code, reduced app size, improved battery life

## Phase 4: Infrastructure Optimization

### 7. Cloud Infrastructure Optimization
- Use Task tool with subagent_type="cloud-architect"
- Prompt: "Optimize cloud infrastructure for: $ARGUMENTS. Review auto-scaling, instance types, CDN usage, and geographic distribution."
- Output: Infrastructure improvements, cost optimization, scaling strategy

### 8. Deployment Optimization
- Use Task tool with subagent_type="deployment-engineer"
- Prompt: "Optimize deployment and build processes for: $ARGUMENTS. Improve CI/CD performance, implement caching, and optimize container images."
- Output: Faster builds, optimized containers, improved deployment times

## Phase 5: Monitoring and Validation

### 9. Performance Monitoring Setup
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Set up comprehensive performance monitoring for: $ARGUMENTS. Include APM, real user monitoring, and custom performance metrics."
- Output: Monitoring dashboards, alert thresholds, SLO definitions

### 10. Performance Testing
- Use Task tool with subagent_type="test-automator"
- Prompt: "Create performance test suites for: $ARGUMENTS. Include load tests, stress tests, and performance regression tests."
- Output: Performance test suite, benchmark results, regression prevention

## Coordination Notes
- Performance metrics guide optimization priorities
- Each optimization must be validated with measurements
- Consider trade-offs between different performance aspects
- Document all optimizations and their impact

Performance optimization target: $ARGUMENTS