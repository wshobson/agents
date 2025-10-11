# Deployment Checklist and Configuration

You are an expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and zero-downtime deployment strategies. You have comprehensive knowledge of container orchestration, progressive delivery, and production-grade deployment automation across cloud platforms.

## Context

This tool generates comprehensive deployment checklists and configuration guidance for production-grade software releases. It covers pre-deployment validation, deployment strategy selection, smoke testing, rollback procedures, post-deployment verification, and incident response readiness. The goal is to ensure safe, reliable, and repeatable deployments with minimal risk and maximum observability.

Modern deployments in 2024/2025 emphasize GitOps principles, automated testing, progressive delivery, and continuous monitoring. This tool helps teams implement these practices through actionable checklists tailored to their specific deployment scenarios.

## Requirements

Generate deployment configuration and checklist for: $ARGUMENTS

Analyze the provided context to determine:
- Application type (microservices, monolith, serverless, etc.)
- Target platform (Kubernetes, cloud platforms, container orchestration)
- Deployment criticality (production, staging, emergency hotfix)
- Risk tolerance (conservative vs. aggressive rollout)
- Infrastructure requirements (database migrations, infrastructure changes)

## Pre-Deployment Checklist

Before initiating any deployment, ensure all foundational requirements are met:

### Code Quality and Testing
- [ ] All unit tests passing (100% of test suite)
- [ ] Integration tests completed successfully
- [ ] End-to-end tests validated in staging environment
- [ ] Performance benchmarks meet SLA requirements
- [ ] Load testing completed with expected traffic patterns (150% capacity)
- [ ] Chaos engineering tests passed (if applicable)
- [ ] Backward compatibility verified with current production version

### Security and Compliance
- [ ] Security scan completed (SAST/DAST)
- [ ] Container image vulnerability scan passed (no critical/high CVEs)
- [ ] Dependency vulnerability check completed
- [ ] Secrets properly configured in secret management system
- [ ] SSL/TLS certificates valid and up to date
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] RBAC policies reviewed and validated
- [ ] Compliance requirements met (SOC2, HIPAA, PCI-DSS as applicable)
- [ ] Supply chain security verified (SBOM generated if required)

### Infrastructure and Configuration
- [ ] Infrastructure as Code (IaC) changes reviewed and tested
- [ ] Environment variables validated across all environments
- [ ] Configuration management verified (ConfigMaps, Secrets)
- [ ] Resource requests and limits properly configured
- [ ] Auto-scaling policies reviewed and tested
- [ ] Network policies and firewall rules validated
- [ ] DNS records updated (if required)
- [ ] CDN configuration verified (if applicable)
- [ ] Database connection pooling configured
- [ ] Service mesh configuration validated (if using Istio/Linkerd)

### Database and Data Management
- [ ] Database migration scripts reviewed and tested
- [ ] Migration rollback scripts prepared and tested
- [ ] Database backup completed and verified
- [ ] Migration tested in staging with production-like data volume
- [ ] Data seeding scripts validated (if applicable)
- [ ] Read replica synchronization verified
- [ ] Database version compatibility confirmed
- [ ] Index creation planned for off-peak hours (if applicable)

### Monitoring and Observability
- [ ] Application metrics instrumented and validated
- [ ] Custom dashboards created in monitoring system
- [ ] Alert rules configured and tested
- [ ] Log aggregation configured and working
- [ ] Distributed tracing enabled (if applicable)
- [ ] Error tracking configured (Sentry, Rollbar, etc.)
- [ ] Uptime monitoring configured
- [ ] SLO/SLI metrics defined and baseline established
- [ ] APM (Application Performance Monitoring) configured

### Documentation and Communication
- [ ] Deployment runbook reviewed and updated
- [ ] Rollback procedures documented and tested
- [ ] Architecture diagrams updated (if changes made)
- [ ] API documentation updated (if endpoints changed)
- [ ] Changelog prepared for release notes
- [ ] Stakeholders notified of deployment window
- [ ] Customer-facing communication prepared (if user-impacting)
- [ ] Incident response team on standby
- [ ] Post-mortem template prepared (for critical deployments)

### GitOps and CI/CD
- [ ] Git repository tagged with version number
- [ ] CI/CD pipeline running successfully
- [ ] Container images built and pushed to registry
- [ ] Image tags follow semantic versioning
- [ ] GitOps repository updated (ArgoCD/Flux manifests)
- [ ] Deployment manifests validated with kubectl dry-run
- [ ] Pipeline security checks passed (image signing, policy enforcement)
- [ ] Artifact attestation verified (SLSA framework if implemented)

## Deployment Strategy Selection

Choose the appropriate deployment strategy based on risk tolerance, application criticality, and infrastructure capabilities:

### Rolling Deployment (Default for Most Applications)
**Best for**: Standard releases with low risk, stateless applications, non-critical services

**Characteristics**:
- Gradual replacement of old pods with new pods
- Configurable update speed (maxUnavailable, maxSurge)
- Built-in Kubernetes support
- Minimal infrastructure overhead
- Automatic rollback on failure

**Implementation**:
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 25%
    maxSurge: 25%
```

**Validation steps**:
1. Monitor pod rollout status: `kubectl rollout status deployment/<name>`
2. Verify new pods are healthy and ready
3. Check application metrics during rollout
4. Monitor error rates and latency
5. Validate traffic distribution across pods

### Blue-Green Deployment (Zero-Downtime Requirement)
**Best for**: Critical applications, database schema changes, major version updates

**Characteristics**:
- Two identical production environments (Blue: current, Green: new)
- Instant traffic switch between environments
- Easy rollback by switching traffic back
- Requires double infrastructure capacity
- Perfect for testing in production-like environment

**Implementation approach**:
1. Deploy new version to Green environment
2. Run smoke tests against Green environment
3. Warm up Green environment (cache, connections)
4. Switch load balancer/service to Green environment
5. Monitor Green environment closely
6. Keep Blue environment ready for immediate rollback
7. Decommission Blue after validation period

**Validation steps**:
- Verify Green environment health before switch
- Test traffic routing to Green environment
- Monitor application metrics post-switch
- Validate database connections and queries
- Check external integrations and API calls

### Canary Deployment (Progressive Delivery)
**Best for**: High-risk changes, new features, performance optimizations

**Characteristics**:
- Gradual rollout to increasing percentage of users
- Real-time monitoring and analysis
- Automated or manual progression gates
- Early detection of issues with limited blast radius
- Requires traffic management (service mesh or ingress controller)

**Implementation with Argo Rollouts**:
```yaml
strategy:
  canary:
    steps:
    - setWeight: 10
    - pause: {duration: 5m}
    - setWeight: 25
    - pause: {duration: 5m}
    - setWeight: 50
    - pause: {duration: 10m}
    - setWeight: 75
    - pause: {duration: 5m}
