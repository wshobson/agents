# Stitch Architecture Reference

Stable patterns for working with Stitch. This file covers concepts and taxonomies that remain consistent across SDK versions. For the current API surface (parameter names, return shapes, enum values), the authoritative source is the SDK repository linked in the Stitch Documentation section of SKILL.md.

---

## Stitch Conceptual Model

- **Project**: Top-level container. One project per landing page engagement. Contains screens and a design system.
- **Screen**: A single generated UI design. Has associated HTML and a screenshot, both available as download URLs. Edits produce new screen versions; originals are preserved and can be revisited.
- **Design System**: Project-wide visual tokens (colors, fonts, shapes, spacing). Applies consistently to all screens. Described in semantic language, not CSS.
- **Generation is asynchronous**: Screen generation can take 1-3 minutes. Do NOT retry a generation call if it seems slow. Use `get_screen` or `list_screens` to check completion status.
- **Assets are URLs**: Both `getHtml()` and `getImage()` return download URLs, not inline content. Download the files using whatever tools are available.
- **Namespace varies**: Stitch MCP tool names may be prefixed differently depending on the server configuration. Always discover the prefix via `list_tools` at startup.

---

## Font Personality Guide

Stitch supports 28 font enums. Use this guide to select fonts based on the brand personality established during the interview. Always select both a headline font and a body font.

### Modern / Clean Sans-Serif
For brands described as: modern, clean, minimal, technical, sharp

| Font Enum | Character | Good for |
|-----------|-----------|----------|
| PLUS_JAKARTA_SANS | Geometric, friendly, highly readable | Default modern choice |
| DM_SANS | Slightly rounded, warm modern | Approachable SaaS |
| GEIST | Sharp, contemporary | Dev tools, Vercel-style products |
| SORA | Geometric with personality | Creative tech, design tools |
| SPACE_GROTESK | Technical, spacious | Engineering tools, data products, APIs |
| IBM_PLEX_SANS | Structured, authoritative | Enterprise, infrastructure |
| INTER | Neutral, ubiquitous | Safe default (may feel generic) |

### Warm / Friendly Sans-Serif
For brands described as: warm, friendly, approachable, inviting

| Font Enum | Character | Good for |
|-----------|-----------|----------|
| NUNITO_SANS | Rounded, soft | Consumer apps, community platforms |
| RUBIK | Slightly rounded, substantial | Collaboration tools, social products |
| LEXEND | Designed for reading ease | Education, accessibility-focused tools |
| MANROPE | Geometric but warm | Lifestyle products, team tools |

### Professional / Corporate
For brands described as: professional, trustworthy, established, reliable

| Font Enum | Character | Good for |
|-----------|-----------|----------|
| PUBLIC_SANS | Government-grade clarity | Compliance, security, finance tools |
| SOURCE_SANS_THREE | Clean professional | Consulting, healthcare tech |
| WORK_SANS | Straightforward workhorse | Utility tools, productivity |
| HANKEN_GROTESK | Crisp, Nordic | Design systems, architecture |
| ARIMO | Familiar, Arial-like | Conservative industries, B2B |

### Traditional / Elegant Serif
For brands described as: elegant, premium, refined, classic

| Font Enum | Character | Good for |
|-----------|-----------|----------|
| NEWSREADER | Editorial, magazine | Content platforms, publishing tools |
| LIBRE_CASLON_TEXT | Classic, bookish | Writing tools, knowledge bases |
| EB_GARAMOND | Old-world elegance | Premium services, high-end products |
| LITERATA | Refined, warm | Boutique SaaS |
| SOURCE_SERIF_FOUR | Warm, readable serif | Professional services |
| DOMINE | Sturdy, readable | Finance, real estate platforms |
| NOTO_SERIF | Comprehensive, global | International products |

### Display / Statement (headline only -- pair with a neutral body font)
For brands that want a distinctive headline presence:

| Font Enum | Character | Good for |
|-----------|-----------|----------|
| EPILOGUE | Distinctive, editorial | Creative agencies, design tools |
| BE_VIETNAM_PRO | Unique character | Consumer products, marketplaces |
| SPLINE_SANS | Technical, precise | Engineering tools, SaaS |
| MONTSERRAT | Geometric, bold | Marketing tools, events platforms |
| METROPOLIS | Urban, strong | Fitness apps, bold brands |

### Recommended Pairings

