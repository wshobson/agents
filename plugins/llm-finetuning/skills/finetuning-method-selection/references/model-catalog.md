# Model Catalog

Last verified: 2026-07-14
Refresh checklist: (1) check Unsloth supported-models page, (2) check the current open-weights leaderboards for each size class, (3) update rows + bump this date. Refresh at least quarterly; this file is the ONLY place base models are named in the llm-finetuning and dgx-spark-ops plugins.

## How to Read This Table

Pick the row matching the target parameter count,
then read across: a text recommendation, a vision
(VLM) recommendation for the same size class, what
that class can do on a single DGX Spark, and any
notes that change the recommendation. Cross-check
the "last verified" date above before trusting a
row — if it's stale, work the refresh checklist
first.

## Catalog (2026-07)

| Size class | Text recommendation | Vision recommendation | Spark feasibility | Notes |
|---|---|---|---|---|
| ≤4B | Qwen3 4B class | SmolVLM / Gemma 3 4B | Full fine-tune feasible | Smallest class where full FT is still *feasible* by default — a hardware/size-class note, not a method recommendation. Method choice (LoRA vs. full FT) is `lora-qlora-recipes`'s LoRA vs QLoRA vs Full FT table, routed by task shape (demonstrations vs. dense knowledge injection); that table governs over this feasibility note whenever the two appear to disagree. |
| 7–9B | Qwen3 8B, Llama-class 8B | Qwen2.5-VL-7B | Full fine-tune ceiling | Above this class, full FT stops being the default on Spark — see 12–32B row. |
| 12–32B | Qwen3 14B/32B, Gemma 3 27B | Qwen2.5-VL-32B | LoRA-only; 27B is the LoRA ceiling at pack≤1024 | 27B is the largest dense model that fits a LoRA run on a single Spark in practice. |
| 70B+ | Llama 3.3 70B class | Use the 12–32B vision class instead — no 70B+ VLM recommendation at this size | QLoRA-only, ≈40GB, 30–48h for 3 epochs | bf16 is not feasible at this class on a single Spark; QLoRA is the only path in. |
| 100B+ MoE | gpt-oss-120b class | Use the 12–32B vision class instead — no 100B+ MoE VLM recommendation at this size | NVFP4-native LoRA via community recipe (`nvfp4-lora-spark`), experimental | Not the default assumption for other 100B+ MoE models — verify per-model before relying on this row. |

## Vision Model Notes

- **LLaVA is legacy.** Do not recommend it for new
  work; it is listed here only so a stale
  recommendation can be recognized as such.
- **InternVL3.5 MoE variants are the MoE VLM
  alternative** to the dense Qwen2.5-VL / Qwen3-VL
  and Gemma 3 vision models above, for cases that
  specifically call for a mixture-of-experts
  vision-language architecture — InternVL3.5 also
  ships dense checkpoints, so pick the MoE variant
  explicitly rather than assuming every InternVL3.5
  release is MoE.
