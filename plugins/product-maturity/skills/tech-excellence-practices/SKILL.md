---
name: tech-excellence-practices
description: World-class technical practices from AWS, Google, Amazon, Netflix, and Meta for building reliable, scalable systems. Use when implementing CI/CD, testing strategies, observability, SRE practices, or adopting FAANG-level engineering standards.
---

# Tech Excellence Practices

## When to Use This Skill

- Implementing CI/CD pipelines and deployment automation
- Establishing testing strategies and quality gates
- Setting up observability and monitoring systems
- Adopting SRE practices (SLOs, error budgets, incident management)
- Improving code quality and review processes
- Scaling infrastructure and systems
- Reducing technical debt systematically
- Learning from FAANG engineering practices

## Overview

Technical excellence practices proven at scale by the world's leading tech companies. These patterns enable teams to ship faster while maintaining reliability, scale to millions of users, and create sustainable engineering cultures.

## CI/CD Excellence

### Google's Approach

**Principles:**
- Every commit triggers automated build and test
- Trunk-based development (no long-lived branches)
- Continuous integration at massive scale (100K+ commits/day)
- Hermetic builds (reproducible, no external dependencies)

**Implementation:**
```yaml
# Google-style CI pipeline
stages:
  - build
  - test
  - integration
  - deploy

build:
  - Parallel builds with distributed caching
  - Incremental builds (only changed targets)
  - Build time < 5 minutes target

test:
  - Unit tests (< 1 second each)
  - Integration tests (< 10 seconds each)
  - Test parallelization
  - Flaky test detection and quarantine

integration:
  - Pre-submit checks mandatory
  - Post-submit continuous testing
  - Test coverage tracking
  - Static analysis gates

deploy:
  - Canary deployments (1%, 10%, 50%, 100%)
  - Automated rollback on failure
  - Blue-green deployments for zero downtime
```

**Key Practices:**
- **Pre-submit checks**: All tests pass before merge
- **Post-submit monitoring**: Continuous validation
- **Hermetic testing**: Isolated, reproducible tests
- **Test selection**: Only run affected tests
- **Build caching**: Reuse previous build artifacts

### Amazon/AWS Approach

**Principles:**
- Deploy must be safe, easy, and fast
- Pipeline code is production code (IaC)
- Automated safety checks at every stage
- Deployment independence (service owns pipeline)

**Implementation:**
```yaml
# AWS-style deployment pipeline
stages:
  - source
  - build
  - test
  - staging_deploy
  - production_deploy

staging_deploy:
  - Deploy to gamma (internal staging)
  - Automated smoke tests
  - Metrics validation (latency, errors)
  - Manual approval gate (high-risk changes)

production_deploy:
  - One-box deploy (single instance)
  - Monitor for 15 minutes
  - Regional rollout (us-east-1, eu-west-1, ...)
  - Automated rollback triggers:
    - Error rate > 0.1%
    - Latency p99 > 2x baseline
    - Customer impact detected
```

**Key Practices:**
- **Pipeline as Code**: CloudFormation/CDK for everything
- **Multi-stage validation**: Gamma → One-box → Production
- **Automated rollback**: Based on metrics, not manual
- **Regional isolation**: Blast radius containment
- **Deployment dashboard**: Real-time visibility

### Netflix Approach

**Principles:**
- Continuous deployment to production (100s of deploys/day)
- Spinnaker for multi-cloud orchestration
- Immutable infrastructure (never patch, always replace)
- Chaos engineering integrated in pipeline

**Implementation:**
```yaml
# Netflix-style continuous deployment
stages:
  - bake_ami
  - deploy_canary
  - chaos_test
  - deploy_production

bake_ami:
  - Bake immutable AMI with app + dependencies
  - Security scanning
  - Compliance checks

deploy_canary:
  - Deploy to 1% of traffic
  - A/B test against current version
  - Compare metrics (streaming quality, errors)
  - Duration: 30-60 minutes

chaos_test:
  - Inject failures (latency, errors, instance kill)
  - Validate resilience
  - Auto-rollback if degradation

deploy_production:
  - Red/black deployment (instant switch)
  - Keep old version warm for quick rollback
  - Gradual rollout across regions
```

**Key Practices:**
- **Immutable deployments**: Never modify running instances
- **Comprehensive testing**: Unit, integration, chaos
- **Fast rollback**: < 1 minute to previous version
- **Regional isolation**: Independent deployments per region
- **Automated everything**: No manual deployment steps