| Product type | Headline | Body | Feel |
|--------------|----------|------|------|
| SaaS / web app | SORA | DM_SANS | Clean and approachable |
| Dev tool / CLI / API | GEIST | SPACE_GROTESK | Technical and sharp |
| Open source project | PLUS_JAKARTA_SANS | INTER | Open, readable, neutral |
| Developer portfolio | EPILOGUE | LITERATA | Distinctive and refined |
| B2B / enterprise | HANKEN_GROTESK | SOURCE_SANS_THREE | Authoritative and clear |
| Consumer product | PLUS_JAKARTA_SANS | NUNITO_SANS | Warm and welcoming |
| Data / analytics | SPACE_GROTESK | IBM_PLEX_SANS | Technical and structured |
| Premium / design tool | EB_GARAMOND | INTER | Elegant with readable body |

---

## Color Variant Decision Tree

Stitch design systems accept a `colorVariant` enum that controls how the palette is generated from the custom color. Use the brand adjectives from the interview to select the right variant.

| Brand personality | colorVariant | Rationale | Example products |
|-------------------|-------------|-----------|-----------------|
| Bold, vibrant, energetic | VIBRANT | High saturation, dynamic | Marketing tools, social apps, community platforms |
| Clean, minimal, technical | NEUTRAL | Muted, restrained | Dev tools, APIs, infrastructure products |
| Sophisticated, subtle | TONAL_SPOT | Nuanced tonal variations | Design tools, analytics platforms, B2B SaaS |
| Dramatic, singular, focused | MONOCHROME | Single-hue depth | Portfolio sites, premium tools, focused products |
| Playful, expressive, creative | EXPRESSIVE | Wide chromatic range | Consumer apps, creative tools, marketplaces |
| True-to-existing-brand | FIDELITY | Stays closest to custom color | Any product with established brand colors |
| Earthy, natural, organic | CONTENT | Warm, content-derived | Wellness apps, sustainability, outdoor |
| Whimsical, festive, diverse | RAINBOW | Full chromatic variety | Creative platforms, community tools |
| Fresh, colorful, cheerful | FRUIT_SALAD | Varied but coherent | Consumer apps, education, social |

### Default Color Suggestions

When the user has no existing brand colors, suggest based on desired emotion:

| Desired emotion | Suggested hex | Color description |
|----------------|--------------|-------------------|
| Trust, reliability | #1E40AF | Deep blue |
| Stability, professionalism | #1E3A5F | Navy |
| Energy, passion, urgency | #DC2626 | Red |
| Warmth, friendliness | #EA580C | Warm orange |
| Growth, health, open source | #16A34A | Green |
| Modern, refreshing | #0D9488 | Teal |
| Creativity, premium | #7C3AED | Purple |
| Technical, developer-focused | #4F46E5 | Indigo |
| Warmth, quality, heritage | #D97706 | Amber |
| Neutrality, sophistication | #374151 | Slate gray |

---

## Prompt Engineering Patterns

### Generation Prompt Template

```
A {DESKTOP|MOBILE} landing page for "{projectName}", {one-sentence description}.

Hero: {headline concept} with a clear "{CTA button text}" button.
Target users: {target user description}.
Mood: {adj1}, {adj2}, {adj3}.

Sections:
1. Hero with headline, subheadline, and primary call-to-action
2. {Second section based on product type}
3. {Third section}
4. {Fourth section}
5. Footer with links and secondary call-to-action
```

Select sections based on product type (see Section Taxonomy below).

### Prompt Guidelines

**Do:**
- Describe layout in terms of sections and content purpose
- Mention the mood/feel even though the design system also encodes it (reinforcement helps)
- Specify CTA button text explicitly (e.g., "Start Free Trial")
- Keep prompts to 6-8 sentences maximum
- Name specific section types (hero, testimonials, features, pricing)

**Do not:**
- Write CSS, HTML, or code in the prompt
- Reference pixels, padding, margins, or breakpoints
- Ask for animations or interactivity (Stitch generates static HTML)
- List more than 5-6 sections (overloading degrades quality)
- Use vague instructions ("make it nice") -- be specific about structure

### Edit Prompt Patterns

| Change type | Prompt pattern |
|------------|---------------|
| Layout reorder | "Move the testimonials section above the features section" |
| Color shift | "Make the hero background darker" or "Use a warmer tone for the section backgrounds" |
| Typography | "Make the headline larger and bolder" |
| Content swap | "Change the headline to '{exact text}'" |
| CTA emphasis | "Make the call-to-action button more prominent with higher contrast" |
| Remove element | "Remove the third feature card" |
| Add section | "Add a pricing section before the footer" |
| Whitespace | "Add more breathing room between sections" |

### Variant Prompt Patterns