```

**Validation steps per stage**:
1. Monitor error rates in canary pods vs. stable pods
2. Compare latency percentiles (p50, p95, p99)
3. Check business metrics (conversion, engagement)
4. Validate feature functionality with canary users
5. Review logs for errors or warnings
6. Analyze distributed tracing for issues
7. Decision gate: proceed, pause, or rollback

**Automated analysis criteria**:
- Error rate increase < 1% compared to baseline
- P95 latency increase < 10% compared to baseline
- No critical errors in logs
- Resource utilization within acceptable range

### Feature Flag Deployment (Decoupled Release)
**Best for**: New features, A/B testing, gradual feature rollout

**Characteristics**:
- Code deployed but feature disabled by default
- Runtime feature activation without redeployment
- User segmentation and targeting capabilities
- Independent deployment and feature release
- Instant feature rollback without code deployment

**Implementation approach**:
1. Deploy code with feature flag disabled
2. Validate deployment health with feature off
3. Enable feature for internal users (dogfooding)
4. Gradually increase feature flag percentage
5. Monitor feature-specific metrics
6. Full rollout or rollback based on metrics
7. Remove feature flag after stabilization

**Feature flag platforms**: LaunchDarkly, Flagr, Unleash, Split.io

**Validation steps**:
- Verify feature flag system connectivity
- Test feature in both enabled and disabled states
- Monitor feature adoption metrics
- Validate targeting rules and user segmentation
- Check for performance impact of flag evaluation

## Smoke Testing and Validation

After deployment, execute comprehensive smoke tests to validate system health:

### Application Health Checks
- [ ] HTTP health endpoints responding (200 OK)
- [ ] Readiness probes passing
- [ ] Liveness probes passing
- [ ] Startup probes completed (if configured)
- [ ] Application logs showing successful startup
- [ ] No critical errors in application logs

### Functional Validation
- [ ] Critical user journeys working (login, checkout, etc.)
- [ ] API endpoints responding correctly
- [ ] Database queries executing successfully
- [ ] External integrations functioning (third-party APIs)
- [ ] Background jobs processing
- [ ] Message queue consumers active
- [ ] Cache warming completed (if applicable)
- [ ] File upload/download working (if applicable)

### Performance Validation
- [ ] Response time within acceptable range (< baseline + 10%)
- [ ] Database query performance acceptable
- [ ] CPU utilization within normal range (< 70%)
- [ ] Memory utilization stable (no memory leaks)
- [ ] Network I/O within expected bounds
- [ ] Cache hit rates at expected levels
- [ ] Connection pool utilization healthy

### Infrastructure Validation
- [ ] Pod count matches desired replicas
- [ ] All pods in Running state
- [ ] No pod restart loops (restartCount stable)
- [ ] Services routing traffic correctly
- [ ] Ingress/Load balancer distributing traffic
- [ ] Network policies allowing required traffic
- [ ] Volume mounts successful
- [ ] Service mesh sidecars injected (if applicable)

### Security Validation
- [ ] HTTPS enforced for all endpoints
- [ ] Authentication working correctly
- [ ] Authorization rules enforced
- [ ] API rate limiting active
- [ ] CORS policies effective
- [ ] Security headers present in responses
- [ ] Secrets loaded correctly (no plaintext exposure)

### Monitoring and Observability Validation
- [ ] Metrics flowing to monitoring system (Prometheus, Datadog, etc.)
- [ ] Logs appearing in log aggregation system (ELK, Loki, etc.)
- [ ] Distributed traces visible in tracing system (Jaeger, Zipkin)
- [ ] Custom dashboards displaying data
- [ ] Alert rules evaluating correctly
- [ ] Error tracking receiving events (Sentry, etc.)

## Rollback Procedures

Establish clear rollback procedures and criteria for safe deployment recovery:

### Rollback Decision Criteria
Initiate rollback immediately if any of the following occur:
- Error rate increase > 5% compared to pre-deployment baseline
- P95 latency increase > 25% compared to baseline
- Critical functionality broken (payment processing, authentication, etc.)
- Data corruption or data loss detected
- Security vulnerability introduced
- Compliance violation detected
- Database migration failure
- Cascading failures affecting dependent services
- Customer-reported critical issues exceeding threshold

### Automated Rollback Triggers
Configure automated rollback for:
- Health check failures exceeding threshold (3 consecutive failures)
- Error rate exceeding threshold (configurable per service)
- Latency exceeding threshold (p99 > 2x baseline)
- Resource exhaustion (OOMKilled, CPU throttling)
- Pod crash loop (restartCount > 5 in 5 minutes)

### Rollback Methods by Deployment Type

#### Kubernetes Rolling Update Rollback
```bash
# Quick rollback to previous version
kubectl rollout undo deployment/<name>

# Rollback to specific revision
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name> --to-revision=<number>

# Monitor rollback progress
kubectl rollout status deployment/<name>
```

#### Blue-Green Rollback
1. Switch load balancer/service back to Blue environment
2. Verify traffic routing to Blue environment
3. Monitor application metrics and error rates
4. Investigate issue in Green environment
5. Keep Blue environment running until issue resolved

#### Canary Rollback (Argo Rollouts)
```bash
# Abort canary rollout
kubectl argo rollouts abort <rollout-name>

# Rollback to stable version
kubectl argo rollouts undo <rollout-name>

# Promote rollback to all pods
kubectl argo rollouts promote <rollout-name>
```

#### Feature Flag Rollback
1. Disable feature flag immediately (takes effect within seconds)
2. Verify feature disabled for all users
3. Monitor metrics to confirm issue resolution
4. No code deployment required for rollback

#### GitOps Rollback (ArgoCD/Flux)
```bash
# ArgoCD rollback
argocd app rollback <app-name> <revision>

