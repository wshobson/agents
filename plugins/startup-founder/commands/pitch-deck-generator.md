---
name: pitch-deck-generator
description: Generate a world-class investor pitch deck tailored to your startup stage and target investors
---

# Pitch Deck Generator

This command creates a comprehensive, investor-ready pitch deck following best practices from successful fundraises at Sequoia, a16z, Benchmark, and other top-tier firms.

## What This Command Does

The `/pitch-deck-generator` command will:

1. **Gather Information** about your startup, traction, and fundraising goals
2. **Generate Slide Content** for each section of your pitch deck
3. **Provide Recommendations** for visuals, data presentation, and storytelling
4. **Create Multiple Formats**:
   - Markdown outline (for easy editing)
   - Google Slides structure (importable)
   - Talking points for each slide
   - Email pitch version (for cold outreach)

## Usage

```bash
# Basic usage
/pitch-deck-generator

# Specify stage
/pitch-deck-generator --stage=seed
/pitch-deck-generator --stage=series-a
/pitch-deck-generator --stage=series-b

# Specify target investors
/pitch-deck-generator --target=sequoia
/pitch-deck-generator --target=a16z

# Specify format
/pitch-deck-generator --format=google-slides
/pitch-deck-generator --format=powerpoint
```

## Interactive Questionnaire

### Section 1: Company Basics
1. Company name and tagline
2. Founding date and location
3. Founders and their backgrounds
4. One-line pitch (10 words or less)
5. Problem you're solving
6. Target customer

### Section 2: Traction and Metrics
1. Current stage (pre-revenue, revenue, scaling)
2. Key metrics:
   - Revenue (MRR/ARR)
   - Users/customers
   - Growth rate
   - Retention metrics
3. Notable customers or logos
4. Key milestones achieved

### Section 3: Market and Competition
1. Total Addressable Market (TAM)
2. Serviceable Addressable Market (SAM)
3. Serviceable Obtainable Market (SOM)
4. Market growth rate
5. Main competitors
6. Your differentiation

### Section 4: Product and Business Model
1. Product description
2. Key features
3. Revenue model
4. Pricing strategy
5. Unit economics (CAC, LTV, payback period)
6. Gross margins

### Section 5: Go-to-Market
1. Customer acquisition channels
2. Sales strategy
3. Marketing approach
4. Partnerships

### Section 6: Team
1. Founder bios (relevant experience)
2. Key team members
3. Advisors and board members
4. Key hires planned

### Section 7: Fundraising
1. Amount raising
2. Previous funding (if any)
3. Use of funds breakdown
4. Milestones to achieve with funding
5. Valuation expectation (optional)

## Generated Deck Structure

The command generates a complete pitch deck with the following slides:

### Slide 1: Title / Company Purpose
```markdown
# [Company Name]
## [Compelling Tagline]

Founded: [Date]
Raising: $[X]M [Stage] Round

[Founder Name], CEO
[Email] | [Phone]
```

**Design Recommendations:**
- Clean, bold typography
- Company logo (if you have one)
- Minimal text, maximum impact
- Professional photo of founders (optional)

### Slide 2: Problem
```markdown
# The Problem

[Target customers] face [specific problem]:

1. [Pain point 1] - costs them $[X] or [Y] hours
2. [Pain point 2] - results in [negative outcome]
3. [Pain point 3] - prevents them from [goal]

"[Customer quote describing frustration]"
- [Name], [Title] at [Company]
```

**Design Recommendations:**
- Use images that illustrate the problem
- Include customer quote with photo
- Quantify the pain when possible
- Dark or muted colors to convey problem

### Slide 3: Solution
```markdown
# Our Solution

[Company] is [simple description]:

✓ [Key benefit 1] - 10x faster than alternatives
✓ [Key benefit 2] - saves $[X] per month
✓ [Key benefit 3] - works with existing tools

[1-sentence value proposition]
```

**Design Recommendations:**
- Product screenshot or demo video
- Before/after comparison
- Simple icons for benefits
- Bright, optimistic colors

### Slide 4: Why Now
```markdown
# Why Now?

Three key trends make this possible:

1. **[Technology trend]**
   - [Specific enabler, e.g., "AI costs dropped 90%"]

2. **[Market/Behavioral trend]**
   - [Specific change, e.g., "Remote work went from 5% to 35%"]

3. **[Regulatory/Economic trend]**
   - [Specific shift, e.g., "New privacy laws favor our approach"]
```

