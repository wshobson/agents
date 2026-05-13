---
name: mutagent-cli-concepts-scorecard-output
description: |
  Per-iteration structured scorecard emitted by the optimizer.
  Covers the ScorecardData shape, where agents see it (watch vs results),
  how to consume NDJSON streams, cost-gate patterns, and criterion drill-down.
triggers:
  - "scorecard"
  - "scorecard output"
  - "optimize scorecard"
  - "scorecard data"
  - "iteration scorecard"
  - "nextAction"
  - "stop-stagnation"
  - "cumulativeUsd"
  - "optimizer results json"
  - "watch optimizer"
---

# Concept — Scorecard Output

> Per-iteration structured scorecard emitted by the optimizer, available
> progressively via `--watch` and as a post-hoc digest via `optimize results`.

## What it is

Every completed optimizer iteration produces a `ScorecardData` record: a
structured snapshot of scores, criterion pass-rates, cumulative cost, and the
optimizer's own next-action decision. The scorecard is the primary signal
surface for agents monitoring or reacting to a running optimization job.

Two delivery modes:

- **Progressive (streaming)** — emitted once per completed iteration over the
  WebSocket event bus while the job runs.
- **Post-hoc (batch)** — the full collection of per-iteration scorecards
  returned in the `/api/optimization/:id/results` response after the job
  finishes (or to inspect a paused job).

---

## Where an agent sees it

### 1. `optimize start --watch --json`

Streams NDJSON to stdout while the job runs. Each iteration emits one line:

```
{ "type": "scorecard.update", "iteration": 1, "scorecard": { ...ScorecardData } }
```

Other line types (e.g. `job.started`, `stage.completed`) may appear in the
stream — branch on `type === "scorecard.update"` to isolate scorecard events.

### 2. `optimize watch <id> --json`

Attaches to an already-running job and streams the same NDJSON shape. Useful
when the agent started the job in a previous session or on behalf of a
background process.

### 3. `optimize results <id> --json`

Returns the complete result digest after job completion:

```json
{
  "job": { "id": "...", "status": "completed", ... },
  "prompt": { ... },
  "scorecard": {
    "rendered": "<ASCII scorecard string>",
    "data": [ ...ScorecardData[] ]
  }
}
```

The `scorecard.data` array contains one entry per completed iteration in
chronological order. `scorecard.rendered` is the ASCII terminal render of the
final iteration (same bytes as the terminal output), included as a convenience
for agents that want to surface a human-readable summary without re-rendering.

---

## `ScorecardData` shape

The optimizer emits this shape on each iteration (TypeScript):

```typescript
interface ScorecardData {
  jobId: string;
  iteration: number;
  totalIterations: number | null;  // null when maxIterations not configured
  timestamp: string;               // ISO-8601
  stage: string;                   // always "result-analysis" for completed iterations

  scores: {
    bestScore: number;             // highest score seen across all iterations so far
    currentScore: number;          // score for this iteration
    targetScore: number | null;    // convergence threshold; null if not set
  };

  criteria: Array<{
    name: string;                  // criterion name from the evaluation rubric
    scoreAvg: number;              // mean LLM score for this criterion this iteration
    passRate: number;              // fraction of dataset items passing (0.0–1.0)
  }>;

  costs: {
    iterationUsd: number;          // LLM cost for this iteration only
    cumulativeUsd: number;         // total cost from job start through this iteration
  };

  durations: {
    iterationMs: number;           // wall-clock duration of this iteration
    stageBreakdown: Record<string, number>; // token counts keyed by stage name
  };

  nextAction:
    | 'continue'          // optimizer will run another iteration
    | 'stop-converged'    // currentScore >= targetScore
    | 'stop-budget'       // cost or token budget exhausted
    | 'stop-stagnation'   // stagnationCount >= patience threshold
    | 'stop-max-iter';    // iteration count reached maxIterations
}
```

Key fields at a glance:

| Field | Why it matters |
|---|---|
| `scores.bestScore` | The best the optimizer has achieved — compare to `targetScore` to estimate progress |
| `scores.currentScore` | This iteration's score — use to detect regressions |
| `scores.targetScore` | Convergence threshold; `null` means run until `maxIterations` |
| `criteria[].passRate` | Per-criterion health — values below `0.5` flag a specific rubric as blocking |
| `costs.cumulativeUsd` | Running cost — gate against any user-approved budget |
| `nextAction` | The optimizer's own routing decision — surface `stop-stagnation` proactively |

---

## How an agent should use it

### Per-iteration monitoring (streaming)

While consuming `optimize start --watch --json` or `optimize watch <id> --json`:

1. **Score trend** — compare `scores.currentScore` against the previous
   iteration's `currentScore`. A sustained downward trend (3+ iterations)
   warrants surfacing to the user before the budget is spent.

2. **`nextAction` gate** — if `nextAction === "stop-stagnation"`, the optimizer
   has detected a plateau and is about to halt. Surface this to the user with
   the current `scores.bestScore` and `costs.cumulativeUsd` so they can decide
   whether to continue with a higher patience budget or accept the result.

3. **Cost gate** — if `costs.cumulativeUsd` crosses a threshold the user
   approved for, alert immediately. The optimizer does not know about
   user-defined soft budgets; the agent is the enforcement layer.

