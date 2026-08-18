# Pattern catalog

Every entry lists the tell and the fix. Quoted strings are illustrative examples, not text to preserve.

## Severity

Every pattern below falls into one of three tiers.

- **P0, credibility killers:** cutoff disclaimers ("As of my last update"), chatbot artifacts ("I hope this helps!"), vague attributions ("Experts believe"), significance inflation on routine events, unfilled placeholders (`[Your Name]`), chat citation markup (`citeturn0search0`), AI-tool tracking parameters (`utm_source=chatgpt.com`).
- **P1, obvious AI smell:** Tier 1 vocabulary, template and slot-fill phrases, "Let's" openers, synonym cycling, formulaic openings, bold overuse, em dashes above one per 1,000 words, future-narrative closers, hedge stacks ("could potentially"), moral adjectives on non-agentic nouns ("an honest shape"), bullet lists of bare noun phrases.
- **P2, polish:** generic conclusions, compulsive rule of three, uniform paragraph length, copula avoidance ("serves as", "boasts"), transition phrases ("Moreover", "Furthermore"), Tier 3 repetition.

## Formatting

- **Em dashes:** target zero, hard max one per 1,000 words, headings included. Catch both the Unicode em dash and the double-hyphen substitute. Carve-out: a dash separating a bolded lead term or a link from its gloss inside a list item (`- **Term** - description`) is typography, not a prose splice. A mid-sentence splice still counts.
- **Bold overuse:** one bolded phrase per major section at most. If something deserves bold, restructure the sentence to lead with it.
- **Emoji in headers:** remove. Social posts may carry one or two at the end of a line.
- **Excessive bullets:** convert bullet-heavy sections to prose. Keep bullets for genuinely list-shaped content: feature comparisons, ordered steps, API parameters.
- **Curly quotes in plain-text contexts:** a weak paste-from-chat signal, meaningful only where nothing auto-curls (code comments, commit messages, plaintext drafts). Word, Google Docs, macOS, and iOS curl by default, so most human prose has them too. Never conclusive. Do not flag curly apostrophes alone.
- **Immaculate typography in casual registers:** perfect spacing and capitalization in issue comments, chat, or DMs is corroborating evidence at most. The inverse matters more: when editing a human's casual text, keep their typos and idiosyncratic capitalization rather than smoothing them away.
- **Inline-header lists:** bullets whose bold header repeats the first words of the item ("**Performance:** Performance improved by..."). Strip the header and write the point.
- **List-label periods:** LLMs end a bullet's short label with a period, then run the gloss as a separate sentence (`- **Intros.** Years of conferences...`). A person writes `- **Intros:** years of conferences...`. Carve-out: a label span that is a full sentence keeps its period.
- **Title case headings:** use sentence case for subheadings.
- **Hyphenated-pair overuse:** two problems. First, strings of compound modifiers piled on one noun; cut to the one that matters. Second, the predicate error. Hyphenate before the noun ("a high-quality report") and not after a linking verb ("the report is high quality").
- **Excessive structure:** more than three headings in under 300 words, or eight-plus bullets in under 200 words, is scaffolding standing in for content. Formulaic headers ("Overview", "Key Points", "Summary") say nothing. A heading followed by a one-line warm-up that restates it should lose the warm-up.

## Sentence structure

- **"It's not X, it's Y."** Rewrite as a direct positive claim. Includes the split-sentence form across two sentences, the multi-negation countdown ("Not the price. Not the features. The trust."), and the tailing negation fragment ("...comes from the selected item, no guessing"). Carve-out: spec constraints in a list ("no dependencies, no telemetry").
- **Hollow intensifiers:** cut `genuine`, `truly`, `quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`.
- **Vague endorsement:** `worth reading`, `worth a look`, `worth your time` substitute a thumbs-up for a reason. Say why.
- **Hedging:** cut `perhaps`, `could potentially`, `it's important to note that`.
- **Hedge-stacked predictions:** a modal plus a hedge adverb: "could potentially create", "may eventually unlock". Either word alone is fine; the stack asserts nothing. Pick one.
- **Missing bridge sentences:** if paragraphs could be reordered without the reader noticing, add connective tissue.
- **Compulsive rule of three:** vary groupings. One "adjective, adjective, and adjective" per piece at most.
- **Copula avoidance:** "Serves as", "features", "boasts", "presents", "represents" instead of "is" and "has". Default to the plain verb.
- **Subjectless fragments and agentless passives:** "No configuration file needed." "Support for nested queries was added." Name the actor when it clarifies. Carve-out: terse reference registers where the fragment is correct, such as changelogs, parameter docs, and commit subjects.
- **Synonym cycling:** "Developers... engineers... practitioners... builders" in one paragraph. Repeat the clearest word instead.
- **Parenthetical hedging:** "(or, more precisely, Y)", "(and perhaps more importantly, W)". Give the aside its own sentence or cut it.
- **False concession:** "While X is impressive, Y remains a challenge." Both halves are vague. Name the specific thing or pick a side.
- **Invented contrast-pair mirroring:** one half of the contrast is a real term of art, the other is fabricated for symmetry: "false precision rather than genuine accuracy". Reach for a real opposite or state the positive claim.
- **False ranges:** "From the Big Bang to dark matter." Sweeping breadth that names nothing. List the actual topics.