### Best Practices Summary

**Essential Practices (Do First):**
1. **Automated builds**: Every commit triggers build
2. **Automated tests**: Run on every change
3. **Trunk-based development**: Small, frequent merges
4. **Feature flags**: Decouple deploy from release
5. **Monitoring integration**: Deployment metrics visible

**Advanced Practices (Do Later):**
1. **Canary deployments**: Progressive rollout
2. **Automated rollback**: Based on metrics
3. **Blue-green deployments**: Zero downtime
4. **Chaos testing**: Resilience validation
5. **Multi-region**: Geographic isolation

**Metrics to Track:**
- Deployment frequency: Target multiple per day
- Lead time: Commit to production < 1 hour
- Change failure rate: < 15%
- MTTR (time to restore): < 1 hour
- Build time: < 10 minutes
- Test execution time: < 5 minutes

## Testing Excellence

### Testing Pyramid

**Google's Testing Philosophy:**
```
        /\
       /  \      E2E Tests (Manual + Automated)
      /    \     Small quantity, high value
     /------\
    /        \   Integration Tests
   /          \  Medium quantity, API/service level
  /------------\
 /              \ Unit Tests
/________________\ Large quantity, fast feedback
```

**Test Distribution:**
- **Unit tests**: 70% (fast, isolated, deterministic)
- **Integration tests**: 20% (API contracts, service interactions)
- **E2E tests**: 10% (critical user journeys)

**Google's Test Sizes:**
- **Small tests**: < 1 second, no I/O, 1 thread
- **Medium tests**: < 10 seconds, localhost only
- **Large tests**: < 300 seconds, can use network

### Meta's Testing Approach

**Principles:**
- Test at scale (100K+ tests per commit)
- Parallel execution (tests run in < 10 minutes)
- Flaky test elimination (automatic quarantine)
- Visual regression testing (screenshot diffs)

**Test Strategy:**
```javascript
// Unit tests - Fast feedback
describe('UserService', () => {
  it('creates user with valid data', () => {
    // Arrange
    const userData = { email: 'test@example.com' };

    // Act
    const user = userService.create(userData);

    // Assert
    expect(user).toBeDefined();
    expect(user.email).toBe(userData.email);
  });
});

// Integration tests - API contracts
describe('User API', () => {
  it('POST /users creates user and returns 201', async () => {
    const response = await api.post('/users', {
      email: 'test@example.com',
      name: 'Test User'
    });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
  });
});

// E2E tests - Critical user journeys
describe('User Registration Flow', () => {
  it('user can sign up and see dashboard', async () => {
    await page.goto('/signup');
    await page.fill('[name=email]', 'test@example.com');
    await page.fill('[name=password]', 'SecurePass123');
    await page.click('[type=submit]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });
});
```

### Netflix's Testing Practices

**Chaos Engineering:**
- Inject failures in production continuously
- Validate resilience, not just functionality
- Learn from real-world conditions

**Types of Chaos:**
1. **Latency injection**: Slow down dependencies
2. **Error injection**: Return errors from services
3. **Instance termination**: Kill random instances
4. **Region failure**: Simulate entire region down
5. **Resource exhaustion**: CPU/memory pressure

**Implementation:**
```yaml
# Chaos experiment definition
experiment:
  name: "User Service Resilience"
  hypothesis: "User service remains available when payment service fails"

  method:
    - target: payment-service
    - action: inject_errors
    - rate: 50%  # 50% of requests fail
    - duration: 5m

  success_criteria:
    - metric: user_service_availability
    - threshold: "> 99.9%"

    - metric: user_service_latency_p99
    - threshold: "< 500ms"

  rollback:
    - condition: availability < 99%
    - action: stop_experiment
```

### AWS Testing Standards

**Principles:**
- Test in production (with safeguards)
- Synthetic monitoring (canaries)
- Load testing at scale
- Security testing automated

**Test Types:**
1. **Unit tests**: Business logic, pure functions
2. **Contract tests**: API compatibility
3. **Load tests**: Performance at scale
4. **Canary tests**: Production smoke tests
5. **Penetration tests**: Security validation

### Testing Best Practices Summary

**Essential Practices:**
1. **High coverage**: Aim for 70%+ code coverage
2. **Fast feedback**: Tests run in < 10 minutes
3. **Reliable tests**: Eliminate flaky tests
4. **Parallel execution**: Use all cores/containers
5. **Test in CI**: Every commit tested