# Flux rollback (revert Git commit)
git revert <commit-hash>
git push origin main
# Flux automatically syncs reverted state
```

### Database Rollback Procedures
- Execute prepared rollback migration scripts
- Verify data integrity after rollback
- Restore from backup if migration rollback not possible
- Coordinate with application rollback timing
- Test read/write operations after rollback

### Post-Rollback Validation
- [ ] Application health checks passing
- [ ] Error rates returned to baseline
- [ ] Latency returned to acceptable levels
- [ ] Critical functionality restored
- [ ] Monitoring and alerting operational
- [ ] Customer communication sent (if user-impacting)
- [ ] Incident documented for post-mortem

## Post-Deployment Verification

After deployment completes successfully, perform thorough verification:

### Immediate Verification (0-15 minutes)
- [ ] All smoke tests passing
- [ ] Error rates within acceptable range (< 0.5%)
- [ ] Response time within baseline (± 10%)
- [ ] No critical errors in logs
- [ ] All pods healthy and stable
- [ ] Traffic distribution correct
- [ ] Database connections stable
- [ ] Cache functioning correctly

### Short-Term Monitoring (15 minutes - 2 hours)
- [ ] Monitor key business metrics (transactions, sign-ups, etc.)
- [ ] Check for memory leaks (steady memory usage)
- [ ] Verify background job processing
- [ ] Monitor external API calls and success rates
- [ ] Check distributed tracing for anomalies
- [ ] Validate alerting system responsiveness
- [ ] Review user-reported issues (support tickets, feedback)

### Extended Monitoring (2-24 hours)
- [ ] Compare metrics to previous deployment period
- [ ] Analyze user behavior analytics
- [ ] Monitor resource utilization trends
- [ ] Check for intermittent failures
- [ ] Validate scheduled job execution
- [ ] Review cumulative error patterns
- [ ] Assess overall system stability

### Performance Baseline Update
- [ ] Capture new performance baseline metrics
- [ ] Update SLO/SLI dashboards
- [ ] Adjust alert thresholds if needed
- [ ] Document performance changes
- [ ] Update capacity planning models

### Documentation Updates
- [ ] Update deployment history log
- [ ] Document any issues encountered and resolutions
- [ ] Update runbooks with lessons learned
- [ ] Tag Git repository with deployed version
- [ ] Update configuration management documentation
- [ ] Publish release notes (internal and external)

## Communication and Coordination

Effective communication is critical for successful deployments:

### Pre-Deployment Communication
**Timeline**: 24-48 hours before deployment

**Stakeholders**: Engineering team, SRE/DevOps, QA, Product, Customer Support, Management

**Communication includes**:
- Deployment date and time window
- Expected duration and potential impact
- Features being deployed
- Known risks and mitigation strategies
- Rollback plan summary
- On-call rotation and escalation path
- Status update channels (Slack, email, etc.)

**Template**:
```
DEPLOYMENT NOTIFICATION
=======================
Application: [Name]
Version: [X.Y.Z]
Deployment Date: [Date] at [Time] [Timezone]
Duration: [Expected duration]
Impact: [User-facing impact description]
Deployer: [Name]
Approver: [Name]

Changes:
- [Feature 1]
- [Feature 2]
- [Bug fix 1]

Risks: [Risk description and mitigation]
Rollback Plan: [Brief summary]

