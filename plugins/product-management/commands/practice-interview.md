---
name: practice-interview
description: Conduct a mock product management interview with real-time feedback. Choose interview type (product design, metrics, behavioral, technical) and company focus (Google, AWS, Microsoft, OpenAI, Anthropic).
---

# Practice Interview Command

Interactive mock interview for Product Manager, Senior PM, Head of Product, and CPO roles.

## Usage

```
/practice-interview [type] [company] [difficulty]
```

**Parameters:**
- `type`: product-design | metrics | behavioral | technical | full-loop
- `company` (optional): google | aws | microsoft | openai | anthropic | generic
- `difficulty` (optional): junior | mid | senior | executive

**Examples:**
```
/practice-interview product-design google senior
/practice-interview metrics aws senior
/practice-interview behavioral amazon senior
/practice-interview technical openai mid
/practice-interview full-loop anthropic executive
```

---

## How This Works

When you run this command, the interview coach will:

1. **Ask you an interview question** appropriate for the type, company, and level
2. **Let you answer** (you can think out loud, ask clarifying questions)
3. **Provide real-time guidance** if you get stuck (optional)
4. **Give detailed feedback** after you finish:
   - What went well
   - What could be improved
   - Specific suggestions
   - Rating (Strong Hire / Hire / Lean Hire / Lean No Hire / No Hire)

---

## Interview Types

### Product Design

**Format**: 35-45 minutes
**Framework**: CIRCLES (Comprehend, Identify, Report, Cut, List, Evaluate, Summarize)

**What's Evaluated:**
- Structured thinking
- User-centric approach
- Creativity and innovation
- Prioritization skills
- Trade-off evaluation
- Communication clarity

**Example Questions:**
- "Design a product for blind users"
- "Improve Instagram for content creators"
- "Design a fitness app for busy professionals"
- "Create a product to reduce food waste"

**Company-Specific Examples:**
- **Google**: "Improve Google Maps for tourists"
- **Amazon**: "Design a new AWS service for startups"
- **Microsoft**: "Design a Teams feature for remote education"
- **OpenAI**: "Design an AI product for legal research using GPT-4"
- **Anthropic**: "Design a feature to make Claude more interpretable"

---

### Metrics & Analytics

**Format**: 35-45 minutes
**Framework**: GAME (Goals, Actions, Metrics, Evaluation)

**What's Evaluated:**
- Metric selection (North Star)
- Funnel thinking (AARRR)
- Counter-metrics awareness
- A/B testing methodology
- Diagnostic reasoning
- Data-driven mindset

**Example Questions:**
- "How would you measure success for Instagram Reels?"
- "YouTube watch time is down 5%. Root cause?"
- "What metrics matter for Slack?"
- "TikTok engagement dropped 10%. Diagnose and fix."

**Company-Specific Examples:**
- **Google**: "How would you measure success for Bard AI?"
- **Amazon**: "Prime Video watch time is declining. Investigate."
- **Microsoft**: "How would you measure success for Copilot?"
- **OpenAI**: "How would you measure success for ChatGPT Enterprise?"
- **Anthropic**: "How would you measure Claude's safety over time?"

---

### Behavioral

**Format**: 45-60 minutes (5-7 questions)
**Framework**: STAR (Situation, Task, Action, Result)

**What's Evaluated:**
- Past experience and impact
- Leadership and influence
- Problem-solving approach
- Cultural alignment
- Self-awareness and learning

**Categories:**
- **Leadership**: "Tell me about a time you led a cross-functional team"
- **Conflict**: "Describe a time you disagreed with your manager"
- **Failure**: "Tell me about a product that failed. What did you learn?"
- **Innovation**: "Tell me about the most innovative product you've built"
- **Customer Focus**: "Tell me about a time you advocated for customers"
- **Execution**: "Tell me about a time you shipped under tight deadlines"

**Company-Specific:**
- **Google**: Focus on Googleyness (collaboration, humility, learning)
- **Amazon**: Cover all 14 Leadership Principles
- **Microsoft**: Emphasize growth mindset, empathy
- **OpenAI**: Demonstrate AI safety awareness, mission alignment
- **Anthropic**: Show responsible AI thinking, long-term perspective

---

### Technical

**Format**: 45-60 minutes
**Framework**: System Design (Requirements → Estimation → API → Architecture → Trade-offs)

**What's Evaluated:**
- Technical depth
- System design thinking
- Scalability understanding
- API design knowledge
- Trade-off evaluation
- Communication with engineers

