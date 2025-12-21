# Architecture Design Workflow

## Purpose
Create comprehensive system architecture that addresses all requirements while ensuring scalability, security, and maintainability.

## Trigger
- PRD approved
- Technical specification needed
- Major system redesign

## Agents Involved
| Agent | Role | Model |
|-------|------|-------|
| architect-review | Lead architect, pattern selection | opus |
| backend-architect | Service design, API architecture | opus |
| database-architect | Data modeling, storage design | opus |
| cloud-architect | Infrastructure design | opus |
| security-auditor | Security architecture | opus |
| observability-engineer | Monitoring design | opus |

## Workflow Steps

### Step 1: Context Analysis
**Agent:** architect-review
**Actions:**
1. Review PRD and requirements
2. Identify architectural drivers
3. Define quality attributes (scalability, reliability, etc.)
4. Map constraints and assumptions

**Output:** Architecture context document

### Step 2: High-Level Design
**Agent:** architect-review
**Actions:**
1. Select architecture pattern (microservices, monolith, etc.)
2. Define system boundaries
3. Identify major components
4. Create C4 Context diagram

**Output:** High-level architecture diagram

### Step 3: Service Design
**Agent:** backend-architect
**Actions:**
1. Define service boundaries
2. Design API contracts
3. Specify communication patterns (sync/async)
4. Create C4 Container diagram

**Output:** Service architecture document

### Step 4: Data Architecture
**Agent:** database-architect
**Actions:**
1. Design data models
2. Select storage technologies
3. Define data flow patterns
4. Plan data migration (if applicable)

**Output:** Data architecture document

### Step 5: Infrastructure Design
**Agent:** cloud-architect
**Actions:**
1. Design cloud infrastructure
2. Plan networking and security groups
3. Define scaling strategies
4. Create deployment architecture

**Output:** Infrastructure architecture document

### Step 6: Security Review
**Agent:** security-auditor
**Actions:**
1. Review all designs for security
2. Define security controls
3. Plan authentication/authorization
4. Document security architecture

**Output:** Security architecture document

### Step 7: Observability Design
**Agent:** observability-engineer
**Actions:**
1. Define logging strategy
2. Plan metrics collection
3. Design distributed tracing
4. Create alerting strategy

**Output:** Observability design document

### Step 8: Architecture Decision Records
**Agent:** architect-review
**Actions:**
1. Document key decisions
2. Record rationale
3. Note alternatives considered
4. Compile ADRs

**Output:** ADR collection

## Architecture Document Structure
```markdown
# System Architecture Document

## 1. Executive Summary
## 2. Architecture Drivers
## 3. High-Level Architecture
## 4. Component Design
## 5. Data Architecture
## 6. Infrastructure Architecture
## 7. Security Architecture
## 8. Observability Architecture
## 9. Deployment Architecture
## 10. Architecture Decision Records
## 11. Appendices
```

## Exit Criteria
- All diagrams complete (C4 levels 1-3)
- Security review passed
- Performance requirements addressed
- ADRs documented
- Stakeholder approval obtained