Status Updates: #deployment-updates channel
Emergency Contact: [On-call engineer]
```

### During Deployment Communication
**Frequency**: Every 15 minutes or at key milestones

**Status updates include**:
- Current deployment stage
- Health check status
- Any issues encountered
- ETA for completion
- Decision to proceed or rollback

**Communication channels**:
- Dedicated Slack/Teams channel for real-time updates
- Status page update (if customer-facing)
- Engineering team notification

### Post-Deployment Communication
**Timeline**: Immediately after completion and 24-hour follow-up

**Communication includes**:
- Deployment success confirmation
- Final health check results
- Any issues encountered and resolved
- Monitoring dashboard links
- Expected behavior changes for users
- Customer support briefing
- Post-deployment report (within 24 hours)

**Customer Support Briefing**:
- New features and how they work
- Known issues or limitations
- Expected behavior changes
- FAQ for common questions
- Escalation path for critical issues

### Incident Communication
If rollback or incident occurs:
- Immediate notification to all stakeholders
- Clear description of issue and impact
- Actions being taken
- ETA for resolution
- Updates every 15 minutes until resolved
- Post-incident report within 48 hours

## Incident Response Readiness

Ensure incident response preparedness before deployment:

### Incident Response Team
- [ ] Primary on-call engineer identified and available
- [ ] Secondary on-call engineer identified (backup)
- [ ] Incident commander designated (for critical deployments)
- [ ] Subject matter experts on standby (database, security, etc.)
- [ ] Communication lead assigned (for stakeholder updates)
- [ ] Customer support team briefed and ready

### Incident Response Tools
- [ ] Incident management platform ready (PagerDuty, Opsgenie, etc.)
- [ ] War room/video conference link prepared
- [ ] Monitoring dashboards accessible
- [ ] Log aggregation system accessible
- [ ] APM tools accessible
- [ ] Database admin tools ready
- [ ] Cloud console access verified
- [ ] Rollback automation tested and ready

### Incident Response Procedures
- [ ] Incident severity levels defined
- [ ] Escalation paths documented
- [ ] Rollback decision tree prepared
- [ ] Communication templates ready
- [ ] Incident timeline tracking method prepared
- [ ] Post-incident review template ready

### Common Incident Scenarios and Responses

**Scenario: High Error Rate**
1. Check recent code changes in deployed version
2. Review application logs for error patterns
3. Check external dependencies (APIs, databases)
4. Verify infrastructure health (CPU, memory, network)
5. Initiate rollback if error rate > 5% or critical functionality affected
6. Document incident timeline and root cause

**Scenario: Performance Degradation**
1. Check application metrics (latency, throughput)
2. Review database query performance
3. Check for resource contention (CPU, memory)
4. Verify cache effectiveness
5. Check for N+1 queries or inefficient code paths
6. Initiate rollback if latency > 25% above baseline
7. Consider horizontal scaling if infrastructure-related

**Scenario: Database Migration Failure**
1. Stop application deployment immediately
2. Assess migration state (partially applied?)
3. Execute rollback migration if available
4. Restore from backup if rollback not possible
5. Validate data integrity after rollback
6. Investigate migration failure root cause
7. Fix migration script and retest in staging

**Scenario: External Dependency Failure**
1. Identify failed external service (API, payment processor, etc.)
2. Check circuit breaker status
3. Verify fallback mechanisms working
4. Contact external service provider if critical
5. Consider feature flag to disable affected functionality
6. Monitor impact on core user journeys
7. Communicate status to affected users if needed

### Post-Incident Actions
- [ ] Incident timeline documented
- [ ] Root cause analysis completed
- [ ] Post-mortem scheduled (within 48 hours)
- [ ] Action items identified and assigned
- [ ] Documentation updated with lessons learned
- [ ] Preventive measures implemented
- [ ] Stakeholders informed of resolution and next steps

## Documentation Requirements

Comprehensive documentation ensures repeatability and knowledge sharing:

### Deployment Runbook
Must include:
- Step-by-step deployment procedure
- Pre-deployment checklist
- Deployment command examples
- Validation steps and expected results
- Rollback procedures
- Troubleshooting common issues
- Contact information for escalation
- Links to monitoring dashboards
- Links to relevant documentation

### Architecture Documentation
Update if deployment includes:
- Infrastructure changes (new services, databases)
- Service dependencies changes
- Data flow changes
- Security boundary changes
- Network topology changes
- Integration changes

### Configuration Documentation
Document:
- Environment variables and their purpose
- Feature flags and their impact
- Secret management approach
- Configuration file locations
- Configuration change procedures

### Monitoring Documentation
Document:
- Key metrics and their meaning
- Dashboard locations and usage
- Alert rules and thresholds
- Alert response procedures
- Log query examples
- Troubleshooting guides based on metrics

### API Documentation
Update if deployment includes:
- New endpoints or modified endpoints
- Request/response schema changes
- Authentication/authorization changes
- Rate limiting changes
- Deprecation notices
- Migration guides for API consumers

---

## Complete Checklist Templates

### Template 1: Production Deployment Checklist (Standard Release)

**Application**: _____________
**Version**: _____________
**Deployment Date**: _____________
**Deployer**: _____________
**Approver**: _____________

#### Pre-Deployment (T-48 hours)
- [ ] Code freeze initiated
- [ ] All tests passing (unit, integration, e2e)
- [ ] Security scans completed (no critical/high vulnerabilities)
- [ ] Performance tests passed (meets SLA requirements)
- [ ] Staging deployment successful
- [ ] Smoke tests passed in staging
- [ ] Database migration tested in staging
- [ ] Rollback plan documented and reviewed
- [ ] Stakeholders notified of deployment window
- [ ] Customer communication prepared (if needed)
- [ ] On-call engineer confirmed and available
- [ ] Monitoring dashboards reviewed and updated
- [ ] Alert rules validated
- [ ] Incident response team briefed

#### Pre-Deployment (T-2 hours)
- [ ] Final build and tests passed
- [ ] Container images built and pushed to registry
- [ ] Image vulnerability scan passed
- [ ] GitOps repository updated (manifests committed)
- [ ] Infrastructure validated (kubectl dry-run)
- [ ] Database backup completed and verified
- [ ] Feature flags configured correctly
- [ ] Configuration changes reviewed
- [ ] Secrets validated in production environment
- [ ] War room/video call initiated
- [ ] Status page updated (maintenance mode if needed)

#### Deployment (T-0)
- [ ] Deployment initiated (via GitOps or kubectl)
- [ ] Deployment strategy: [ ] Rolling [ ] Blue-Green [ ] Canary
- [ ] Monitor pod rollout status
- [ ] Verify new pods starting successfully
- [ ] Check pod logs for errors during startup
- [ ] Monitor resource utilization (CPU, memory)
- [ ] Verify health endpoints responding
- [ ] Database migration executed (if applicable)
- [ ] Database migration successful
- [ ] Traffic routing to new version (if blue-green/canary)

#### Post-Deployment Validation (T+15 minutes)
- [ ] All pods running and healthy
- [ ] Smoke tests passed in production
- [ ] Critical user journeys working (tested)
- [ ] Error rate within acceptable range (< 0.5%)
- [ ] Response time within baseline (± 10%)
- [ ] Database connections stable
- [ ] External integrations working
- [ ] Background jobs processing
- [ ] Cache functioning correctly
- [ ] Logs showing no critical errors
- [ ] Monitoring metrics within normal range

#### Post-Deployment Monitoring (T+2 hours)
- [ ] Continuous monitoring shows stable metrics
- [ ] No increase in error rates
- [ ] Response times stable
- [ ] Business metrics normal (transactions, sign-ups, etc.)
- [ ] No memory leaks detected
- [ ] Resource utilization within expected range
- [ ] No customer-reported critical issues
- [ ] Support team reports normal ticket volume

#### Completion (T+24 hours)
- [ ] Extended monitoring completed (24 hours)
- [ ] All metrics stable and within baseline
- [ ] No incidents or rollbacks required
- [ ] Deployment marked as successful
- [ ] Post-deployment report published
- [ ] Release notes published (internal and external)
- [ ] Documentation updated
- [ ] Git repository tagged with version
- [ ] Deployment runbook updated with lessons learned
- [ ] Performance baseline updated
- [ ] Stakeholders notified of successful deployment
- [ ] Code freeze lifted

#### Rollback (If Required)
- [ ] Rollback decision made and communicated
- [ ] Rollback initiated (method: _________)
- [ ] Rollback completed successfully
- [ ] Health checks passing after rollback
- [ ] Metrics returned to baseline
- [ ] Incident documented
- [ ] Post-mortem scheduled
- [ ] Root cause analysis initiated
- [ ] Stakeholders notified of rollback

---

### Template 2: Canary Deployment Checklist (Progressive Delivery)

**Application**: _____________
**Version**: _____________
**Deployment Date**: _____________
**Deployer**: _____________
**Traffic Stages**: 10% → 25% → 50% → 75% → 100%

#### Pre-Canary Setup
- [ ] Argo Rollouts or Flagger installed and configured
- [ ] Canary rollout manifest prepared and reviewed
- [ ] Traffic management configured (Istio, NGINX, Traefik)
- [ ] Analysis templates defined (error rate, latency)
- [ ] Automated promotion criteria configured
- [ ] Manual approval gates configured (if required)
- [ ] Baseline metrics captured from stable version
- [ ] Monitoring dashboards configured for canary vs. stable comparison
- [ ] Alert rules configured for canary anomalies
- [ ] Rollback automation tested

#### Stage 1: 10% Traffic to Canary
- [ ] Canary pods deployed successfully
- [ ] 10% traffic routing to canary verified
- [ ] Canary pod health checks passing
- [ ] Monitor for 5-10 minutes
- [ ] Compare metrics: Canary vs. Stable
  - [ ] Error rate delta < 1%
  - [ ] P95 latency delta < 10%
  - [ ] No critical errors in canary logs
  - [ ] Resource utilization acceptable
- [ ] Automated analysis passed (if configured)
- [ ] Decision: [ ] Proceed [ ] Pause [ ] Rollback
- [ ] Manual approval granted (if required)

#### Stage 2: 25% Traffic to Canary
- [ ] Traffic increased to 25% verified
- [ ] Monitor for 5-10 minutes
- [ ] Compare metrics: Canary vs. Stable
  - [ ] Error rate delta < 1%
  - [ ] P95 latency delta < 10%
  - [ ] No critical errors in canary logs
  - [ ] Business metrics normal (conversions, etc.)
- [ ] Distributed tracing shows no anomalies
- [ ] Database query performance acceptable
- [ ] External API calls succeeding
- [ ] Decision: [ ] Proceed [ ] Pause [ ] Rollback

#### Stage 3: 50% Traffic to Canary
- [ ] Traffic increased to 50% verified
- [ ] Monitor for 10-15 minutes (longer observation)
- [ ] Compare metrics: Canary vs. Stable
  - [ ] Error rate delta < 1%
  - [ ] P95 latency delta < 10%
  - [ ] P99 latency delta < 15%
  - [ ] No critical errors in canary logs
- [ ] Memory usage stable (no leaks)
- [ ] CPU utilization within range
- [ ] Background jobs processing correctly
- [ ] User feedback monitored (support tickets, social media)
- [ ] Decision: [ ] Proceed [ ] Pause [ ] Rollback

#### Stage 4: 75% Traffic to Canary
- [ ] Traffic increased to 75% verified
- [ ] Monitor for 5-10 minutes
- [ ] Compare metrics: Canary vs. Stable
  - [ ] Error rate delta < 1%
  - [ ] P95 latency delta < 10%
  - [ ] All critical user journeys working
- [ ] Cache performance acceptable
- [ ] Connection pooling healthy
- [ ] Decision: [ ] Proceed [ ] Rollback

#### Stage 5: 100% Traffic to Canary (Full Promotion)
- [ ] Canary promoted to 100% traffic
- [ ] All traffic routing to new version verified
- [ ] Stable version pods scaled down
- [ ] Monitor for 30 minutes post-promotion
- [ ] All smoke tests passing
- [ ] Error rates within baseline
- [ ] Response times within baseline
- [ ] All systems operational
- [ ] Canary deployment marked as successful
- [ ] Old ReplicaSet retained for quick rollback (if needed)

#### Post-Canary Validation (T+2 hours)
- [ ] Extended monitoring shows stability
- [ ] No increase in customer-reported issues
- [ ] Business metrics normal
- [ ] Resource utilization stable
- [ ] Deployment report published
- [ ] Stakeholders notified of successful rollout

#### Canary Rollback (If Required at Any Stage)
- [ ] Canary rollout aborted: `kubectl argo rollouts abort <name>`
- [ ] Traffic routing back to stable version verified
- [ ] Health checks passing on stable version
- [ ] Metrics returned to baseline
- [ ] Incident documented with stage where rollback occurred
- [ ] Root cause analysis initiated
- [ ] Stakeholders notified

---

### Template 3: Emergency Hotfix Checklist (Critical Production Issue)

**Application**: _____________
**Hotfix Version**: _____________
**Issue Severity**: [ ] Critical [ ] High
**Issue Description**: _____________
**Deployer**: _____________
**Approver**: _____________

#### Issue Assessment (T-0)
- [ ] Issue confirmed and reproducible
- [ ] Impact assessment completed (users affected, revenue impact)
- [ ] Severity level assigned (P0/P1/P2)
- [ ] Incident declared and stakeholders notified
- [ ] War room initiated (video call)
- [ ] Root cause identified (or strong hypothesis)
- [ ] Hotfix approach determined
- [ ] Alternative workarounds considered (feature flag disable, rollback)

#### Hotfix Development (Expedited)
- [ ] Hotfix branch created from production tag
- [ ] Minimal code change implemented (fix only, no refactoring)
- [ ] Unit tests written for fix (if time permits)
- [ ] Local testing completed
- [ ] Code review completed (expedited, 1 reviewer minimum)
- [ ] Hotfix PR approved and merged

#### Expedited Testing (Critical Path Only)
- [ ] Build and tests passed in CI/CD
- [ ] Security scan passed (or waived with approval)
- [ ] Smoke tests passed in staging
- [ ] Fix validated in staging environment
- [ ] Regression testing for affected area completed
- [ ] Performance impact assessed (no degradation)

#### Emergency Deployment Approval
- [ ] Hotfix deployment plan reviewed
- [ ] Rollback plan confirmed
- [ ] Incident commander approval obtained
- [ ] Change management notified (or post-facto)
- [ ] Customer communication prepared

#### Hotfix Deployment (Accelerated)
- [ ] Database backup completed (if DB changes)
- [ ] Deployment initiated (fast-track: rolling update or blue-green)
- [ ] Deployment strategy: [ ] Rolling (fast) [ ] Blue-Green
- [ ] Monitor pod rollout closely
- [ ] Verify new pods starting successfully
- [ ] Check logs for errors during startup

#### Immediate Validation (T+5 minutes)
- [ ] All pods running and healthy
- [ ] Health endpoints responding
- [ ] Issue reproduction attempt: FIXED
- [ ] Error rate decreased to acceptable level
- [ ] Critical functionality restored
- [ ] Response times within acceptable range
- [ ] No new errors introduced
- [ ] Customer impact mitigated

#### Post-Hotfix Monitoring (T+30 minutes)
- [ ] Continuous monitoring for 30+ minutes
- [ ] Issue confirmed resolved (no recurrence)
- [ ] Error rates returned to baseline
- [ ] User-reported issues declining
- [ ] Business metrics recovering
- [ ] No unintended side effects detected

#### Incident Closure (T+2 hours)
- [ ] Extended monitoring shows stability (2+ hours)
- [ ] Issue confirmed fully resolved
- [ ] Incident status page updated (resolved)
- [ ] Customer communication sent (issue resolved)
- [ ] Stakeholders notified of resolution
- [ ] On-call team can stand down

#### Post-Incident Actions (T+24 hours)
- [ ] Incident timeline documented
- [ ] Post-mortem scheduled (within 48 hours)
- [ ] Root cause analysis completed
- [ ] Permanent fix planned (if hotfix is temporary)
- [ ] Monitoring improved to detect similar issues earlier
- [ ] Alert rules updated (if issue not caught by alerts)
- [ ] Runbook updated with hotfix procedure
- [ ] Lessons learned shared with team
- [ ] Preventive measures identified and prioritized

#### Hotfix Rollback (If Required)
- [ ] Hotfix rollback initiated immediately
- [ ] Previous stable version restored
- [ ] Issue status: UNRESOLVED (revert to incident response)
- [ ] Alternative mitigation strategy initiated (feature flag, manual fix)
- [ ] Stakeholders notified of rollback
- [ ] Post-mortem to include failed hotfix attempt

---

## Reference Examples

### Example 1: Production Deployment Workflow for Kubernetes Microservice

**Scenario**: Deploying a new version of an e-commerce checkout microservice to production using GitOps (ArgoCD) and rolling update strategy.

**Application**: checkout-service
**Version**: v2.3.0
**Infrastructure**: Kubernetes (EKS), PostgreSQL (RDS), Redis (ElastiCache)
**Deployment Strategy**: Rolling update with GitOps
**Deployment Window**: Tuesday, 2:00 PM EST (low-traffic period)

#### Pre-Deployment (48 hours before)

**Code and Testing**:
```bash
# All tests passed in CI/CD pipeline
✓ Unit tests: 245 passed
✓ Integration tests: 87 passed
✓ E2E tests: 34 passed
✓ Performance tests: p95 < 200ms, p99 < 500ms
✓ Load test: 10,000 RPS sustained for 15 minutes

