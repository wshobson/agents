---
name: presale-methodology
description: World-class pre-sale methodology combining AWS, Azure, Google Cloud, Microsoft, and SAP best practices. Use when conducting discovery, qualifying opportunities, designing solutions, or managing pre-sale cycles.
---

# VK Cloud Pre-Sale Methodology

## When to Use This Skill

- Qualifying new sales opportunities
- Conducting discovery sessions
- Designing cloud solutions
- Creating proposals and RFP responses
- Managing complex pre-sale cycles
- Training pre-sale teams

## Pre-Sale Lifecycle

### Stage 1: Qualification (MEDDIC)

**Goal**: Determine if opportunity is worth pursuing

**MEDDIC Framework** (from enterprise sales):

1. **M**etrics: What economic impact will this deliver?
   - Cost savings (TCO reduction)
   - Revenue impact (faster time-to-market)
   - Risk mitigation (compliance, sanctions)

2. **E**conomic Buyer: Who has budget authority?
   - CIO, CTO (technology decisions)
   - CFO (budget approval)
   - CEO (strategic decisions)

3. **D**ecision Criteria: What requirements must be met?
   - Technical (performance, scalability, security)
   - Business (cost, ROI, strategic fit)
   - Compliance (152-FZ, GOST, industry regulations)

4. **D**ecision Process: What is formal approval process?
   - POC → Proposal → Procurement → Legal → Approval
   - Timeline (3-6 months typical for enterprise)
   - Approval chain (CTO → CFO → CEO for large deals)

5. **I**dentify Pain: What critical problems drive urgency?
   - Current infrastructure can't scale
   - AWS sanctions risk concerns
   - High cloud costs (30-40% overpaying)
   - 152-FZ compliance requirement

6. **C**hampion: Who will sell internally on our behalf?
   - Technical champion (architect, lead developer)
   - Business champion (VP/Director who benefits)
   - Executive sponsor (C-level backer)

**Qualification Questions**:
- "What problem are you trying to solve?" (Pain)
- "What's the budget for this project?" (Metrics, Economic Buyer)
- "What does success look like?" (Metrics, Decision Criteria)
- "Who else is involved in this decision?" (Economic Buyer, Champion)
- "What's your timeline?" (Decision Process, Urgency)
- "What happens if you don't solve this?" (Identify Pain)

**Qualify or Disqualify**:
- **Qualified**: Pain identified, budget allocated, timeline clear, champion exists
- **Disqualified**: No pain, no budget, no urgency, no champion

---

### Stage 2: Discovery (Deep Dive)

**Goal**: Understand current state, requirements, and constraints in detail

**Discovery Framework** (AWS/Azure-inspired):

#### Phase 1: Business Context (30 min)

**Questions**:
1. **Strategic Goals**:
   - "Какие бизнес-цели вы хотите достичь?"
   - "Какие KPI определят успех?"
   - "Expected ROI и payback period?"

2. **Current Challenges**:
   - "Топ-3 проблемы с текущей инфраструктурой?"
   - "Что мешает вам scale или innovate?"
   - "Были ли production incidents за последние 6 месяцев?"

3. **Timeline & Budget**:
   - "Желаемый timeline миграции?"
   - "Бюджет на миграцию и cloud infrastructure?"
   - "Hard deadlines (compliance, contract expirations)?"

#### Phase 2: Technical Discovery (60-90 min)

**Infrastructure Inventory**:
- Compute: VMs, bare metal (specs, utilization)
- Storage: Block, object, file storage (capacity, IOPS)
- Databases: Relational, NoSQL, analytics (size, HA configuration)
- Network: Topology, bandwidth, VPN/connectivity
- Platform Services: Kubernetes, CI/CD, monitoring, message queues

**Architecture Review**:
- Application architecture (monolith vs. microservices)
- Data flow (ingestion, processing, storage, consumption)
- Integrations (external APIs, internal systems)
- Security & compliance (encryption, access control, regulations)

**Questions**:
- "Current infrastructure specs? (vCPU, RAM, storage)"
- "Average vs. peak utilization?"
- "SLA requirements (uptime, RTO, RPO)?"
- "Compliance requirements (152-FZ, GOST, PCI-DSS)?"
- "Integration dependencies?"

#### Phase 3: Requirements Gathering (60 min)

**Non-Functional Requirements**:
1. **Performance**:
   - Latency targets (p50, p95, p99)
   - Throughput (requests/second, transactions/second)
   - Concurrency (simultaneous users)

2. **Scalability**:
   - Growth projections (users, data, traffic)
   - Peak load vs. average load
   - Auto-scaling requirements

3. **Availability**:
   - Uptime SLA (99%, 99.9%, 99.95%)
   - RTO (Recovery Time Objective)
   - RPO (Recovery Point Objective)
   - Multi-AZ/region requirements

4. **Security**:
   - Data sovereignty (must stay in Russia?)
   - Compliance frameworks (152-FZ, GOST, PCI-DSS, HIPAA)
   - Encryption (at rest, in transit)
   - Access control (RBAC, MFA, SSO)

