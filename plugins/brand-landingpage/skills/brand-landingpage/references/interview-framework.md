# Brand Discovery Interview Framework

## Interview Philosophy

- Ask a maximum of 10 questions across all phases. Developers will lose patience faster than most -- they want to ship.
- The user is technically literate. You can say "CTA," "hex value," "HTML," or "deploy." What needs translating is design language: "visual hierarchy," "brand identity," "color temperature," "typographic contrast."
- If the user volunteers information unprompted (e.g., dumps a README or product description), extract answers from it and skip those questions.
- When the user seems uncertain about design preferences, offer 2-3 concrete examples to choose from rather than waiting for them to articulate from scratch.
- Treat the interview as a conversation, not a form. Acknowledge answers before moving on.
- One question at a time. Never stack multiple questions in a single message.
- Respect short answers. Developers tend to be terse. If the answer covers the question, move on.
- **The user will try to skip this.** They'll say "just generate something" or "here's my README, figure it out." Push back gently. The interview is the skill's primary value -- without it, you're producing a generic template they could get from any page builder.

---

## Phase A: Product & Purpose

**Goal:** Understand what the product does, who it's for, and what action the landing page should drive.

### Core Questions (ask in order, skip any already answered)

1. "What's your project called?"
   - Extract exact spelling, capitalization, and any tagline they mention.

2. "Give me the elevator pitch -- what does it do and why should someone care?"
   - If too technical: "Imagine explaining this to someone who might use it but isn't a developer. What problem does it solve for them?"
   - If overly broad: "If you had to pick the one thing that makes this worth checking out, what is it?"

3. "Who are your target users? Developers? Designers? Non-technical teams? Everyone?"
   - If they say "developers": "What kind -- frontend, backend, DevOps, data? What stack or ecosystem?"
   - If they say "everyone": "Who's shown the most interest so far, or who would you pitch to first?"
   - If they have no users yet: "Who did you build this for originally? Whose problem were you solving?"

4. "What's the primary action you want a visitor to take? For example: sign up, start a free trial, join the waitlist, book a demo, star the repo, or try a live demo."
   - If they list multiple: "Which one matters most right now -- the one you'd put on the biggest button?"
   - Map their answer to button text internally (e.g., "try it out" --> "Try It Free").

### What to Extract From Phase A

| Field | Example |
|-------|---------|
| Project name (exact spelling) | "Railtrack" |
| Elevator pitch (1-2 sentences) | "Open-source deployment pipeline that catches breaking changes before they hit production" |
| Target users | "Backend engineers working with Kubernetes, mostly at mid-size companies" |
| Primary CTA | "Start free trial" --> button text "Start Free Trial" |
| Bonus (if volunteered) | Repo URL, existing docs, tech stack, pricing model |

### Transition Rule

Move to Phase B when you have: project name + elevator pitch + target users + primary CTA. These four are non-negotiable.

If the user tries to skip ahead ("just generate something, it's a CLI tool for managing databases"):
- Extract what you can from their statement.
- Ask only the essential gaps (CTA + brand feel at minimum -- 2 questions).
- Default everything else with reasonable choices and tell them what you defaulted: "I'm going with a clean, modern look with a dark theme since this is a dev tool. We can adjust after you see it."

---

## Phase B: Brand Feel

**Goal:** Understand the emotional impression the brand should make and whether it leans light or dark.

### Core Questions

1. "Pick 3 words that describe how your product should come across to visitors."
   - Offer a menu if they hesitate:
     > Some options: bold, clean, minimal, technical, friendly, trustworthy, modern, playful, fast, precise, approachable, sophisticated, sharp, innovative, reliable, developer-friendly, premium, fun, lightweight, serious
   - Accept any 3 words, even ones not on the list.
   - If they say "I don't know" or "I haven't thought about it": "Think about the products you respect most. When you land on Stripe's page, or Linear's, or Tailwind's -- what feeling do you get? What's the equivalent for your product?"

