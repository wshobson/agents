---
name: startup-init
description: Initialize a new startup project with comprehensive documentation, frameworks, and strategic planning materials
---

# Startup Initialization Command

This command helps you set up a complete startup project structure with all essential documents, frameworks, and strategic planning materials needed to build a successful company from 0 to $100M ARR.

## What This Command Does

When you run `/startup-init`, the system will:

1. **Gather Information** about your startup idea through interactive questions
2. **Create Project Structure** with organized directories for all startup materials
3. **Generate Core Documents** including:
   - Business Model Canvas
   - Value Proposition Canvas
   - Lean Startup Plan
   - Product Roadmap
   - Financial Projections Template
   - Investor Materials (pitch deck outline, data room structure)
   - Team Planning (hiring roadmap, equity allocation)
   - Go-to-Market Strategy
4. **Set Up Frameworks** for tracking metrics, OKRs, and growth
5. **Create Templates** for ongoing operations

## Usage

```bash
/startup-init
```

The command will guide you through an interactive questionnaire:

### Phase 1: Startup Overview

**Questions:**
1. What is your startup name?
2. One-line description of what you're building?
3. What problem are you solving?
4. Who is your target customer?
5. What stage are you at? (Idea, MVP, Product-Market Fit, Scaling)
6. Have you raised funding? If yes, how much and from whom?

### Phase 2: Market and Competition

**Questions:**
1. How big is your target market (TAM)?
2. What's your beachhead market?
3. Who are your main competitors?
4. What's your unique differentiation?
5. Why now? (Market timing and trends)

### Phase 3: Product and Business Model

**Questions:**
1. Describe your product/solution
2. What's your revenue model? (SaaS, marketplace, transaction, etc.)
3. What's your pricing strategy?
4. What are your unit economics? (if known)
5. What's your go-to-market strategy?

### Phase 4: Team and Resources

**Questions:**
1. Who are the founders and their roles?
2. How many team members do you have?
3. What key roles do you need to hire?
4. What's your current monthly burn rate?
5. How much runway do you have?

### Phase 5: Goals and Milestones

**Questions:**
1. What's your goal for the next 3 months?
2. What's your goal for the next 12 months?
3. What metrics matter most to you?
4. When do you plan to raise funding next?
5. What's your long-term vision (3-5 years)?

## Generated Structure

After completing the questionnaire, the following structure will be created:

```
[startup-name]/
├── README.md                          # Startup overview and quick links
├── strategy/
│   ├── business-model-canvas.md       # BMC framework
│   ├── value-proposition-canvas.md    # VPC framework
│   ├── lean-canvas.md                 # Lean startup canvas
│   ├── competitive-analysis.md        # Competitor research
│   ├── market-sizing.md               # TAM/SAM/SOM analysis
│   └── positioning.md                 # Positioning statement
├── product/
│   ├── product-vision.md              # Long-term product vision
│   ├── product-roadmap.md             # Quarterly roadmap
│   ├── user-personas.md               # Target customer personas
│   ├── user-stories.md                # Feature requirements
│   ├── mvp-scope.md                   # MVP definition
│   └── aha-moment.md                  # Core value delivery
├── go-to-market/
│   ├── gtm-strategy.md                # Overall GTM approach
│   ├── customer-acquisition.md        # Channel strategy
│   ├── pricing-strategy.md            # Pricing and packaging
│   ├── sales-playbook.md              # Sales process
│   └── marketing-plan.md              # Marketing calendar
├── metrics/
│   ├── north-star-metric.md           # NSM definition
│   ├── kpi-dashboard.md               # Key metrics to track
│   ├── okrs.md                        # Objectives and Key Results
│   ├── unit-economics.md              # CAC, LTV, payback
│   └── cohort-analysis.md             # Retention tracking
├── fundraising/
│   ├── fundraising-strategy.md        # Round planning
│   ├── pitch-deck-outline.md          # Slide structure
│   ├── investor-targeting.md          # VC research
│   ├── financial-model.xlsx           # 3-5 year projections
│   ├── data-room/                     # Due diligence docs
│   │   ├── company-overview.md
│   │   ├── legal/
│   │   ├── financial/
│   │   └── product/
│   └── investor-updates/              # Monthly update templates
├── team/
│   ├── hiring-roadmap.md              # Hiring plan by quarter
│   ├── org-chart.md                   # Current and future structure
│   ├── equity-allocation.md           # Cap table and option pool
│   ├── culture-values.md              # Company values
│   ├── job-descriptions/              # JD templates
│   └── onboarding/                    # New hire onboarding
├── operations/
│   ├── meeting-rhythms.md             # Weekly/monthly meetings
│   ├── communication-guidelines.md    # How team communicates
│   ├── decision-framework.md          # How decisions are made
│   └── tools-stack.md                 # Tech stack and tools
└── templates/
    ├── weekly-update.md               # Team update format
    ├── customer-interview.md          # Interview script
    ├── feature-spec.md                # Product spec template
    └── postmortem.md                  # Incident review template
```

## Example Generated Content

### README.md

