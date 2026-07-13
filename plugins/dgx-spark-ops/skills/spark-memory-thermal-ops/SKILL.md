---
name: spark-memory-thermal-ops
description: Manage unified memory and thermals during long-running ML jobs on NVIDIA DGX Spark. Use when planning memory headroom for a training run on GB10, when a job OOMs on unified memory, or when monitoring temperature and power during multi-hour training.
---

# Spark Memory & Thermal Ops

DGX Spark's GB10 chip has one 128GB unified
memory (UMA) pool shared by CPU and GPU, and a
sustained power ceiling well below its rated
figure. Both break assumptions from
discrete-GPU boxes: memory headroom isn't what
`nvidia-smi` reports, and a multi-hour run that
starts fast will slow down partway through with
nothing misconfigured. This skill covers
planning memory headroom, working an actual
OOM, and watching thermals across a long job.
For launch-time failure modes (ABI mismatches,
flash-attn, playbook breakage), see
`spark-training-gotchas` instead — this skill
assumes the job starts and covers what happens
once it's running.

## Common Issues Quick Reference

| Situation | Do this |
|---|---|
| Planning headroom before launch | Budget against `free -g`, not `nvidia-smi` — see UMA Memory Model |
| Job OOMs on unified memory | Work the OOM Ladder in order: flush, then batch/pack, then method downgrade |
| Throughput drops mid-run | Check the power/temp log before assuming a config bug — see Thermal Monitoring |
| Trainer + inference server both wanted | Run one at a time — see Concurrent Workloads |

## When to Use This Skill

- Sizing a training run against the 128GB pool
  before launching it — will this model, method,
  and batch/pack combination fit.

- A run OOMs mid-load or mid-step and the
  remediation order matters — what to try first,
  second, third.

- Watching temperature and power during a
  multi-hour or multi-epoch job, and deciding
  whether a slowdown is thermal throttling or
  something else.

- Planning to run a trainer alongside an
  inference server (vLLM, Ollama) on the same
  box.

## UMA Memory Model

Spark has no separate GPU VRAM — the GPU and CPU
share one 128GB pool. Two consequences follow
directly:

- **`nvidia-smi` and `cudaMemGetInfo`
  underreport pressure.** Both report
  CUDA-allocator-visible memory, not the unified
  pool's actual state — a box can show
  comfortable headroom in `nvidia-smi` and still
  OOM, because page-cache and mmap'd pages the
  allocator doesn't see are consuming the same
  pool.

- **Model load is a transient peak, not the
  steady state.** Loading safetensors weights
  mmaps the file, then copies into CUDA
  tensors — for a window during load, both the
  mmap'd pages and the CUDA copy count against
  the pool at once. A model that fits once
  training is running can still OOM during load
  if headroom was sized for the post-load
  footprint instead of this doubled transient.

Plan and diagnose against `free -g`, not
`nvidia-smi`:

```bash
free -g | awk 'NR==2 {print "free:", $4, "GB"}'
```

Rule of thumb: take that free figure, subtract a
few GB for OS and driver overhead, and budget
against the result — not the 128GB spec number.
The worksheet in `references/uma-accounting.md`
accepts parameter count, dtype, and method as
input, and returns a total memory estimate to
compare against known anchors.

### Planning Sequence

Before launch, work through these in order:

1. Read `free -g`; subtract OS/driver overhead
   for the budget.
2. Estimate weights + optimizer + gradients +
   activations from `references/uma-accounting.md`.
3. Compare against the closest anchor (70B
   QLoRA, 27B LoRA, 9B full FT) rather than
   trusting the estimate alone.
4. If the estimate is close to the budget, start
   with shorter packing or a smaller batch —
   cheaper than hitting the OOM Ladder mid-run.

### Example: Sizing a 70B QLoRA Run

A quick sanity check against the worksheet
formula before trusting the ≈40GB anchor for a
specific run:

