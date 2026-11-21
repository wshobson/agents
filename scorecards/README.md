# Scorecard results

<a id="scorecard-results"></a>

This directory holds raw results for the [Verified scorecards](../docs/verified/README.md). Each run writes one JSON file under `runs/<date>/`. No runs have been published yet.

Every file follows [`result.schema.json`](result.schema.json), which is generated from `RunResult` in [`tools/verified/models.py`](../tools/verified/models.py). A test fails if the two drift apart. To regenerate the schema after changing the model:

```bash
uv run --project plugins/plugin-eval python -m tools.verified.runner schema
```

| Field | Meaning |
|---|---|
| `workflow` | The workflow and variant, for example `debug/free-error-debugging` |
| `workflow_version` | The plugin version that was run |
| `harness`, `harness_version` | The coding tool and its version |
| `model` | The model alias passed to the harness |
| `case_id`, `case_visibility` | Which case ran, and whether it is public or private |
| `passed`, `failed_checks` | The verdict, and the name of each check that failed |
| `tokens_in`, `tokens_out`, `cost_usd` | Usage as the harness reported it, or null when it did not |
| `wall_seconds` | How long the agent ran |
| `run_at` | When the run happened, in UTC |
| `runner_version` | The version of `tools/verified` that produced the file |

Results for private cases are kept here too, so the pass rates of private cases can be checked once those cases are published.