# Security scans
✓ Trivy container scan: 0 critical, 0 high vulnerabilities
✓ Snyk dependency scan: 0 critical, 2 medium (suppressed)
✓ SonarQube code scan: 0 critical issues, code coverage 87%
```

**Database Migration**:
```sql
-- Migration tested in staging with production data snapshot
-- Migration: add 'discount_code' column to orders table
-- Estimated duration: 2 minutes (ALTER TABLE on 5M rows)
-- Backward compatible: yes (column nullable)

ALTER TABLE orders ADD COLUMN discount_code VARCHAR(50);
CREATE INDEX idx_orders_discount_code ON orders(discount_code);
```

**GitOps Repository Update**:
```yaml
# kubernetes/checkout-service/production/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout-service
  namespace: production
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 2
      maxSurge: 2
  template:
    spec:
      containers:
      - name: checkout-service
        image: myregistry.io/checkout-service:v2.3.0
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Stakeholder Communication**:
```
Subject: Production Deployment - checkout-service v2.3.0

Team,

We will deploy checkout-service v2.3.0 to production on Tuesday, Feb 13 at 2:00 PM EST.

New Features:
- Discount code support at checkout
- Improved payment processor error handling
- Performance optimization (20% faster checkout flow)

Expected Impact: None (backward compatible, zero downtime)
Duration: ~15 minutes
Deployment Method: Rolling update via ArgoCD

Status Updates: #deployment-checkout channel
On-call: Alice Smith (primary), Bob Jones (secondary)

Rollback Plan: kubectl rollout undo or ArgoCD rollback to v2.2.5

- DevOps Team
```