5. **Operational**:
   - Monitoring and alerting requirements
   - Backup frequency and retention
   - Maintenance windows
   - Support SLAs

#### Phase 4: Constraints & Dependencies (30 min)

**Constraints**:
- Budget limitations
- Timeline constraints
- Technology constraints (must use certain tools)
- Regulatory constraints (government compliance)
- Personnel constraints (limited ops team)

**Dependencies**:
- External systems (APIs, partners)
- Legacy systems (cannot be migrated)
- Data synchronization requirements
- Network connectivity (VPN, Direct Connect)

**Deliverables**:
- Discovery notes (markdown)
- Current state architecture diagram
- Requirements matrix (prioritized: Must/Should/Could)
- Gap analysis (requirements vs. VK Cloud capabilities)

---

### Stage 3: Solution Design (Design Phase)

**Goal**: Design VK Cloud architecture that meets requirements

**Design Principles**:
1. **Cloud-Native**: Kubernetes, immutable infrastructure, auto-scaling
2. **High Availability**: Multi-AZ deployment, load balancers, automated failover
3. **Security by Design**: Defense in depth, encryption, least privilege
4. **Cost-Optimized**: Right-sizing, auto-scaling, reserved instances
5. **Operational Excellence**: Monitoring, logging, automated backups
6. **No Lock-In**: Open standards (K8s, S3, PostgreSQL) for portability
7. **Data Sovereignty**: All data in Russian data centers (152-FZ)

**Design Process**:

1. **Service Mapping**:
   - Current infrastructure → VK Cloud services
   - Example: On-prem PostgreSQL → PostgreSQL DBaaS
   - Example: VMware VMs → VK Cloud VMs or Kubernetes

2. **Architecture Diagramming**:
   - Logical architecture (high-level)
   - Physical architecture (detailed resources)
   - Network topology (VPC, subnets, security groups)
   - Data flow diagram (ingestion → processing → storage → consumption)

3. **Sizing & Capacity Planning**:
   - Right-size compute instances based on utilization
   - Storage capacity with growth projections
   - Database sizing (CPU, RAM, IOPS requirements)
   - Network bandwidth requirements

4. **HA & DR Design**:
   - Multi-AZ deployment for critical components
   - Load balancers with health checks
   - Database replication and automated failover
   - Backup strategy (frequency, retention, RTO/RPO)

5. **Security Architecture**:
   - Network isolation (VPC, security groups)
   - Encryption at rest and in transit
   - IAM and access control (RBAC, MFA)
   - Compliance mapping (152-FZ, GOST)

6. **Migration Strategy**:
   - Approach: Lift-and-shift, replatform, or refactor
   - Phased migration roadmap (waves, milestones)
   - Data migration plan (tools, validation, cutover)
   - Rollback procedures

**Deliverables**:
- Architecture diagrams (multiple views)
- Technical specification document
- VK Cloud service bill of materials
- Migration plan with timeline
- Risk assessment and mitigation plan

---

### Stage 4: Business Case Development (Justify Investment)

**Goal**: Build financial justification for VK Cloud investment

**Components**:

1. **TCO Analysis** (3-year):
   - Current state costs (infrastructure, personnel, support)
   - VK Cloud costs (compute, storage, database, network, support)
   - Migration costs (one-time investment)
   - 3-year total comparison

2. **ROI Calculation**:
   - Annual savings (VK Cloud vs. current)
   - Payback period (months to break even)
   - 3-year ROI percentage

3. **Strategic Value** (beyond cost):
   - Data sovereignty (compliance, risk mitigation)
   - Agility (faster time-to-market, innovation velocity)
   - Scalability (handle growth without infrastructure bottlenecks)
   - Operational efficiency (managed services reduce ops burden)

4. **Risk Mitigation**:
   - Sanctions risk elimination (vs. AWS/Azure/GCP)
   - Disaster recovery (built-in HA, backups)
   - Vendor diversification (multi-cloud strategy)

**Deliverables**:
- TCO comparison spreadsheet (3-year)
- ROI model with assumptions
- Business case presentation (executive summary)
- Sensitivity analysis (best/worst case scenarios)

---

### Stage 5: Proposal Development (Winning the Deal)

**Goal**: Create compelling proposal that wins competitive deal

**Proposal Types**:
1. **Commercial Proposal**: Unsolicited proposal (5-15 pages)
2. **RFP Response**: Formal tender response (20-100+ pages)
3. **Technical Proposal**: Detailed design (10-30 pages)
4. **Statement of Work (SOW)**: Professional services scope (5-15 pages)

**Proposal Structure** (Commercial Proposal):

1. **Executive Summary** (1 page):
   - Problem statement
   - Proposed solution (VK Cloud architecture)
   - Business value (ROI, TCO, strategic benefits)
   - Investment summary
   - Timeline and next steps

2. **Understanding Your Business** (1-2 pages):
   - Customer's industry, challenges, goals
   - Current infrastructure and pain points
   - Why now? (compelling events, urgency)

3. **Proposed Solution** (3-5 pages):
   - Logical architecture diagram
   - VK Cloud services mapping
   - Key capabilities and features
   - Competitive differentiation (vs. AWS/Azure/Yandex)
   - Customer references and proof points

