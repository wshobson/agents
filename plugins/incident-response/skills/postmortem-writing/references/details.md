# postmortem-writing — templates and worked examples

## Templates

### Template 1: Standard Postmortem

```markdown
# Postmortem: [Incident Title]

**Date**: 2024-01-15
**Authors**: @alice, @bob
**Status**: Draft | In Review | Final
**Incident Severity**: SEV2
**Incident Duration**: 47 minutes

## Executive Summary

On January 15, 2024, the payment processing service experienced a 47-minute outage affecting approximately 12,000 customers. The root cause was a database connection pool exhaustion triggered by a configuration change in deployment v2.3.4. The incident was resolved by rolling back to v2.3.3 and increasing connection pool limits.

**Impact**:

- 12,000 customers unable to complete purchases
- Estimated revenue loss: $45,000
- 847 support tickets created
- No data loss or security implications

## Timeline (All times UTC)

| Time  | Event                                           |
| ----- | ----------------------------------------------- |
| 14:23 | Deployment v2.3.4 completed to production       |
| 14:31 | First alert: `payment_error_rate > 5%`          |
| 14:33 | On-call engineer @alice acknowledges alert      |
| 14:35 | Initial investigation begins, error rate at 23% |
| 14:41 | Incident declared SEV2, @bob joins              |
| 14:45 | Database connection exhaustion identified       |
| 14:52 | Decision to rollback deployment                 |
| 14:58 | Rollback to v2.3.3 initiated                    |
| 15:10 | Rollback complete, error rate dropping          |
| 15:18 | Service fully recovered, incident resolved      |

## Root Cause Analysis

### What Happened

The v2.3.4 deployment included a change to the database query pattern that inadvertently removed connection pooling for a frequently-called endpoint. Each request opened a new database connection instead of reusing pooled connections.

### Why It Happened

1. **Proximate Cause**: Code change in `PaymentRepository.java` replaced pooled `DataSource` with direct `DriverManager.getConnection()` calls.

2. **Contributing Factors**:
   - Code review did not catch the connection handling change
   - No integration tests specifically for connection pool behavior
   - Staging environment has lower traffic, masking the issue
   - Database connection metrics alert threshold was too high (90%)

3. **5 Whys Analysis**:
   - Why did the service fail? → Database connections exhausted
   - Why were connections exhausted? → Each request opened new connection
   - Why did each request open new connection? → Code bypassed connection pool
   - Why did code bypass connection pool? → Developer unfamiliar with codebase patterns
   - Why was developer unfamiliar? → No documentation on connection management patterns

### System Diagram
```

[Client] → [Load Balancer] → [Payment Service] → [Database]
↓
Connection Pool (broken)
↓
Direct connections (cause)

```

## Detection

### What Worked
- Error rate alert fired within 8 minutes of deployment
- Grafana dashboard clearly showed connection spike
- On-call response was swift (2 minute acknowledgment)

### What Didn't Work
- Database connection metric alert threshold too high
- No deployment-correlated alerting
- Canary deployment would have caught this earlier

### Detection Gap
The deployment completed at 14:23, but the first alert didn't fire until 14:31 (8 minutes). A deployment-aware alert could have detected the issue faster.

## Response

### What Worked
- On-call engineer quickly identified database as the issue
- Rollback decision was made decisively
- Clear communication in incident channel

### What Could Be Improved
- Took 10 minutes to correlate issue with recent deployment
- Had to manually check deployment history
- Rollback took 12 minutes (could be faster)

## Impact

### Customer Impact
- 12,000 unique customers affected
- Average impact duration: 35 minutes
- 847 support tickets (23% of affected users)
- Customer satisfaction score dropped 12 points

### Business Impact
- Estimated revenue loss: $45,000
- Support cost: ~$2,500 (agent time)
- Engineering time: ~8 person-hours

### Technical Impact
- Database primary experienced elevated load
- Some replica lag during incident
- No permanent damage to systems

## Lessons Learned

### What Went Well
1. Alerting detected the issue before customer reports
2. Team collaborated effectively under pressure
3. Rollback procedure worked smoothly
4. Communication was clear and timely

### What Went Wrong
1. Code review missed critical change
2. Test coverage gap for connection pooling
3. Staging environment doesn't reflect production traffic
4. Alert thresholds were not tuned properly

### Where We Got Lucky
1. Incident occurred during business hours with full team available
2. Database handled the load without failing completely
3. No other incidents occurred simultaneously

## Action Items

| Priority | Action | Owner | Due Date | Ticket |
|----------|--------|-------|----------|--------|
| P0 | Add integration test for connection pool behavior | @alice | 2024-01-22 | ENG-1234 |
| P0 | Lower database connection alert threshold to 70% | @bob | 2024-01-17 | OPS-567 |
| P1 | Document connection management patterns | @alice | 2024-01-29 | DOC-89 |
| P1 | Implement deployment-correlated alerting | @bob | 2024-02-05 | OPS-568 |
| P2 | Evaluate canary deployment strategy | @charlie | 2024-02-15 | ENG-1235 |
| P2 | Load test staging with production-like traffic | @dave | 2024-02-28 | QA-123 |

## Appendix

### Supporting Data

#### Error Rate Graph
[Link to Grafana dashboard snapshot]

#### Database Connection Graph
[Link to metrics]

### Related Incidents
- 2023-11-02: Similar connection issue in User Service (POSTMORTEM-42)

#