**Design Recommendations:**
- Timeline graphic showing trends
- Statistics with large numbers
- Icons representing each trend
- Upward arrows/growth imagery

### Slide 5: Market Size
```markdown
# Market Opportunity

**TAM:** $[X]B Total Addressable Market
- [Brief explanation of how calculated]

**SAM:** $[X]B Serviceable Addressable Market
- [Geographic or segment focus]

**SOM:** $[X]M Serviceable Obtainable Market (3-year target)
- [Your realistic beachhead]

Growing at [X]% annually
```

**Design Recommendations:**
- Concentric circles (TAM > SAM > SOM)
- Source citations for credibility
- Growth rate prominently displayed
- Comparison to successful companies in space

### Slide 6: Product
```markdown
# Product

[Screenshot or demo video]

Key capabilities:
- [Feature 1 with benefit]
- [Feature 2 with benefit]
- [Feature 3 with benefit]

Product roadmap: [Next major feature coming Q[X]]
```

**Design Recommendations:**
- Actual product screenshots (not mockups)
- Annotate key features on screenshot
- Show real customer data (anonymized)
- Clean, intuitive UI is a selling point

### Slide 7: Traction
```markdown
# Traction

[Large chart showing growth curve up and to the right]

**Key Metrics:**
- **Revenue:** $[X]K MRR → $[Y]K MRR (+[Z]% in [N] months)
- **Customers:** [X] → [Y] (+[Z]%)
- **Retention:** [X]% monthly retention
- **NRR:** [X]% (net revenue retention)

Notable customers: [Logos or names]
```

**Design Recommendations:**
- Large, impressive growth chart
- Callout boxes for key numbers
- Customer logos (if recognizable)
- Green/upward colors
- Trend lines, not just bar charts

### Slide 8: Business Model
```markdown
# Business Model

**Revenue Model:** [SaaS subscription / Marketplace take rate / Transaction fee]

**Pricing:**
- Starter: $[X]/month
- Professional: $[Y]/month
- Enterprise: $[Z]/month

**Unit Economics:**
- LTV: $[X]
- CAC: $[Y]
- LTV:CAC = [Z]:1
- Payback: [N] months
- Gross Margin: [X]%

Path to profitability: [Brief statement]
```

**Design Recommendations:**
- Pricing tiers in table format
- Unit economics as simple formulas
- Break-even analysis chart
- Icons for different plan types

### Slide 9: Competition & Differentiation
```markdown
# Competition

[2x2 positioning matrix or comparison table]

**Quadrant 1:** [Competitor A] - [Their weakness]
**Quadrant 2:** [Competitor B] - [Their weakness]
**Quadrant 3:** [Our position] - [Our strength]

**Why we win:**
1. [Unique advantage 1]
2. [Unique advantage 2]
3. [Unique advantage 3]

"Before [Company], you had to choose between [A] or [B]. Now you get both."
```

**Design Recommendations:**
- Positioning map with clear axes
- Your company highlighted/circled
- Checkmarks vs. X's in comparison table
- Logos of competitors for recognition

### Slide 10: Team
```markdown
# Team

**[Founder 1 Name], CEO**
- Previously: [Relevant experience]
- Built/scaled [notable achievement]
- [Relevant domain expertise]

**[Founder 2 Name], CTO**
- Previously: [Tech experience]
- Built systems at [recognizable company]
- [Relevant technical expertise]

**Advisors & Board:**
- [Advisor 1]: [Credentials]
- [Advisor 2]: [Credentials]

**Key Hires Planned:** VP Sales, VP Eng (+$[X]K of this raise)
```

**Design Recommendations:**
- Professional headshots
- Logo of previous companies
- Brief bullets (not paragraphs)
- Highlight relevant expertise only

### Slide 11: Financial Projections
```markdown
# Financial Projections

[Chart showing revenue growth over 3-5 years]

|          | Year 1 | Year 2 | Year 3 |
|----------|--------|--------|--------|
| Revenue  | $[X]M  | $[Y]M  | $[Z]M  |
| Customers| [A]    | [B]    | [C]    |
| Team     | [D]    | [E]    | [F]    |

**Key Assumptions:**
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]
```

**Design Recommendations:**
- Hockey stick growth chart
- Conservative/realistic/aggressive scenarios
- Highlight key assumptions
- Show path to profitability or next round

