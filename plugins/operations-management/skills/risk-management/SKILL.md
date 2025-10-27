---
name: risk-management
description: Master operational risk identification, assessment, and mitigation. Use when evaluating business risks, developing contingency plans, managing operational resilience, or preparing for disruptions.
---

# Risk Management Skill

## When to Use This Skill

- Identifying potential operational, financial, and strategic risks
- Assessing risk probability and impact
- Developing risk mitigation and contingency strategies
- Creating business continuity and disaster recovery plans
- Managing vendor and supply chain risks
- Implementing risk controls and monitoring
- Preparing for scenario planning and stress testing
- Building operational resilience and redundancy

## Core Concepts

### Risk Framework

**Risk Definition**: Uncertainty that could impact business objectives
- **Probability**: Likelihood of occurrence (1-5 scale or percentage)
- **Impact**: Potential consequence if it occurs (1-5 scale or financial value)
- **Risk Score**: Probability × Impact determines priority

**Risk Categories**:

1. **Strategic Risks**
   - Market disruption and competition
   - Business model obsolescence
   - Regulatory changes and compliance
   - Mergers and acquisition risks

2. **Operational Risks**
   - Process failures and bottlenecks
   - System/technology outages
   - Key person dependencies
   - Supplier/vendor failures
   - Quality and product issues

3. **Financial Risks**
   - Cash flow and liquidity risk
   - Currency and commodity price volatility
   - Debt and credit risks
   - Budget overruns and cost inflation

4. **Compliance & Legal Risks**
   - Regulatory violations (GDPR, SOC2, HIPAA, etc.)
   - Intellectual property disputes
   - Litigation and legal claims
   - Contract breach by partners

5. **Reputational Risks**
   - Customer dissatisfaction and churn
   - Brand damage and negative publicity
   - Data breaches and security incidents
   - Executive/leadership scandals

6. **People Risks**
   - Talent loss and key person dependencies
   - Cultural issues and retention
   - Skills gaps and training gaps
   - Leadership transitions

### Risk Identification Process

**Structured Brainstorming**:
- Bring together cross-functional team
- Ask: "What could prevent us from achieving our objectives?"
- Document all concerns without filtering
- Group similar risks together
- Avoid dismissing concerns without analysis

**Risk Questionnaires**:
- Industry-specific risk surveys
- Stakeholder interviews
- Customer feedback analysis
- Competitor analysis for strategic threats
- Technical assessments for system risks

**Historical Analysis**:
- Past issues and lessons learned
- Industry incidents and case studies
- Internal incident logs and near-misses
- Trend analysis (increasing or decreasing risks)

**Process & System Review**:
- Dependencies and single points of failure
- Manual processes prone to error
- Outdated technology and systems
- Inadequate documentation or training

### Risk Assessment & Prioritization

**Probability Assessment**:
- **5 (Very High)**: Likely within 12 months (>50% probability)
- **4 (High)**: Possible within 12 months (20-50%)
- **3 (Medium)**: Could occur within 2-3 years (5-20%)
- **2 (Low)**: Unlikely but possible (1-5%)
- **1 (Very Low)**: Highly unlikely (<1%)

**Impact Assessment**:
- **5 (Critical)**: Business continuity threatened, >$1M loss, major regulatory violation
- **4 (High)**: Significant operational disruption, $100K-$1M loss, moderate regulatory impact
- **3 (Medium)**: Moderate business impact, $10K-$100K loss, minor regulatory concern
- **2 (Low)**: Limited impact, $1K-$10K loss, minimal regulatory impact
- **1 (Minimal)**: Negligible impact, <$1K loss, no regulatory impact

**Risk Matrix**:
```
Impact  High |        Risk Zone (5,4)
        Med  |     Risk Zone (4,5)
        Low  |  Monitor (3,4)  Risk Zone (4,5)
             ├─────────────────────────────
             |  Low    Med    High
             └─ Probability
```

**Risk Prioritization**:
1. High probability × High impact = Top priority (immediate action)
2. Medium probability × High impact OR High probability × Medium impact = High priority
3. Everything else = Monitor or accept

### Risk Mitigation Strategies

**Four Response Options**:

**1. Avoid**
- Eliminate the risk by changing approach or strategy
- Example: Don't enter high-risk market; use proven technology
- Cost: May limit opportunities or increase other costs
- Best for: Strategic risks, catastrophic risks

**2. Mitigate**
- Reduce probability or impact
- Example: Backup power system reduces outage probability
- Cost: Prevention or control costs
- Best for: High-impact or medium-impact risks