## Openers, transitions, closers

- **Formulaic openings:** broad context before the point ("In the rapidly evolving world of..."). Lead with the news.
- **Transition phrases:** "Moreover", "Furthermore", "Additionally", "In today's X", "When it comes to", "At the end of the day", "In conclusion". Restructure so the connection is obvious.
- **Reader-steering frames:** "Here's what's interesting", "Here's what caught my eye". Let the content signal its own importance.
- **"Let's" constructions:** "Let's explore", "Let's break this down". Start with the point.
- **Rhetorical question openers:** "But what does this mean for developers?" If you know the answer, say it.
- **Speculative scenario openers:** "Imagine a world where...". The scenario does the persuading and no evidence arrives. Carve-out: fiction, a thought experiment with a stated payoff, and instructional "imagine you have a sorted array".
- **Numbered list inflation:** "Three key takeaways", "Five things to know". Only number a list when the content genuinely has that many parallel items.
- **Generic conclusions:** "The future looks bright", "Only time will tell", "As we move forward". Cut.
- **Generic future-narrative closers:** modal plus "become" plus "one of the most [adjective] [narrative / trend / chapter]". Grammatically a prediction, containing nothing testable. Replace with a falsifiable version or cut.
- **Template phrases:** slot-fill constructions: "a [adjective] step towards [adjective] AI infrastructure", "Whether you're [X] or [Y]" (false breadth: pick the audience), "I recently had the pleasure of [verb]-ing".

## Inflation and false depth

- **Significance inflation:** "Marking a pivotal moment in the evolution of...". If the sentence still works after deleting the inflation clause, delete it.
- **Aphorism formulas:** "X is the language of Y", "the architecture of trust". The shape does the persuading. Replace with the concrete claim. Carve-out: quotations and established idioms.
- **"Real" and "actual" adjective inflation:** "Real on-chain tokenomics", "genuine utility". The intensifier implies the rest of the field is fake without saying what makes this one real. Carve-out: when the sentence names the contrast ("actual revenue from paying customers, not grants").
- **Moral-adjective category errors:** moral adjectives glued to non-agentic nouns: "an honest shape", "flagged honestly". State the concrete property instead. Related: "the assumption stops being true" (assumptions break down, they do not flip), and gratuitous universal quantifiers ("taught in every first-year course").
- **Novelty inflation:** treating established concepts as inventions: "he introduced a term", "a failure mode nobody's naming". Describe what the person did with the concept. Also flag invented labels, meaning pseudo-analytical compounds coined mid-sentence and never defined.
- **Superficial -ing analyses:** "Symbolizing the region's commitment to progress, reflecting decades of investment". Also the declarative form: "this represents a broader shift". Show the consequence or cut.
- **Promotional language:** tourism-brochure prose: "nestled within the breathtaking foothills", "a thriving ecosystem". Replace with plain description.
- **Formulaic challenges:** "Despite challenges, X continues to thrive." Name the challenge and the response or cut the sentence.
- **Emotional flatline:** "What surprised me most", "I was fascinated to discover", and the header form "Interesting part of the project:". If the thing is surprising, the content should show it.
- **Lingering-attention claims:** "I can't stop thinking about this", "still thinking about this one". The claim is about the writer's attention and arrives before the reader has a reason to care. Carve-out: when the sentence says why the thing recurred.
- **Self-labeling significance:** pointing back at an item to label it: "that last move is the contrarian one", "here's where it gets clever". If the move is contrarian, the description already showed it.
- **Confidence calibration phrases:** "Interestingly", "Notably", "Importantly", "Undoubtedly". One in 2,000 words is fine; three in 500 is emphasis stacking. Related persuasive-authority tropes: "the real question is", "at its core", "fundamentally", "make no mistake".
- **Filler phrases:** "It is important to note that", "In terms of", "The reality is that".

## Manufactured credibility

- **Vague attributions:** "Experts believe", "Studies show". Cite the source or state the claim directly.
- **Vague third-party validation:** an unnamed authority plus a superlative: "independent testing confirms", "third-party benchmarks show we lead". Name the source, the test, and the result. Carve-out: a named benchmark, a linked report, a dated audit.
- **Notability name-dropping:** piling on prestigious citations to borrow their weight. One specific reference beats four names. Related: historical analogy stacking ("like the printing press, the telegraph, and the internet before it").
- **Speculative gap-filling:** guesses formatted as background: "is believed to have", "likely began his career in". Worse than a cutoff disclaimer because it hides the gap. Cut or source it.

## Conversational-register tells

