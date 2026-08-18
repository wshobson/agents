# Word tiers

112 single-word and short-phrase entries across three tiers, plus 10 multi-word
boilerplate phrases. The tier says how much weight a hit carries, not how hard the
fix is. Counts here are derived from the upstream tables and enforced against them
in the upstream CI.

**Match inflected forms.** Each entry covers the listed word and its morphological
variants: adverb, gerund, plural, comparative, and verb conjugations. `delve` covers
`delving`, `leverage` covers `leveraging`. When a variant carries a separate honest
sense (`real` meaning factual rather than the intensifier in "a real improvement"),
judge by context instead of matching blindly.

The tiering is adapted from [brandonwise/humanizer](https://github.com/brandonwise/humanizer)'s
vocabulary research, which reduces false positives on words that are fine alone and
suspicious in clusters.

## Tier 1: always replace

Tier 1 splits into two bands. Both get replaced and the edit is identical. What
differs is what a hit *means*.

**1A, AI frequency markers.** Words claimed to appear far more often in machine text
than in human writing. A cluster of these is evidence about how a passage was produced.

**1B, clarity edits.** Wordiness and inflated formality. Replacing them is good writing
regardless of who wrote the sentence, and a 1B hit is **not** evidence of machine
authorship. Measured against 257 paragraphs of verified pre-2023 human prose, 1B entries
fire on ordinary professional writing at a meaningful rate: `in order to`, `utilize`,
`commence`, `ascertain`, and `endeavor` are simply the words some people reach for.
Weight them like Tier 2 and keep them out of any density signal, so a wordiness fix can
never push a document toward an AI classification. In detect mode, report the two bands
separately.

Caveat worth keeping visible: the "appears far more often in AI text" claim behind 1A is
inherited rather than measured. It traces to brandonwise/humanizer, which states a 5 to 20x
ratio without publishing a method or dataset. Treat 1A as a well-supported convention until
someone measures the ratios against a machine-written corpus.

### Tier 1A: AI frequency markers (49 entries)

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why it matters |
| hit differently / hits different | (say what specifically changed, or cut) |
| watershed moment | turning point, shift (or describe what changed) |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut — say something specific or nothing) |
| only time will tell | (cut — say something specific or nothing) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite what makes it busy) |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities, or use "problems" / "details") |
| ever-evolving | changing, growing (or describe how) |
| enduring | lasting, long-running (or cite how long) |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe their actual contribution) |
| best practices | what works, proven methods, standard approach |
| at its core | (cut — just state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| keen (as intensifier) | interested, eager, enthusiastic (or cut — just state the interest) |
| genuinely / genuine (as intensifier) | (cut — just state the fact) |
| symphony (metaphor) | (describe the actual coordination or combination) |
| embrace (metaphor) | adopt, accept, use, switch to |
| load-bearing *(metaphor)* | essential, critical, necessary — or say what breaks if you remove it |

**Hyphen required:** unhyphenated "load bearing" is ordinary English ("the load bearing
down on the bridge"). Only the hyphenated compound is the tell.

**Construction carve-out:** `load-bearing` before a literal structural noun (`wall`, `beam`,
`column`, `joist`, `truss`, `footing`, `slab`, `stud`, `masonry`, `lintel`, `rafter`,
`girder`, `capacity`), optionally with one material or position adjective in between, is
standard building terminology. Abstract-capable nouns (`structure`, `element`, `frame`,
`foundation`) stay flaggable, so "the load-bearing structure of his argument" still fires.

### Tier 1B: clarity edits (10 entries)

Wordiness and formality, not authorship evidence. Same fix, weaker claim.

| Replace | With |
|---|---|
| utilize | use |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |

## Tier 2: flag when two or more appear in one paragraph (40 entries)

These words are legitimate alone. Two or more together usually means the paragraph
needs a rewrite.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape (or describe what changed) |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed (or name the actual nuance) |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets, or cut) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging (or cite a number) |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| quietly | cut, or name the concrete contrast |
| deeply *(significance collocations only — "deeply integrated," "deeply committed," "deeply rooted"; literal uses like "deeply nested" or "cares deeply" never count toward a cluster)* | cut, or name what specifically runs deep |
| underpinning / underpinnings | basis, foundation, what supports |

## Tier 3: flag only at high density (13 entries)

Normal words. Flag them only when the text is saturated, which signals that vague
praise filled the space where specifics belonged. Roughly 3 percent of total words is
the threshold worth a second look.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |
| verbatim | Usually redundant with the verb ("copies X verbatim" = "copies X") — cut it. If the exactness marks a contrast, name it: byte-for-byte, word for word, unchanged. Term of art in legal/research/QA registers ("verbatim transcript / record / testimony"), so weigh density in that context before flagging |

## Tier 3 phrases: flag at density or in clusters (10 entries)

Multi-word boilerplate that is individually unobjectionable and stacks heavily in
generated content. Crypto, web3, DePIN, and AI infrastructure reviews are the worst
offenders. Two rules apply: the same phrase used twice, and three or more *distinct*
phrases from this table in one piece even when each appears once. The second rule
catches the shape models take when they vary their own boilerplate to seem less
repetitive.

| Phrase | What to do |
|---|---|
| emerging sector / emerging space / emerging category | Name the actual sector or what's emerging about it |
| the integration of (X with Y) | Describe what's being integrated and what changes for the user |
| the intersection of (X and Y) | Pick the specific overlap that matters or cut the framing |
| community-driven | Name what the community does. "Community-driven" alone is filler |
| long-term sustainability | Cite the time horizon and the constraint. "Long-term" is hand-waving |
| user engagement | Name the action. "Engagement" is a wrapper around clicks/comments/retention |
| decentralized compute | Specify the architecture or cut. The phrase has become a category label, not a claim |
| (sustainable) reward emissions | Cite the emission schedule and the sink |
| tokenized incentive structures | Describe the actual mechanism (vesting, gauge, bonded LP, etc.) |
| designed for long-term [X] | Cut "designed for" — either it is or it isn't. Then state the property |

## Context adjustments

`technical-blog` gives legitimate technical meaning back to `robust`, `comprehensive`,
`seamless`, `ecosystem`, `leverage` (actual platform leverage or APIs), `facilitate`,
`underpin`, and `streamline`. Still flag `delve`, `tapestry`, `beacon`, `embark`,
`testament to`, `game-changer`, and `harness` there.

`docs` relaxes the full table. `casual` drops to P0 patterns only. See
`references/profiles.md` for the whole matrix.