**Advanced Practices:**
1. **Chaos testing**: Inject failures
2. **Visual regression**: Screenshot comparison
3. **Performance testing**: Load and stress tests
4. **Security testing**: SAST, DAST, dependency scanning
5. **Production testing**: Synthetic monitoring

**Anti-Patterns to Avoid:**
- Ice cream cone (too many E2E tests)
- Slow test suites (> 30 minutes)
- Flaky tests (non-deterministic)
- No test coverage tracking
- Testing in production without safeguards

## Observability Excellence

### Google's Observability Stack

**Three Pillars:**
1. **Metrics**: Time-series data (Monarch)
2. **Logs**: Structured logging (Cloud Logging)
3. **Traces**: Distributed tracing (Cloud Trace)

**Plus:**
4. **Profiling**: CPU, memory, contention
5. **Events**: Deployments, incidents, changes

**Implementation:**
```go
// Metrics - Counter, Gauge, Histogram
deployments := counter.New("deployments_total")
deployments.Inc()

latency := histogram.New("request_latency_ms", []float64{10, 50, 100, 500, 1000})
latency.Observe(requestDuration)

// Logs - Structured with context
log.Info("user_created",
  "user_id", userID,
  "email", email,
  "source", "web_signup",
)

// Traces - Distributed tracing
ctx, span := trace.StartSpan(ctx, "createUser")
defer span.End()

span.SetAttributes(
  "user.id", userID,
  "user.email", email,
)

// Propagate context to downstream services
client.CreateUser(ctx, userData)
```

### Amazon/AWS Observability

**CloudWatch Principles:**
- Metrics for everything (system + business)
- Alarms with automatic actions
- Dashboards for operators and business
- Log insights for debugging

**Key Metrics:**
```yaml
# System metrics (AWS defaults)
- CPUUtilization
- MemoryUtilization
- NetworkIn/Out
- DiskReadOps/WriteOps

# Application metrics (custom)
- RequestCount
- ErrorCount
- Latency (p50, p99, p999)
- BusinessMetrics (orders, revenue, users)

# Alarms
HighErrorRate:
  metric: ErrorCount
  statistic: Sum
  period: 300  # 5 minutes
  threshold: 100
  action: SNS notification + Lambda auto-remediation

HighLatency:
  metric: Latency
  statistic: p99
  period: 60  # 1 minute
  threshold: 1000  # 1 second
  action: Scale out instances
```

**X-Ray Distributed Tracing:**
- Automatically instrument applications
- Visualize service map and dependencies
- Identify performance bottlenecks
- Trace errors across services

### Netflix's Observability Approach

**Tools:**
- **Atlas**: High-cardinality metrics
- **Mantis**: Real-time stream processing
- **Vizceral**: Traffic flow visualization

**Principles:**
- High-cardinality dimensions (user_id, device_type, region)
- Real-time alerting (sub-second detection)
- Self-service dashboards (teams own visibility)
- Anomaly detection (ML-powered)

**Dashboard Example:**
```yaml
# Netflix-style dashboard
title: "Streaming Service Health"

rows:
  - name: "Key Metrics"
    panels:
      - title: "Plays per Second"
        metric: plays
        dimensions: [region, device_type]

      - title: "Streaming Quality"
        metric: video_quality_score
        percentiles: [p50, p99]

      - title: "Error Rate"
        metric: errors
        threshold: 0.1%
        alert: critical

  - name: "User Experience"
    panels:
      - title: "Startup Time"
        metric: time_to_first_frame
        target: < 2s

      - title: "Rebuffer Rate"
        metric: rebuffers_per_hour
        target: < 0.5
```

### Meta's Observability Practices

**Scuba - Real-time Analytics:**
- Query billions of events in seconds
- High-cardinality dimensions
- Ad-hoc exploration and analysis

**Typical Queries:**
```sql
-- Find slow endpoints
SELECT endpoint, p99(latency)
FROM requests
WHERE timestamp > now() - 1h
GROUP BY endpoint
HAVING p99(latency) > 500
ORDER BY p99(latency) DESC

-- Analyze errors by type
SELECT error_type, count(*), exemplar(trace_id)
FROM errors
WHERE timestamp > now() - 15m
GROUP BY error_type
ORDER BY count(*) DESC
```

### Observability Best Practices

**Essential Practices:**
1. **Golden signals**: Latency, traffic, errors, saturation
2. **Structured logging**: JSON format with context
3. **Distributed tracing**: Trace IDs across services
4. **Dashboards**: Operator and business views
5. **Alerting**: Actionable alerts only

