---
name: spark-memory-thermal-ops
description: Manage unified memory and thermals during long-running ML jobs on NVIDIA DGX Spark. Use when planning memory headroom for a training run on GB10, when a job OOMs on unified memory, or when monitoring temperature and power during multi-hour training.
---

# Spark Memory & Thermal Ops

DGX Spark's GB10 chip has one 128GB unified
memory (UMA) pool shared by CPU and GPU, and a
sustained power ceiling well below its rated
figure. Both break discrete-GPU assumptions:
headroom isn't what `nvidia-smi` reports, and a
run that starts fast will slow down mid-job
with nothing misconfigured. This skill covers
planning memory headroom, working an actual
OOM, and watching thermals across a long job.
For launch-time failure modes (ABI mismatches,
flash-attn, playbook breakage), see
`spark-training-gotchas` — this skill assumes
the job starts.

## Common Issues Quick Reference

| Situation | Do this |
|---|---|
| Planning headroom before launch | Budget against `free -g`, not `nvidia-smi` — see UMA Memory Model |
| Job OOMs on unified memory | Work the OOM Ladder in order: flush, then batch/pack, then method downgrade |
| Throughput drops mid-run | Check the power/temp log before assuming a config bug — see Thermal Monitoring |
| Trainer + inference server both wanted | Run one at a time — see Concurrent Workloads |

## When to Use This Skill

- Sizing a training run against the 128GB pool
  before launch — will this model, method, and
  batch/pack combination fit.
- A run OOMs mid-load or mid-step and the
  remediation order matters — what to try first,
  second, third.
- Watching temperature and power during a
  multi-hour job, deciding whether a slowdown is
  thermal throttling or something else.
- Planning to run a trainer alongside an
  inference server (vLLM, Ollama) on the same box.

## UMA Memory Model

Spark has no separate GPU VRAM — the GPU and
CPU share one 128GB pool. Two consequences:

- **`nvidia-smi` and `cudaMemGetInfo`
  underreport pressure — or report nothing at
  all.** Both report CUDA-allocator-visible
  memory, not the pool's actual state — a box can
  show headroom in `nvidia-smi` and still OOM,
  because page-cache and mmap'd pages the
  allocator doesn't see consume the same pool. On
  some driver/setups, the memory query returns
  `[N/A], [N/A]` outright instead of a number — a
  script grepping for a numeric value there gets
  nothing, not a misleading undercount (see
  `spark-training-gotchas` gotcha G3).

- **Model load is a transient peak, not the
  steady state.** Loading safetensors weights
  mmaps the file, then copies into CUDA
  tensors — for a window during load, both the
  mmap'd pages and the CUDA copy count against
  the pool at once. A model that fits while
  training can still OOM during load if headroom
  was sized for the post-load footprint instead
  of this doubled transient.

Plan and diagnose with `free -g`, not
`nvidia-smi`:

```bash
free -g | awk 'NR==2 {print "free:", $4, "GB"}'
```

Rule of thumb: take that free figure, subtract a
few GB for OS/driver overhead, and budget against
the result — not the 128GB spec number.
The worksheet in `references/uma-accounting.md`
accepts parameter count, dtype, and method as
input, and returns a memory estimate to compare
against known anchors.

### Planning Sequence

Before launch, work through these in order:

1. Read `free -g`; subtract OS/driver overhead
   for the budget.
2. Estimate weights + optimizer + gradients +
   activations from `references/uma-accounting.md`.
3. Compare against the closest anchor (70B
   QLoRA, 27B LoRA, 9B full FT), not the
   estimate alone.
4. If the estimate is close to the budget, start
   with shorter packing or a smaller batch —
   cheaper than hitting the OOM Ladder mid-run.

### Example: Sizing a 70B QLoRA Run

A sanity check of the worksheet formula against
the ≈40GB anchor:

