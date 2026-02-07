---
description: "Orchestrate end-to-end application performance optimization from profiling to monitoring"
argument-hint: "<application or service> [--focus latency|throughput|cost|balanced] [--depth quick-wins|comprehensive|enterprise]"
---

# Performance Optimization Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.performance-optimization/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.performance-optimization/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress performance optimization session:
  Target: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.performance-optimization/` directory and `state.json`:

```json
{
  "target": "$ARGUMENTS",
  "status": "in_progress",
  "focus": "balanced",
  "depth": "comprehensive",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--focus` and `--depth` flags. Use defaults if not specified.

### 3. Parse target description

Extract the target description from `$ARGUMENTS` (everything before the flags). This is referenced as `$TARGET` in prompts below.

---

## Phase 1: Performance Profiling & Baseline (Steps 1–3)

### Step 1: Comprehensive Performance Profiling

Use the Task tool to launch the performance engineer:

```
Task:
  subagent_type: "performance-engineer"
  description: "Profile application performance for $TARGET"
  prompt: |
    Profile application performance comprehensively for: $TARGET.

    Generate flame graphs for CPU usage, heap dumps for memory analysis, trace I/O operations,
    and identify hot paths. Use APM tools like DataDog or New Relic if available. Include database
    query profiling, API response times, and frontend rendering metrics. Establish performance
    baselines for all critical user journeys.

    ## Deliverables
    1. Performance profile with flame graphs and memory analysis
    2. Bottleneck identification ranked by impact
    3. Baseline metrics for critical user journeys
    4. Database query profiling results
    5. API response time measurements

    Write your complete profiling report as a single markdown document.
```

Save the agent's output to `.performance-optimization/01-profiling.md`.

Update `state.json`: set `current_step` to 2, add step 1 to `completed_steps`.

### Step 2: Observability Stack Assessment

Read `.performance-optimization/01-profiling.md` to load profiling context.

Use the Task tool:

```
Task:
  subagent_type: "observability-engineer"
  description: "Assess observability setup for $TARGET"
  prompt: |
    Assess current observability setup for: $TARGET.

    ## Performance Profile
    [Insert full contents of .performance-optimization/01-profiling.md]

    Review existing monitoring, distributed tracing with OpenTelemetry, log aggregation,
    and metrics collection. Identify gaps in visibility, missing metrics, and areas needing
    better instrumentation. Recommend APM tool integration and custom metrics for
    business-critical operations.

    ## Deliverables
    1. Current observability assessment
    2. Instrumentation gaps identified
    3. Monitoring recommendations
    4. Recommended metrics and dashboards

    Write your complete assessment as a single markdown document.
```

Save the agent's output to `.performance-optimization/02-observability.md`.

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

### Step 3: User Experience Analysis

Read `.performance-optimization/01-profiling.md`.

Use the Task tool:

```
Task:
  subagent_type: "performance-engineer"
  description: "Analyze user experience metrics for $TARGET"
  prompt: |
    Analyze user experience metrics for: $TARGET.

    ## Performance Baselines
    [Insert contents of .performance-optimization/01-profiling.md]

    Measure Core Web Vitals (LCP, FID, CLS), page load times, time to interactive,
    and perceived performance. Use Real User Monitoring (RUM) data if available.
    Identify user journeys with poor performance and their business impact.

    ## Deliverables
    1. Core Web Vitals analysis
    2. User journey performance report
    3. Business impact assessment
    4. Prioritized improvement opportunities

    Write your complete analysis as a single markdown document.
```

Save the agent's output to `.performance-optimization/03-ux-analysis.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the profiling results for review.

Display a summary from `.performance-optimization/01-profiling.md`, `.performance-optimization/02-observability.md`, and `.performance-optimization/03-ux-analysis.md` (key bottlenecks, observability gaps, UX findings) and ask:

```
Performance profiling complete. Please review:
- .performance-optimization/01-profiling.md
- .performance-optimization/02-observability.md
- .performance-optimization/03-ux-analysis.md

Key bottlenecks: [summary]
Observability gaps: [summary]
UX findings: [summary]

1. Approve — proceed to optimization
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: Database & Backend Optimization (Steps 4–6)

### Step 4: Database Performance Optimization

Read `.performance-optimization/01-profiling.md` and `.performance-optimization/03-ux-analysis.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Optimize database performance for $TARGET"
  prompt: |
    You are a database optimization expert. Optimize database performance for: $TARGET.

    ## Profiling Data
    [Insert contents of .performance-optimization/01-profiling.md]

    ## UX Analysis
    [Insert contents of .performance-optimization/03-ux-analysis.md]

    Analyze slow query logs, create missing indexes, optimize execution plans, implement
    query result caching with Redis/Memcached. Review connection pooling, prepared statements,
    and batch processing opportunities. Consider read replicas and database sharding if needed.

    ## Deliverables
    1. Optimized queries with before/after performance
    2. New indexes with justification
    3. Caching strategy recommendation
    4. Connection pool configuration
    5. Implementation plan with priority order

    Write your complete optimization plan as a single markdown document.
```

Save output to `.performance-optimization/04-database.md`.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

### Step 5: Backend Code & API Optimization

Read `.performance-optimization/01-profiling.md` and `.performance-optimization/04-database.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Optimize backend services for $TARGET"
  prompt: |
    You are a backend performance architect. Optimize backend services for: $TARGET.

    ## Profiling Data
    [Insert contents of .performance-optimization/01-profiling.md]

    ## Database Optimizations
    [Insert contents of .performance-optimization/04-database.md]

    Implement efficient algorithms, add application-level caching, optimize N+1 queries,
    use async/await patterns effectively. Implement pagination, response compression,
    GraphQL query optimization, and batch API operations. Add circuit breakers and
    bulkheads for resilience.

    ## Deliverables
    1. Optimized backend code with before/after metrics
    2. Caching implementation plan
    3. API improvements with expected impact
    4. Resilience patterns added
    5. Implementation priority order

    Write your complete optimization plan as a single markdown document.
```

Save output to `.performance-optimization/05-backend.md`.

Update `state.json`: set `current_step` to 6, add step 5 to `completed_steps`.

### Step 6: Microservices & Distributed System Optimization

Read `.performance-optimization/01-profiling.md` and `.performance-optimization/05-backend.md`.

Use the Task tool:

```
Task:
  subagent_type: "performance-engineer"
  description: "Optimize distributed system performance for $TARGET"
  prompt: |
    Optimize distributed system performance for: $TARGET.

    ## Profiling Data
    [Insert contents of .performance-optimization/01-profiling.md]

    ## Backend Optimizations
    [Insert contents of .performance-optimization/05-backend.md]

    Analyze service-to-service communication, implement service mesh optimizations,
    optimize message queue performance (Kafka/RabbitMQ), reduce network hops. Implement
    distributed caching strategies and optimize serialization/deserialization.

    ## Deliverables
    1. Service communication improvements
    2. Message queue optimization plan
    3. Distributed caching setup
    4. Network optimization recommendations
    5. Expected latency improvements

    Write your complete optimization plan as a single markdown document.
```

Save output to `.performance-optimization/06-distributed.md`.

Update `state.json`: set `current_step` to "checkpoint-2", add step 6 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of optimization plans from steps 4-6 and ask:

```
Backend optimization plans complete. Please review:
- .performance-optimization/04-database.md
- .performance-optimization/05-backend.md
- .performance-optimization/06-distributed.md

1. Approve — proceed to frontend & CDN optimization
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Frontend & CDN Optimization (Steps 7–9)

### Step 7: Frontend Bundle & Loading Optimization

Read `.performance-optimization/03-ux-analysis.md` and `.performance-optimization/05-backend.md`.

Use the Task tool:

```
Task:
  subagent_type: "frontend-developer"
  description: "Optimize frontend performance for $TARGET"
  prompt: |
    Optimize frontend performance for: $TARGET targeting Core Web Vitals improvements.

    ## UX Analysis
    [Insert contents of .performance-optimization/03-ux-analysis.md]

    ## Backend Optimizations
    [Insert contents of .performance-optimization/05-backend.md]

    Implement code splitting, tree shaking, lazy loading, and dynamic imports. Optimize bundle
    sizes with webpack/rollup analysis. Implement resource hints (prefetch, preconnect, preload).
    Optimize critical rendering path and eliminate render-blocking resources.

    ## Deliverables
    1. Bundle optimization with size reductions
    2. Lazy loading implementation plan
    3. Resource hint configuration
    4. Critical rendering path optimizations
    5. Expected Core Web Vitals improvements

    Write your complete optimization plan as a single markdown document.
```

Save output to `.performance-optimization/07-frontend.md`.

Update `state.json`: set `current_step` to 8, add step 7 to `completed_steps`.

### Step 8: CDN & Edge Optimization

Read `.performance-optimization/07-frontend.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Optimize CDN and edge performance for $TARGET"
  prompt: |
    You are a cloud infrastructure and CDN optimization expert. Optimize CDN and edge
    performance for: $TARGET.

    ## Frontend Optimizations
    [Insert contents of .performance-optimization/07-frontend.md]

    Configure CloudFlare/CloudFront for optimal caching, implement edge functions for
    dynamic content, set up image optimization with responsive images and WebP/AVIF formats.
    Configure HTTP/2 and HTTP/3, implement Brotli compression. Set up geographic
    distribution for global users.

    ## Deliverables
    1. CDN configuration recommendations
    2. Edge caching rules
    3. Image optimization strategy
    4. Compression setup
    5. Geographic distribution plan

    Write your complete optimization plan as a single markdown document.
```

Save output to `.performance-optimization/08-cdn.md`.

Update `state.json`: set `current_step` to 9, add step 8 to `completed_steps`.

### Step 9: Mobile & Progressive Web App Optimization

Read `.performance-optimization/07-frontend.md` and `.performance-optimization/08-cdn.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Optimize mobile experience for $TARGET"
  prompt: |
    You are a mobile performance optimization expert. Optimize mobile experience for: $TARGET.

    ## Frontend Optimizations
    [Insert contents of .performance-optimization/07-frontend.md]

    ## CDN Optimizations
    [Insert contents of .performance-optimization/08-cdn.md]

    Implement service workers for offline functionality, optimize for slow networks with
    adaptive loading. Reduce JavaScript execution time for mobile CPUs. Implement virtual
    scrolling for long lists. Optimize touch responsiveness and smooth animations. Consider
    React Native/Flutter specific optimizations if applicable.

    ## Deliverables
    1. Mobile-optimized code recommendations
    2. PWA implementation plan
    3. Offline functionality strategy
    4. Adaptive loading configuration
    5. Expected mobile performance improvements

    Write your complete optimization plan as a single markdown document.
```

Save output to `.performance-optimization/09-mobile.md`.

Update `state.json`: set `current_step` to "checkpoint-3", add step 9 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — User Approval Required

Display a summary of frontend/CDN/mobile optimization plans and ask:

```
Frontend optimization plans complete. Please review:
- .performance-optimization/07-frontend.md
- .performance-optimization/08-cdn.md
- .performance-optimization/09-mobile.md

1. Approve — proceed to load testing & validation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 4 until the user approves.

---

## Phase 4: Load Testing & Validation (Steps 10–11)

### Step 10: Comprehensive Load Testing

Read `.performance-optimization/01-profiling.md`.

Use the Task tool:

```
Task:
  subagent_type: "performance-engineer"
  description: "Conduct comprehensive load testing for $TARGET"
  prompt: |
    Conduct comprehensive load testing for: $TARGET using k6/Gatling/Artillery.

    ## Original Baselines
    [Insert contents of .performance-optimization/01-profiling.md]

    Design realistic load scenarios based on production traffic patterns. Test normal load,
    peak load, and stress scenarios. Include API testing, browser-based testing, and WebSocket
    testing if applicable. Measure response times, throughput, error rates, and resource
    utilization at various load levels.

    ## Deliverables
    1. Load test scripts and configurations
    2. Results at normal, peak, and stress loads
    3. Response time and throughput measurements
    4. Breaking points and scalability analysis
    5. Comparison against original baselines

    Write your complete load test report as a single markdown document.
```

Save output to `.performance-optimization/10-load-testing.md`.

Update `state.json`: set `current_step` to 11, add step 10 to `completed_steps`.

### Step 11: Performance Regression Testing

Read `.performance-optimization/10-load-testing.md` and `.performance-optimization/01-profiling.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Create performance regression tests for $TARGET"
  prompt: |
    You are a test automation expert specializing in performance testing. Create automated
    performance regression tests for: $TARGET.

    ## Load Test Results
    [Insert contents of .performance-optimization/10-load-testing.md]

    ## Original Baselines
    [Insert contents of .performance-optimization/01-profiling.md]

    Set up performance budgets for key metrics, integrate with CI/CD pipeline using GitHub
    Actions or similar. Create Lighthouse CI tests for frontend, API performance tests with
    Artillery, and database performance benchmarks. Implement automatic rollback triggers
    for performance regressions.

    ## Deliverables
    1. Performance test suite with scripts
    2. CI/CD integration configuration
    3. Performance budgets and thresholds
    4. Regression detection rules
    5. Automatic rollback triggers

    Write your complete regression testing plan as a single markdown document.
```

Save output to `.performance-optimization/11-regression-testing.md`.

Update `state.json`: set `current_step` to "checkpoint-4", add step 11 to `completed_steps`.

---

## PHASE CHECKPOINT 4 — User Approval Required

Display a summary of testing results and ask:

```
Load testing and validation complete. Please review:
- .performance-optimization/10-load-testing.md
- .performance-optimization/11-regression-testing.md

1. Approve — proceed to monitoring & continuous optimization
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 5 until the user approves.

---

## Phase 5: Monitoring & Continuous Optimization (Steps 12–13)

### Step 12: Production Monitoring Setup

Read `.performance-optimization/02-observability.md` and `.performance-optimization/10-load-testing.md`.

Use the Task tool:

```
Task:
  subagent_type: "observability-engineer"
  description: "Implement production performance monitoring for $TARGET"
  prompt: |
    Implement production performance monitoring for: $TARGET.

    ## Observability Assessment
    [Insert contents of .performance-optimization/02-observability.md]

    ## Load Test Results
    [Insert contents of .performance-optimization/10-load-testing.md]

    Set up APM with DataDog/New Relic/Dynatrace, configure distributed tracing with
    OpenTelemetry, implement custom business metrics. Create Grafana dashboards for key
    metrics, set up PagerDuty alerts for performance degradation. Define SLIs/SLOs for
    critical services with error budgets.

    ## Deliverables
    1. Monitoring dashboard configurations
    2. Alert rules and thresholds
    3. SLI/SLO definitions
    4. Runbooks for common performance issues
    5. Error budget tracking setup

    Write your complete monitoring plan as a single markdown document.
```

Save output to `.performance-optimization/12-monitoring.md`.

Update `state.json`: set `current_step` to 13, add step 12 to `completed_steps`.

### Step 13: Continuous Performance Optimization

Read all previous `.performance-optimization/*.md` files.

Use the Task tool:

```
Task:
  subagent_type: "performance-engineer"
  description: "Establish continuous optimization process for $TARGET"
  prompt: |
    Establish continuous optimization process for: $TARGET.

    ## Monitoring Setup
    [Insert contents of .performance-optimization/12-monitoring.md]

    ## All Previous Optimization Work
    [Insert summary of key findings from all previous steps]

    Create performance budget tracking, implement A/B testing for performance changes,
    set up continuous profiling in production. Document optimization opportunities backlog,
    create capacity planning models, and establish regular performance review cycles.

    ## Deliverables
    1. Performance budget tracking system
    2. Optimization backlog with priorities
    3. Capacity planning model
    4. Review cycle schedule and process
    5. A/B testing framework for performance changes

    Write your complete continuous optimization plan as a single markdown document.
```

Save output to `.performance-optimization/13-continuous.md`.

Update `state.json`: set `current_step` to "complete", add step 13 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Performance optimization complete: $TARGET

## Files Created
[List all .performance-optimization/ output files]

## Optimization Summary
- Profiling: .performance-optimization/01-profiling.md
- Observability: .performance-optimization/02-observability.md
- UX Analysis: .performance-optimization/03-ux-analysis.md
- Database: .performance-optimization/04-database.md
- Backend: .performance-optimization/05-backend.md
- Distributed: .performance-optimization/06-distributed.md
- Frontend: .performance-optimization/07-frontend.md
- CDN: .performance-optimization/08-cdn.md
- Mobile: .performance-optimization/09-mobile.md
- Load Testing: .performance-optimization/10-load-testing.md
- Regression Testing: .performance-optimization/11-regression-testing.md
- Monitoring: .performance-optimization/12-monitoring.md
- Continuous: .performance-optimization/13-continuous.md

## Success Criteria
- Response Time: P50 < 200ms, P95 < 1s, P99 < 2s for critical endpoints
- Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Throughput: Support 2x current peak load with <1% error rate
- Database Performance: Query P95 < 100ms, no queries > 1s
- Resource Utilization: CPU < 70%, Memory < 80% under normal load
- Cost Efficiency: Performance per dollar improved by minimum 30%
- Monitoring Coverage: 100% of critical paths instrumented with alerting

## Next Steps
1. Implement optimizations in priority order from each phase
2. Run regression tests after each optimization
3. Monitor production metrics against baselines
4. Review performance budgets in weekly cycles
```
