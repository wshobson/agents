# Client Onboarding Workflow

## Overview
Structured process for onboarding new MDS clients from initial contact to active engagement.

## Workflow ID
`wf_client_onboarding`

## Trigger
- New client inquiry received
- Contract signed
- Referral received

## Phases

### Phase 1: Intake
**Duration:** 30-60 minutes
**Primary Agent:** business-analyst

**Steps:**
1. Capture client information
2. Understand business context
3. Identify pain points
4. Document current state
5. Set expectations

**Outputs:**
- Client profile document
- Initial requirements list
- Communication preferences

### Phase 2: Assessment
**Duration:** 1-2 hours
**Primary Agent:** architect-review
**Support Agents:** security-auditor, data-scientist

**Steps:**
1. Technical environment assessment
2. Current tooling evaluation
3. Integration requirements
4. Security posture review
5. Data readiness assessment

**Outputs:**
- Technical assessment report
- Integration requirements document
- Risk assessment

### Phase 3: Proposal
**Duration:** 1-2 hours
**Primary Agent:** docs-architect
**Support Agents:** business-analyst

**Steps:**
1. Define engagement scope
2. Create implementation roadmap
3. Estimate resources and timeline
4. Prepare pricing/package
5. Draft proposal document

**Outputs:**
- Engagement proposal
- Implementation roadmap
- Resource plan

### Phase 4: Kickoff
**Duration:** 30-60 minutes
**Primary Agent:** business-analyst
**Support Agents:** all relevant specialists

**Steps:**
1. Present final proposal
2. Confirm scope and timeline
3. Assign team members
4. Set up communication channels
5. Schedule first working session

**Outputs:**
- Signed statement of work
- Project setup in system
- Kickoff meeting scheduled

## Agent Involvement

```json
{
  "phase1_intake": ["business-analyst"],
  "phase2_assessment": ["architect-review", "security-auditor", "data-scientist"],
  "phase3_proposal": ["docs-architect", "business-analyst"],
  "phase4_kickoff": ["business-analyst", "ceo-agent"]
}
```

## Quality Gates

- [ ] Client profile complete
- [ ] Technical assessment approved
- [ ] Proposal reviewed and approved
- [ ] SOW signed
- [ ] Project created in system

## Templates

### Client Profile Template
```markdown
# Client Profile: {Client Name}

## Contact Information
- Primary Contact:
- Email:
- Phone:

## Business Context
- Industry:
- Company Size:
- Current Challenges:

## Technical Environment
- Primary Languages:
- Key Technologies:
- Infrastructure:

## Engagement Goals
1.
2.
3.
```

## Success Metrics
- Time to onboard: <1 week
- Client satisfaction: >4.5/5
- Scope accuracy: >90%