**3. Transfer**
- Shift risk to another party (usually via insurance or contract)
- Example: Insurance for property damage; vendor manages service delivery
- Cost: Insurance premiums or contract terms
- Best for: Financial risks, liability risks

**4. Accept**
- Acknowledge risk and accept consequences
- Requires contingency plan for if risk occurs
- Cost: Potential impact if risk occurs
- Best for: Low-probability or low-impact risks, or unavoidable risks

### Contingency Planning

**If-Then Planning**:
- **If** this risk occurs
- **Then** execute this contingency plan
- **Responsibility**: Assign clear owner
- **Timeline**: How quickly must we respond?
- **Resources**: What's needed to execute?

**Business Continuity Planning**:

**Critical Functions**: Which business processes are essential?
- Revenue-generating processes
- Customer-facing operations
- Compliance and regulatory requirements
- Financial management

**Recovery Strategies**:
- **Hot Standby**: Duplicate systems running in parallel (expensive, fast recovery)
- **Warm Standby**: Systems ready to activate quickly (moderate cost/recovery)
- **Cold Standby**: Systems available but need activation time (low cost, slower)
- **Manual Processes**: Paper-based backup if systems fail

**Recovery Time Objectives (RTO)**:
- How long can we tolerate being down?
- Customer expectations and SLAs
- Financial impact per hour of downtime
- Regulatory requirements

**Recovery Point Objective (RPO)**:
- How much data can we afford to lose?
- Backup frequency and retention requirements
- Data protection and encryption

### Supply Chain & Vendor Risk

**Vendor Assessment**:
- Financial stability and credit rating
- Capacity and capability to deliver
- Quality track record and certifications
- Security and compliance posture
- Geographic concentration and disaster risk

**Risk Mitigation Approaches**:
- **Diversification**: Multiple vendors for critical services
- **Contracts**: SLAs, penalty clauses, insurance requirements
- **Monitoring**: Regular audits, performance tracking
- **Relationships**: Transparency and contingency planning discussions
- **Documentation**: Full system knowledge, not just vendor dependency

**Supplier Code of Conduct**:
- Quality standards and testing requirements
- Compliance with regulations (labor, environmental, safety)
- Cybersecurity and data protection requirements
- Incident notification and transparency
- Right to audit and inspect

### Risk Monitoring & Control

**Key Risk Indicators (KRIs)**:
- Leading indicators that warn of increasing risk
- Example: % of maintenance deferred → Equipment failure risk
- Example: Employee turnover rate → Key person risk
- Example: Days of cash on hand → Liquidity risk

**Regular Risk Reviews**:
- Quarterly risk assessment updates
- New risks that have emerged
- Risks that have been mitigated or eliminated
- Effectiveness of mitigation strategies
- Changes in probability or impact

**Escalation Triggers**:
- Define thresholds for executive escalation
- If risk score increases above X, escalate
- If mitigation is ineffective, escalate
- New risks in critical areas trigger escalation

## Common Risk Scenarios & Responses

### Scenario: Key Employee Departure

**Risk**: Loss of institutional knowledge, project delays, customer relationships
**Mitigation**:
- Cross-training and knowledge documentation
- Succession planning and development
- Competitive compensation and engagement
- Gradual knowledge transfer upon departure

**Contingency**:
- Documented processes and procedures
- Access to documentation and systems
- Mentoring relationships
- Project continuity plans

### Scenario: Cloud Provider Outage

**Risk**: Service unavailability, customer impact, revenue loss
**Mitigation**:
- Multi-region or multi-cloud architecture
- Regular disaster recovery testing
- Documented failover procedures
- Vendor SLA with penalties

**Contingency**:
- Manual workarounds for critical functions
- Customer communication plan
- Alternative provider activation
- Root cause investigation and prevention

### Scenario: Cybersecurity Breach

**Risk**: Data loss, customer harm, regulatory fines, reputation damage
**Mitigation**:
- Security controls (encryption, access management, firewalls)
- Regular security assessments and penetration testing
- Employee training on security practices
- Incident response plan
- Insurance coverage

**Contingency**:
- Incident response procedures and team
- Customer notification plan
- Legal and regulatory expertise on call
- Public relations response plan

## References

- Enterprise Risk Management (ERM) frameworks
- ISO 31000 for risk management processes
- Business continuity and disaster recovery planning standards
- Vendor risk management frameworks
- Scenario planning and stress testing methodologies