**Advanced Practices:**
1. **Continuous profiling**: Always-on performance analysis
2. **Real user monitoring**: Actual user experience
3. **Synthetic monitoring**: Proactive testing
4. **Anomaly detection**: ML-powered alerting
5. **Correlation analysis**: Relate metrics, logs, traces

**Metrics to Track:**
- Latency: p50, p95, p99, p999
- Errors: By type, endpoint, user segment
- Traffic: Requests per second, users, business metrics
- Saturation: CPU, memory, network, disk, connection pools

## SRE Practices

### Google SRE Model

**Core Principles:**
1. **SLIs** (Service Level Indicators): Metrics that matter
2. **SLOs** (Service Level Objectives): Target reliability
3. **Error budgets**: Allowable unreliability
4. **Toil reduction**: Automate repetitive work
5. **Blameless post-mortems**: Learning culture

**SLI/SLO Example:**
```yaml
service: payment-api

SLIs:
  availability:
    description: "Percentage of successful requests"
    measurement: "successful_requests / total_requests"

  latency:
    description: "99th percentile latency"
    measurement: "p99(request_duration_ms)"

  quality:
    description: "Percentage of requests without errors"
    measurement: "(total_requests - error_requests) / total_requests"

SLOs:
  availability: 99.95%  # 21.9 minutes downtime/month
  latency: 200ms  # p99
  quality: 99.9%  # 0.1% error rate

error_budget:
  monthly_downtime: 21.9 minutes
  current_burn_rate: 0.5x  # Using half of budget

  policy:
    - if budget > 0: ship new features
    - if budget <= 0: focus on reliability
    - if burn_rate > 2x: page on-call
```

