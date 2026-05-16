---
name: recsys-pipeline-architect
description: Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced X For You algorithm. Use when building any system that picks "the top K items for a (user, context)" — content feeds, search ranking, RAG rerankers, task prioritizers, notification triage, ad selection.
---

# Recsys Pipeline Architect

A spec-and-scaffold skill for building composable recommendation, ranking, and feed pipelines. Encodes the six-stage pattern popularized by xAI's open-sourced [For You algorithm](https://github.com/xai-org/x-algorithm) (Apache 2.0) and applies it to any "top K for (user, context)" problem.

## Overview

Most "recommendation systems" in production aren't exotic ML — they're *pipelines*: fetch candidates from one or more sources, enrich them with metadata, drop the ineligible, score the rest, sort and pick the top K, then fire async side effects. The pattern is universal. The scoring function and the items change; the pipeline shape doesn't.

This skill is an independent reimplementation of the pattern (MIT) — no code copied from the original.

## When to Use This Skill

- Building any system that returns "the top K items for a user/context"
- Designing or refactoring a personalized feed (content, search results, notifications)
- Wrapping an LLM/ML scorer in proper pipeline plumbing (sources, hydration, filters, side effects)
- Adding multi-action prediction with tunable weights (instead of a single relevance score)
- Building a RAG retrieval reranker (cheap retrieval → expensive rerank)
- Designing a task prioritizer or alert triage system

## The Six-Stage Framework

| # | Stage | Job | Parallel? |
|---|---|---|---|
| 1 | **Source** | Fetch candidates from one or more origins | Yes — multiple sources run in parallel |
| 2 | **Hydrator** | Enrich candidates with metadata needed for filtering and scoring | Yes — independent hydrators run in parallel |
| 3 | **Filter** | Drop ineligible candidates (blocked, expired, duplicate, ineligible) | Sequential — each filter sees fewer items |
| 4 | **Scorer** | Assign each surviving candidate one or more scores | Sequential — later scorers see earlier scores |
| 5 | **Selector** | Sort by final score, return top K | Single op |
| 6 | **SideEffect** | Cache, log, emit events, update served-history | Async — must never block the response |

### Why this exact order

- Sources before hydration: know what candidates exist before paying to enrich
- Hydration before filtering: many filters need metadata the source didn't provide
- Filtering before scoring: scoring is the expensive stage — drop the ineligible first
- Scorer chain (not single scorer): real systems compose ML scoring + diversity reranking + business rules
- Selector after scoring: keeps scoring deterministic and cacheable
- SideEffects last and async: side effects must never block the user response

## Workflow When Invoked

Walk the user through eight steps:

1. **Clarify the use case** (one round, three questions only if missing): items being ranked, input context, language/runtime
2. **Identify the candidate sources** (usually in-network + out-of-network, but single-source also valid)
3. **List required hydrations** — for each filter and scorer, what data does it need that the source didn't provide?
4. **List the filters** — cheap before expensive, universal before user-specific (duplicate, self, age, block/mute, previously-served, eligibility)
5. **Design the scorer chain** — primary ML/heuristic → combiner (multi-action with weights) → diversity → business rules
6. **Selector** — sort descending by final score, take top K (or stratified mix)
7. **SideEffects** — cache served IDs, emit impression events, update counters, log analytics; all fire-and-forget
8. **Generate the scaffold** in the user's stack

## Key Trade-offs to Surface

Never default silently on these — they are product decisions disguised as technical ones.

### 1. Single score vs multi-action prediction

- **Single score:** train one model to predict relevance. To change behavior → retrain.
- **Multi-action:** predict `P(action)` for many actions (`P(read)`, `P(like)`, `P(share)`, `P(skip)`, `P(report)`), combine with weights at serving time. To change behavior → change weights. No retraining.

The X For You algorithm uses multi-action with both positive and negative weights. Recommend multi-action when the user expects to tune frequently.

### 2. Candidate isolation vs joint scoring

- **Isolated:** each candidate scored independently. Deterministic, cacheable.
- **Joint:** candidates attend to each other during scoring (e.g., transformer over the whole batch). More expressive but non-deterministic across batches.

Default to isolation. Joint only when there's a specific reason (e.g., explicit batch-aware diversity).

### 3. Online vs offline batch

- **Request-time (online):** pipeline runs on each request. Latency budget: 100–300ms.
- **Pre-computed (offline batch):** pipeline runs periodically, results cached. Lower latency, lower freshness.
- **Hybrid:** candidate retrieval offline, ranking online.

## Hard Rules

1. **Do not invent benchmark numbers.** "How fast is this?" → "depends on workload, run it yourself."
2. **Attribution discipline.** Attribute the pattern as "popularized by xAI's open-sourced For You algorithm" / `github.com/xai-org/x-algorithm` (Apache 2.0).
3. **No trademark use.** Don't name the user's artifact "X-like" or use "For You" branding. Use neutral names: "candidate pipeline", "feed pipeline", "ranking pipeline".
4. **Surface trade-offs.** Multi-action vs single, isolation vs joint, online vs offline — never default silently.
5. **The generated scaffold must run.** No pseudocode passing as code.
6. **Filter order matters.** Cheap before expensive. Universal before user-specific.
7. **Side effects never block.** Wrap in fire-and-forget patterns (goroutines / promises without await / asyncio tasks).

## Anti-Patterns

- ❌ Scoring before filtering (wastes compute on candidates that will be dropped)
- ❌ Synchronous side effects (cache writes / impression emits blocking the response)
- ❌ A single "relevance" score when the product needs multi-objective tuning
- ❌ Joint scoring as default (non-deterministic, uncacheable, doesn't compose with reranking)
- ❌ Pseudocode "for illustration" — the scaffold must actually run

## Common Use Cases

### Content feed (Strapi v5 plugin, TypeScript)

User has a CMS with 50k articles, wants a personalized "for you" feed. Walk through 8 steps → generate a Strapi plugin scaffold with multi-action scoring, author diversity, standard filters, async side-effect lane.

### RAG retrieval reranker (Python async)

User's RAG returns top-50 chunks from a vector DB, wants to rerank with a more expensive scorer and return top-5. Single-source pipeline with a scorer chain (cheap retrieval + expensive rerank).

### Task prioritizer (FastAPI service)

User has a queue of incoming task suggestions, wants to rank by "what should this user work on next" considering their past patterns. Items reversed (tasks instead of content), same shape applies.

### Notification triage (offline-batch job)

User wants a daily digest that picks the top 10 from the last 24h queue. Offline-batch pipeline. Source = queue, filters = age/dedup/eligibility, scorer = urgency × user-affinity, selector = top 10, side effect = email send (still async).

## Upstream

This skill is a single-file adapter for the upstream repository, which ships 5 load-on-demand reference docs and 3 runnable example scaffolds (Strapi v5 / Go / Python — every one green on its test suite, 9/9 tests total).

- **Upstream:** https://github.com/mturac/recsys-pipeline-architect
- **Release:** v0.1.0 (MIT)
- **References:** interfaces in 4 languages (TS/Go/Python/Rust), multi-action scoring, candidate isolation, filter cookbook (12 patterns), scorer cookbook
- **Cross-platform install:** `npx skills add mturac/recsys-pipeline-architect`
