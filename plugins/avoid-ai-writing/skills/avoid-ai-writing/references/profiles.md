# Context and voice profiles

Two independent axes. A context profile sets *how strict* to be for an audience. A
voice profile sets *how the prose should sound*. Blunt for a blog and warm for docs
are both valid combinations.

## Context profiles

- **`linkedin`**: short-form social. Punchy fragments and visual formatting matter.
- **`blog`**: the default. Standard long-form prose, every rule at full strength.
- **`technical-blog`**: long-form with code, architecture, and APIs. Technical terms get a pass.
- **`investor-email`**: high-trust audience. Tighten everything. Promotional language is the biggest risk.
- **`docs`**: documentation, READMEs, guides. Clarity over voice.
- **`casual`**: chat messages, internal notes, quick replies. Only the worst offenders.

### Auto-detection

When no context is named, infer it:

| Signal | Inferred context |
|--------|-----------------|
| Under 300 words plus hashtags or mentions | `linkedin` |
| Code blocks, API references, or architecture | `technical-blog` |
| Salutation plus investor or fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog`, the safest default |

Say which profile you inferred and why. The writer can override.

### Tolerance matrix

Rules absent from the table apply at full strength everywhere. "Skip" means the rule
does not apply to that register. "Extra strict" means flag borderline instances too:
in an investor email, one "thriving ecosystem" can undermine the whole message.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work on LinkedIn) | strict | relaxed (technical lists OK) | strict | skip (lists are docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate in technical) | strict | relaxed | skip |
| Word table (full list) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell is expected) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |
| Hashtag stuffing | strict | strict | strict | **extra strict** | skip (no hashtags in docs) | skip |
| Bullet-NP lists | strict | strict | relaxed (technical option lists OK) | strict | relaxed (parameter lists OK) | skip |
| Tier 3 phrase clustering | strict | strict | strict | **extra strict** | relaxed | skip |
| Future-narrative closers | strict | strict | strict | **extra strict** | skip | skip |
| Social endorsement closers | strict (the LinkedIn share-post tell) | strict | strict | strict | skip | relaxed (1 OK in a DM) |
| Hedge-stacked predictions | strict | strict | relaxed ("could" is hedged accuracy) | **extra strict** | relaxed | skip |
| Real/actual inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Moral-adjective category errors | strict | strict | relaxed | strict | relaxed | skip |
| Invented contrast-pair mirroring | strict | strict | relaxed | strict | relaxed | skip |
| Subjectless fragments and agentless passives | relaxed (short-form fragments are the register) | strict | relaxed | strict | skip (fragment lists are docs) | skip |

**Technical-blog word table exceptions.** These terms carry legitimate technical meaning
and stay unflagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`,
`leverage` (when the subject is actual platform leverage or APIs), `facilitate`, `underpin`,
`streamline`. Still flag `delve`, `tapestry`, `beacon`, `embark`, `testament to`,
`game-changer`, and `harness` there.

One scoping rule lives in the pattern itself rather than in this table. Wall-of-text
replies fire only in conversational reply registers, and a plain issue comment
auto-detects as `blog`, so the judgment has to sit with the rule.

## Voice profiles

Voice is optional. With no profile named, infer the register from the input and avoid
imposing a persona on text that already has one. Each profile is a set of concrete
targets rather than a vibe. Targets shape what survives the edit; they never authorize
adding stance, personality, or facts the source lacks. The rewrite guardrails in
`SKILL.md` bind here too.

**`casual`**: contractions throughout, since their absence reads stiff. Short sentences,
averaging 14 words or fewer. Fragments allowed. Keep first-person and concrete
touches where the source has them; never add one it lacks. Near-zero jargon. Keep warm hedges ("honestly", "I think") and cut corporate ones
("it's worth noting"). Fits blog posts, social, community writing.

**`professional`**: active voice for most sentences. Vary sentence length. Prefer a concrete
claim (a number, a name, a date) over "experts say" when the source provides one. Keep
the ask explicit where the source makes one; never invent facts or an ask.
Low tolerance for hedging. Fits LinkedIn, investor email, pitches.

**`technical`**: prefer plain copulatives ("X is Y") over inflated substitutes ("serves as",
"stands as a testament to"). One idea per sentence, imperative mood for instructions.
Jargon is fine when defined on first use. Tables and lists only where the content is
genuinely list-shaped. Fits docs and technical blogs.

**`warm`**: address the reader directly where the source already speaks to them, and
keep its acknowledgment rather than adding one. Cut intensifiers
("very", "truly", "incredibly") in favor of stronger verbs. No performative-empathy openers.
Medium sentences of 15 to 20 words for an unhurried cadence. Fits mentorship, onboarding,
thank-yous.

**`blunt`**: lead with the claim and cut the windup. Dashes are rare here; use periods for
emphasis. No padding to reach a rule of three. Near-zero hedging, and flag "may / could /
potentially" stacks. Short declaratives with the occasional long sentence for contrast.
Fits decision memos, thought leadership, hard feedback.

**Calibrate to a sample instead.** Given a sample of the writer's own work, analyze its
sentence-length pattern, contraction rate, paragraph openings, and recurring word choices,
then match those rather than a named profile. Do not upgrade their vocabulary: if they
write "stuff" and "things", keep that register.

## How the axes compose

A voice target always applies, even where a context profile would skip that category.
Technical voice still prefers plain copulatives in a casual context that otherwise ignores
copula avoidance. Where both axes govern the same rule and agree, they reinforce each other.
Where they disagree, resolve toward the stricter of the two: a warm voice on `docs` still
does not get decorative tables. Sensible default pairings are casual with casual,
professional with linkedin or investor-email, technical with docs or technical-blog.