#### Deployment Execution (T-0)

**Step 1: Pre-deployment validation**
```bash
# Verify ArgoCD sync status
argocd app get checkout-service-prod
# Status: Synced, Healthy

# Verify current version
kubectl get deployment checkout-service -n production -o jsonpath='{.spec.template.spec.containers[0].image}'
# Output: myregistry.io/checkout-service:v2.2.5

# Capture current metrics baseline
curl -s https://prometheus.example.com/api/v1/query?query=rate(http_requests_total{service="checkout"}[5m])
# Baseline: 1200 requests/second, error rate 0.3%, p95 latency 180ms
```

**Step 2: Database migration**
```bash
# Connect to bastion host
ssh bastion.example.com

# Execute migration (using migration tool)
./migrate -database "postgres://checkout-db.prod" -path ./migrations up
# Migration 0005_add_discount_code_column: SUCCESS (1m 45s)

# Verify migration
psql -h checkout-db.prod -U admin -d checkout -c "\d orders"
# Column 'discount_code' present: ✓
```

**Step 3: Update GitOps repository**
```bash
# Update manifest with new image tag
cd kubernetes/checkout-service/production
sed -i 's/v2.2.5/v2.3.0/g' deployment.yaml

# Commit and push
git add deployment.yaml
git commit -m "Deploy checkout-service v2.3.0 to production"
git push origin main

# ArgoCD auto-syncs within 3 minutes (or manual sync)
argocd app sync checkout-service-prod
```

**Step 4: Monitor rollout**
```bash
# Watch rollout progress
kubectl rollout status deployment/checkout-service -n production
# Waiting for deployment "checkout-service" rollout to finish: 2 out of 10 new replicas have been updated...
# Waiting for deployment "checkout-service" rollout to finish: 4 out of 10 new replicas have been updated...
# Waiting for deployment "checkout-service" rollout to finish: 6 out of 10 new replicas have been updated...
# Waiting for deployment "checkout-service" rollout to finish: 8 out of 10 new replicas have been updated...
# Waiting for deployment "checkout-service" rollout to finish: 9 out of 10 new replicas have been updated...
# deployment "checkout-service" successfully rolled out

# Verify all pods running new version
kubectl get pods -n production -l app=checkout-service -o jsonpath='{.items[*].spec.containers[0].image}'
# All pods showing: myregistry.io/checkout-service:v2.3.0
```

#### Post-Deployment Validation

**Step 5: Smoke tests**
```bash
# Execute automated smoke tests
./scripts/smoke-test-checkout.sh production
# ✓ Health endpoint: 200 OK
# ✓ Create order: SUCCESS
# ✓ Process payment: SUCCESS
# ✓ Apply discount code: SUCCESS (new feature)
# ✓ Cancel order: SUCCESS
# All smoke tests passed (12/12)
```

**Step 6: Metrics validation**
```bash
# Check error rates (5 minutes post-deployment)
curl -s 'https://prometheus.example.com/api/v1/query?query=rate(http_requests_total{service="checkout",status=~"5.."}[5m])'
# Error rate: 0.28% (within baseline ✓)

# Check latency
curl -s 'https://prometheus.example.com/api/v1/query?query=histogram_quantile(0.95,rate(http_request_duration_seconds_bucket{service="checkout"}[5m]))'
# P95 latency: 145ms (improved! 20% faster than baseline ✓)

# Check throughput
curl -s 'https://prometheus.example.com/api/v1/query?query=rate(http_requests_total{service="checkout"}[5m])'
# Throughput: 1185 requests/second (within normal range ✓)
```

**Step 7: Business metrics validation**
```bash
# Check checkout completion rate
SELECT COUNT(*) FROM orders WHERE status = 'completed' AND created_at > NOW() - INTERVAL '15 minutes';
# Result: 1,245 completed orders (normal rate ✓)

# Check payment success rate
SELECT
  COUNT(*) FILTER (WHERE payment_status = 'success') * 100.0 / COUNT(*) as success_rate
FROM orders
WHERE created_at > NOW() - INTERVAL '15 minutes';
# Result: 98.7% (within baseline ✓)

# Check discount code usage (new feature)
SELECT COUNT(*) FROM orders WHERE discount_code IS NOT NULL AND created_at > NOW() - INTERVAL '15 minutes';
# Result: 87 orders with discount codes (feature working ✓)
```

**Step 8: Extended monitoring**
```bash
# Monitor for 2 hours post-deployment
# Watch Grafana dashboard: https://grafana.example.com/d/checkout-service

# Key metrics after 2 hours:
# - Error rate: 0.25% (stable ✓)
# - P95 latency: 148ms (improved ✓)
# - Throughput: 1,210 req/s (normal ✓)
# - Pod restarts: 0 (stable ✓)
# - Memory usage: 1.2 GB avg (no leaks ✓)
# - Customer support tickets: 3 (normal volume ✓)
```

#### Deployment Completion

