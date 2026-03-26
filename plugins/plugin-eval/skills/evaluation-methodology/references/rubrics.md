# Judge Rubrics — Anchored Scoring Reference

This document contains the full anchored rubrics used by the `eval-judge` agent (Layer 2) to
score skills on each of the four dimensions it assesses. Each dimension uses a 0.0–1.0 scale
with five anchor points. The judge interpolates between anchors based on the evidence gathered
from reading SKILL.md and any `references/` files.

These rubrics are the authoritative scoring standard. When calibrating expectations, filing
score disputes, or training new judge models, use these anchors as ground truth.

---

## Dimension 1 — Triggering Accuracy

**Weight in composite:** 0.25 (highest)

**Layer blend (deep depth):** static 15%, judge 25%, Monte Carlo 60%

### What is being measured

Triggering accuracy measures whether the skill's `description` field in the frontmatter
causes Claude Code to invoke the skill at the right times. A skill with perfect triggering
accuracy fires on every prompt that genuinely needs it (high recall) and never fires on
prompts where it is irrelevant (high precision). The score is conceptually the F1 of
precision and recall across a representative prompt distribution.

### How the judge scores it

The judge generates 10 mental test prompts: 5 that should trigger the skill and 5 that
should not. It assesses whether the description would lead Claude Code's routing model to
activate (or not activate) for each prompt. The F1 score of this 10-prompt evaluation
becomes the dimension score.

The judge also considers whether the description provides actionable trigger signals rather
than just naming or describing the skill in passive terms.

### Anchored Rubric

**0.0 – 0.19 (Grade F) — Unusable trigger**

The description is absent, empty, or so vague that it provides no routing signal. Examples:
- Description is under 10 characters
- Description is just the skill name: "evaluation-methodology"
- Description describes what the skill is, not when to use it: "A skill about evaluation"
- Description uses entirely passive language with no conditional framing

A skill at this level will almost never be autonomously invoked. It may be invoked if the
user explicitly names it, but that defeats the purpose of a plugin ecosystem.

**0.20 – 0.39 (Grade F/D) — Weak trigger**

The description exists and is somewhat meaningful but has major gaps:
- Mentions the domain but lacks trigger phrases ("Use when..." or similar)
- Trigger language is present but maps to only one narrow use case
- Description would trigger the skill on clearly wrong prompts (precision failure)
- Description would miss 3+ of the 5 should-trigger test prompts (recall failure)

Example of a 0.30-scoring description:
> "PluginEval quality methodology — dimensions, rubrics, statistical methods."

This names the topic but provides no trigger signal. The routing model cannot infer when
to use it.

**0.40 – 0.59 (Grade D/C) — Partial trigger**

The description has some trigger signal but is imprecise:
- Contains "Use when" but only one specific context
- Would correctly handle 3 of 5 should-trigger prompts
- Some false positives — would fire for adjacent but wrong use cases
- Trigger phrase is generic ("Use when working with evaluations") rather than specific

Example of a 0.50-scoring description:
> "PluginEval quality methodology — dimensions, rubrics. Use when understanding evaluation."

Better — has a trigger phrase — but "understanding evaluation" is too generic. It would
catch some legitimate uses but also fire for unrelated evaluation tasks.

**0.60 – 0.79 (Grade C/B) — Good trigger**

Description clearly identifies when to invoke the skill with only minor gaps:
- Contains "Use when..." or "Use this skill when..." with at least two specific contexts
- Would correctly handle 4 of 5 should-trigger prompts
- Precision is good (few false positives)
- May miss edge-case trigger scenarios not explicitly listed

Example of a 0.70-scoring description:
> "PluginEval quality methodology. Use this skill when understanding how plugin quality is
> measured or when interpreting evaluation results."

Good — two explicit trigger contexts — but misses calibration and stakeholder scenarios.

**0.80 – 1.00 (Grade A/B) — Excellent trigger**

