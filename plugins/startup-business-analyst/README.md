# Startup Business Analyst Plugin

Comprehensive business analysis plugin specialized for early-stage startups, providing market sizing, financial modeling, team planning, and strategic research capabilities.

## Overview

This plugin equips Claude with expert-level startup business analysis capabilities, focusing on the critical calculations and strategic insights needed by entrepreneurs, founders, and investors.

## Features

### 5 Specialized Skills

- **market-sizing-analysis** - TAM/SAM/SOM calculations with multiple methodologies
- **startup-financial-modeling** - 3-5 year financial projections with scenarios
- **team-composition-analysis** - Organizational design and compensation planning
- **competitive-landscape** - Market positioning and competitive strategy
- **startup-metrics-framework** - Key metrics for different business models

### 3 Interactive Commands

- `/startup-business-analyst:market-opportunity` - Generate market opportunity analysis
- `/startup-business-analyst:financial-projections` - Create financial models with scenarios
- `/startup-business-analyst:business-case` - Generate comprehensive business case documents

### 1 Expert Agent

- **startup-analyst** - Specialized agent for early-stage startup analysis

## Installation

```bash
/plugin install startup-business-analyst@claude-code-workflows
```

## Usage

### Automatic Skill Activation

Skills activate automatically based on your questions:

```
"What's the TAM for a B2B SaaS project management tool?"
→ Activates market-sizing-analysis skill

"Create a 3-year financial model for my marketplace startup"
→ Activates startup-financial-modeling skill

"What are the key SaaS metrics I should track?"
→ Activates startup-metrics-framework skill
```

### Commands

**Market Opportunity Analysis:**

```bash
/startup-business-analyst:market-opportunity
```

Generates comprehensive market sizing with TAM/SAM/SOM breakdown.

**Financial Projections:**

```bash
/startup-business-analyst:financial-projections
```

Creates 3-scenario financial model with revenue, costs, and runway.

**Business Case:**

```bash
/startup-business-analyst:business-case
```

Produces investor-ready business case document.

### Agent Usage

The startup-analyst agent triggers automatically for business-related questions:

```
"Help me analyze the competitive landscape for my fintech startup"
"What should my team structure look like at $1M ARR?"
"Calculate my customer acquisition payback period"
```

## Skills Reference

### Market Sizing Analysis

Covers three methodologies:

- **Top-down**: Industry reports and market research
- **Bottom-up**: Customer segment calculations
- **Value theory**: Problem value and willingness to pay

Includes templates for SaaS, marketplace, consumer, B2B, and fintech.

### Startup Financial Modeling

Components:

- Revenue projections (by customer segment)
- Cost structure (COGS, S&M, R&D, G&A)
- Cash flow and runway calculations
- Headcount planning
- Scenario analysis (conservative, base, optimistic)

### Team Composition Analysis

Covers:

- Role-by-stage recommendations
- Compensation benchmarks (US-focused)
- Equity/options allocation strategies
- Full-time vs. contractor decisions
- Organizational design

### Competitive Landscape

Frameworks:

- Porter's Five Forces
- Blue Ocean Strategy
- Positioning maps
- Go-to-market strategy
- Competitive pricing analysis

### Startup Metrics Framework

Business model coverage:

- **SaaS**: ARR, MRR, NRR, CAC, LTV, Magic Number
- **Marketplace**: GMV, Take Rate, Liquidity
- **Consumer**: DAU/MAU, Retention, Virality
- **B2B**: ACR, Win Rate, Sales Cycle
- **Fintech**: TPV, Monetization Rate, Fraud Rate

## Examples

### Example 1: TAM/SAM/SOM Calculation

```markdown
"Calculate TAM/SAM/SOM for an AI-powered email marketing tool for e-commerce"

→ Skill activates and provides:

- TAM: Total email marketing software market
- SAM: AI-powered tools for e-commerce segment
- SOM: Realistic 3-5 year capture
- Methodology explanation
- Market growth assumptions
- Data sources and citations
```

### Example 2: Financial Model

```markdown
"Create a 3-year financial model for a SaaS product with $50/mo pricing"

→ Command generates:

- Revenue by cohort
- Cost structure breakdown
- Headcount plan
- Cash flow projection
- Runway calculation
- 3 scenarios (conservative/base/optimistic)
```

### Example 3: Competitive Analysis

```markdown
"Analyze competitors in the project management software space"

→ Agent provides:

- Competitive landscape map
- Feature comparison matrix
- Pricing analysis
- Market positioning recommendations
- Differentiation opportunities
```

## Best Practices

1. **Provide Context**: Share your business model, target market, and stage
2. **Be Specific**: Include numbers, timeframes, and assumptions where possible
3. **Iterate**: Start with high-level analysis, then drill into details
4. **Validate Assumptions**: Question and refine assumptions with the agent
5. **Cite Sources**: Ask for data sources and validation methods

## Requirements

- Claude Code CLI
- Internet access (for web research capabilities)
- No external dependencies

## Model Configuration

- **Agent Model**: `inherit` (uses your session default model)
- **Recommended**: Sonnet for balance of speed and quality
- **Use Opus for**: Complex multi-market analysis or detailed financial models

## Contributing

Found an issue or have suggestions? Please open an issue or PR at:
https://github.com/wshobson/agents

## License

MIT License - see repository LICENSE file for details.

## Version History

- **1.0.0** (2026-01-13): Initial release
  - 5 specialized skills
  - 3 interactive commands
  - 1 expert agent
  - Comprehensive startup analysis capabilities
