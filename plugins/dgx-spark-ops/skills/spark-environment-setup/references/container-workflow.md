Last verified: 2026-07-13 — refresh when the blessed container tags change.

# Container Workflow

Concrete `docker run` invocations for the two blessed images, plus the bare-pip fallback.

## NGC PyTorch container

General-purpose training/inference base:

```bash
docker run --runtime=nvidia --gpus all -it --rm \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -v "$(pwd)/finetuning:/workspace/finetuning" \
  nvcr.io/nvidia/pytorch:25.11-py3
```

- `--runtime=nvidia --gpus all` gives the container access to the GB10 GPU; without it, PyTorch inside the container will report no CUDA device even though the host sees one fine.
- `--ipc=host` and the `ulimit` flags avoid shared-memory starvation for PyTorch's DataLoader workers.
- Mount the repo's `finetuning/` run directory so checkpoints and logs land on the host filesystem, not inside the ephemeral container layer — the `--rm` flag deletes the container (and anything not mounted out) on exit.

## Unsloth container

For Unsloth-centric fine-tuning runs, prefer the purpose-built image over the generic NGC one — it ships the pinned Triton/xformers/transformers combination already validated for this hardware:

```bash
docker run --runtime=nvidia --gpus all -it --rm \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -v "$(pwd)/finetuning:/workspace/finetuning" \
  unsloth/unsloth:dgxspark-latest
```

Same flag rationale as above. Prefer this over rebuilding a custom Unsloth image from the NGC base.

## Pull vs rebuild

Pull a fresh tag when: a new blessed release is announced, or you're chasing a bug that a recent tag's changelog says it fixes.

Rebuild locally (starting `FROM` one of the two images above) when: you need an extra system package or Python dependency layered in for a specific project, and that dependency doesn't conflict with the pinned training stack. Don't rebuild to "upgrade" a component that the base image already pins — that reintroduces the version-matrix problem the container exists to avoid.

## Bare-pip escape hatch

If a container genuinely doesn't fit (see `SKILL.md`'s Container-First Rule), isolate the environment with `uv` rather than the system Python, and follow the NVIDIA playbook install sequence from `SKILL.md` inside it.

Caveat: if `uv` insists on a dependency version that conflicts with what the playbook pins (a common outcome given how young the aarch64/CUDA-13 wheel ecosystem is), use `uv pip install --override-dependencies` to force the pinned versions through rather than letting the resolver silently substitute an incompatible build. Verify the result with the Verification Commands section of `SKILL.md` before trusting the environment.