**Toil Categories:**
- Manual (requires human)
- Repetitive (same task repeatedly)
- Automatable (can be automated)
- Reactive (interrupt-driven)
- No enduring value (doesn't improve service)

**Toil Reduction:**
```yaml
toil_inventory:
  - task: "Restart service when memory leak occurs"
    frequency: "5x per week"
    time_per_occurrence: "15 minutes"
    total_monthly: "5 hours"
    automation_plan: "Fix memory leak + auto-restart"

  - task: "Manually scale during traffic spikes"
    frequency: "3x per week"
    time_per_occurrence: "30 minutes"
    total_monthly: "6 hours"
    automation_plan: "Auto-scaling based on metrics"

target: < 50% of SRE time on toil
current: 65%
actions:
  - Prioritize automation backlog
  - Hire additional SRE
  - Reduce feature velocity temporarily
```

### AWS Operational Excellence

**Well-Architected Pillars:**
1. Operational excellence
2. Security
3. Reliability
4. Performance efficiency
5. Cost optimization
6. Sustainability

**Operations Practices:**
- **Runbooks**: Documented procedures for common tasks
- **Playbooks**: Response plans for incidents
- **Game days**: Simulated incident drills
- **Chaos engineering**: Proactive resilience testing
- **COE (Correction of Error)**: Root cause analysis

**COE Template:**
```markdown
# Correction of Error: API Outage 2025-01-15

## Impact
- Duration: 45 minutes
- Affected users: 5,000 (2% of total)
- Revenue impact: $12,000 estimated
- Customer complaints: 127

## Timeline
- 14:00 UTC: Deploy v2.3.5 to production
- 14:05 UTC: Error rate spike detected (0.1% → 15%)
- 14:07 UTC: Incident declared, page sent
- 14:10 UTC: Investigation started
- 14:25 UTC: Root cause identified (database connection pool exhausted)
- 14:30 UTC: Rollback initiated
- 14:45 UTC: Service restored

## Root Cause
Database connection pool size insufficient for new query pattern introduced in v2.3.5. Load testing did not include this scenario.

## Action Items
1. [P0] Increase connection pool size (Owner: @db-team, Due: 2025-01-16)
2. [P0] Add load test for this query pattern (Owner: @qa-team, Due: 2025-01-20)
3. [P1] Implement connection pool monitoring (Owner: @sre-team, Due: 2025-01-25)
4. [P1] Review all query patterns in upcoming releases (Owner: @backend-team, Due: 2025-02-01)
5. [P2] Improve rollback automation (Owner: @devops-team, Due: 2025-02-15)

## Lessons Learned
- Load testing scenarios incomplete
- Connection pool monitoring missing
- Rollback took 15 minutes (too slow)

## What Went Well
- Fast detection (2 minutes)
- Clear incident response
- Good communication
```

### Netflix's Resilience Engineering

**Principles:**
- Assume failures will happen
- Build resilience into architecture
- Test resilience continuously
- Learn from every failure

**Resilience Patterns:**
1. **Circuit breaker**: Stop calling failing service
2. **Timeout**: Don't wait forever
3. **Retry with backoff**: Try again intelligently
4. **Fallback**: Degrade gracefully
5. **Bulkhead**: Isolate resources

**Implementation:**
```javascript
// Circuit breaker pattern
const circuitBreaker = new CircuitBreaker(paymentService.charge, {
  timeout: 3000,  // 3 seconds
  errorThreshold: 50,  // Open after 50% errors
  resetTimeout: 30000,  // Try again after 30 seconds
});

try {
  const result = await circuitBreaker.fire(paymentData);
  return result;
} catch (error) {
  if (error.message === 'Circuit breaker is open') {
    // Fallback: Queue for later processing
    await queuePayment(paymentData);
    return { status: 'queued' };
  }
  throw error;
}

// Bulkhead pattern (isolate thread pools)
const userServicePool = new ThreadPool({ size: 10 });
const paymentServicePool = new ThreadPool({ size: 20 });

// Payment service issues won't exhaust user service capacity
```

### SRE Best Practices Summary

**Essential Practices:**
1. **Define SLOs**: Start with availability and latency
2. **Track error budgets**: Use as decision framework
3. **On-call rotation**: Sustainable, compensated
4. **Incident response**: Clear procedures, runbooks
5. **Post-mortems**: Blameless, actionable

**Advanced Practices:**
1. **Chaos engineering**: Continuous resilience testing
2. **Capacity planning**: Predict and prevent issues
3. **Load shedding**: Graceful degradation under load
4. **Multi-region**: Geographic redundancy
5. **Cost optimization**: Efficient resource usage

## Code Quality Practices

### Google's Code Review Standards

**Mandatory Requirements:**
- All changes reviewed by at least one other engineer
- Reviewer must understand the change completely
- Author must address all comments before merge
- Automated checks must pass (tests, linting, security)

**Review Checklist:**
```markdown
- [ ] Design: Is this the right approach?
- [ ] Functionality: Does it do what it's supposed to?
- [ ] Complexity: Is it as simple as possible?
- [ ] Tests: Appropriate tests included?
- [ ] Naming: Clear, consistent names?
- [ ] Comments: Necessary and helpful?
- [ ] Documentation: Public APIs documented?
- [ ] Style: Follows style guide?
- [ ] Performance: No obvious performance issues?
- [ ] Security: No vulnerabilities introduced?
```

**Review Response Time:**
- **Same day**: For small changes (< 100 lines)
- **Next day**: For medium changes (100-500 lines)
- **2-3 days**: For large changes (> 500 lines, but these should be rare)

### Meta's Code Quality

**Static Analysis:**
- Infer (Facebook's static analyzer)
- Finds null pointer dereferences, resource leaks, concurrency issues
- Runs on every diff, blocks submission on new issues

**Code Style:**
- Automated formatters (Prettier for JS, Black for Python)
- No style debates in reviews
- Pre-commit hooks enforce formatting

**Technical Debt:**
- Regular "tech debt sprints"
- 20% of capacity allocated
- Tracked as backlog items with priority

### Best Practices Summary

**Essential Practices:**
1. **Code reviews**: Mandatory for all changes
2. **Automated testing**: Run on every commit
3. **Static analysis**: Catch bugs before runtime
4. **Linting**: Enforce style automatically
5. **Documentation**: Public APIs and complex logic

**Advanced Practices:**
1. **Continuous refactoring**: Improve as you go
2. **Tech debt tracking**: Measure and manage
3. **Pair programming**: For complex problems
4. **Architecture reviews**: For significant changes
5. **Security reviews**: For sensitive code

## Reference Materials

See `references/` directory for:
- Detailed implementation guides
- Tool comparisons and recommendations
- Migration playbooks (e.g., Jenkins → GitHub Actions)
- Troubleshooting guides
- Case studies

See `assets/` directory for:
- Architecture diagrams
- Pipeline configurations
- Dashboard screenshots
- Metrics examples

## Success Indicators

This skill is being applied effectively when:
- Deployment frequency increasing
- Lead time decreasing
- Change failure rate decreasing
- MTTR decreasing
- Test coverage increasing
- Incident frequency decreasing
- Team confidence improving
