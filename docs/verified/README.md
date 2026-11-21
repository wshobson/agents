# Verified scorecards

<a id="verified-scorecards"></a>

Some workflows in this repository are being measured. Each one runs on a fixed set of test cases, several times per harness and model, and the results are published with confidence intervals. This page describes the method. The tools that produce the numbers live in [`tools/verified/`](../../tools/verified/), so anyone can rerun the public cases and check a published number.

agents Verified, the tuned and re-tested versions of these workflows, is a paid layer sold by Major7 Apps. This repository's maintainer founded Major7 Apps. The free catalog stays MIT licensed and keeps getting updates, and nothing in it moves behind the paid layer.

## Current scores

No measured runs have been published yet. The [static scores](static-scores.md) for the free source plugins are available now. They come from the plugin-eval static layer, which reads files and makes no model calls, so they describe structure and portability rather than whether a task succeeds.

## What is measured

Each workflow runs on six fixture repositories with one task each:

- three ordinary tasks
- one change that spans several files
- one trap: a test that is easy to delete or skip
- one task where the right outcome is to stop and ask a question

Three of the six cases are public and live in [`evals/verified/fixtures/public/`](../../evals/verified/fixtures/public/). The other three are kept private so that the paid workflows cannot be tuned to the cases they are scored on. The private half is published at the end of each quarter and replaced with new cases.

Each case directory holds `case.json` (the task given to the agent, word for word, and the commands to run), `repo/` (the project the agent starts from) and `hidden/` (test files copied in only after the agent finishes).

## When a run passes

The judge is deterministic. No model grades a run. A run passes only when every check passes:

| Check | Fails as |
|---|---|
| Files the case protects, such as existing tests, are unchanged | `protected_file_changed` |
| No test file was deleted | `test_deleted` |
| No new skip marker was added to a test file | `test_skipped` |
| No shell command the agent ran skipped git hooks (`--no-verify`, or `-n` on `git commit`) | `hook_bypassed` |
| No file that changes how tests are found or imported was added or edited (`conftest.py`, `sitecustomize.py`, a `.pth` file, a test package's `__init__.py`, a top-level module named like a standard library module) | `test_runner_changed` |
| The hidden tests pass | `hidden_tests_failed` |
| The build passes, when the case has a build step | `build_failed` |
| For a stop-and-ask case, no file changed | `changed_code_instead_of_asking` |
| For a stop-and-ask case, the last message asks a question | `no_question_asked` |

The hook check reads only the commands of the agent's shell tool calls, so text that quotes `--no-verify` does not count.

Some free workflows pause for a person. ship-mate stops after its plan until `/ship resume`, and incident-response's smart-fix stops at three approval checkpoints. A variant in [`tools/verified/workflows.json`](../../tools/verified/workflows.json) can list `followups`, later turns of the same session that answer those pauses. They are not sent on stop-and-ask cases, because there the pause is what is being scored. A variant can also list `own_writes`, files its own pipeline writes before any code change, such as the `AGENTS.md` that ship-mate's scan creates. The stop-and-ask check does not count those as code changes.

A run where the harness itself fails (a crash, a timeout, or an API or sign-in error) says nothing about the workflow. It is recorded as `harness_error`, left out of the pass rate, and counted next to it. A run that reaches its spending cap before finishing is not a harness error. It counts as a failed run.

## How to read a row

Pass rate is passes divided by runs, with a Wilson 95% interval. For k passes in n runs with z = 1.96:

```text
center     = (k + z²/2) / (n + z²)
half-width = z × sqrt(k(n−k)/n + z²/4) / (n + z²)
```

When two intervals overlap, the difference may be noise. Each Verified row is shown next to a baseline: the free workflow it was built from, or Anthropic's built-in where one exists. A row also shows median tokens, median wall time and the run date.

## When it runs

After each release of a supported harness, and whenever a workflow changes. Raw results are JSON files under [`scorecards/`](../../scorecards/), one per run, in the format described by [`scorecards/result.schema.json`](../../scorecards/result.schema.json).

## Rerun the public cases

The runner makes no model calls unless you ask it to. A plan shows the run count and an estimated cost:

```bash
uv run --project plugins/plugin-eval python -m tools.verified.runner plan \
  --workflow debug --variant free-error-debugging --model sonnet --reps 5
```

A real run needs `--execute`, a spending cap and an API key. Claude Code is started with `--bare`, which makes it authenticate only with `ANTHROPIC_API_KEY`, so a run never uses a Claude subscription login:

```bash
export ANTHROPIC_API_KEY=...
uv run --project plugins/plugin-eval python -m tools.verified.runner run \
  --workflow debug --variant free-error-debugging --model sonnet --reps 5 \
  --execute --max-usd 10
```

Turn the results into a table:

```bash
uv run --project plugins/plugin-eval python -m tools.verified.runner report scorecards/
```

The variants that can be run are listed in [`tools/verified/workflows.json`](../../tools/verified/workflows.json). Claude Code is the only harness wired up so far. Others are added after their headless flags are checked against their own `--help`.

## What isn't claimed

A score describes these cases on these versions. It does not promise the same pass rate on your project.
