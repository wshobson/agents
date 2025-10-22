# Product Management Plugin

Expert product management guidance for strategy, market analysis, roadmap planning, and go-to-market execution.

## Overview

This plugin provides comprehensive product management expertise covering:
- **Product Strategy**: Vision definition, market positioning, competitive analysis
- **Market Analysis**: TAM/SAM/SOM sizing, competitive landscape, trend identification
- **Roadmap Planning**: Feature prioritization (RICE), phased delivery, resource planning
- **User Research**: Customer discovery, needs validation, persona development
- **Go-to-Market**: Launch planning, positioning, distribution strategy, success metrics
- **Metrics & Analytics**: OKR definition, KPI selection, success measurement

## Contents

### Agents

#### Product Manager (`product-manager.md`)
Expert product manager with deep knowledge of product strategy, market analysis, user research, and business metrics. Masters feature prioritization, competitive positioning, and go-to-market strategies.

**Model**: Sonnet (complex reasoning for strategic decisions)

**Key Capabilities**:
- Product strategy and vision definition
- Market opportunity sizing (TAM/SAM/SOM)
- Competitive analysis and positioning
- Feature prioritization (RICE framework)
- Roadmap planning and execution
- User research and customer discovery
- OKR and metrics definition
- Go-to-market strategy

### Commands

#### Strategy Analysis (`strategy-analysis.md`)
Comprehensive product strategy analysis tool. Conducts market opportunity assessment, competitive analysis, roadmap planning, and go-to-market strategy definition.

**Phases**:
1. Market Understanding & Discovery
2. Strategic Foundation (vision, positioning, metrics)
3. Tactical Planning (roadmap, prioritization, GTM)
4. Implementation Readiness (stakeholder alignment, execution)

**Outputs**:
- Market opportunity assessment
- Product vision and positioning statement
- OKR framework and success metrics
- Product roadmap with RICE scoring
- Go-to-market plan
- Implementation timeline

### Skills

#### Product Strategy (`product-strategy/SKILL.md`)
Master product strategy frameworks, market opportunity sizing, competitive positioning, and roadmap planning. Covers:

**Key Topics**:
- Product vision and strategy framework
- Market opportunity sizing (TAM/SAM/SOM calculation)
- Competitive positioning (SWOT analysis)
- Roadmap planning (theme-based, outcome-based, risk/reward)
- Feature prioritization (RICE framework)
- Success metrics and OKRs
- Go-to-market strategy
- Product-market fit indicators

## Quick Start

### For New Product Planning
```
/product-management:strategy-analysis --product-maturity=pre-launch --strategy-type=greenfield
```

Creates comprehensive strategy from market validation through launch readiness.

### For Market Analysis
Prompt the product-manager agent directly:
```
"Analyze the market opportunity for [product concept].
Size the market (TAM/SAM/SOM), identify competitors,
and assess product-market fit potential."
```

### For Roadmap Planning
```
"Create a 12-month product roadmap for [product].
Use RICE prioritization framework, identify dependencies,
and plan phased delivery from MVP to GA."
```

### For Go-to-Market Strategy
```
"Develop a go-to-market strategy for [product launch].
Define target customer profile, positioning, distribution channels,
and launch timeline with success metrics."
```

## Integration with Other Plugins

This plugin works well with:

- **Backend Development** - For technical architecture and implementation planning
- **Code Review AI** - For evaluating product features and user experience
- **Full-Stack Orchestration** - For coordinating cross-functional feature development
- **Observability Monitoring** - For setting up product metrics and success monitoring
- **Security Scanning** - For identifying security requirements in product strategy
- **Business Analytics** - For financial modeling and business metrics

## Common Use Cases

### 1. New Product Launch
- Define market opportunity and product vision
- Analyze competitive landscape and positioning
- Create go-to-market strategy
- Plan phased rollout from beta to GA
- Set up success metrics and OKRs

### 2. Scaling Existing Product
- Identify adjacent market opportunities
- Plan expansion into new customer segments
- Develop retention and engagement strategy
- Create pricing and monetization models
- Plan organizational scaling

### 3. Competitive Response
- Analyze competitive threat and market impact
- Reassess product positioning and differentiation
- Plan product features to compete
- Update go-to-market messaging
- Define new success metrics

### 4. Feature Prioritization
- Gather candidate features from various sources
- Apply RICE prioritization framework
- Assess business impact and technical feasibility
- Create roadmap with dependencies
- Communicate decisions to stakeholders

### 5. Product-Market Fit Analysis
- Assess current retention and engagement metrics
- Conduct user research to identify pain points
- Test positioning with customers
- Measure product-market fit indicators (NPS, retention, viral coefficient)
- Plan iterations to improve fit

## Framework Reference

### RICE Prioritization
```
RICE Score = (Reach × Impact × Confidence) / Effort

- Reach: Number of users affected (quarterly)
- Impact: Value per user (3=massive, 2=high, 1=medium, 0.5=low)
- Confidence: Certainty of estimates (1.0=high, 0.8=medium, 0.5=low)
- Effort: Person-months required (1-15)
```

### OKR Structure
```
Objective: Qualitative goal (inspiring, strategic)
  ├── Key Result 1: Measurable outcome (0-1.0 scale)
  ├── Key Result 2: Measurable outcome (0-1.0 scale)
  └── Key Result 3: Measurable outcome (0-1.0 scale)
```

### Market Sizing
```
TAM (Total Addressable Market): Entire market opportunity
SAM (Serviceable Available Market): Market you can serve
SOM (Serviceable Obtainable Market): Realistic capture target
```

## Version History

- **1.0.0** - Initial release with product-manager agent, strategy-analysis command, and product-strategy skill

## Contributing

To extend this plugin:
1. Add new agents for specialized PM roles (e.g., growth-manager, product-operations)
2. Add new commands for specific analyses (e.g., user-research-planning, pricing-strategy)
3. Expand skills with domain-specific knowledge (e.g., mobile-product-strategy, b2b-saas-strategy)
4. Update marketplace.json with new components

## Resources

- [Product Manager Agent Capabilities](./agents/product-manager.md)
- [Strategy Analysis Command Guide](./commands/strategy-analysis.md)
- [Product Strategy Skill](./skills/product-strategy/SKILL.md)
- [CLAUDE.md - Plugin Development Guide](../../CLAUDE.md)