```python
params = 70e9
weights_gb = params * 0.5 / 1e9      # NF4, step 1
adapter_gb = 0.5                     # step 5, negligible
total_gb = weights_gb + adapter_gb   # + activations
print(f"{total_gb:.0f}GB before activations")
```

Weights alone already land near the ≈40GB
anchor — a plan estimating far above that for
the same model class is a signal to recheck
dtype and method, not just add headroom.

## The OOM Ladder

When a job OOMs on unified memory, work this
ladder in order. Each step is more disruptive
than the last, so don't skip ahead —
**reducing batch size is never step 1.**

1. **Flush the buffer cache.** Page cache from a
   previous run or a large dataset read often
   accounts for GB of the "missing" headroom
   `nvidia-smi` never showed in the first place.
   This costs nothing but a rerun and doesn't
   touch the job's configuration:

   ```bash
   sync; echo 3 > /proc/sys/vm/drop_caches
   ```

   Needs root; it's a between-run reset, not
   something to run mid-training. See
   `spark-training-gotchas` (gotcha G3) for the
   full diagnostic behind this step.

2. **Reduce batch size or packing length.** Only
   after a flush fails to free enough headroom,
   cut the batch size or packing length — the
   first step that changes what the run actually
   does. Prefer packing length first; it drives
   the activation footprint more directly at
   long context.

3. **Downgrade the method: bf16 LoRA before
   QLoRA.** If flushing and shrinking batch/pack
   still OOM, drop the method down a tier — bf16
   LoRA is next, not the reverse. QLoRA's
   bitsandbytes dequantization buffers are
   transient CUDA-side allocations that can push
   a run over the edge before an equivalent bf16
   LoRA run would, even though QLoRA's
   steady-state footprint is smaller. A QLoRA
   OOM is not proof the model doesn't fit — try
   bf16 LoRA first.

Only fall back further (smaller model,
multi-Spark) once all three steps have been
tried and the job still won't fit.

## Thermal Monitoring

Multi-hour runs push into Spark's sustained
power ceiling, well under the rated figure.
Treat this as expected platform behavior, not a
symptom to explain away:

- Sample temperature and power alongside the
  training logs, not after a slowdown is
  noticed — every 30-60 seconds is enough to
  correlate a throughput drop with a thermal
  event after the fact. Keep the output in the
  CSV format `assets/thermal-sample.sh` writes,
  so timestamps line up against the log:

  ```bash
  bash assets/thermal-sample.sh 30 thermal.log
  ```

- **A sustained ~100W power draw is the platform
  cap, not a configuration bug.** Don't spend
  time re-tuning batch size or precision to "fix"
  a plateau that's actually the box behaving
  normally under load. If temperature climbs
  while power stays flat under the rated 240W
  figure, that's the signature to recognize.

- Log throttle events explicitly instead of
  letting a run silently slow down without
  record. A run whose per-step time doubles two
  hours in should show that in the log,
  correlated against the thermal sample at that
  timestamp. Full throttling diagnostics and the
  reboot failure mode live in
  `spark-training-gotchas` (gotcha G4).

## Concurrent Workloads

Because the 128GB pool is global, memory isn't
the only resource one job can take from
another — eviction happens without either
process's logs showing an OOM:

- Run one memory-heavy job at a time. A training
  run and an inference server (vLLM, Ollama)
  started side by side compete for the same
  pool.

- Inference servers evict trainer pages silently
  under contention, and vice versa — neither
  logs an error when it happens, so a
  mysteriously slow run or a lost KV cache is a
  contention symptom to check for. Stop
  unrelated GPU-resident servers before a long
  or full-pool run.

Check for other GPU-resident processes first:

```bash
ps aux | grep -E 'vllm|ollama|trl|axolotl' | grep -v grep
```

This procedure complements
`plugins/dgx-spark-ops/skills/spark-training-gotchas/SKILL.md`
(gotchas G3, G4, G6) — that skill covers
launch-time failures; this one covers what
happens once a job is already running.

Memory math worksheets: see
`references/uma-accounting.md`.