| Intent | Prompt | Suggested settings |
|--------|--------|--------------------|
| Subtle refinement | "Polish the typography and spacing" | REFINE, aspects: [TEXT_FONT, LAYOUT] |
| Color exploration | "Try warmer color palettes" | EXPLORE, aspects: [COLOR_SCHEME] |
| Layout alternatives | "Show different ways to arrange the hero section" | EXPLORE, aspects: [LAYOUT] |
| Broad exploration | "Try a different approach to this page" | EXPLORE, aspects: [LAYOUT, COLOR_SCHEME, IMAGES] |
| Total rethink | "Reimagine this page from scratch" | REIMAGINE, all aspects |

---

## Landing Page Section Taxonomy

### Standard Sections (in suggested order)

| # | Section | Purpose | Include when |
|---|---------|---------|-------------|
| 1 | Hero | Headline + subheadline + primary CTA + optional visual | Always (first section) |
| 2 | Social Proof Bar | Logos of users/companies, GitHub stars, "used by X teams" | Product has notable adopters or metrics |
| 3 | Problem / Solution | What pain point you solve and how | Target users have a specific, articulable problem |
| 4 | Features / Benefits | 3-4 value propositions with icons | Product has multiple distinct capabilities |
| 5 | How It Works | 3-step process or workflow | Product has a clear usage flow (install, configure, run) |
| 6 | Code Snippet / Demo | Example usage, CLI output, or API call | Dev tools, CLIs, SDKs, APIs |
| 7 | Integrations | Logos of compatible tools/platforms | Product connects to an ecosystem |
| 8 | Testimonials | 2-3 user quotes or case studies | Product has user feedback or endorsements |
| 9 | Pricing | Tiers, free/paid, or open source badge | When pricing model is a selling point |
| 10 | FAQ | 4-6 common questions | When the product needs explanation |
| 11 | About / Story | Brief founder or team narrative | Personal brands, indie projects |
| 12 | Final CTA | Repeat primary action with urgency | Always (second-to-last) |
| 13 | Footer | Links, social, legal, GitHub link | Always (last) |

### Section Selection by Product Type

| Product type | Recommended sections |
|--------------|---------------------|
| SaaS / web app | Hero, Social Proof, Features, How It Works, Pricing, Testimonials, Final CTA, Footer |
| Dev tool / CLI | Hero, Code Snippet, Features, How It Works, Integrations, Final CTA, Footer |
| API / SDK | Hero, Code Snippet, Features, Integrations, Pricing, FAQ, Final CTA, Footer |
| Open source project | Hero, Code Snippet, Features, Social Proof (stars/contributors), About, Final CTA, Footer |
| Developer portfolio | Hero, Featured Projects, Testimonials, About, Final CTA, Footer |
| Side project / indie product | Hero, Problem/Solution, Features, Pricing, FAQ, Final CTA, Footer |
| Agency / consultancy | Hero, Problem/Solution, How It Works, Testimonials, Social Proof, Final CTA, Footer |

---

## Design System Quick Reference

### Roundness Values

| Enum | Radius | Feel | Tailwind parallel | Typical use |
|------|--------|------|-------------------|-------------|
| ROUND_FOUR | 4px | Sharp, precise | `rounded` | Fintech, enterprise, dev tools |
| ROUND_EIGHT | 8px | Balanced, modern | `rounded-lg` | Default for most products |
| ROUND_TWELVE | 12px | Soft, friendly | `rounded-xl` | Consumer apps, SaaS |
| ROUND_FULL | Pill/full circle | Playful, bold | `rounded-full` | Startups, creative, badges |

### Design System Creation Sequence

1. Call `create_project` with the project name as the title
2. Build the DesignSystem object using the translation mappings from the interview
3. Call `create_design_system` with the project ID
4. Immediately call `update_design_system` -- this is required to render the system; create alone is not sufficient
5. Save the project ID and design system asset ID to `.stitch/metadata.json`

### Applying a Design System to Existing Screens

This is the step that requires careful data handling:

1. Call `get_project` with the project name to retrieve `screenInstances`
2. Each screenInstance contains two required fields:
   - `id` -- the instance ID (different from screen ID)
   - `sourceScreen` -- resource name in format `projects/{project}/screens/{screen}`
3. Build a `selectedScreenInstances` array containing objects with both `id` and `sourceScreen`
4. Call `apply_design_system` with `projectId`, `assetId` (from the design system), and `selectedScreenInstances`
5. Re-fetch screens after applying to get updated HTML

Common mistake: using the screen ID as the instance ID. They are different values. The instance ID comes from the `screenInstances` array in the `get_project` response.