### Slide 12: The Ask
```markdown
# The Ask

**Raising:** $[X]M [Stage] Round

**Use of Funds:**
- Engineering & Product: $[X]M ([Y]%)
- Sales & Marketing: $[X]M ([Y]%)
- Team & Hiring: $[X]M ([Y]%)
- Operations: $[X]M ([Y]%)

**Milestones (18 months):**
- Reach $[X]M ARR
- Grow team to [Y] people
- Expand to [new market/product]
- Achieve [key metric goal]

**Timeline:** Closing round in [X] weeks
```

**Design Recommendations:**
- Pie chart for use of funds
- Timeline graphic for milestones
- Clear, confident ask
- Urgency without desperation

### Appendix Slides (For Q&A)

Additional slides for common questions:

- Detailed financials
- Technology architecture
- Go-to-market plan details
- Customer case studies
- Detailed competitive analysis
- Regulatory/legal considerations
- International expansion plans

## Output Formats

### 1. Markdown Version
```markdown
Complete deck in markdown format with:
- All slide content
- Talking points
- Design recommendations
- Data visualization suggestions
```

### 2. Google Slides Import Format
```
Slide-by-slide content ready to copy into Google Slides:
- Headline text
- Body bullets
- Chart data
- Image suggestions
```

### 3. Email Pitch Version
```
Condensed 1-page pitch for email outreach:
- Problem + Solution (2 sentences)
- Traction (key metrics)
- Market (TAM + growth)
- Team (why you'll win)
- Ask (amount and timeline)
```

### 4. Talking Points Document
```
Script for presenting each slide:
- Opening hook
- Key points to emphasize
- Anticipated questions
- Transition to next slide
```

## Best Practices Included

The generator follows these proven principles:

1. **Tell a Story**
   - Clear narrative arc: problem → solution → traction → opportunity
   - Emotional connection to problem
   - Vision for future

2. **Show, Don't Tell**
   - Product screenshots over descriptions
   - Growth charts over statements
   - Customer logos over claims

3. **Quantify Everything**
   - Market size with sources
   - Growth rates (%, not just numbers)
   - Customer ROI with examples
   - Unit economics with formulas

4. **Keep It Simple**
   - One idea per slide
   - Minimal text (use images)
   - Consistent design throughout
   - Easy to read from distance

5. **Build Credibility**
   - Customer testimonials
   - Brand logos
   - Founder expertise
   - Advisor credentials
   - Data sources cited

6. **Create Urgency**
   - Why now timing
   - Competitive pressure
   - Market opportunity window
   - Fundraising timeline

## Customization Options

Tailor the deck to specific investors:

**For Sequoia:**
- Emphasis on huge market and category creation
- Strong unit economics
- Exceptional founders
- Path to market leadership

**For a16z:**
- Technical innovation and moats
- Network effects
- Product vision
- Cultural impact

**For Benchmark:**
- Capital efficiency
- Product-market fit evidence
- Sustainable business model
- Founder ownership and control

**For Tiger Global / Coatue (Growth Stage):**
- Revenue growth rate
- Market opportunity at scale
- Competitive positioning
- Path to IPO or strategic exit

## Integration with Other Tools

Works seamlessly with:
- `/startup-init` - Uses data from initialization
- `@fundraising-expert` - Get feedback on content
- `venture-capital-fundraising` skill - Reference best practices
- Financial model templates - Import projections

## Example Workflow

```bash
# 1. Generate initial deck
/pitch-deck-generator --stage=series-a

# 2. Review with fundraising expert
@fundraising-expert review my pitch deck and suggest improvements

# 3. Customize for specific investor
/pitch-deck-generator --target=sequoia --update

# 4. Create email version for outreach
/pitch-deck-generator --format=email-pitch

# 5. Practice with CEO agent
@startup-founder-ceo help me practice my pitch and anticipate questions
```

## Tips for Success

**Before Generating:**
- Have your metrics ready and accurate
- Know your unit economics
- Research your target investors
- Prepare customer testimonials

**After Generating:**
- Customize slide design (use tools like Pitch, Beautiful.ai, or Figma)
- Add high-quality product screenshots
- Include real customer logos (with permission)
- Practice your presentation multiple times

**When Presenting:**
- Stay under 20 minutes
- Skip slides if running long (use appendix)
- Make eye contact, not reading slides
- Tell stories, not just facts
- End with clear ask and next steps

---

**Ready to create your pitch deck?** Run `/pitch-deck-generator` to get started.
