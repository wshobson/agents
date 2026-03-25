---
name: evaluation-methodology
description: "PluginEval quality methodology — dimensions, rubrics, statistical methods. Use when understanding how plugin quality is measured or when interpreting evaluation results."
---

# Evaluation Methodology

## Quality Dimensions (Ranked by Weight)

1. **Triggering accuracy (0.25)** — Does the skill fire when it should?
2. **Orchestration fitness (0.20)** — Works as a worker in agent→skill hierarchy?
3. **Output quality (0.15)** — Consistent, correct results?
4. **Scope calibration (0.12)** — Right depth and breadth?
5. **Progressive disclosure (0.10)** — SKILL.md lean, depth in refs?
6. **Token efficiency (0.06)** — Minimal context waste?
7. **Robustness (0.05)** — Handles edge cases?
8. **Structural completeness (0.03)** — Right sections present?
9. **Code template quality (0.02)** — Working examples?
10. **Ecosystem coherence (0.02)** — Cross-references, no duplication?

## Three Evaluation Layers

- **Layer 1 (Static):** Deterministic analysis, <2 seconds, no LLM
- **Layer 2 (LLM Judge):** G-Eval style rubric assessment via Agent SDK
- **Layer 3 (Monte Carlo):** N simulated invocations with statistical CIs

## Statistical Methods

- **Wilson score interval:** Triggering activation rate CIs
- **Bootstrap resampling (1000x):** Output quality CIs
- **Clopper-Pearson exact:** Failure rate CIs
- **Cohen's kappa:** Inter-judge agreement
- **Elo/Bradley-Terry:** Pairwise ranking against gold corpus

## Quality Badges

| Badge | Composite | Elo | Meaning |
|-------|-----------|-----|---------|
| Platinum | 90+ | 1600+ | Reference quality |
| Gold | 80+ | 1500+ | Production ready |
| Silver | 70+ | 1400+ | Functional, needs improvement |
| Bronze | 60+ | 1300+ | Minimum viable |
