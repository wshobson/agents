Last verified: 2026-07-13

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
   of identical or near-identical rows. Cheapest
   stage, run first, removes generation-loop repeats
   before anything downstream sees them.
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
