# PRD Creation Workflow

## Purpose
Create comprehensive Product Requirements Documents that align stakeholders and guide development.

## Trigger
- New feature approved from analysis phase
- Product initiative kickoff
- Major enhancement request

## Agents Involved
| Agent | Role | Model |
|-------|------|-------|
| backend-architect | Technical requirements | opus |
| frontend-developer | UI/UX requirements | sonnet |
| docs-architect | Document structure | opus |
| security-auditor | Security requirements | opus |

## Workflow Steps

### Step 1: Requirements Gathering
**Agent:** backend-architect
**Actions:**
1. Extract functional requirements from analysis outputs
2. Define technical requirements
3. Identify integration points
4. Specify performance requirements

**Output:** Technical requirements list

### Step 2: User Experience Requirements
**Agent:** frontend-developer
**Actions:**
1. Define user stories
2. Map user journeys
3. Specify UI requirements
4. Define accessibility needs

**Output:** UX requirements document

### Step 3: Security & Compliance
**Agent:** security-auditor
**Actions:**
1. Define security requirements
2. Identify compliance needs
3. Specify authentication/authorization
4. Define data handling requirements

**Output:** Security requirements document

### Step 4: Document Assembly
**Agent:** docs-architect
**Actions:**
1. Compile all requirements into PRD template
2. Ensure consistency and completeness
3. Add acceptance criteria
4. Define success metrics

**Output:** Complete PRD

## PRD Template Structure
```markdown
# Product Requirements Document

## 1. Overview
- Product Name
- Version
- Author
- Date
- Status

## 2. Problem Statement
- Background
- Pain Points
- Target Users

## 3. Goals & Success Metrics
- Primary Goals
- Key Metrics
- Success Criteria

## 4. Functional Requirements
- Core Features
- User Stories
- Acceptance Criteria

## 5. Technical Requirements
- Architecture Overview
- Integration Points
- Performance Requirements
- Scalability Needs

## 6. Security Requirements
- Authentication
- Authorization
- Data Protection
- Compliance

## 7. UX Requirements
- User Journeys
- UI Specifications
- Accessibility

## 8. Out of Scope
- Excluded Features
- Future Considerations

## 9. Timeline & Milestones
- Phase 1
- Phase 2
- Release

## 10. Risks & Mitigations
```

## Exit Criteria
- All sections completed
- Stakeholder review completed
- Sign-off obtained
- Ready for solutioning phase
