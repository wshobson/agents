Last verified: 2026-07-14

# Synthetic Data: Generation, Filtering, Distillation

Full detail backing `SKILL.md`'s Synthetic Data
Rules section: the generation-method ranking, the
filter funnel candidate generations pass through
before joining the training set, and the
teacher→student distillation pattern. Base models
are never named as recommendations here — `TEACHER`
and `STUDENT` are placeholders for whichever
checkpoints a given run uses; see
`finetuning-method-selection`'s
`references/model-catalog.md` for actual model
choice.

## Generation-Method Ranking

Methods below are ordered roughly weakest to
strongest for sample efficiency and downstream
quality at the same generation budget. Each level
subsumes the previous — a rejection-sampling
pipeline typically generates its candidates with
Magpie or persona-conditioned prompts underneath,
rather than replacing them:

1. **Self-Instruct** — bootstrap new prompts from a
   small seed set by having a model paraphrase and
   extend them. Cheapest, weakest: prompt diversity
   plateaus quickly and quality tracks the seed set
   closely.
2. **Evol-Instruct** — iteratively rewrite prompts
   to increase complexity (add constraints, deepen
   reasoning, broaden scope) across generations.
   Improves difficulty coverage over Self-Instruct
   but still seed-dependent.
3. **Magpie** — extract prompts directly from the
   target model's own chat-template prior by
   sampling from the template's user-turn position
   with no seed prompt at all. Removes seed-set bias
   entirely; this is why it's a workhorse rather
   than a niche technique.
4. **Persona-conditioned generation** — condition
   prompt generation on a sampled persona/role
   description to broaden style and topic coverage
   beyond what a single generation policy produces
   unconditioned.
5. **Rejection sampling / verifier-filtered** —
   generate multiple candidate completions per
   prompt and keep only those a filter, verifier, or
   judge accepts. This is the other workhorse from
   `SKILL.md`, and it composes with any of the
   prompt-generation methods above — it's a
   completion-side filter, not a prompt-generation
   method by itself.

**Targeted, student-aware generation** — steering
prompt or persona selection toward the current
student model's actual failure modes rather than
sampling uniformly — layers on top of any method
above and is what delivers the 1.3–2x sample
efficiency gain cited in `SKILL.md`. It requires an
eval signal on the student to know what its failure
modes currently are; without that signal, generation
defaults to untargeted/static.

## Filter Funnel

Apply filters in this order — each stage is
cheaper than the next, so cheap stages should
eliminate volume before expensive stages run on
what's left:

1. **Exact dedup.** Hash-based exact-match removal
   of identical rows (after normalization —
   whitespace/casing collapsed before hashing).
   Cheapest stage, run first, removes generation-loop
   repeats before anything downstream sees them.
2. **Semantic dedup (~0.92 similarity threshold).**
   Embed each candidate and drop rows whose
   nearest-neighbor cosine similarity to an
   already-kept row exceeds ~0.92. Catches
   paraphrase-level duplicates exact dedup misses.
3. **Length filter.** Drop candidates below a
   minimum or above a maximum token length for the
   task — too-short responses are usually degenerate,
   too-long ones are usually rambling or off-task.
4. **Language ID filter.** Drop candidates that
   fail a language-ID check against the target
   language(s) — generation occasionally drifts
   language, especially from multilingual base
   models on under-specified prompts.
5. **Score-based top-30% filter.** Score remaining
   candidates (reward model, heuristic, or
   self-consistency score) and keep roughly the
   top 30% — this is a coarse quality cut before the
   most expensive stage runs.
6. **Judge ≥ threshold.** Run the most expensive
   check last, on the smallest remaining set: an
   LLM-judge or human-equivalent quality check
   against a fixed threshold. Rows that fail here
   are dropped regardless of how they scored
   upstream.

The **10–30% typical accept rate** from `SKILL.md`
is the funnel's end-to-end yield across all six
stages, not any single stage's pass rate — budget
raw generation volume against the full-funnel yield,
not against any one stage's rate.

## Teacher→Student Distillation Pattern

1. **Generate teacher traces.** Sample completions
   (with reasoning traces, where applicable) from
   `TEACHER` against the target task's prompt
   distribution.
2. **Verify.** Run the traces through the Filter
   Funnel above — a distillation set is a synthetic
   dataset like any other and still needs the
   ≥25% real-data floor from `SKILL.md` respected
   in the final training mix, plus the same dedup
   and quality stages.
3. **SFT the student.** Train `STUDENT` on the
   verified traces using the standard SFT format
   and template rules from `SKILL.md` and
   `references/formats-and-templates.md` — a
   distillation dataset is not a special format,
   it's a provenance label on an otherwise-ordinary
   instruct or ChatML dataset.

Record `TEACHER` identity and generation
configuration (sampling temperature, prompt
template used to elicit traces) in the dataset
card's provenance field — "distilled from `TEACHER`"
is a provenance fact `/finetune` and downstream
audits both expect to find there, not something to
leave implicit.

## Replay-Mix Construction

The implementation recipe behind
`checkpoint-promotion`'s catastrophic-forgetting
escalation ladder (`SKILL.md`'s owning document for
*when* and *how far* to move the replay fraction —
this section covers *how to build the rows*, the
single most common REJECT remediation and the part
most often improvised ad hoc under time pressure).
Five decisions, in the order they come up:

### 1. General-Domain Source Selection

Pick a source that is genuinely general-domain for
the capability being protected, not a narrow slice
that happens to be convenient. Two failure modes to
avoid:

