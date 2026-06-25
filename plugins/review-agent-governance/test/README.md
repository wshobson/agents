# review-agent-governance policy tests

Guards `policies/review-agent-governance.cedar` against the #598 `in`-on-String
forbid bug.

```bash
./run-tests.sh   # exit 0 pass · 1 fail
```

- **Part A** (always runs, needs only `grep`): asserts the policy contains no
  `context.<attr> in [ ... ]` forbid pattern (which Cedar silently discards) and
  uses `[ ... ].contains(context.<attr>)` instead.
- **Part B** (runs only if the `cedar` CLI is installed): `cedar validate` the
  policy against `review-agent-governance.cedarschema`. With the context
  attributes typed as `String`, `cedar validate` rejects the `in`-on-String form
  at load time and accepts `.contains()`.

Note: the shipped runtime is `protect-mcp serve` (Cedar-via-WASM); this test
validates the policy source directly and does not depend on protect-mcp.
