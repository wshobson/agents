# AI Systems Audit Workflow

## Overview
Comprehensive evaluation of client's current AI capabilities, gaps, and opportunities.

## Workflow ID
`wf_ai_systems_audit`

## Trigger
- New AI initiative planned
- Current AI system underperforming
- Technology refresh needed
- Compliance requirement

## Phases

### Phase 1: Current State Assessment
**Duration:** 2-4 hours
**Primary Agent:** ai-engineer
**Support Agents:** data-scientist, architect-review

**Steps:**
1. Inventory existing AI/ML systems
2. Document current architectures
3. Review data pipelines
4. Assess model performance
5. Evaluate infrastructure

**Outputs:**
- AI systems inventory
- Architecture diagrams
- Performance baseline report

### Phase 2: Gap Analysis
**Duration:** 2-3 hours
**Primary Agent:** architect-review
**Support Agents:** ai-engineer, security-auditor

**Steps:**
1. Compare against industry standards
2. Identify capability gaps
3. Assess technical debt
4. Evaluate scalability
5. Security posture analysis

**Outputs:**
- Gap analysis report
- Technical debt inventory
- Security findings

### Phase 3: Opportunity Mapping
**Duration:** 1-2 hours
**Primary Agent:** ai-engineer
**Support Agents:** business-analyst, prompt-engineer

**Steps:**
1. Identify automation opportunities
2. Evaluate AI use cases
3. Prioritize by impact/effort
4. Define quick wins
5. Map long-term initiatives

**Outputs:**
- Opportunity matrix
- Use case prioritization
- Quick wins list

### Phase 4: Recommendations
**Duration:** 1-2 hours
**Primary Agent:** docs-architect
**Support Agents:** architect-review, ai-engineer

**Steps:**
1. Synthesize findings
2. Create recommendations
3. Define implementation phases
4. Estimate resources
5. Prepare executive summary

**Outputs:**
- Recommendations report
- Implementation roadmap
- Executive presentation

## Agent Involvement

```json
{
  "phase1_current_state": ["ai-engineer", "data-scientist", "architect-review"],
  "phase2_gap_analysis": ["architect-review", "ai-engineer", "security-auditor"],
  "phase3_opportunities": ["ai-engineer", "business-analyst", "prompt-engineer"],
  "phase4_recommendations": ["docs-architect", "architect-review", "ai-engineer"]
}
```

## Audit Framework

### AI Maturity Levels
| Level | Description | Characteristics |
|-------|-------------|-----------------|
| 1 - Ad Hoc | No formal AI | Manual processes, no ML |
| 2 - Exploratory | Pilot projects | POCs, siloed experiments |
| 3 - Defined | Systematic approach | Standards, some production |
| 4 - Managed | Scaled AI | MLOps, monitoring, governance |
| 5 - Optimizing | AI-first | Continuous improvement, innovation |

### Assessment Categories
- **Data Readiness**: Quality, availability, governance
- **Model Operations**: Training, deployment, monitoring
- **Infrastructure**: Compute, storage, networking
- **Talent**: Skills, team structure, training
- **Governance**: Ethics, compliance, security

## Quality Gates

- [ ] All AI systems documented
- [ ] Performance baselines established
- [ ] Gaps prioritized
- [ ] Recommendations approved
- [ ] Roadmap accepted

## Success Metrics
- Audit completion time: <2 weeks
- Finding actionability: >80%
- Recommendation adoption: >60%