```markdown
# [Startup Name]

[One-line description]

## Quick Links
- [Business Model Canvas](./strategy/business-model-canvas.md)
- [Product Roadmap](./product/product-roadmap.md)
- [Pitch Deck Outline](./fundraising/pitch-deck-outline.md)
- [KPI Dashboard](./metrics/kpi-dashboard.md)

## Current Status
- Stage: [Pre-seed / Seed / Series A]
- ARR: $[X]
- Team: [X] people
- Runway: [X] months
- Raised: $[X] from [investors]

## Goals This Quarter
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Key Metrics
- North Star: [metric]
- Users: [X]
- Revenue: $[X]
- Growth: [X]% MoM

Last updated: [Date]
```

### Business Model Canvas

```markdown
# Business Model Canvas

## Key Partners
- [Partner type 1]
- [Partner type 2]

## Key Activities
- [Activity 1]
- [Activity 2]

## Key Resources
- [Resource 1]
- [Resource 2]

## Value Propositions
- [Value prop 1]
- [Value prop 2]

## Customer Relationships
- [Relationship type]

## Channels
- [Channel 1]
- [Channel 2]

## Customer Segments
- [Segment 1]
- [Segment 2]

## Cost Structure
- [Cost 1]: $[X]/month
- [Cost 2]: $[X]/month

## Revenue Streams
- [Stream 1]: $[X]/month
- [Stream 2]: $[X]/month
```

### OKRs Template

```markdown
# OKRs - Q[X] 202[Y]

## Company OKRs

### Objective 1: [Achieve product-market fit]
- KR1: Reach 100 paying customers (currently: 25)
- KR2: Achieve 80%+ month-2 retention (currently: 60%)
- KR3: NPS score of 50+ (currently: 35)

### Objective 2: [Build world-class team]
- KR1: Hire VP Engineering and 3 senior engineers
- KR2: Employee NPS of 70+
- KR3: Reduce time-to-hire to <30 days

### Objective 3: [Prepare for Series A]
- KR1: Reach $1M ARR (currently: $400K)
- KR2: Achieve LTV:CAC ratio of 3:1
- KR3: Complete pitch deck and financial model

## Team-Specific OKRs

### Engineering
[Team OKRs aligned with company objectives]

### Sales/Growth
[Team OKRs aligned with company objectives]

### Product
[Team OKRs aligned with company objectives]
```

## Command Options

You can customize the initialization with flags:

```bash
# Minimal setup (core docs only)
/startup-init --minimal

# Include financial model templates
/startup-init --with-financials

# Include investor pitch materials
/startup-init --with-fundraising

# Full setup with all templates
/startup-init --full

# Specify stage
/startup-init --stage=seed
/startup-init --stage=series-a
```

## Next Steps After Initialization

After running `/startup-init`, the system will guide you to:

1. **Complete Core Documents**
   - Fill out Business Model Canvas
   - Define your Value Proposition
   - Set OKRs for next quarter

2. **Activate Relevant Agents**
   - `startup-founder-ceo` for strategic guidance
   - `fundraising-expert` if raising capital
   - `growth-strategist` for scaling plans
   - `team-builder` for hiring

3. **Use Relevant Skills**
   - `product-market-fit` for validation
   - `venture-capital-fundraising` for funding prep
   - `niche-discovery` for market research

4. **Generate Specific Materials**
   - `/pitch-deck-generator` for investor materials
   - `/business-model-canvas` for strategy
   - `/investor-outreach` for fundraising

## Integration with Other Commands

This command works seamlessly with:
- `/pitch-deck-generator` - Creates pitch deck from your data
- `/financial-model` - Generates detailed projections
- `/investor-outreach` - Preps for fundraising
- `/hiring-plan` - Creates recruitment roadmap

## Best Practices

1. **Keep Documents Updated**
   - Review and update monthly
   - Track changes in version control
   - Share with team regularly

2. **Use as Single Source of Truth**
   - Link to these docs in meetings
   - Reference in decision-making
   - Onboard new team members with these

3. **Iterate Based on Learning**
   - Update assumptions as you learn
   - Track what changed and why
   - Document pivots and decisions

4. **Share with Stakeholders**
   - Investors: fundraising folder
   - Team: strategy and product folders
   - Advisors: relevant sections

## Example Workflow

```bash
# 1. Initialize startup project
/startup-init --full

# 2. Activate CEO agent for strategic guidance
@startup-founder-ceo help me fill out the Business Model Canvas

# 3. Generate pitch deck when ready
/pitch-deck-generator

# 4. Get help with specific areas
@fundraising-expert help me target the right VCs
@growth-strategist help me build our acquisition strategy
@team-builder help me create job descriptions

# 5. Regular updates
# Update OKRs quarterly
# Update metrics weekly
# Update roadmap monthly
```

## Support

For help with this command:
- Review the generated README.md in your startup folder
- Consult relevant skills in the `skills/` directory
- Activate the `startup-founder-ceo` agent for guidance
- Check example templates in `templates/` directory

---

**Ready to start building?** Run `/startup-init` now to create your startup foundation.
