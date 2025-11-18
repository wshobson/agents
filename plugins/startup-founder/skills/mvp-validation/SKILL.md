---
name: mvp-validation
description: Framework for building, launching, and validating Minimum Viable Products including defining scope, measuring success, and iterating based on feedback. Use when building or validating your first product version.
---

# MVP Validation

## When to Use This Skill

- Defining the scope of your Minimum Viable Product
- Building your first product version quickly
- Launching and getting initial user feedback
- Measuring early traction and validation
- Deciding what to build next based on data
- Determining if you should pivot or persevere

## Core Concepts

### What is an MVP?

**Eric Ries Definition:**
"The MVP is that version of a new product which allows a team to collect the maximum amount of validated learning about customers with the least effort."

**Key Principles:**
- **Minimum**: Smallest feature set to test hypothesis
- **Viable**: Good enough that people will use it
- **Product**: Delivers core value, not just a mockup

**MVP is NOT:**
- A beta version with all features
- A buggy, unusable product
- Just a landing page (that's a smoke test)
- An excuse for poor quality

**MVP IS:**
- Focused on one core use case
- Good enough to charge for (if B2B/SaaS)
- Testable with real users
- Fast to build (weeks, not months)

### The MVP Spectrum

```
Lower Fidelity ←→ Higher Fidelity

1. Problem Interview
   - Talk to customers about problem
   - No product needed
   - Validates problem exists

2. Landing Page / Smoke Test
   - Value proposition + email signup
   - Measures interest
   - Validates demand

3. Concierge MVP
   - Manually deliver service
   - No automation or software
   - Validates willingness to pay

4. Wizard of Oz MVP
   - Looks automated, actually manual
   - Frontend exists, backend is human
   - Validates user experience

5. Single-Feature MVP
   - Working product, one main feature
   - Automated core workflow
   - Validates product-solution fit

6. Feature-Complete MVP
   - Multiple features integrated
   - Self-service experience
   - Validates product-market fit
```

### Choosing the Right MVP Type

**For B2B SaaS:**
- Start: Concierge or Wizard of Oz
- Then: Single-feature MVP with manual onboarding
- Goal: 10-20 paying customers

**For Consumer Apps:**
- Start: Landing page + prototype
- Then: Single-feature MVP with core loop
- Goal: 1,000+ active users

**For Marketplace:**
- Start: Single-sided, curated supply
- Then: Two-sided with limited matching
- Goal: 50+ transactions

**For Hardware:**
- Start: 3D renders + pre-orders
- Then: Prototype + small batch
- Goal: 100+ pre-orders at full price

## Defining MVP Scope

### The Core Value Hypothesis

**Template:**
"We believe that [target customer] has a problem with [problem]. We can solve this with [solution] and they will use it because [key benefit]."

**Example (Uber):**
"We believe that professionals in San Francisco have a problem with unreliable, expensive taxis. We can solve this with an app that connects them to black car drivers and they will use it because it's convenient, trackable, and cashless."

### Feature Prioritization Framework

**Must Have (Core Value):**
- Features required to deliver core value
- Without these, product is useless
- Example (Uber): Request ride, see car location, pay in app

**Should Have (Important but not critical):**
- Enhance experience but not core to value
- Can be manual or come in V2
- Example (Uber): Ride history, favorites, split payment

**Could Have (Nice to have):**
- Would improve product but low priority
- Delay until after validation
- Example (Uber): Music control, luxury cars, scheduled rides

**Won't Have (Not now):**
- Out of scope for MVP
- Future vision but not now
- Example (Uber): Food delivery, freight, flying cars

### The One-Feature Rule

**Pick ONE problem to solve extremely well**

Poor MVP: "Calendar app with scheduling, video calls, task management, CRM, and email"

Strong MVP: "One-click scheduling links that eliminate email back-and-forth" (Calendly)

**How to Choose the One Feature:**
1. What's the most painful problem for customers?
2. What delivers value fastest?
3. What's technically feasible in 4-8 weeks?
4. What creates most "wow" moment?
5. What can you defend/improve over time?

## Building Your MVP

### The 8-Week MVP Timeline

**Week 1: Scope and Design**
- Finalize feature list
- Create user flow diagrams
- Design key screens (wireframes)
- Define success metrics
- Set up development environment

**Week 2-5: Core Development**
- Build authentication (use Auth0, Firebase, etc.)
- Implement core feature
- Create basic UI (use component libraries)
- Set up database
- Focus on happy path only

**Week 6: Polish and Testing**
- Fix critical bugs
- Improve UX for core flow
- Add basic error handling
- Internal testing
- Get feedback from 5 friendly users

**Week 7: Beta Launch**
- Deploy to production
- Invite first 10-20 users
- Monitor closely for issues
- Gather feedback actively
- Fix showstopper bugs

**Week 8: Iterate**
- Analyze usage data
- Implement top improvements
- Prepare for wider launch
- Document learnings

### MVP Build Principles

**1. Use Existing Tools and Platforms**
- Don't build authentication (Auth0, Firebase, Clerk)
- Don't build payment processing (Stripe, PayPal)
- Don't build email service (SendGrid, Mailgun)
- Don't build analytics (Mixpanel, Amplitude)

**2. Choose Fast Development Tools**
- Web apps: Next.js, Vercel, Supabase
- Mobile: React Native, Expo
- No-code: Webflow, Bubble, Airtable
- Backend: Firebase, Supabase, Railway

**3. Ruthlessly Cut Scope**
- No admin dashboards (use database tools)
- No advanced permissions
- No edge cases initially
- No perfect design (use Tailwind CSS)

**4. Manual Before Automated**
- Manual onboarding vs. self-service
- Manual matching vs. algorithms
- Manual customer support (email, not chat widget)
- Manual payment collection if needed

**5. Build for 10 Users, Not 10,000**
- Don't worry about scale
- Don't optimize performance
- Don't build for edge cases
- Do make it work reliably for early users

### No-Code / Low-Code MVPs

**When to Use No-Code:**
- Non-technical founder
- Simple workflows
- Speed is critical
- Budget constrained

**Popular No-Code Stacks:**

**Landing Pages:**
- Webflow, Carrd, Typedream
- Framer (with CMS)

**Web Apps:**
- Bubble (full applications)
- Softr (built on Airtable)
- Glide (mobile apps from spreadsheets)

**Automation:**
- Zapier, Make (connecting tools)
- Airtable (database + simple UI)

**Marketplaces:**
- Sharetribe, Arcadier
- Webflow + Airtable + Zapier

**Example No-Code MVP (Job Board):**
```
Stack:
- Airtable: Store jobs and applications
- Softr: Create public job board UI
- Stripe: Payment for job postings
- Zapier: Email notifications
- Google Forms: Job submission

Time: 1-2 weeks
Cost: $50-100/month
```

## Launching Your MVP

### Pre-Launch Checklist

**Product:**
✓ Core feature works reliably
✓ Basic error handling in place
✓ Mobile-responsive (if web)
✓ Fast load times (<3 seconds)
✓ Works in major browsers
✓ Analytics tracking set up

**Content:**
✓ Clear value proposition on homepage
✓ Simple onboarding flow
✓ Help documentation (basic)
✓ Contact method (email at minimum)
✓ Privacy policy and terms

**Technical:**
✓ SSL certificate installed
✓ Domain name purchased
✓ Error monitoring (Sentry, Bugsnag)
✓ Backup system in place
✓ Can handle 100 concurrent users

**Go-to-Market:**
✓ Launch post written
✓ Target communities identified
✓ Email list ready (if any)
✓ Social media accounts created
✓ Press list prepared (if applicable)

### Launch Strategy

**Phase 1: Friends and Family (Week 1)**
- 10-20 people you know
- Ask for brutal honesty
- Watch them use it (if possible)
- Fix critical issues

**Phase 2: Expanded Beta (Week 2-3)**
- 50-100 early adopters
- Post in relevant communities
- Personally onboard each user
- Weekly feedback calls

**Phase 3: Public Launch (Week 4)**
- Product Hunt launch
- Post in relevant subreddits
- Tweet and LinkedIn post
- Email any press contacts
- Reach 500-1000 users

**Phase 4: Iteration (Ongoing)**
- Analyze usage patterns
- Implement top requests
- Improve retention
- Scale what's working

### Launch Channels for MVPs

**Organic/Free:**
- Product Hunt
- Hacker News (if technical product)
- Reddit (find relevant subreddits)
- LinkedIn (personal posts, not ads)
- Twitter (share your story)
- Facebook groups
- Slack communities
- IndieHackers

**Low-Cost Paid ($500-1000):**
- Google Ads (search intent)
- Facebook/Instagram ads
- LinkedIn ads (B2B)
- Reddit ads (if niche subreddit)

**Personal Outreach:**
- Email to network
- Direct messages on social
- Ask existing users for referrals
- Attend relevant meetups/events

**Content Marketing:**
- Blog posts solving related problems
- YouTube tutorials
- Guest posts on relevant sites
- Podcast interviews

## Measuring MVP Success

### Key Metrics to Track

**Acquisition Metrics:**
- Visitors to landing page
- Signup conversion rate (target: 2-5%)
- Traffic sources
- Cost per signup (if using paid)

**Activation Metrics:**
- % who complete core action (target: 40%+)
- Time to first value (target: <24 hours)
- Onboarding completion rate
- Setup abandonment points

**Engagement Metrics:**
- Daily/Weekly/Monthly active users
- Session frequency
- Session duration
- Feature usage rates
- Core action repetition

**Retention Metrics:**
- Day 1, Day 7, Day 30 retention
- Cohort retention curves
- Churn rate
- Power user percentage (use 3+ times/week)

**Revenue Metrics (if monetizing):**
- Trial-to-paid conversion (target: 20-40%)
- Average revenue per user (ARPU)
- Monthly recurring revenue (MRR)
- Customer acquisition cost (CAC)

**Qualitative Metrics:**
- Sean Ellis score (% "very disappointed" without product)
- Net Promoter Score (NPS)
- Customer testimonials
- Feature requests (what they want)

### Success Thresholds

**For B2B SaaS MVP:**
✓ 10+ paying customers
✓ $5K+ MRR
✓ 80%+ month 2 retention
✓ 40%+ would be "very disappointed" without it
✓ <3 month sales cycle

**For Consumer App MVP:**
✓ 1,000+ weekly active users
✓ 40%+ Day 7 retention
✓ 30%+ DAU/MAU ratio
✓ Organic growth (10%+ weekly without paid)
✓ NPS >50

**For Marketplace MVP:**
✓ 50+ completed transactions
✓ 20+ active supply (sellers/hosts)
✓ 50+ active demand (buyers/guests)
✓ 30%+ repeat transaction rate
✓ 4+ star average rating

### Red Flags (Time to Pivot)

**Usage Red Flags:**
❌ <20% activation rate (most don't use core feature)
❌ Retention curve never flattens (linear decline)
❌ Low session frequency (<1x per week for weekly product)
❌ No organic growth (100% paid acquisition)
❌ High uninstall rate (>50% within week 1)

**Feedback Red Flags:**
❌ "This is nice but..." (not must-have)
❌ Can't get anyone to pay
❌ Users ask for completely different product
❌ Complaints about core feature (not bugs)
❌ No passionate users (all lukewarm)

**Market Red Flags:**
❌ Takes >6 months to get first 10 customers
❌ Can't find more similar customers
❌ Sales cycle is >12 months
❌ Churning as fast as acquiring
❌ Unit economics don't work ($100 CAC, $50 LTV)

## Feedback and Iteration

### Collecting Feedback

**In-App Surveys:**
- After core action: "How was that experience?"
- After first week: Sean Ellis test
- Weekly: NPS survey
- On churn: Exit survey

**User Interviews:**
- Schedule with power users (weekly)
- Talk to churned users (understand why)
- Watch users use product (usability testing)
- Ask about workflow and pain points

**Support Channels:**
- Email (personal response from founder)
- In-app chat (Intercom, Drift)
- Twitter/social media mentions
- Feature request board (Canny, Productboard)

**Analytics:**
- Where do users drop off?
- Which features are unused?
- What's the common path to value?
- How do power users differ from churned users?

### The Build-Measure-Learn Loop

**1. Build (1-2 weeks)**
```
Based on hypothesis:
"We believe adding [feature] will increase [metric] by [X]"

Example:
"We believe adding email reminders will increase Day 7 retention from 40% to 55%"

Build:
- Smallest version to test
- Ship to subset of users (A/B test)
- Instrument with analytics
```

**2. Measure (1 week)**
```
Collect data:
- Quantitative: Does metric improve?
- Qualitative: Do users mention it positively?
- Usage: Are they using the feature?

Example:
- Day 7 retention: 42% (no change)
- Only 10% opened reminder emails
- Users say emails are "annoying"
```

**3. Learn (1 week)**
```
Analyze results:
- Was hypothesis correct?
- Why or why not?
- What did we learn?
- What should we test next?

Example:
- Hypothesis was wrong
- Email reminders don't help retention
- Real issue: Users forget what value they got
- Next test: Improve initial "aha moment"
```

**4. Repeat**

### Prioritizing Improvements

**The RICE Framework:**

For each potential improvement, score:
- **Reach**: How many users impacted per quarter?
- **Impact**: How much impact per user? (0.25 = low, 3 = massive)
- **Confidence**: How confident in estimates? (50% = low, 100% = high)
- **Effort**: Person-weeks required?

**Score = (Reach × Impact × Confidence) / Effort**

**Example:**

```
Feature 1: Better onboarding
- Reach: 1000 new users/quarter
- Impact: 2 (major improvement)
- Confidence: 80%
- Effort: 2 weeks
Score: (1000 × 2 × 0.8) / 2 = 800

Feature 2: Social sharing
- Reach: 500 users/quarter
- Impact: 1 (moderate)
- Confidence: 50%
- Effort: 3 weeks
Score: (500 × 1 × 0.5) / 3 = 83

Priority: Do Feature 1 first
```

## Common MVP Mistakes

### Mistake #1: Building Too Much
```
Problem: 6-12 months building "perfect" product
Impact: Miss market timing, run out of money, wrong features
Solution: Ship in 4-8 weeks, iterate based on real usage
```

### Mistake #2: Building Too Little
```
Problem: Product doesn't deliver core value
Impact: Users bounce, can't validate anything
Solution: Ensure MVP actually solves the problem
```

### Mistake #3: Not Talking to Users
```
Problem: Building in isolation, no feedback loop
Impact: Build wrong features, miss real problems
Solution: Talk to 5-10 users per week minimum
```

### Mistake #4: Ignoring Data
```
Problem: Building based on opinions, not evidence
Impact: Wasted effort on unused features
Solution: Track metrics, A/B test, follow data
```

### Mistake #5: Scaling Too Early
```
Problem: Marketing spend before product-market fit
Impact: Acquiring users who churn
Solution: Fix retention before growth
```

## From MVP to Product-Market Fit

### Transition Indicators

**You're Ready to Scale When:**
✓ Retention curves have flattened
✓ Users are passionate (40%+ "very disappointed")
✓ Word-of-mouth growth happening organically
✓ Unit economics work (LTV:CAC >3:1)
✓ You can articulate why product works
✓ Repeatable customer acquisition channel found

**What Changes in Scale Mode:**
- Focus shifts from product to distribution
- Hire specialists instead of generalists
- Build processes and systems
- Invest in growth channels
- Improve onboarding and activation
- Add features for expansion/retention

### MVP Evolution Path

```
Stage 1: MVP (months 0-3)
- Single feature, manual processes
- 10-100 users
- Founder does everything
- Validate core hypothesis

Stage 2: Enhanced Product (months 3-9)
- 3-5 core features
- 100-1,000 users
- Small team (3-5 people)
- Validate product-market fit

Stage 3: Growth Product (months 9-18)
- Full feature set for core use case
- 1,000-10,000 users
- Team of 10-20
- Scale what works

Stage 4: Platform (18+ months)
- Multiple use cases / products
- 10,000+ users
- Team of 50+
- Market leadership
```

## References

See the `references/` directory for:
- MVP scope templates
- Launch checklists
- User interview scripts
- Metrics tracking spreadsheets
- A/B testing frameworks
- Feature prioritization tools