```python
params = 70e9
weights_gb = params * 0.5 / 1e9      # NF4, step 1
adapter_gb = 0.5                     # step 5, negligible
total_gb = weights_gb + adapter_gb   # + activations
print(f"{total_gb:.0f}GB before activations")
```

Weights alone land near the ≈40GB anchor — a plan
estimating far above that for the same model
class is a signal to recheck dtype and method.

## The OOM Ladder

When a job OOMs on unified memory, work this
ladder in order. Each step is more disruptive
than the last — don't skip ahead:
**reducing batch size is never step 1.**

1. **Flush the buffer cache.** Page cache from a
   previous run or a large dataset read often
   accounts for GB of the "missing" headroom.
   This costs nothing but a rerun and doesn't
   touch the job's configuration:

   ```bash
   sync; echo 3 > /proc/sys/vm/drop_caches
   ```

   Needs root; a between-run reset, not a
   mid-training step. See
   `spark-training-gotchas` (gotcha G3) for the
   full diagnostic behind this step.

2. **Reduce batch size or packing length.** Only
   after a flush fails to free enough headroom,
   cut batch size or packing length — the first
   step that changes what the run does. Prefer
   packing length first; it drives activation
   footprint more directly at long context.

3. **Downgrade the method: bf16 LoRA before
   QLoRA.** If flushing and shrinking batch/pack
   still OOM, drop the method a tier — bf16 LoRA
   is next, not the reverse. QLoRA's bitsandbytes
   dequantization buffers are transient CUDA-side
   allocations that can OOM before an equivalent
   bf16 LoRA run would, even though QLoRA's
   steady-state footprint is smaller. A QLoRA OOM
   is not proof the model doesn't fit.

Fall back further (smaller model, multi-Spark)
only after all three steps and the job still
won't fit.

## Thermal Monitoring

Multi-hour runs push into Spark's sustained
power ceiling, well under the rated figure —
expected platform behavior, not a symptom to
explain away:

- Sample temperature and power alongside the
  training logs, not after a slowdown is
  noticed — every 30-60 seconds correlates a
  throughput drop with a thermal event. Keep
  the CSV output format `assets/thermal-sample.sh`
  writes, so timestamps line up against the log:

  ```bash
  bash assets/thermal-sample.sh 30 thermal.log
  ```

- **A sustained ~100W power draw is the platform
  cap, not a configuration bug.** Don't re-tune
  batch size or precision to "fix" a plateau
  that's the box behaving normally under load.
  If temperature climbs while power stays flat
  under the rated 240W figure, that's the
  signature to recognize.

- Log throttle events explicitly instead of
  letting a run silently slow down unrecorded. A
  run whose per-step time doubles two hours in
  should show that in the log, correlated against
  the thermal sample at that timestamp. Full
  throttling diagnostics: `spark-training-gotchas`
  (gotcha G4).

## Concurrent Workloads

Because the 128GB pool is global, eviction
happens without either process's logs showing
an OOM:

- The one-heavy-job rule applies to **uncapped or
  near-capacity** workloads — an uncapped trainer
  and inference server (vLLM, Ollama) compete for
  the same pool. A small, capped workload doesn't:
  a <4GB LoRA fine-tune coexists fine alongside
  vLLM capped at `gpu-memory-utilization<=0.5` —
  check the other process's cap, not just its
  presence, before stopping it.

- Inference servers evict trainer pages silently
  under uncapped/near-capacity contention, and
  vice versa — neither logs an error, so a slow
  run or lost KV cache is a contention symptom to
  check for. Stop unrelated *uncapped* servers
  before a long or full-pool run.

Check for GPU-resident processes first:

```bash
ps aux | grep -E 'vllm|ollama|trl|axolotl' | grep -v grep
```

This procedure complements `spark-training-gotchas`
(gotchas G3, G4, G6) — that skill covers launch-time
failures; this one, the running job.

Memory math worksheets:
`references/uma-accounting.md`.