2. "Name a product or site whose landing page you admire. Doesn't have to be in your space."
   - If they name one: "What specifically do you like about it -- the colors, the layout, the overall vibe, the copy?"
   - If they can't think of one: skip and move on. Don't push.
   - Common developer references and what they imply:
     - Stripe: clean, premium, lots of whitespace, subtle gradients
     - Linear: dark, minimal, fast-feeling, sharp
     - Vercel: dark/light contrast, geometric, developer-focused
     - Tailwind: bright, colorful, friendly, well-structured
     - Supabase: dark, green accent, technical but approachable
     - Raycast: dark, polished, product-focused

3. "Light theme or dark theme?"
   - This maps directly to colorMode (LIGHT vs DARK).
   - Developers building dev tools tend toward dark. Products targeting non-technical users tend toward light. Note this to the user if they're unsure: "Dev tools usually go dark, consumer-facing products usually go light. What fits your audience?"

### Follow-Up Triggers

- **Contradictory adjectives** (e.g., "playful" + "serious"): "Interesting combination. If they conflict, which wins -- the approachable side or the authoritative side?"
- **All-technical** (e.g., "fast, reliable, scalable"): "Those describe the product. Now think about the page itself -- when someone sees it for the first time, what impression should it leave?"
- **"Just make it look professional"**: "Professional covers a lot of ground -- Stripe-professional or IBM-professional? Clean and spacious, or dense and information-rich?"

### Adjective Interpretation

Map the user's 3 adjectives to a Stitch `colorVariant` using the Color Variant Decision Tree in `references/stitch-architecture.md`. That file contains the full mapping table with rationale and example products.

### Transition Rule

Move to Phase C when you have: 3 brand adjectives + light/dark direction.
The reference product is a bonus signal, not a blocker.

---

## Phase C: Visual Preferences

**Goal:** Determine color, font feel, and shape direction for the design system.

### Core Questions

1. Color direction:
   - "Do you have existing brand colors -- maybe from your app's UI, your docs site, or your repo?"
   - If yes with a hex, Tailwind class, or CSS variable: use it directly.
   - If yes with a name ("indigo," "the GitHub green"): translate to hex.
   - If no: "What color comes to mind for your product? Or think about what feeling you want -- trust (blues), energy (oranges/reds), growth (greens), creativity (purples)."

2. Font feel:
   - "For the landing page text, do you prefer something clean and geometric (like Inter or DM Sans), or something with more character and weight (like a serif)?"
   - If they say "monospace" or reference a code font: "Monospace works in code, but on a marketing page it can feel cold. I'd recommend a clean sans-serif that has a similar technical feel -- like Space Grotesk or Geist. You good with that?"

3. Shape direction:
   - "Sharp corners or rounded? Think about the buttons in your UI -- same direction?"
   - Developers usually have a strong instinct here from their framework's defaults (Tailwind `rounded-lg`, MUI's defaults, etc.).

### Common Color Name to Hex Mapping

| User says | Hex | Notes |
|-----------|-----|-------|
| Indigo / Tailwind indigo | #4F46E5 | Common dev tool accent |
| Navy / dark blue | #1E3A5F | Professional, trust |
| Royal blue | #1E40AF | Confident, established |
| Red | #DC2626 | Energy, urgency |
| Orange | #EA580C | Warmth, friendliness |
| Green | #16A34A | Growth, open source |
| Teal / cyan | #0D9488 | Modern, fresh |
| Purple / violet | #7C3AED | Creative, premium |
| Amber / gold | #D97706 | Warmth, quality |
| Charcoal / near-black | #1F2937 | Use instead of pure #000 |

### Transition to Generation

Confirm before proceeding:

> "Here's the brand direction:
> - Project: {name} -- {elevator pitch}
> - Target users: {users}
> - Primary CTA: {action}
> - Brand feel: {adj1}, {adj2}, {adj3}
> - Style: {light/dark} theme, {color} accent, {clean/serif} typography, {sharp/rounded} shapes
>
> Look right?"

If the user corrects anything, update before proceeding.
Then: "Setting up the design system and generating the first draft. Takes about a minute."

### Edge Cases