### Post-hoc analysis (`optimize results`)

1. **Criterion drill-down** — iterate `scorecard.data` (all iterations) and
   collect `criteria[].passRate` per criterion. Any criterion with a mean
   `passRate < 0.5` across iterations did not benefit from optimization and
   should be flagged back to the user as potentially mis-specified or
   conflicting with another criterion.

2. **Best-iteration identification** — find the entry where
   `scores.currentScore === Math.max(...data.map(d => d.scores.currentScore))`.
   This is the iteration the optimizer treats as `bestIteration`. Compare its
   `criteria` snapshot to the final iteration to detect regressions in
   individual rubrics even when the composite score improved.

3. **Cost/iteration trade-off** — divide `costs.cumulativeUsd` by
   `iteration` to get average cost per iteration. Present this when asking the
   user whether to re-run with more iterations.

---

## Parsing example

Minimal Node.js / Bun snippet — consume NDJSON from `optimize start --watch --json`
and branch on `nextAction`:

```js
import { spawn } from 'node:child_process';
import * as readline from 'node:readline';

const proc = spawn('mutagent', ['optimize', 'start', JOB_ID, '--watch', '--json']);
const rl = readline.createInterface({ input: proc.stdout });

rl.on('line', (line) => {
  let event;
  try { event = JSON.parse(line); } catch { return; }
  if (event.type !== 'scorecard.update') return;

  const { scorecard } = event;
  const { scores, costs, criteria, nextAction } = scorecard;

  console.log(`Iter ${scorecard.iteration}: score=${scores.currentScore.toFixed(3)} cost=$${costs.cumulativeUsd.toFixed(4)}`);

  if (nextAction === 'stop-stagnation') {
    // Surface to user — optimizer is about to halt without converging
    console.warn(`[ALERT] Optimizer stagnated at score ${scores.bestScore}. Consider raising patience.`);
  }

  const weakCriteria = criteria.filter(c => c.passRate < 0.5).map(c => c.name);
  if (weakCriteria.length > 0) {
    console.warn(`[ALERT] Low-pass criteria: ${weakCriteria.join(', ')}`);
  }
});
```

---

## Cross-references

- [concepts/eval-criteria.md](./eval-criteria.md) — how evaluation criteria are
  defined; `criteria[].name` in `ScorecardData` maps to `name` in the rubric.
- [workflows/optimization.md](../workflows/optimization.md) — full optimization
  loop; the scorecard is produced at Step 8 (watch) and Step 9 (results).

---

## CLI commands

```bash
# Discovery (no LLM cost)
mutagent prompts optimize --help                                # list optimize subcommands
mutagent prompts optimize start --help                          # read flags before first use (Rule 2)

# 💰 LLM COST -- requires usage check (Rule 5) + provider catalog check (Rule 6)
mutagent prompts optimize start <id> --dataset <d> --evaluation <e> --json
                                                                # start job (cost = exec_model × items × iterations
                                                                # + judge_model × items × iterations)
mutagent prompts optimize start <id> --dataset <d> --evaluation <e> --watch --json
                                                                # start + stream NDJSON events to stdout

# Polling / watching (no LLM cost; just reads job state)
mutagent prompts optimize status <job-id> --json                # poll progress snapshot (includes bestScore)
mutagent prompts optimize watch <job-id> --json                 # attach to running job (NDJSON stream)
mutagent prompts optimize results <job-id> --json               # full scorecard after completion (emits verbatim card)
mutagent prompts optimize results <job-id> --diff --json        # view prompt diff (no apply)

# Mutation (no LLM cost itself; modifies stored prompt)
mutagent prompts optimize results <job-id> --apply --json       # apply optimized prompt -> updates stored version
                                                                # (irreversible without manual revert via prompts update)
```

**Flag glossary** (optimize-specific):
- `--dataset <d>` -- dataset ID (from `prompts dataset list`). Items run through both exec and judge models.
- `--evaluation <e>` -- evaluation ID (from `prompts evaluation list`). Drives the judge model's scoring rubric.
- `--watch` -- after start, stream NDJSON events instead of returning immediately. Equivalent to `start` then `watch`.
- `--max-iterations N` -- bound the optimizer loop. **Defaults to 1**; never raise without explicit user consent (each iteration = full eval × dataset round-trip).
- `--exec-model <model>` / `--eval-model <model>` -- override defaults. Validate first via `mutagent providers list --models --json` (Rule 6).
- `--apply` -- write optimized prompt back to stored version. Cannot be undone via flag; use `prompts update` to revert.
- `--diff` -- view before/after diff without applying.
- `--json` -- structured output (Rule 1: always use). Returns `_directive` + `_links` + `_compat`.

**Cost note**: `optimize start` is the ONLY cost-incurring command in this family. Always run `mutagent usage --json` first (Rule 5) to surface remaining quota; show the result to the user; require explicit confirmation. The `--max-iterations` default of 1 keeps cost bounded.

**Verbatim card protocol**: `optimize start`, `optimize status`, and `optimize results` all emit `_directive.renderedCard` -- the agent MUST echo the rendered card verbatim into chat before any next action (per SKILL.md § "MANDATORY: Verbatim Card Display Protocol"). The card also auto-echoes to stderr via `echoDirectiveToStderr`, but bash blocks may be collapsed in the user's UI.