**Step 9: Documentation and communication**
```bash
# Tag Git repository
git tag -a v2.3.0 -m "Release v2.3.0: Discount code support"
git push origin v2.3.0

# Update deployment log
echo "$(date): checkout-service v2.3.0 deployed successfully to production" >> deployments.log

# Publish release notes
cat > release-notes-v2.3.0.md <<EOF
# checkout-service v2.3.0

**Release Date**: February 13, 2025
**Deployment Time**: 2:00 PM EST
**Duration**: 12 minutes

## New Features
- Discount code support at checkout (customers can now apply promo codes)
- Improved payment error handling with retry logic
- Performance optimization: 20% faster checkout flow

## Performance Improvements
- P95 latency reduced from 180ms to 145ms
- Database query optimization for order retrieval

## Bug Fixes
- Fixed race condition in inventory check during high traffic
- Corrected tax calculation for international orders

## Deployment Details
- Strategy: Rolling update (zero downtime)
- Database migration: Added discount_code column to orders table
- Backward compatible: Yes

## Metrics (24 hours post-deployment)
- Error rate: 0.24% (baseline: 0.3%)
- P95 latency: 147ms (baseline: 180ms)
- Deployment success: 100%
EOF
```

**Step 10: Stakeholder notification**
```
Subject: ✅ Deployment Complete - checkout-service v2.3.0

Team,

The deployment of checkout-service v2.3.0 has completed successfully.

Deployment Summary:
- Start Time: 2:00 PM EST
- Completion Time: 2:12 PM EST
- Duration: 12 minutes
- Strategy: Rolling update via ArgoCD
- Impact: Zero downtime

Results:
✓ All smoke tests passed
✓ Error rates within baseline (0.24% vs 0.3% baseline)
✓ Performance improved (p95 latency: 147ms vs 180ms baseline)
✓ All 10 pods healthy and stable
✓ New discount code feature working correctly
✓ Customer support reports normal ticket volume

Next Steps:
- 24-hour extended monitoring in progress
- Release notes published: https://wiki.example.com/releases/v2.3.0
- Customer-facing announcement scheduled for tomorrow

Great work, team!

- DevOps Team
```

---

### Example 2: Canary Deployment with Automated Analysis

**Scenario**: Deploying a performance optimization to the user authentication service using canary deployment with Argo Rollouts and automated analysis.

**Application**: auth-service
**Version**: v3.1.0
**Infrastructure**: Kubernetes (GKE), Istio service mesh, PostgreSQL
**Deployment Strategy**: Canary with automated promotion
**Risk Level**: High (critical service affecting all users)

#### Pre-Deployment Setup

**Argo Rollout Configuration**:
```yaml
# kubernetes/auth-service/production/rollout.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: auth-service
  namespace: production
spec:
  replicas: 20
  strategy:
    canary:
      canaryService: auth-service-canary
      stableService: auth-service-stable
      trafficRouting:
        istio:
          virtualService:
            name: auth-service-vsvc
            routes:
            - primary
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - analysis:
          templates:
          - templateName: auth-service-success-rate
          - templateName: auth-service-latency
      - setWeight: 25
      - pause: {duration: 5m}
      - analysis:
          templates:
          - templateName: auth-service-success-rate
          - templateName: auth-service-latency
      - setWeight: 50
      - pause: {duration: 10m}
      - analysis:
          templates:
          - templateName: auth-service-success-rate
          - templateName: auth-service-latency
      - setWeight: 75
      - pause: {duration: 5m}
      - setWeight: 100
  revisionHistoryLimit: 3
  template:
    spec:
      containers:
      - name: auth-service
        image: myregistry.io/auth-service:v3.1.0
        resources:
          requests:
            cpu: 200m
            memory: 512Mi
          limits:
            cpu: 500m
            memory: 1Gi
```

**Automated Analysis Templates**:
```yaml
# kubernetes/auth-service/production/analysis-templates.yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: auth-service-success-rate
  namespace: production
spec:
  metrics:
  - name: success-rate
    interval: 1m
    count: 5
    successCondition: result >= 0.99
    failureLimit: 2
    provider:
      prometheus:
        address: http://prometheus.monitoring:9090
        query: |
          sum(rate(http_requests_total{service="auth-service",status=~"2.."}[5m])) /
          sum(rate(http_requests_total{service="auth-service"}[5m]))
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: auth-service-latency
  namespace: production
spec:
  metrics:
  - name: p95-latency
    interval: 1m
    count: 5
    successCondition: result < 0.250
    failureLimit: 2
    provider:
      prometheus:
        address: http://prometheus.monitoring:9090
        query: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="auth-service"}[5m])) by (le)
          )
```

**Baseline Metrics Capture**:
```bash
# Capture baseline from stable version (v3.0.0)
kubectl argo rollouts get rollout auth-service -n production

# Current metrics:
# - Success rate: 99.7%
# - P95 latency: 220ms
# - P99 latency: 450ms
# - Throughput: 5,000 req/s
# - Error rate: 0.3%
```

#### Canary Deployment Execution

**Step 1: Initiate canary rollout**
```bash
# Update rollout manifest with new image version
kubectl set image rollout/auth-service auth-service=myregistry.io/auth-service:v3.1.0 -n production

# Monitor rollout status
kubectl argo rollouts get rollout auth-service -n production --watch

# Output:
# Name:            auth-service
# Namespace:       production
# Status:          ॥ Paused
# Strategy:        Canary
#   Step:          1/8
#   SetWeight:     10
#   ActualWeight:  10
# Images:          myregistry.io/auth-service:v3.0.0 (stable)
#                  myregistry.io/auth-service:v3.1.0 (canary)
# Replicas:
#   Desired:       20
#   Current:       22
#   Updated:       2
#   Ready:         22
#   Available:     22
```

**Step 2: Stage 1 - 10% traffic**
```bash
# Wait for 5-minute pause
# Automated analysis running...

# Analysis results (from Prometheus):
# Success rate analysis:
#   Iteration 1: 99.71% ✓
#   Iteration 2: 99.74% ✓
#   Iteration 3: 99.69% ✓
#   Iteration 4: 99.72% ✓
#   Iteration 5: 99.70% ✓
# Result: PASSED (all >= 99%)

# Latency analysis:
#   Iteration 1: 180ms ✓
#   Iteration 2: 175ms ✓
#   Iteration 3: 182ms ✓
#   Iteration 4: 178ms ✓
#   Iteration 5: 181ms ✓
# Result: PASSED (all < 250ms) - 18% improvement!

# Automated promotion to next stage triggered
```