4. **Business Case** (2-3 pages):
   - TCO analysis (3-year comparison)
   - ROI calculation with payback period
   - Strategic value (data sovereignty, risk mitigation)
   - Success metrics

5. **Implementation Approach** (2-3 pages):
   - Phased migration roadmap
   - Migration strategy (lift-and-shift, replatform)
   - Risk mitigation strategies
   - Roles & responsibilities (VK Cloud, customer, partners)

6. **Pricing** (1-2 pages):
   - Detailed cost breakdown (by service)
   - Monthly recurring costs
   - One-time costs (migration, setup, training)
   - Payment terms

7. **About VK Cloud** (1 page):
   - Company overview
   - Key customers and case studies
   - Certifications (GOST, ISO)
   - Support and SLAs

8. **Next Steps** (1 page):
   - Recommended actions (POC, pilot, design workshop)
   - Timeline for decision
   - Contact information

**Proposal Best Practices**:
- Executive summary on page 1 (most important)
- Use visuals (architecture diagrams, charts, graphs)
- Quantify value (specific numbers, not vague claims)
- Include proof points (customer stories, references, benchmarks)
- Address objections proactively
- Clear, actionable next steps
- Professional formatting (branded PDF)

**Deliverables**:
- Proposal document (PDF)
- Presentation deck (PowerPoint/Google Slides)
- Supporting materials (case studies, datasheets, whitepapers)

---

### Stage 6: POC/Pilot (Validate & De-Risk)

**Goal**: Prove VK Cloud meets technical requirements

**POC Scope Definition**:
1. **Objective**: What are you validating? (performance, integration, migration feasibility)
2. **Duration**: 2-4 weeks typical
3. **Success Criteria**: Quantifiable metrics (e.g., "Query latency <100ms")
4. **Exit Criteria**: Go/no-go decision criteria
5. **Resources**: VK Cloud credits, technical support, customer personnel

**POC Types**:
1. **Performance POC**: Migrate test workload, benchmark vs. current
2. **Integration POC**: Validate API integrations, data sync, SSO
3. **Migration Pilot**: Migrate non-critical app to validate migration process
4. **DR POC**: Validate backup/restore, failover procedures

**POC Process**:
1. **Planning**: Define scope, success criteria, timeline
2. **Setup**: Provision VK Cloud resources, configure networking
3. **Migration**: Migrate test workload to VK Cloud
4. **Testing**: Functional, performance, integration testing
5. **Measurement**: Collect metrics vs. success criteria
6. **Evaluation**: Go/no-go decision
7. **Documentation**: POC report with results and recommendations

**Deliverables**:
- POC plan document
- VK Cloud environment setup
- Test results and benchmarks
- POC report (success/failure, recommendations)
- Migration lessons learned

---

## Pre-Sale Metrics & KPIs

**Opportunity Metrics**:
- **Win Rate**: >50% of qualified opportunities
- **Average Deal Size**: $100K-$2M ARR (enterprise)
- **Sales Cycle**: 3-6 months (qualification to contract)
- **Qualification Rate**: >30% of inbound leads qualify

**Activity Metrics**:
- **Discovery Sessions**: 5-10 per month
- **Proposals Delivered**: 3-5 per month
- **POCs Running**: 2-4 concurrent
- **Customer References**: >10 referenceable customers

**Quality Metrics**:
- **Proposal Win Rate**: >50%
- **POC to Deal Conversion**: >70%
- **Time to Proposal**: <7 days from discovery
- **Customer NPS on Proposal Quality**: >8/10

---

## Key Principles

1. **Qualify Ruthlessly**: One well-qualified deal > 10 unqualified opportunities
2. **Discovery Over Pitching**: Ask questions, don't pitch products
3. **Customer Success First**: Design for customer outcomes, not VK Cloud features
4. **Quantify Everything**: Specific numbers (TCO, ROI, performance) beat vague claims
5. **Acknowledge Gaps**: Honesty builds trust—admit where competitors are stronger
6. **Proof Over Claims**: Customer stories, benchmarks, references beat marketing claims
7. **Visualize Solutions**: Diagrams reveal insights that text hides
8. **Compete on Value**: Total value (outcomes / cost), not just price
9. **Champion Development**: No champion = no deal. Find, enable, protect champions
10. **Follow Up Relentlessly**: Pre-sale is iterative—discovery, design, refine, repeat

---

## Tools & Templates

**Discovery Templates**:
- Infrastructure inventory spreadsheet
- Requirements matrix (Must/Should/Could)
- Dependency map
- Current state architecture diagram template

**Design Templates**:
- Reference architecture diagrams (Mermaid)
- Technical specification outline
- Migration plan template
- Risk assessment matrix

**Proposal Templates**:
- Commercial proposal template
- RFP response checklist
- Technical proposal outline
- SOW template

**POC Templates**:
- POC plan template
- Success criteria checklist
- POC report outline
- Benchmark comparison template

---

Use this methodology systematically to increase win rates, accelerate sales cycles, and deliver customer success with VK Cloud solutions.
