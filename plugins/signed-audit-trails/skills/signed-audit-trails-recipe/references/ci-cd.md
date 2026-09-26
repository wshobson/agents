# CI/CD workflow for the signed audit trail recipe

The signing key is gitignored, so a CI job needs it from a secret. Create an
environment named `receipt-signing` and limit its deployment branches to the
default branch. Store the contents of `./protect-mcp.key` as that
environment's secret `PROTECT_MCP_KEY`, and store its `publicKey` value as the
repository variable `PROTECT_MCP_PUBLIC_KEY`. The hooks sign receipts with the
secret key while the agent runs, and the verify step checks them with the
public key. Without the key, the receipts are unsigned and the verify step
exits 1.

Run this job only on reviewed code, such as pushes to the default branch. Do
not run it on pull requests, for two reasons:

- GitHub does not pass secrets to a workflow run for a pull request from a
  fork, so the key is empty and the verify step fails.
- On a pull request from a branch in the same repository, the job would run
  that branch's `scripts/run_agent.py` after it writes the key to disk. The
  branch could change the script to read the key and send it elsewhere.

The environment's branch limit is a second guard: if someone later adds a
pull request trigger, jobs for other branches still cannot read the key.

```yaml
# .github/workflows/verify-receipts.yml
name: Verify Decision Receipts
on:
  push:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    environment: receipt-signing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - name: Install signing key
        env: { KEY: '${{ secrets.PROTECT_MCP_KEY }}' }
        run: umask 077 && printf '%s' "$KEY" > protect-mcp.key
      - name: Run governed agent
        run: python scripts/run_agent.py
      - name: Verify receipts
        env: { PUB: '${{ vars.PROTECT_MCP_PUBLIC_KEY }}' }
        run: npx @veritasacta/verify@0.9.2 --replay-chain receipts/receipts.jsonl --key "$PUB"
      - name: Upload receipts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: decision-receipts
          path: receipts/
```

The upload step keeps the receipts after the job ends, including when the
verify step fails.
