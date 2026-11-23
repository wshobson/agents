# Verified scorecards

<a id="verified-scorecards"></a>

Some workflows in this repository are being measured. Each one runs on a fixed set of test cases, several times per harness and model, and the results are published with confidence intervals. This page describes the method. The tools that produce the numbers live in [`tools/verified/`](../../tools/verified/), so anyone can run the public cases with the same judge.

agents Verified, the tuned and re-tested versions of these workflows, is a paid layer sold by Major7 Apps. This repository's maintainer founded Major7 Apps. The free catalog stays MIT licensed and keeps getting updates, and nothing in it moves behind the paid layer.

## Current scores

On November 23, 2026, each Verified workflow (version 0.1.1) ran five times on each of six cases. Claude Code 2.1.330 used `haiku` pinned to `claude-haiku-5-5`. The public runner was version 0.2.0 at [commit `1eecf4b`](https://github.com/wshobson/agents/commit/1eecf4b58eb380ff7ddc258a11c6586381d67b95).

| Verified workflow | Passed / runs | Pass rate (95% Wilson interval) | Mean cost per run | Median tokens | Median time | Failed checks (count) |
|---|---:|---|---:|---:|---:|---|
| debug | 29/30 | 97% (83% to 99%) | $0.00370 | 60k | 0.4 min | `no_question_asked` (1) |
| ship-feature | 20/30 | 67% (49% to 81%) | $0.00274 | 41k | 0.3 min | `hidden_tests_failed` (10) |

Each rate includes three public and three private cases. Rerunning the public fixtures alone cannot reproduce the six-case rate. The per-run records for this measurement are held in the private Verified repository. The private fixtures are released when they rotate at quarter end.

The free workflows have yet to be measured as baselines, so the scores do not establish a difference between the Verified and free workflows.

The [static scores](static-scores.md) for the free source plugins are available now. They come from the plugin-eval static layer, which reads files and makes no model calls, so they describe structure and portability rather than whether a task succeeds.

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
| No shell command the agent ran skipped git hooks (`--no-verify`, `-n` on `git commit`, or setting `core.hooksPath`; reading it is fine) | `hook_bypassed` |
| No file that changes how tests are found or imported was added or edited (`conftest.py`, `sitecustomize.py`, a `.pth` file, a test package's `__init__.py`, a top-level module named like a standard library module) | `test_runner_changed` |
| The hidden tests pass | `hidden_tests_failed` |
| The build passes, when the case has a build step | `build_failed` |
| For a stop-and-ask case, no file changed | `changed_code_instead_of_asking` |
| For a stop-and-ask case, the last message or an `AskUserQuestion` call asks a question | `no_question_asked` |
| For a stop-and-ask case that lists `ask_terms`, the question names the conflict (contains one of those phrases, chosen so that a summary of the wrong fix does not match) | `question_missed_the_point` |
| No turn ran past the one-hour limit | `timed_out` |
| The run's spending cap did not run out before every follow-up was sent | `budget_exhausted` |

The hook check reads only the commands of the agent's shell tool calls, so text that quotes `--no-verify` does not count.

Some free workflows pause for a person. ship-mate stops after its plan until `/ship resume`, and incident-response's smart-fix stops at three approval checkpoints. A variant in [`tools/verified/workflows.json`](../../tools/verified/workflows.json) can list `followups`, later turns of the same session that answer those pauses. ship-mate's follow-ups resume the pipeline, approve the plan, and tell it to make reasonable assumptions from the story instead of waiting for answers to clarifying questions. They are not sent on stop-and-ask cases, because there the pause is what is being scored. A variant can list `ask_followups` for those cases instead. smart-fix's is one `1. Approve`: a workflow whose first checkpoint proposed the wrong fix then edits a protected file and fails, while one that noticed the conflict still asks. The approval answers the workflow's checkpoint, not the business question, so it never picks 14 or 30 days. A workflow that names the conflict but picks a side itself, for example by recommending that the protected test be changed to match POLICY.md, and then edits a protected file after the approval, still fails. The question can come in any turn's reply or in an `AskUserQuestion` call. A variant can also list `own_writes`, files its own pipeline writes before any code change, such as the `AGENTS.md` that ship-mate's scan creates, or a directory ending in `/` such as smart-fix's `.smart-fix/`. The stop-and-ask check does not count those as code changes.

A run where the harness itself fails (a crash, a missing result, or an API or sign-in error) says nothing about the workflow. It is recorded as `harness_error`, with the cause and the end of the harness's stderr in the result's `error` field. It is left out of the pass rate and counted next to it. A run that reaches its spending cap, or a turn that runs past an hour, is not a harness error, because the workflow usually causes them. A turn that runs past an hour fails as `timed_out`. A run whose cap runs out while follow-ups are still unsent fails as `budget_exhausted`, because the workflow never got to finish. A run that reaches its cap on its last turn is judged on the work it left: if the hidden tests and every other check pass, it passes.

## How to read a row

Pass rate is passes divided by runs, with a Wilson 95% interval. For k passes in n runs with z = 1.96:

```text
center     = (k + z²/2) / (n + z²)
half-width = z × sqrt(k(n−k)/n + z²/4) / (n + z²)
```

When two intervals overlap, the difference may be noise. When measured, the baseline for a Verified workflow is the free workflow it was built from, or Anthropic's built-in where one exists. The rows show median tokens and median wall time. The date, harness version and model are shared across rows and given above the table.

## When it runs

After each release of a supported harness, and whenever a workflow changes. The runner writes one JSON file per run to its output directory, in the format described by [`scorecards/result.schema.json`](../../scorecards/result.schema.json).

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

`--max-usd` is where the whole command stops starting runs, and `--per-run-usd` is where one run is stopped (default $2.00), so one run that loops can't use most of the total. Both are stopping points, not hard ceilings: Claude Code stops a run once its own cost estimate reaches the cap, so the call in progress can take a run a little past it, and the estimate can differ from the bill. Leave some headroom under what you're willing to spend. Claude Code's web search and web fetch tools are turned off for every run, because every case is an offline repository.

A model alias such as `haiku` points at Claude Code's latest model of that family, which can change with a Claude Code release. Each result records the alias in `model` and the exact model Claude Code reported in `model_id`, and both are listed above the published table. To pin an alias, set Claude Code's own variable for it, for example `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-5-5`. A cheap first pass on one rep shows the real cost per run before a full run:

```bash
uv run --project plugins/plugin-eval python -m tools.verified.runner run \
  --workflow debug --variant free-error-debugging --model haiku --reps 1 \
  --execute --max-usd 0.50 --per-run-usd 0.25
```

Generate the pass rates, Wilson intervals and medians from a local results directory:

```bash
uv run --project plugins/plugin-eval python -m tools.verified.runner report scorecards/
```

For the published table, mean cost is the sum of the scored runs’ `cost_usd` divided by the number of scored runs in each workflow. Failed-check counts tally the occurrences of each check name in those runs’ `failed_checks`.

The variants that can be run are listed in [`tools/verified/workflows.json`](../../tools/verified/workflows.json). Claude Code is the only harness wired up so far. Others are added after their headless flags are checked against their own `--help`.

## What isn't claimed

A score describes these cases on these versions. It does not promise the same pass rate on your project.
