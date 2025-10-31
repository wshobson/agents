---
name: strategy-analysis
description: Comprehensive product strategy analysis and planning tool. Conducts market opportunity assessment, competitive analysis, roadmap planning, and go-to-market strategy definition. Coordinates product-manager agent with market research, stakeholder interviews, and strategic framework application.
---

# Product Strategy Analysis

Conduct comprehensive product strategy analysis covering market opportunity sizing, competitive positioning, roadmap planning, and go-to-market execution.

[Extended thinking: This command orchestrates the product-manager agent to deliver comprehensive strategic analysis. It guides through discovery phases (market understanding, user research, competitive landscape), strategic planning (vision definition, positioning, opportunity sizing), tactical execution (roadmap planning, prioritization, success metrics), and implementation readiness (go-to-market planning, stakeholder alignment, metric setup). The command adapts based on product maturity level (pre-launch, growth-stage, scaling, mature) and provides templated outputs for each phase.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Product Maturity Level
- **pre-launch**: Concept validation, MVP planning, market entry strategy
- **early-stage**: MVP launched, product-market fit validation, early growth
- **growth-stage**: Strong PMF signals, scaling planning, new market opportunities
- **scaling**: Rapid growth, organizational scaling, new product lines
- **mature**: Market leadership, adjacent markets, optimization focus

### Strategy Type
- **greenfield**: New product from scratch, market creation focus
- **adjacency**: Existing product, new market/segment expansion
- **optimization**: Mature product, efficiency and retention focus
- **competitive**: Established market, differentiation and market share

### Analysis Depth
- **quick**: 1-2 hour analysis, key findings and recommendations
- **standard**: 4-8 hour analysis, comprehensive planning with templates
- **deep**: 1-2 day analysis, detailed research with primary sources and validation

## Phase 1: Market Understanding & Discovery

1. **Market Context Definition**
   - What is the current market size and growth trajectory?
   - What are the key market segments and customer archetypes?
   - What are major industry trends and disruption signals?
   - What regulatory or technology shifts are impacting the market?
   - Who are the primary competitors and what are they doing?

2. **Customer Needs Assessment**
   - What are the primary user pain points and needs?
   - How are customers currently solving these problems?
   - What would be the ideal solution from customer perspective?
   - Who are the different buyer personas and their motivations?
   - What are the willingness-to-pay levels for different segments?

3. **Competitive Landscape Analysis**
   - Who are direct competitors and what are their strengths/weaknesses?
   - What is their positioning and go-to-market strategy?
   - What market share do they have and how are they growing?
   - What customer feedback exists about competitors?
   - Where are there market gaps and underserved segments?

**Output**: Market opportunity assessment document with customer insights and competitive analysis

## Phase 2: Strategic Foundation

4. **Vision & Positioning Definition**
   - Use Task tool with subagent_type="product-management:product-manager"
   - Prompt: "Define product vision and market positioning for: $ARGUMENTS. Current market context: [include market analysis from Phase 1]. Define: (1) Clear product vision that's inspiring and measurable, (2) Mission statement explaining why the product exists, (3) Target customer segments with detailed personas, (4) Competitive differentiation and positioning, (5) Core values and guiding principles, (6) 3-year strategic goals aligned with business objectives."
   - Expected output: Vision document, positioning statement, strategic goals
   - Context: Market analysis, business constraints, user research

5. **Market Opportunity Sizing**
   - Use Task tool with subagent_type="product-management:product-manager"
   - Prompt: "Size market opportunity for: $ARGUMENTS. Using market data: [include competitive analysis]. Calculate: (1) Total Addressable Market (TAM) using top-down and bottom-up approaches, (2) Serviceable Available Market (SAM) given our constraints, (3) Serviceable Obtainable Market (SOM) for Years 1-3, (4) Growth trajectory and market trends, (5) Key market assumptions and validation needs."
   - Expected output: Market sizing model, opportunity assessment, growth projections
   - Context: Market research, competitive positioning, business model

6. **Strategic Success Metrics**
   - Use Task tool with subagent_type="product-management:product-manager"
   - Prompt: "Define strategic success metrics and OKRs for: $ARGUMENTS. Business vision: [include vision from step 4]. Create: (1) North Star metric representing core value delivery, (2) Company-level OKRs (3-year, annual, quarterly), (3) Product team OKRs aligned with company goals, (4) Leading and lagging indicators for each KR, (5) Success metric dashboard and tracking approach, (6) Benchmarks and targets by stage (early, growth, mature)."
   - Expected output: OKR framework, metrics dashboard, success criteria
   - Context: Product vision, market opportunity, business objectives

## Phase 3: Tactical Planning

7. **Roadmap & Prioritization Planning**
   - Use Task tool with subagent_type="product-management:product-manager"
   - Prompt: "Create product roadmap and prioritization plan for: $ARGUMENTS. Strategic context: [include vision and metrics from previous steps]. Deliver: (1) Feature brainstorming and validation, (2) RICE scoring for all candidate features, (3) 12-month roadmap with theme-based or outcome-based organization, (4) Phased release plan with MVP, Alpha, Beta, GA phases, (5) Dependency mapping and critical path analysis, (6) Resource requirements and team allocation."
   - Expected output: Roadmap artifacts, prioritized feature list, phased delivery plan
   - Context: Strategic goals, market opportunity, team capacity

8. **Go-to-Market Strategy**
   - Use Task tool with subagent_type="product-management:product-manager"
   - Prompt: "Develop go-to-market (GTM) strategy for: $ARGUMENTS. Product roadmap: [include roadmap from step 7]. Plan: (1) Target customer profile (TCP) with detailed personas, (2) Positioning and messaging, (3) Distribution channel strategy (direct, partnerships, B2B2C), (4) Marketing and sales approach by stage, (5) Launch phasing (soft launch, beta, public), (6) Success metrics and validation milestones, (7) Competitive response plan."
   - Expected output: GTM plan, positioning document, launch timeline, marketing strategy
   - Context: Product roadmap, market positioning, business model

## Phase 4: Implementation Readiness

9. **Stakeholder Alignment & Communication**
   - Present strategic plan to key stakeholders (executive team, engineering, design, marketing)
   - Gather feedback and refine plan based on input
   - Create communication materials for different audiences:
     - Executive summary for leadership
     - Detailed roadmap for product/engineering teams
     - Go-to-market plan for marketing/sales
     - Customer communication for launch
   - Schedule regular strategy reviews (quarterly)

10. **Execution Kickoff**
   - Translate strategy into quarterly OKRs and team goals
   - Create detailed implementation plans for next phase
   - Establish metrics tracking and dashboard setup
   - Plan for regular retrospectives and strategy adjustments
   - Schedule customer interviews and feedback loops

**Output**: Quarterly execution plan, team OKRs, implementation timeline

## Output Artifacts

### Strategy Document Contents
1. **Executive Summary** (1-2 pages)
   - Market opportunity
   - Competitive positioning
   - Strategic vision
   - Key metrics and targets

2. **Market Analysis** (5-10 pages)
   - Market sizing (TAM/SAM/SOM)
   - Customer segments and personas
   - Competitive landscape
   - Market trends and opportunities

3. **Strategic Plan** (5-10 pages)
   - Product vision and mission
   - Positioning and differentiation
   - Long-term strategic goals (3-year)
   - Success metrics and OKRs

4. **Roadmap & Execution** (3-5 pages)
   - Feature prioritization (RICE scores)
   - 12-month product roadmap
   - Phased delivery plan
   - Resource requirements

5. **Go-to-Market Plan** (5-10 pages)
   - Target customer profiles
   - Positioning and messaging
   - Distribution and marketing strategy
   - Launch plan and timeline
   - Success metrics for each phase

6. **Financial Model** (if applicable)
   - Customer acquisition cost (CAC)
   - Lifetime value (LTV) projections
   - Revenue models and pricing strategy
   - Unit economics and break-even analysis

## Usage Patterns

### For New Product Launch
```
/product-management:strategy-analysis --product-maturity=pre-launch --strategy-type=greenfield
```

Follow all 10 steps to create comprehensive strategy from market validation through launch readiness.

### For Product in Growth
```
/product-management:strategy-analysis --product-maturity=growth-stage --strategy-type=adjacency --analysis-depth=standard
```

Focus on market opportunity sizing, positioning in new segments, and adjacency roadmap planning.

### For Mature Product Optimization
```
/product-management:strategy-analysis --product-maturity=mature --strategy-type=optimization --analysis-depth=quick
```

Quick analysis of retention optimization, operational efficiency, and market expansion opportunities.

### For Competitive Response
```
/product-management:strategy-analysis --strategy-type=competitive --analysis-depth=deep
```

Deep competitive analysis with strategic positioning and differentiation planning.

## Success Criteria

✅ **Strong Strategy Output Includes:**
- Clear market opportunity quantification (TAM/SAM/SOM)
- Compelling product vision aligned with market opportunity
- Differentiated positioning based on competitive analysis
- Validated customer needs and persona definitions
- Realistic revenue and growth projections
- Prioritized feature roadmap with business justification
- Clear go-to-market plan with distribution strategy
- Aligned team OKRs and success metrics
- Stakeholder buy-in and organizational alignment
- Regular review and adaptation process

## When to Use This Command

- **Planning new products** - Validate market opportunity and define go-to-market
- **Pivoting existing products** - Reassess market positioning and new strategy
- **Entering new markets** - Analyze adjacency opportunity and expansion strategy
- **Competitive threats** - Respond to competitive moves with strategic plan
- **Annual planning** - Update 3-year strategy aligned with business goals
- **Stakeholder alignment** - Present comprehensive strategy to leadership
- **Team onboarding** - New PMs or executives understanding product strategy

## Related Tasks

- **User Research** - Conduct deeper customer validation and interview analysis
- **Competitive Analysis** - More detailed competitive intelligence and benchmarking
- **Financial Modeling** - Build detailed unit economics and revenue models
- **Marketing Planning** - Detailed go-to-market execution and campaign planning
- **Product Launch** - Orchestrate product launch with all teams