- **User wants to skip entirely**: "Just make me a landing page, it's a CLI for managing Postgres backups." Extract what you can. Ask only CTA + brand feel (2 questions max). Default the rest and tell them: "I'm defaulting to dark theme, clean sans-serif, rounded corners, and a blue accent. We can change any of it after you see the first draft."
- **User shares their app URL, repo, or docs**: Don't fetch or parse the linked content. Ask the user to describe the existing look in their own words — primary color, light vs dark theme, typography direction, overall vibe. Confirm their description: "So your app is dark theme, indigo accents, clean sans-serif — should the landing page match that, or go in a different direction?"
- **User pastes a README or description**: Parse it for project name, pitch, target users, and features. Skip to the gaps.

---

## Feedback Facilitation Guide

### After Each Generation, Ask These Three Questions

1. **First impression**: "What's your gut reaction in the first 5 seconds?"
2. **Brand alignment**: "Does this feel like YOUR product?"
3. **Issues**: "Is there anything that feels wrong, missing, or not quite right?"

Do not ask "Do you like it?" -- this produces yes/no answers with no actionable information.

### Guiding the User Toward Useful Feedback

Developers often give feedback in implementation terms. Redirect toward design intent:

| User says | They likely mean | Follow-up to ask |
|-----------|-----------------|-----------------|
| "I don't like it" | Overall mismatch | "Is it the colors, the layout, or the overall mood that feels off?" |
| "It's boring" / "too plain" | Low visual energy | "Would you like more color contrast, a bolder layout, or both?" |
| "It's too busy" | Visual clutter | "Which part feels most cluttered? The hero, the features section, or everything?" |
| "It looks like a template" | Generic, no personality | "What would make it feel more specific to your product? A different layout, stronger colors, more distinctive typography?" |
| "It's too marketing-y" | Over-designed, too much flair | "Should we strip it down -- less decoration, more information density, tighter layout?" |
| "The colors are off" | Palette mismatch | "Too bright, too dull, or just the wrong hue?" |
| "More whitespace" / "too cramped" | Layout density | Edit: "Add more breathing room between sections" |
| "Needs more padding" / "font-size too small" | CSS-level observation | Translate: "Which section feels too tight or hard to read?" |
| "Make it pop" | Weak visual hierarchy | "What should stand out more -- the headline, the CTA button, or the overall contrast?" |
| "I love the layout but not the colors" | Partial approval | Variant signal: keep layout, change COLOR_SCHEME only |
| "Show me something totally different" | Fundamental rethink | REIMAGINE creative range |
| "Can I just edit the HTML?" | Wants direct control | "Stitch handles the regeneration cycle, so let's iterate here first -- then you can hand-edit the final output." |

### Design Dimensions to Highlight for the User

When presenting a design for review, draw the user's attention to specific elements. These help non-designers evaluate design without knowing design vocabulary:

- **Message clarity**: "Can a visitor tell what your product does within 5 seconds of landing here?"
- **CTA visibility**: "How quickly did your eye find the primary button? Could you miss it?"
- **Color impression**: "Do these colors match the feel you described -- {their 3 adjectives}?"
- **Reading flow**: "When you scan top to bottom, does the section order make sense for someone discovering your product?"
- **Credibility**: "If you were evaluating this product for the first time, does this page make it look like a real, maintained project?"

### Steering Toward Approval

- After positive-but-uncommitted feedback: "What's the one thing that would make this feel right?"
- After choosing from options: "Want me to tweak anything on this one, or lock it in?"
- After 3+ rounds of minor tweaks: "This is looking solid. Want to keep iterating or ship it and refine later?"
- After 5+ rounds: "What's the single most important change left? Let's nail that one thing."

Developers often prefer to ship something decent and iterate rather than perfecting before launch. If you sense this, offer the exit: "This is in a good place. Want me to bundle it so you can deploy and see how it looks in the real context?"

### Feedback Priority Framework

Help users separate critical from cosmetic:

1. **Must fix**: The page doesn't communicate what the product does, or the CTA is unclear/missing.
2. **Should improve**: The mood doesn't match the brand direction, or a section is missing/unnecessary.
3. **Nice to have**: Font weight preference, exact shade of a color, spacing tweaks.

Guide users to address category 1 first, then 2, then 3. This prevents endless loops on cosmetic details while structural problems persist.
