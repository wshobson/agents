# Open-Issue Resolution — Design

- **Date:** 2026-06-25
- **Status:** Approved (brainstorming) — pending implementation plan
- **Branch:** `fix/issues-591-598`
- **Scope decision:** Real fixes for **#591** and **#598**; triage-close (no code) for **#579, #580, #570, #595**. (#560 already closed — Antigravity harness is not being pursued.)

## Context

A review of the 7 open GitHub issues sorted them into three buckets:

1. **Real engineering work:** #591 (confirmed plugin-eval bug) and #598 (Cedar policy hardening).
2. **Already fixed on `main`** (reporter on stale pinned versions): #579, #580.
3. **Already converted to PRs:** #570 → PR #577, #595 → PR #596.

Both substantive bugs were confirmed at the code level, and the relevant library
patterns were verified against current docs via Context7
(`/anthropics/claude-agent-sdk-python`, `/cedar-policy/cedar-docs`).

---

## #591 — plugin-eval LLM judge silently emits fake 0.5 scores

### Root cause (confirmed)

`plugins/plugin-eval/src/plugin_eval/layers/judge.py` (`query_llm`, ~L83-85) reads the
LLM response from a field that does not exist:

```python
if isinstance(message, ResultMessage):
    for block in getattr(message, "content", []):   # ResultMessage has NO .content
        if hasattr(block, "text"):
            result_text += block.text
```

`ResultMessage` exposes `result: str | None` and `structured_output: Any` — there is
no `content` attribute (confirmed against installed `claude-agent-sdk` 0.2.101 and the
official SDK docs). So `result_text` is always `""`, `json.loads("")` raises, and the
code silently falls back (`judge.py` ~L96-98):

```python
except json.JSONDecodeError:
    return {"raw": result_text, "score": 0.5}   # fabricated 0.5 == grade F
```

Every judge sub-score becomes `0.5` with `raw: ""`, the composite reports confident
**F grades**, and the command exits **0**. The judge layer carries ~72% of the rubric
weight, so a genuinely strong skill is reported as failing. The **identical bug** exists
in `monte_carlo.py` (~L81-84). The reporter (lkjie, issue #591) assumed it was their
z.ai model; it is not — the bug fails for any ambient-configured model.

### Fix

1. **Correct extraction** (`judge.py` and `monte_carlo.py`): follow the documented SDK
   pattern — iterate `AssistantMessage` messages and accumulate `TextBlock.text`; use
   `ResultMessage.result` as a fallback when no assistant text was captured. Inspect
   `ResultMessage.is_error` / `subtype` so a non-success result is treated as a *failed
   measurement*, not as empty text.

   ```python
   from claude_agent_sdk import AssistantMessage, TextBlock, ResultMessage
   result_text = ""
   errored = False
   async for message in query(prompt=full_prompt, options=...):
       if isinstance(message, AssistantMessage):
           for block in message.content:
               if isinstance(block, TextBlock):
                   result_text += block.text
       elif isinstance(message, ResultMessage):
           if message.is_error:
               errored = True
           if not result_text and message.result:
               result_text = message.result
   ```

   (`structured_output` is noted as a possible future hardening, but we stay on the
   documented text path for this fix.)

2. **No more fabricated scores** (behavioral decision): when extraction yields no
   parseable JSON *or* the run errored, return an explicit **"unmeasured"** signal
   rather than `0.5`. Route the judge layer through the engine's existing
   negative-sentinel "unmeasured" path (`engine.py` ~L269-271) so the composite is
   computed **static-only** with a "judge unavailable" confidence note, and print a
   clear **stderr warning** naming the cause. Exit code stays `0` unless `--threshold`
   is set (a missing key / offline run must not become a hard failure when the static
   layer succeeded).

3. **Remove dead config:** drop `auth` and `model_tier` from the config dataclasses and
   the JSON output — they are threaded through but never used (the SDK call inherits the
   ambient model). Real tiered model selection is a separate future enhancement.

### Testing

Add a unit test that exercises the **real** extraction path (today `tests/test_judge.py`
mocks `query_llm` wholesale, which is why this slipped through): feed fabricated
`AssistantMessage` / `ResultMessage` objects and assert (a) valid JSON → real sub-scores,
(b) empty / errored result → "unmeasured", never `0.5`.

### Out of scope

Wiring real Haiku/Sonnet tier selection; the reporter's specific z.ai configuration
(the extraction fix makes any ambient-configured model work).

---

## #598 — Cedar `in`-on-String in review-agent-governance policy

### Assessment

`plugins/review-agent-governance/policies/review-agent-governance.cedar` (shipped on
`main` via PR #495) has 5 `forbid` rules using `context.<attr> in [string literals]`
plus a terminal blanket `permit`. Under **standard Cedar**, `in` requires an entity LHS,
so `context.command_pattern in [...]` is a type error and the erroring `forbid` is
silently discarded — which is the disclosure's claim (issue #598, upstream
`cedar-policy/cedar#2428`).

An initial hypothesis was that the plugin's runtime (protect-mcp) might treat
`in [string-set]` as set membership, making the disclosure a false positive. **Live
verification (2026-06-25) refuted that** and confirmed the disclosure is essentially
**correct**: `protect-mcp@0.5.5` evaluates Cedar via the real engine (WASM), which
discards `in`-on-String forbids exactly as standard Cedar does. The verification also
surfaced a **separate, larger defect** — `protect-mcp@0.5.5` has no `evaluate`/`sign`
subcommands at all (its CLI is `serve` / `init-hooks` / `simulate` / `--cedar`), so the
plugin's `hooks/hooks.json` (and protect-mcp's own `test/run-tests.sh`, which both invoke
`evaluate`) don't run as shipped. That broken-hook integration is tracked as its own
issue. The `.contains()` rewrite is correct, validator-clean Cedar regardless
(`["a","b"].contains(context.x)` validates; confirmed via Context7).