- **Don't teach to the gate.** If the replay source
  is drawn from the exact same distribution as the
  drift suite's benchmarks (e.g. the same GSM8K
  train split the drift suite's test split comes
  from), the resulting drift score partially
  measures "did this model see similar items in
  training," not "did fine-tuning preserve the
  underlying capability." This is not automatically
  disallowed — see `checkpoint-promotion`'s
  instruction-reuse disclosure rule — but it must be
  disclosed, and a broader source (not scoped to the
  drift suite's own benchmarks) is the more
  defensible default when one exists.
- **Match the source to the forgetting signature.**
  If error analysis on the failing checkpoint shows
  a specific lost capability (e.g. chain-of-thought
  math reasoning, not general knowledge), a replay
  source targeting that capability recovers it
  faster than a generic instruct-tuning mix — but
  narrows the "general-domain" claim; state in the
  dataset card which capability the replay mix
  targets and why.

### 2. Prompt Shape

Decide what shape replay rows take in the
messages-shaped SFT set — this is a real choice,
not a detail:

- **Natural instruction** — however the source
  data's own prompts are phrased. Lowest effort,
  least targeted.
- **The drift harness's exact phrasing** — matches
  the eval's instruction wording. Most directly
  addresses an instruction-following forgetting
  signature (e.g. "ignores the show-your-work
  instruction"), but triggers the instruction-reuse
  disclosure rule in `checkpoint-promotion` and
  inflates the post-replay score on that specific
  benchmark.
- **Bare input, no instruction wrapper** — closest
  to raw continued-pretraining signal; weakest at
  restoring instruction-following specifically.

Pick based on the forgetting signature from error
analysis, not by default — and disclose the choice
in the dataset card regardless of which one.

### 3. Answer Reformatting

Decide whether replay reference answers get
reformatted toward the target task's output
convention, or kept in the source format as-is.
Example: rewriting a math dataset's `#### N`
final-answer terminator to match the target
task's own extraction convention. This is a
judgment call that changes what the model learns
to emit on replay-domain prompts — record the
exact transformation applied (or "none — kept
source format") in the dataset card, since it
changes what a downstream error-analysis pass
should expect to see.

### 4. Val-Split Treatment

Decide whether the validation split gains replay
rows or stays task-only:

- **Task-only val split** keeps `eval_loss` directly
  comparable across runs that only differ in replay
  fraction — the training loop has zero visibility
  into replay fit, and replay recovery is only
  measurable at the next Phase 5 re-gate.
- **Replay rows in val too** gives in-loop visibility
  into replay fit, at the cost of `eval_loss` no
  longer being an apples-to-apples comparison against
  a prior run's task-only val split.

Neither is universally correct; state which was
chosen and why in the dataset card, and don't
compare `eval_loss` across runs that made different
choices here without noting the confound.

### 5. Disjointness Verification

Before training, verify replay rows don't overlap
the drift suite or the goldens set — required, not
optional, regardless of which source was picked in
step 1:

- **Split-level separation** — draw replay rows only
  from a source split (e.g. a train split) disjoint
  from whatever split the drift suite's items are
  drawn from.
- **Exact-match text filter** — normalize and
  exact-match replay row question/prompt text
  against the drift suite's selected items and
  `eval/goldens.jsonl`; drop any hit. Record the
  overlap count found (expect 0) in the dataset card
  — a nonzero count found and silently dropped is
  still worth recording, since it signals the source
  pool needs a tighter split boundary next time.

### When a Later Run Changes the Replay Fraction: Swap, Don't Add

If a checkpoint-promotion gate calls for moving the
replay fraction (see `checkpoint-promotion`'s
escalation ladder), implement the change by **swapping
rows, not adding them**: drop target-task rows out of
the training set as replay rows go in, so the total
row/step count holds constant between the old and new
run. Adding replay rows on top of the existing set
changes replay fraction and total optimizer steps in
the same move, making it impossible to attribute a
later drift-score change to either variable alone —
this confound has produced misleading run-to-run
trajectories in practice, so treat swap-not-add as a
hard rule for this recipe, not a style preference.

**Row count is not token count.** Swapping rows
1-for-1 holds the *row* count constant, but replay
rows and target-task rows are rarely the same length —
a swap can still shift total training tokens (and
therefore `max_steps` under a fixed batch size and
sequence-packing scheme) even though the row count
didn't move. Hold total training tokens, or `max_steps`
directly, constant between the old and new run — not
just row count — and record the packed-token count
for each run (not just the row count) in the dataset
card before attributing a drift-score change to the
replay-fraction change alone. A run that swapped rows
but grew packed tokens 10% has the same attribution
problem as one that added rows outright.

## Synthetic-Only Datasets and the ≥25% Real Floor

`SKILL.md`'s Synthetic Data Rules require ≥25% real
data as a collapse guard. When a training set is
100% synthetic by construction (a greenfield task
with no real-data pool to draw from at all — not
merely a lot of synthetic augmentation on top of a
real base), that floor is unmeetable by definition
unless something in the mix counts as "real."

**Resolution: general-domain replay rows count
toward the ≥25% floor.** "Real" in this rule means
"not generated for this specific task from this
specific student model" — a replay row pulled from
an existing general-instruct dataset (human-authored
or otherwise pre-existing, not freshly generated by
the student or its teacher for this run) satisfies
that definition even though the target-task rows
around it are 100% synthetic. Build the replay mix
per the five decisions above, then compute the
synthetic/real ratio the dataset card requires
treating replay rows as the "real" share — and state
explicitly in the card that this is how the ratio
was met, so a later audit doesn't misread an
all-synthetic-target-data run as having silently
skipped the collapse guard.