**Example Questions:**
- "Design the backend for Twitter"
- "Design Instagram's photo storage system"
- "Design Uber's dispatch system"
- "Design Zoom's video conferencing system"
- "Design a recommendation system for e-commerce"

**Company-Specific:**
- **Google**: Design at 1B+ user scale, global infrastructure
- **Amazon**: Design AWS service, focus on reliability and scalability
- **Microsoft**: Design enterprise system, hybrid cloud
- **OpenAI**: Design API for AI model inference, rate limiting, safety
- **Anthropic**: Design system for LLM with 200K context, safety monitoring

---

### Full Loop

**Format**: 3-4 hours (multiple rounds)
**Structure**: Simulates real interview loop at target company

**Google Loop:**
1. Product Design (45 min)
2. Analytical (45 min)
3. Technical (45 min)
4. Googleyness/Leadership (45 min)
5. Hiring Committee (feedback session)

**Amazon Loop:**
1. Leadership Principles #1 (45 min)
2. Leadership Principles #2 (45 min)
3. Product Case Study (45 min)
4. Bar Raiser (45 min)
5. Debrief (feedback session)

**Microsoft Loop:**
1. Product Design & Strategy (60 min)
2. Technical & Architecture (60 min)
3. Leadership & Collaboration (60 min)
4. As-Appropriate (AA) (45 min)

**OpenAI Loop:**
1. AI Product Design (60 min)
2. Technical (ML/API systems) (60 min)
3. Strategy & Market (45 min)
4. Mission & Values (45 min)

**Anthropic Loop:**
1. AI Product Design (60 min)
2. Technical (LLMs, safety) (60 min)
3. Research Collaboration (45 min)
4. Responsible AI & Strategy (45 min)

---

## Difficulty Levels

### Junior (PM, 0-3 years)

**Product Design:**
- Simpler products (single feature, consumer-focused)
- Less emphasis on business model
- Focus on user empathy and structured thinking

**Metrics:**
- Basic funnel metrics (acquisition, activation, retention)
- Simple A/B test design
- Common metrics (DAU, conversion rate)

**Behavioral:**
- Execution-focused stories
- Working with teams
- Learning and growth

### Mid-Level (Senior PM, 3-6 years)

**Product Design:**
- More complex products (multi-sided, platform, B2B)
- Business model and go-to-market
- Technical depth and scalability

**Metrics:**
- North Star Metric definition
- Complex funnels and counter-metrics
- Segmentation analysis
- Advanced A/B testing

**Behavioral:**
- Leadership and influence
- Strategic decisions
- Cross-functional impact
- Handling ambiguity

### Senior (Principal PM, Director, 6-10 years)

**Product Design:**
- Strategic products (new market entry, platform play)
- Ecosystem thinking
- Competitive differentiation
- Long-term vision (3-5 years)

**Metrics:**
- Business metrics (LTV, CAC, unit economics)
- Portfolio metrics (multiple products)
- Strategic trade-offs
- Market sizing and TAM

**Behavioral:**
- Building teams and organizations
- Company-level strategy
- Influencing executives
- Organizational change

### Executive (VP, CPO, 10+ years)

**Product Design:**
- Company-level strategy
- Market creation
- Portfolio management
- M&A and build vs buy

**Metrics:**
- Board-level metrics
- Company OKRs
- Multi-year trends
- Market share and competitive dynamics

**Behavioral:**
- Building product culture
- Organizational transformation
- Board and investor communication
- Industry leadership

---

## How to Get the Most from This

### Before the Interview