### Plan

1. **Live verification first** — attempt to evaluate the policy with the real engine.
   *Outcome:* `protect-mcp@0.5.5` has no `evaluate` subcommand, so the policy can't be
   exercised that way; the disclosure is confirmed essentially correct (real Cedar
   discards `in`-on-String), and the broken-hook integration is filed separately. The
   reply credits the reporter rather than calling it a false positive.
2. **Rewrite** all 5 `forbid` rules: `context.x in [list]` → `[list].contains(context.x)`.
3. **Add a `.cedarschema`** typing the context attributes (`command_pattern`,
   `target_branch`, `path_starts_with`, `method`, `url_host`) as `String`, so
   `cedar validate` turns this class of mistake into a load-time error. *Caveat:*
   protect-mcp may not consume the schema at runtime; its value is for `cedar validate`,
   documentation, and future-proofing.
4. **Permanent regression test** — a `test/run-tests.sh` that does NOT depend on
   `protect-mcp evaluate` (it doesn't exist): Part A always greps the policy for the
   `in`-on-String pattern (catching a regression), and Part B runs `cedar validate`
   against the schema when the `cedar` CLI is present (else skips). Covers
   `review-agent-governance.cedar`, which had zero coverage.
5. **Reply to the reporter** (responsible disclosure): acknowledge + credit, explain the
   engine distinction (their test used `cedar-policy 4.8.2`; the plugin runs
   `protect-mcp@0.5.5`), state the verified result, and note the `.contains()` hardening
   plus the `cedar-policy/cedar#2428` reference.

### Out of scope

protect-mcp's own fixtures/docs that use the same idiom; a repo-wide cedar lint.

---

## Triage closes (no code)

| Issue | Action | Comment substance |
|---|---|---|
| **#579** manifest conflicts | Close (fixed) | Resolved by format-modernization commit `4820385`; current marketplace has no `strict`/component arrays. Update the marketplace / unpin from 1.0.1/1.2.x. |
| **#580** shell-scripting paths | Close (fixed) | Same modernization; shell-scripting is now 1.2.3 with auto-discovery, skills load fine. Update to latest. |
| **#570** skill-forge | Close (superseded) | Converted to PR #577 (trimmed 3-skill version); tracking moves there. |
| **#595** operating-kit | Close (superseded) | Converted to PR #596; tracking moves there. |

---

## Rollout

- All code work lands on branch `fix/issues-591-598` → PR, not direct to `main`.
- Gates before merge: `make validate STRICT=1`, `make garden`, `make test` (the new
  judge extraction test runs here), plus `make generate-all` drift check (no harness
  artifacts change, so drift should be clean).
- Issue closes and the #598 reply are posted only after the maintainer approves (they
  are outward-facing).

## Risks / open items

- **#598 severity** is unresolved until the live protect-mcp run; the reply wording
  branches on it.
- The `.cedarschema` may be advisory-only if protect-mcp doesn't load it — acceptable
  (documentation + `cedar validate` value), flagged honestly in the reply.
- The new Cedar round-trip test requires `npx`/network; it must skip gracefully in CI
  rather than hard-fail when unavailable.