- **Chatbot artifacts:** "I hope this helps!", "Certainly!", "Feel free to reach out", "In this article, we will explore...". Remove.
- **Sycophantic tone:** "Great question!", "You're absolutely right!". Validation aimed at the reader rather than content.
- **Narrated candor:** announcing disclosure instead of disclosing: "Two caveats I would rather flag than let you discover later:", "To be fully transparent:". Apply the deletion test: cut the frame and see whether any information is lost. Carve-outs: the substantive admission itself, and conventional conflict-of-interest disclosure that carries a material fact. Judgment-only, since every regex tight enough to spare the carve-outs stopped matching the tell.
- **Acknowledgment loops:** "To answer your question", "The question of whether". Also opening a section by summarizing the previous one.
- **Recap-flattery openers:** summarizing someone's own work back at them with praise before getting to the point. One plain clause of thanks, then substance.
- **Wall-of-text replies:** in reply registers (issue comments, chat, DMs), roughly under 150 words with four or more sentences and no line break anywhere. Break at thought boundaries. Never fires on continuous long-form prose, where a dense paragraph is correct.
- **Reasoning chain artifacts:** "Let me think step by step", "Breaking this down", "Here's my thought process". Scaffolding the reader does not need.
- **Cutoff disclaimers:** "As of my last update", "I don't have access to real-time data". Never publish a sentence admitting the writer did not look something up.

## Social-post tells

- **Hashtag stuffing:** six or more hashtags on a short post, usually one specific tag mixed with broad category tags. Two or three specific tags maximum. Not counted: issue and PR references (`#88`), hex colors containing a digit, preprocessor directives, URL fragments, headings, and anything inside code.
- **Social endorsement closers:** "This one is worth your time:", "Bookmark this.", "Thank me later." The endorsement could sit under any link. Say what the thing is and who it is for, then drop the call to action.
- **Infomercial engagement hooks:** "The catch?", "Plot twist:", "Here's the thing." Mid-flow teasers that fake momentum. Delete the hook and state the thing. Same move in a fake-candid register: "Honestly?", "Real talk:" as standalone openers. Mid-sentence "honestly" is ordinary English.
- **Bullet lists of bare noun phrases:** five or more consecutive items, each a short adjective-plus-noun phrase with no verb. The tell is the symmetry: every item the same shape, none of them checkable. Rewrite items as full claims. Does not apply to changelog entries, todo lists, or parameter docs.
- **Manufactured punchlines:** three or more same-shape fragments in a row, each engineered to land like a closer. Keep the one that earns its emphasis and fold the rest into ordinary sentences.

## Machine fingerprints

These are deterministic publishing artifacts. A token proves a chat tool touched the text's pipeline, not who wrote the surrounding prose; treat each one as mandatory cleanup, never as an authorship verdict.

- **Unfilled placeholders:** `[Your Name]`, `[INSERT SOURCE URL]`, `2025-XX-XX`, HTML comments with placeholder verbs. Treat as a publishing bug.
- **Chat citation markup leaks:** `citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`, `grok_card`. Strip every token.
- **AI-tool URL parameters:** `utm_source=chatgpt.com`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`. Strip the AI-referrer tracking parameter from every URL that carries one, and leave the rest of the query string alone; a functional parameter (`?page=2`, `?v=4`) is not evidence of anything.

## Rhythm and structure

Structural regularity is the hardest signal to mask: a piece with every flagged word replaced and its rhythm untouched still reads as machine output. Weight rhythm above vocabulary when reviewing.

- **Sentence-length uniformity:** most sentences landing in the 15 to 25 word band sounds robotic. Mix three-to-eight word sentences with 20-plus word ones. Fragments work.
- **Paragraph-length uniformity:** vary deliberately. Some paragraphs should be one sentence.
- **Missing first-person perspective:** where the genre carries a voice, relentless neutrality is itself a tell.
- **Suspiciously clean grammar:** deliberate fragments, sentences opening with "And" or "But", and comma splices for effect belong to the author's voice. Keep them.
- **Over-polishing:** editing out every irregularity pushes human writing toward the machine profile. Applying every rule at maximum strictness manufactures the uniformity the skill exists to remove.
- **Read-aloud test:** text that a speech engine could read without sounding odd is probably too uniform.
- **Vocabulary diversity:** in pieces over 200 words, type-token ratio (distinct types over total tokens) usually lands near 0.50 to 0.65 in English prose. Below 0.40 is worth a second look on general prose. It is not proof: narrow topics, reference material, and second-language writing all compress vocabulary legitimately. The fix is to broaden the subject matter, not to run a thesaurus over it.
- **Diff-anchored writing:** docs that narrate a change instead of describing the thing: "this function was added to replace the previous approach". A reader without the commit history gets archaeology. Carve-out: changelogs, release notes, migration guides, and decision records are version-scoped by design.

## Writer-side tests

Judgment checks with no detectable surface form.

- **Paragraph-reshuffle immunity:** can two body paragraphs swap without breaking the piece? If order does not matter, it is a list of points rather than an argument that builds. The fix is structural.
- **Treadmill effect:** read each paragraph and ask what is new. If you could cut 40 to 60 percent and lose nothing, the prose is restating its premise in fresh words. Name the one fact or turn each paragraph contributes, or cut it.
- **Rewrite from scratch instead of patching** when five or more vocabulary flags, three or more distinct pattern categories, and uniform sentence and paragraph length all appear together.