1. **Choose appropriate type and difficulty** for where you are in prep
2. **Set aside uninterrupted time** (don't rush)
3. **Have pen and paper** ready (for notes, diagrams)
4. **Get into "interview mode"** (formal, focused)

### During the Interview

1. **Ask clarifying questions** (shows thoughtfulness)
2. **Think out loud** (shows your reasoning process)
3. **Use frameworks** (CIRCLES, GAME, STAR)
4. **Be specific** (numbers, names, concrete examples)
5. **Ask for hints** if truly stuck (better than silence)

### After the Interview

1. **Review feedback carefully** (take notes)
2. **Identify 1-2 areas to improve** (focus on highest impact)
3. **Practice those areas** before next mock
4. **Don't be discouraged** by "No Hire" - it's practice!
5. **Track progress** (keep a log of mocks and ratings)

---

## Feedback Components

After your answer, you'll receive:

### 1. Rating

- **Strong Hire**: Exceptional answer, would definitely hire
- **Hire**: Good answer, would hire
- **Lean Hire**: Okay answer, borderline hire
- **Lean No Hire**: Weak answer, borderline no hire
- **No Hire**: Poor answer, would not hire

### 2. What Went Well

- Specific strengths demonstrated
- Good use of frameworks
- Strong communication
- Impressive depth or insights

### 3. What Could Be Improved

- Gaps in answer
- Missing frameworks or structure
- Areas lacking depth
- Communication issues

### 4. Specific Suggestions

- Exactly what to practice
- How to improve weak areas
- Resources to study
- Sample better answers

### 5. Company-Specific Feedback

- How well you aligned with company culture
- Specific values demonstrated (or missing)
- Cultural fit assessment

---

## Example Session

**User:**
```
/practice-interview product-design google senior
```

**Interview Coach:**

Great! I'll conduct a Google-style product design interview at the Senior PM (L6) level. This will be a 45-minute interview.

---

**Question:**

"Google wants to help small brick-and-mortar businesses compete with Amazon and other e-commerce giants. Design a product to help these small businesses thrive in the digital economy."

**Take your time to:**
1. Ask clarifying questions (3-5 questions)
2. Structure your answer using CIRCLES
3. Think out loud so I can see your reasoning

When you're ready, please start by asking clarifying questions.

---

**[User provides answer using CIRCLES method]**

---

**Interview Coach - Feedback:**

Thank you for your answer! Let me provide comprehensive feedback.

**Rating: HIRE**

### What Went Well

1. **Strong Structure**: You used CIRCLES clearly, which made your answer easy to follow. You signposted each section ("First, let me clarify...", "Now, let me identify users...", "For solutions, I'm considering 3 options...").

2. **Excellent Clarifying Questions**: Your questions were thoughtful and relevant:
   - "Should I focus on helping them get online, or assume they already have basic web presence?"
   - "Are we thinking about retail stores, restaurants, services, or all of the above?"
   - "Is this a free tool for businesses or a paid product?"

3. **User Empathy**: You clearly understood the pain points of small business owners (limited tech skills, tight budgets, competing with Amazon's convenience).

4. **Multiple Solutions**: You brainstormed 4 different solutions (Google-powered e-commerce template, local delivery network, smart inventory management, online-to-offline customer engagement), showing creativity.

5. **Quantified Success Metrics**: You defined clear metrics (adoption rate, GMV from small businesses, customer satisfaction) and explained how you'd measure them.

### What Could Be Improved

1. **Deeper Business Model**: You mentioned this would be freemium, but didn't fully explore the revenue model. For a L6 interview, I'd expect you to discuss:
   - How Google makes money (ads? transaction fees? subscription?)
   - Unit economics (CAC vs LTV for small businesses)
   - Why this is strategic for Google (beyond "helping small businesses")

2. **Competitive Analysis**: You didn't mention competitors (Shopify, Square, Wix). At Senior PM level, Google wants to see awareness of the market and differentiation strategy.

3. **Go-to-Market**: You defined the product well, but didn't explain how small businesses would discover and adopt it. How do you get from 0 to 10,000 businesses using it?

4. **Technical Depth**: You could have discussed integration challenges:
   - How does this integrate with Google My Business, Maps, Search?
   - What's the data model (inventory, orders, customers)?
   - How do we handle payments and compliance?

5. **10x Thinking**: Your solution was solid but incremental. Google loves "10x thinking" - what would a 10x better solution look like? (e.g., "AI assistant that runs the entire online business for you")

### Specific Suggestions

1. **Practice business model thinking**: For every product you design, ask:
   - How does the company make money?
   - Why is this strategic (beyond user value)?
   - What's the economic model (unit economics, margins)?

2. **Add competitive analysis**: Always mention 2-3 competitors and how your product differentiates. Structure:
   - "Shopify does X well, but we can differentiate by..."

3. **Think about distribution**: Add a "Go-to-Market" step after CIRCLES:
   - How do you get first 100 customers?
   - How do you scale to 10K, 100K?
   - What's the acquisition strategy?

4. **Show 10x ambition**: After proposing your solution, add:
   - "If we think 10x bigger, we could [ambitious vision]"
   - Shows you can think beyond incremental improvements

### Google-Specific Feedback

**Cultural Fit: GOOD**

- ✅ User-first thinking (you started with small business pain points)
- ✅ Data-driven (you defined metrics and A/B testing approach)
- ✅ Collaboration (you mentioned working with Google My Business, Maps teams)
- ✅ Structured thinking (clear CIRCLES framework)

- ⚠️ 10x thinking: Could be stronger (solution was solid but not "moonshot")
- ⚠️ Global scale: Didn't discuss international expansion (Google thinks globally)

**Would you pass this round at Google?**

Yes, likely. This is a solid "Hire" - you demonstrated strong PM fundamentals, clear communication, and good structure. The areas for improvement wouldn't disqualify you, but addressing them would move you to "Strong Hire" territory.

**Next Interview Round: Technical**

You'd likely move forward to a technical round where they'd ask about system design or architecture for your proposed solution.

---

### Practice Recommendations

Before your next mock:

1. **Do 5 more product design questions**, focusing on:
   - Business model (how does company make money?)
   - Competitive differentiation
   - Go-to-market strategy

2. **Study Google's business model**:
   - How do Google Maps, Search, YouTube, Cloud make money?
   - Apply similar thinking to your product designs

3. **Practice "10x thinking"**:
   - For any product, ask: "What's the moonshot version of this?"
   - Read about Google X, Project Loon, Waymo (moonshot examples)

4. **Read case studies**:
   - How Shopify grew from 0 to 1M merchants
   - How Square disrupted payments
   - How Google My Business helps local businesses

**Great job overall! You're well on your way to interview success. Keep practicing! 🚀**

---

## Frequently Asked Questions

### How many practice interviews should I do?

**Minimum**: 5 full mocks (1 of each type)
**Recommended**: 10-15 mocks (2-3 of each type)
**Optimal**: 20+ mocks (especially before senior/executive roles)

**Rule of thumb**: You should do at least 2 mocks where you get "Strong Hire" or "Hire" rating consistently before feeling ready for real interviews.

### Can I request specific companies or questions?

Yes! Use the command parameters:

```
/practice-interview product-design openai senior
/practice-interview behavioral amazon executive
```

Or specify in your message:
"Can you give me an Amazon-style behavioral question focused on Customer Obsession?"

### How realistic are these mocks?

Very realistic. The interview coach is trained on:
- Real interview questions from Google, Amazon, Microsoft, OpenAI, Anthropic
- Actual evaluation rubrics used by these companies
- Feedback from PMs who've interviewed at these companies
- Best practices from "Cracking the PM Interview" and other resources

### What if I get stuck during the interview?

You have options:

1. **Ask for a hint**: "I'm stuck on prioritization. Can you give me a hint?"
2. **Think out loud**: "Let me work through this... I'm considering X vs Y..."
3. **Skip and come back**: "Let me move on to solutions and come back to this"

Just like a real interview, asking for help is better than staying silent.

### Can I pause and resume later?

Yes, but it's better to do the full interview in one session (more realistic). If you need to pause:
- Note where you stopped
- Resume within the same day
- Try to maintain "interview mode"

### How long should I wait between practice interviews?

**Early in prep (Week 1-3)**: Daily or every other day
**Mid prep (Week 4-5)**: 2-3 times per week
**Late prep (Week 6)**: Once a week (avoid burnout)

**After each mock**: Give yourself time to study the feedback and practice weak areas before the next mock.

### What if I keep getting "No Hire"?

Don't be discouraged! This means:

1. **You're challenging yourself** (good!)
2. **You have clear areas to improve** (focus on feedback)
3. **You need more foundational work** (study frameworks more)

**Action plan if you're consistently getting "No Hire":**
- Step back and study frameworks (CIRCLES, GAME, STAR)
- Do 10-20 practice questions solo (without mocks)
- Watch YouTube videos of great PM interviews
- Read "Cracking the PM Interview" chapters
- Return to mocks after 1-2 weeks of study

### Can I practice with a peer instead?

Yes! Peer practice is highly effective:

1. **Use this command as a template** (for question types, evaluation criteria)
2. **Take turns interviewing each other**
3. **Give each other honest feedback** using the rating system
4. **Compare notes** (what would the interview coach say?)

**Tip**: Do both peer practice AND AI coach practice. Peers help with human interaction, AI coach provides consistent, unbiased feedback.

---

## Ready to Practice?

Choose your interview type and difficulty:

```
/practice-interview [product-design|metrics|behavioral|technical|full-loop] [company] [difficulty]
```

**Recommended starting point for most candidates:**
```
/practice-interview product-design generic senior
```

**For company-specific prep:**
```
/practice-interview behavioral amazon senior
/practice-interview technical openai mid
/practice-interview full-loop google senior
```

Let's get you ready to land your dream product role! 🎯🚀