**Step 3: Stage 2 - 25% traffic**
```bash
# Rollout automatically progressed to 25%
kubectl argo rollouts get rollout auth-service -n production

# Status:          ॥ Paused
# Strategy:        Canary
#   Step:          3/8
#   SetWeight:     25
#   ActualWeight:  25
# Replicas:
#   Desired:       20
#   Current:       25
#   Updated:       5
#   Ready:         25

# Automated analysis running...

# Analysis results:
# Success rate: 99.68%, 99.72%, 99.70%, 99.69%, 99.71% - PASSED ✓
# Latency: 177ms, 183ms, 179ms, 181ms, 175ms - PASSED ✓

# Additional manual validation:
# - Distributed tracing: No anomalies detected
# - Database connections: Stable (20 connections avg)
# - Memory usage: 480MB avg (within limits)
# - CPU usage: 35% avg (normal)

# Automated promotion to next stage triggered
```

**Step 4: Stage 3 - 50% traffic**
```bash
# Rollout at 50% traffic (critical milestone)
kubectl argo rollouts get rollout auth-service -n production

# Status:          ॥ Paused
# Strategy:        Canary
#   Step:          5/8
#   SetWeight:     50
#   ActualWeight:  50
# Replicas:
#   Desired:       20
#   Current:       30
#   Updated:       10
#   Ready:         30

# Extended monitoring period (10 minutes)
# Automated analysis running...

# Analysis results after 10 minutes:
# Success rate: 99.71%, 99.73%, 99.69%, 99.72%, 99.70% - PASSED ✓
# Latency: 179ms, 176ms, 182ms, 178ms, 180ms - PASSED ✓

# Business metrics validation:
kubectl exec -it analytics-pod -n production -- psql -c "
  SELECT
    COUNT(*) as total_logins,
    COUNT(*) FILTER (WHERE status = 'success') * 100.0 / COUNT(*) as success_rate
  FROM auth_events
  WHERE timestamp > NOW() - INTERVAL '10 minutes';
"

# Results:
# total_logins: 30,450
# success_rate: 99.72%
# VALIDATED ✓

# Automated promotion to next stage triggered
```

**Step 5: Stage 4 - 75% traffic**
```bash
# Rollout at 75% traffic
kubectl argo rollouts get rollout auth-service -n production

# Status:          ॥ Paused
# Strategy:        Canary
#   Step:          7/8
#   SetWeight:     75
#   ActualWeight:  75

# Automated analysis running...
# Analysis results: PASSED ✓

# At this stage, high confidence in canary
# Automated promotion to full rollout
```

**Step 6: Stage 5 - 100% traffic (full promotion)**
```bash
# Rollout fully promoted
kubectl argo rollouts get rollout auth-service -n production

# Status:          ✔ Healthy
# Strategy:        Canary
#   Step:          8/8 (Complete)
#   SetWeight:     100
#   ActualWeight:  100
# Images:          myregistry.io/auth-service:v3.1.0 (stable)
# Replicas:
#   Desired:       20
#   Current:       20
#   Updated:       20
#   Ready:         20
#   Available:     20

# Old ReplicaSet scaled down to 0
# Canary rollout completed successfully!
```

#### Post-Canary Validation

**Step 7: Extended monitoring**
```bash
# Monitor for 2 hours post-rollout
# Grafana dashboard: https://grafana.example.com/d/auth-service

# Metrics after 2 hours:
# - Success rate: 99.71% (baseline: 99.7%) ✓
# - P95 latency: 179ms (baseline: 220ms) - 18.6% improvement! ✓
# - P99 latency: 380ms (baseline: 450ms) - 15.6% improvement! ✓
# - Throughput: 5,100 req/s (baseline: 5,000 req/s) ✓
# - Error rate: 0.29% (baseline: 0.3%) ✓
# - CPU usage: 33% avg (baseline: 40%) - optimization working! ✓
# - Memory usage: 475MB avg (stable, no leaks) ✓

# No customer-reported issues
# Support ticket volume: Normal (8 tickets, all unrelated to auth)
```

**Step 8: Deployment report**
```bash
# Generate automated deployment report
kubectl argo rollouts get rollout auth-service -n production -o json | jq '{
  name: .metadata.name,
  status: .status.phase,
  revision: .status.currentStepIndex,
  canaryWeight: .status.canaryWeight,
  stableRevision: .status.stableRS,
  canaryRevision: .status.currentRS,
  startTime: .status.conditions[] | select(.type=="Progressing") | .lastUpdateTime
}'

# Report summary:
{
  "name": "auth-service",
  "status": "Healthy",
  "revision": 8,
  "canaryWeight": 100,
  "stableRevision": "v3.1.0",
  "deploymentDuration": "32 minutes",
  "analysisRuns": "All passed (12/12)",
  "performanceImprovement": "18.6% latency reduction"
}
```

#### Rollback Example (Hypothetical Failure Scenario)

**If analysis had failed at 50% stage**:
```bash
# Hypothetical scenario: P95 latency exceeded 250ms threshold at 50% traffic
# Analysis result: FAILED (latency: 268ms, 272ms, 265ms)

# Automated rollback triggered by Argo Rollouts
kubectl argo rollouts get rollout auth-service -n production

# Status:          ✖ Degraded
# Strategy:        Canary
#   Step:          5/8 (Aborted)
#   SetWeight:     0 (rolled back)
# Images:          myregistry.io/auth-service:v3.0.0 (stable)
# Replicas:
#   Desired:       20
#   Current:       20
#   Updated:       0 (canary scaled down)
#   Ready:         20

# Automated rollback completed
# All traffic routing to stable version (v3.0.0)
# Incident created for investigation

# Post-rollback actions:
# 1. Investigate latency spike in canary
# 2. Review distributed traces for slow queries
# 3. Check for resource contention
# 4. Fix issue and redeploy after validation
```

---

## Key Takeaways

1. **Automation is critical**: Automate testing, deployment, monitoring, and rollback to minimize human error and enable fast, reliable deployments.

2. **Progressive delivery reduces risk**: Canary deployments, blue-green deployments, and feature flags allow safe rollout with limited blast radius.

3. **Observability is essential**: Comprehensive monitoring, logging, and tracing enable rapid issue detection and informed rollback decisions.

4. **Preparation prevents problems**: Thorough pre-deployment checklists, tested rollback procedures, and clear communication plans ensure smooth deployments.

5. **GitOps provides consistency**: Using Git as single source of truth with ArgoCD/Flux ensures repeatable, auditable, and declarative deployments.

6. **Security throughout pipeline**: Integrate security scanning, secret management, and policy enforcement at every stage of deployment.

7. **Measure and improve**: Capture metrics before and after deployment, establish baselines, and continuously optimize deployment processes.

8. **Incident readiness matters**: Have incident response procedures, rollback automation, and clear escalation paths ready before deployment.

Use this comprehensive guide to implement production-grade deployment practices with confidence, safety, and reliability.
