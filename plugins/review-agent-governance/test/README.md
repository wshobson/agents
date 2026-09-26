# review-agent-governance policy tests

Guards `policies/review-agent-governance.cedar` against the #598 `in`-on-String
forbid bug and the #705 entity-shape regression.

```bash
./run-tests.sh   # exit 0 pass · 1 fail
```

- **Part A** (always runs, needs only `grep`): with `//` comment lines stripped,
  asserts the policy contains no `context.<attr> in [ ... ]` forbid pattern
  (which Cedar silently discards), uses `.contains()` or the protect-mcp 0.7
  `context.input.<field> like` form, and targets `Action::"MCP::Tool::call"`.
- **Part B** (runs only if the `cedar` CLI is installed): `cedar validate` the
  policy against `review-agent-governance.cedarschema`.
- **Part C** (runs if `node`, `npx`, and `python3` are installed): pipes Claude
  Code hook payloads through the exact `hooks.json` command. Deny cases must
  exit 2 with protect-mcp's `cedar_deny` reason, so a fail-closed exit (the
  evaluator could not run, or a policy errored) does not count as a pass. The
  cases cover review commands reworded to dodge a prefix match, `gh api`
  writes (including `-fbody=x` and `-X GET -X POST`), pushes to protected
  branches, force pushes (including `--mirror` and `+feature`), and workflow
  writes. Allow guards cover `git push origin maintenance`,
  `gh pr view 42 --comments`, and `gh api repos/o/r/pulls/42`; an allow must
  not come from evaluate.sh's "no policy file" fallback.