Description is precise and comprehensive:
- Contains "Use when..." or "Use this skill when..." with 3+ specific, distinct contexts
- Would correctly handle all 5 should-trigger prompts
- Would correctly NOT trigger on all 5 should-not prompts
- Contexts are concrete and discriminative (not "when evaluating" but "when interpreting
  dimension scores and letter grades" or "when calibrating scoring thresholds")
- Optionally includes "proactively" for skills that should auto-activate

Example of a 0.90-scoring description:
> "PluginEval quality methodology — dimensions, rubrics, statistical methods. Use this skill
> when understanding how plugin quality is measured, interpreting evaluation results,
> calibrating scoring thresholds, or explaining quality badges to stakeholders."

Four specific, distinct contexts. Fires on exactly the right prompts.

### Good Trigger Description Patterns

- Start with a one-sentence summary of what the skill covers
- Follow immediately with "Use this skill when..." and list 3+ concrete scenarios
- Name specific technologies, output types, or file formats when relevant
- Disambiguate from adjacent skills (e.g., "when *interpreting* results, not when *running*
  evaluations — use the eval command for that")
- Keep the total description under 200 characters for clean display in the CLI

### Common Mistakes

- Using "Use when interpreting results" — too generic; results of what?
- Listing only one trigger context — needs 3+ to score above 0.70
- Passive descriptions ("This skill covers...") that never state when to use the skill
- Combining trigger and description without separating them clearly

---

## Dimension 2 — Orchestration Fitness

**Weight in composite:** 0.20 (second highest)

**Layer blend (deep depth):** static 10%, judge 70%, Monte Carlo 20%

### What is being measured

Orchestration fitness measures whether a skill behaves as a pure worker in the
agent → skill hierarchy. A skill should receive a delegated task, execute it using its
own instructions, and return structured output. It should NOT:
- Make decisions about which other tools or skills to call
- Manage multi-step workflows across multiple agents
- Act as a supervisor that delegates to sub-workers
- Contain conditional orchestration logic

This dimension is almost entirely judge-assessed (70% judge weight) because static analysis
cannot reliably detect orchestration intent from surface patterns alone.

### How the judge scores it

The judge reads the SKILL.md in full and asks: does this skill's instruction set define
a worker (receives task → executes → returns output) or an orchestrator (plans → delegates
→ aggregates)? It looks for specific signals in both directions.

**Worker signals (positive):**
- Documents what it receives (inputs/parameters)
- Documents what it returns (output format, structure)
- Instructions are self-contained execution steps
- Code blocks show the skill doing work, not calling other skills
- Scoped, focused responsibilities

**Orchestrator signals (negative):**
- Uses words like "orchestrate", "coordinate", "dispatch", "delegate", "manage workflow"
- Contains logic like "if X, call skill Y; if Z, call agent W"
- Describes itself as a "supervisor" or "orchestrator"
- Output is routing decisions rather than execution results
- References multiple external agents by name in a decision tree

### Anchored Rubric

**0.0 – 0.19 (Grade F) — Standalone agent**

The skill is written as a fully autonomous agent that manages its own tool calls,
sub-task delegation, and workflow coordination. It has no defined input/output contract.
It reads like an agent system prompt, not a worker instruction set.

Example characteristics:
- "You will first assess the situation, then call the appropriate specialist..."
- Dispatches to other skills based on internal logic
- Has no "Input:" or "Output:" sections
- Describes a complete agentic loop

**0.20 – 0.39 (Grade F/D) — Mixed roles**

The skill mixes worker and orchestrator responsibilities. It does some work itself but
also contains orchestration logic. The boundaries are unclear.

Example characteristics:
- Has an output format but also contains "if the user asks for X, also invoke Y"
- Worker sections mixed with supervisor-style conditional routing
- Returns both results and routing recommendations
- Ambiguous whether it executes or coordinates

**0.40 – 0.59 (Grade D/C) — Functional worker with structural issues**

The skill is mostly a worker but the output format is not structured for supervisor
consumption. The calling agent cannot easily parse or route on the output.

Example characteristics:
- Produces narrative/prose output rather than structured data
- No explicit output format documentation
- Assumes the calling agent "just knows" what to do with the result
- Instructions are adequate for execution but not for composability

**0.60 – 0.79 (Grade C/B) — Clean worker, minor gaps**

The skill functions as a clean worker. Inputs and outputs are documented. The instructions
produce output that a supervisor agent can consume. Minor issues remain.

Example characteristics:
- Has input and output documentation, but output schema could be more explicit
- Instructions are worker-style throughout with only one or two ambiguous lines
- Code blocks show worker behavior but coverage is incomplete
- No orchestration language but also no explicit composability design

**0.80 – 1.00 (Grade A/B) — Pure worker**

The skill is a composable, contract-defined worker. It is clear what it takes in and what
it produces. The output format is specified in a way that a calling agent can rely on.

Example characteristics:
- Explicit "## Input" and "## Output" or "## Returns" sections
- Output format is structured (JSON schema, typed fields, or clearly specified markdown)
- Instructions are execution steps with no decision-tree routing to external services
- Code blocks demonstrate realistic worker behavior
- Skill is designed to be called repeatedly with different inputs

### Good Signals vs. Bad Signals

**Good signals (push score up):**
- Documents expected inputs and output format explicitly
- Produces artifacts a supervisor agent can consume without parsing prose
- Uses imperative instructions ("Analyze X and return Y"), not conditional delegation
- Has 2+ code blocks showing concrete worker behavior
- Output format section uses a schema, template, or typed field list

**Bad signals (push score down):**
- Contains "orchestrate", "coordinate", "dispatch" in instruction text
- References other skills as execution dependencies (not just "see also")
- Manages multi-step workflows that span multiple tool boundaries internally
- Output is described as "a comprehensive report" with no structure specification
- Skill tells the model to "decide" what to do next rather than do the work

### Common Mistakes

- Documenting what the skill "does" without specifying what it "returns"
- Including "Related skills" sections that imply the skill will call them
- Writing instructions as if the skill controls the entire conversation
- Mixing the worker's execution logic with stakeholder communication steps

---

## Dimension 3 — Output Quality

**Weight in composite:** 0.15 (third highest)

**Layer blend (deep depth):** static 0%, judge 40%, Monte Carlo 60%

### What is being measured

Output quality measures whether the skill's instructions would guide Claude to produce
correct, complete, and useful output across a representative range of real-world tasks.
This dimension is entirely empirical — static analysis cannot assess whether instructions
will produce quality outputs, so the layer blend is 0% static.

At deep depth, Monte Carlo simulation (60% blend) produces actual outputs from real prompts
and scores them. At standard depth (judge only), the judge simulates three tasks mentally.

### How the judge scores it

The judge selects three realistic tasks that the skill is designed to handle — varying from
simple to complex. For each task, it mentally executes the skill's instructions and assesses
whether the resulting output would be:
- **Correct** — factually accurate, technically valid
- **Complete** — covers all aspects the task requires
- **Useful** — actionable, well-formatted, appropriate length

The average across three tasks becomes the dimension score.

### Anchored Rubric

**0.0 – 0.19 (Grade F) — Instructions produce incorrect output**

Following the skill's instructions would lead Claude to produce wrong answers or actively
harmful output. The instructions contain factual errors, logical contradictions, or
directives that produce the opposite of the intended result.

Example characteristics:
- Incorrect formulas or algorithms presented as correct
- Contradictory instructions that cannot both be followed
- Instructions that assume wrong tool behaviors
- Missing critical information that would cause systematic failure

**0.20 – 0.39 (Grade F/D) — Incomplete, major gaps**

Instructions produce output for simple cases but fail on anything non-trivial. Major aspects
of the skill's domain are unaddressed. A user following this skill would get partial help
for basic requests and no help for moderate complexity.

Example characteristics:
- Handles the "hello world" case but not any realistic variant
- Critical decision points have no guidance (the model must guess)
- Output format is undefined — model produces inconsistent structure
- No examples to calibrate expected quality

**0.40 – 0.59 (Grade D/C) — Adequate for basic cases**

Instructions produce reasonable output for straightforward tasks but struggle with any
complexity. The skill is usable but requires the user to fill in significant gaps.

Example characteristics:
- Basic case is well-handled; complex case guidance is thin or absent
- Output format is suggested but not enforced
- Edge cases are not addressed — model must improvise
- Examples are present but only cover the simplest scenario

**0.60 – 0.79 (Grade C/B) — Good for most cases**

Instructions produce quality output for the majority of realistic tasks. A few edge cases
or complex scenarios may be handled suboptimally but the core use cases work well.

Example characteristics:
- Three or more concrete examples covering varied complexity
- Output format is clearly specified
- At least one edge case addressed explicitly
- Instructions are actionable and specific, not just descriptive
- Output would be correct and useful for 80%+ of real invocations

**0.80 – 1.00 (Grade A/B) — Excellent across the board**

Instructions are comprehensive, specific, and produce high-quality output for even complex
or edge-case tasks. The skill represents a genuine expertise distillation.

Example characteristics:
- Examples cover simple, moderate, and complex cases
- Output format is precisely specified with schema or template
- Multiple edge cases addressed with specific handling guidance
- Instructions are expert-level — they encode domain knowledge, not just procedure
- A user following the instructions would produce output comparable to an expert
- Troubleshooting guidance is provided for failure modes

### Judge Checks for Output Quality

When assessing code examples and technical instructions, the judge verifies:
- All code blocks are syntactically correct and would run without modification
- Workflows are shown end-to-end, not as fragments requiring integration
- Error handling is included for the most common failure modes
- APIs referenced are current (not deprecated in the skill's target environment)
- Version constraints are stated when the skill targets a specific library version

### Common Mistakes

- Describing what good output looks like without explaining how to produce it
- Providing examples of output without explaining the reasoning behind them
- Instructions that are too vague to follow ("produce a comprehensive analysis")
- Missing error handling — what should the skill do when the input is malformed?
- Using placeholder pseudocode instead of real, runnable examples

---

## Dimension 4 — Scope Calibration

**Weight in composite:** 0.12 (fourth highest)

**Layer blend (deep depth):** static 30%, judge 55%, Monte Carlo 15%

### What is being measured

Scope calibration measures whether the skill is the right size for its purpose. Too thin
(stub) and it provides no value. Too broad (bloated) and it wastes tokens, confuses the
model, and overlaps with sibling skills. The ideal skill is exactly as large as it needs
to be — comprehensive for its defined domain, not a line longer.

This dimension requires human judgment (55% judge blend) because "right size" is
context-dependent. A skill covering a complex framework legitimately needs more content
than a skill covering a simple utility function.

### How the judge scores it

The judge assesses scope by asking:
1. Does the skill cover all the important aspects of its stated domain?
2. Does it cover anything outside its stated domain?
3. Is the depth appropriate — neither superficial nor excessively detailed?
4. Is the content density high (every line earns its place) or padded?

The judge also considers the skill's category (reference documentation, workflow assistant,
code generator, etc.) when calibrating expectations.

### Anchored Rubric

**0.0 – 0.19 (Grade F) — Stub**

The skill is a placeholder. It has a name and description but the body contains less than
50 lines or covers fewer than half of its stated domain. Someone invoking this skill
would receive fragmentary guidance insufficient to complete any real task.

Example characteristics:
- Fewer than 50 lines total
- Body is a bulleted list of topics without elaboration
- The description promises more than the content delivers
- A competent practitioner would need to fill in all the gaps themselves

**0.20 – 0.39 (Grade F/D) — Too narrow**

The skill covers its domain but only the surface layer. Important aspects exist but are
mentioned without sufficient depth to be actionable. The skill is not a stub but it is
thin enough that users will frequently run into unaddressed scenarios.

Example characteristics:
- 50–100 lines covering 2–3 of the skill's 6+ important aspects
- Core happy path is documented; anything unusual is missing
- No examples or only one trivial example
- Useful as a starting point but not as a self-sufficient reference

**0.40 – 0.59 (Grade D/C) — Slightly off-scope**

The skill is either moderately under-scoped (missing a few important aspects) or slightly
over-scoped (includes content that belongs in a different skill). The content that exists
is reasonable in quality but the overall package is not well-calibrated.

Example characteristics:
- Under-scoped: Covers most aspects but one or two important ones are absent or cursory
- Over-scoped: Includes content that duplicates a sibling skill or is only tangentially
  related to the skill's stated domain
- May be the right total size but wrong distribution of content across topics

**0.60 – 0.79 (Grade C/B) — Well-scoped with minor issues**

The skill covers its domain well. Important aspects are addressed at appropriate depth.
One or two gaps remain, or there is a small amount of tangential content, but these are
minor issues.

Example characteristics:
- 80–90% of the important aspects covered at useful depth
- A practitioner could complete most tasks using only this skill
- Any content outside the core domain is clearly supporting material, not distraction
- Minor gaps would affect fewer than 20% of invocations

**0.80 – 1.00 (Grade A/B) — Perfectly calibrated**

The skill is exactly what it needs to be. It covers all important aspects of its domain
at the right depth, with no padding and no gaps. Every section earns its place. The skill
could be used as a reference implementation for its category.

Example characteristics:
- Comprehensive coverage of all important aspects without redundancy
- Each section directly supports completing the skill's stated purpose
- Appropriate use of `references/` for supporting material that doesn't belong in the
  main execution path
- Content density is high — no filler, no repetition
- Would satisfy a senior practitioner working on a complex variant of the skill's task
- Serves as a model for what this category of skill should look like

### Skill Category Calibration Norms

Scope expectations vary by skill category. Use these as baseline calibration guides:

| Category | Target lines (SKILL.md) | Pattern |
|---|---|---|
| Reference / Documentation | 200–500 | Deep coverage + references/ for extended material |
| Workflow / Process | 150–300 | Step-by-step + decision points + worked example |
| Code generator | 100–200 | Instructions + references/ for templates |
| Diagnostic / Debugging | 200–400 | Decision trees + failure modes + procedures |
| Integration / Configuration | 150–350 | Setup + options + copy-paste examples |
| Coordination / Planning | 100–200 | Decisions + checklists + handoff protocol |

### Common Mistakes

- Writing a stub and planning to "expand later" — submit when the content is ready
- Including content that belongs in a sibling skill to inflate scope
- Treating a narrowly-scoped skill as too thin — a single-purpose utility skill can
  be 100 lines and perfectly calibrated
- Over-explaining background theory that the model already knows — focus on the
  domain-specific guidance the model cannot infer from training data alone
- Adding filler headings ("Overview", "Introduction") that restate the description
  without adding actionable content

---

## Rubric Calibration and Consistency

### Inter-Judge Agreement

When running with `judges > 1`, PluginEval reports Cohen's kappa to measure agreement
between judge instances. Target kappa ≥ 0.70 for a stable, well-defined skill.

| Kappa range | Interpretation |
|---|---|
| ≥ 0.80 | Strong agreement — skill is clearly written |
| 0.60 – 0.79 | Moderate agreement — skill has some ambiguous sections |
| 0.40 – 0.59 | Fair agreement — skill needs clarity improvements |
| < 0.40 | Poor agreement — skill is ambiguous or judges are not calibrated |

Low kappa on a specific dimension points to the area needing clarification. Low
triggering_accuracy kappa usually means the description maps to multiple different
interpretations of when to use the skill.

### Calibration Corpus

The gold corpus (initialized via `plugin-eval init`) provides Platinum and Gold-badged
skills as calibration anchors. Before running a batch evaluation, compare your expected
scores against one or two corpus entries to verify your judge is calibrated correctly.

If your judge consistently scores a known Platinum skill below 85 on any dimension, check
for model version drift or prompt injection in the skill content that may be confusing the
judge.

### Score Drift Across Model Versions

Judge model upgrades can shift scores by ± 5–10 points on subjective dimensions
(output_quality, scope_calibration). After any model upgrade, re-certify the top 10 corpus
entries to establish new baseline calibration. If drift exceeds 5 points on any dimension,
update the anchored examples in this rubric document to reflect the new model's scoring
behavior.
