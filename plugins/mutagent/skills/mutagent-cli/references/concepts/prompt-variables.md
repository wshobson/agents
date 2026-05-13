---
name: mutagent-cli-concepts-prompt-variables
description: |
  Prompt template variable delimiter inference contract.
  Platform canonical is single-brace {variable}. Third-party frameworks vary
  (Handlebars / Mustache / Liquid / Jinja2 use double {{variable}}).
  `mutagent explore` infers the delimiter per file and surfaces it in
  `--json` output as `delimiter: "single" | "double"`.
  Includes conversion rules for upload and apply phases.
triggers:
  - "prompt variables"
  - "template variables"
  - "single vs double brace"
  - "{variable}"
  - "{{variable}}"
  - "delimiter"
  - "inferPromptVariables"
  - "brace convention"
  - "convert variables"
---

# Concept — Prompt Variables

## Platform canonical

**MutagenT platform uses single-brace `{variable}`.** The platform renders
prompts by substituting `{name}` with the provided value at optimization /
evaluation time.

## Third-party framework variance

Real-world codebases use different delimiters depending on which prompt
framework the user already has installed:

| Framework | Delimiter | Example |
|---|---|---|
| **MutagenT platform** (canonical) | single | `{document}` |
| **LangChain** `PromptTemplate` | single | `{document}` |
| **LangChain** `ChatPromptTemplate` + Mustache | double | `{{document}}` |
| **Handlebars** | double | `{{document}}` |
| **Mustache** | double | `{{document}}` |
| **LiquidJS** | double | `{{ document }}` |
| **Jinja2** (Python) | double | `{{ document }}` |

---

## Brace conversion — upload and apply

Getting this wrong breaks templates after optimization. Follow the two-phase rule:

### Phase 1 — Upload (code → MutagenT)

If the code has `{{double}}` braces:
1. Warn the user: "Your template uses `{{double}}` braces (Handlebars/LangChain Mustache). MutagenT uses `{single}` braces. I'll convert before uploading."
2. Convert `{{name}}` → `{name}` in the prompt content passed to `mutagent prompts create`.
3. Record the original delimiter in `.mutagent/mutation-context.md` so the apply phase knows to convert back.

If the code has `{single}` braces: no conversion needed — upload as-is.

### Phase 2 — Apply (MutagenT → code)

After optimization, the platform returns a prompt with `{single}` braces.

If the original codebase used `{{double}}` braces:
1. Convert `{name}` → `{{name}}` in the optimized prompt before writing to the source file.
2. Confirm with the user before saving.

If the original codebase used `{single}` braces: write the optimized prompt as-is.

**Summary table:**

| Code uses | Upload | Optimized output | Write back to code |
|---|---|---|---|
| `{single}` | as-is | `{single}` | as-is |
| `{{double}}` | convert to `{single}` | `{single}` | convert back to `{{double}}` |

---

## Per-file inference — `mutagent explore`

The CLI's `mutagent explore` command calls `inferPromptVariables()` on every
matching source file and **infers the delimiter per file** rather than
globally. A single repository may contain both LangChain `PromptTemplate`
(single) and Handlebars email templates (double) side by side.

### Inference algorithm

1. **Strip fenced markdown code blocks** first (` ``` ... ``` `). Avoids false
   positives from prompts that document JSON examples in fenced blocks.
2. **Count `{{name}}` matches** → `doubleHits`.
3. **Count `{name}` matches** that are NOT adjacent to `{` (not part of `{{...}}`)
   and NOT followed by `"` (JSON-key skip) → `singleHits`.
4. **Majority wins**: `doubleHits > singleHits` → `double`, else `single`.
5. **Tie-break**: singleHits === doubleHits (including the 0/0 case) →
   `single` (platform canonical).

### Escaped-JSON caveat

Prompts like `"Return {\"status\": \"ok\"}"` — the `{` is followed by `"`, so
the single-brace regex deliberately skips it. Never treat literal JSON keys as
template variables.

---

## How to use the delimiter field

`mutagent explore --json` surfaces the inferred delimiter per discovered prompt:

```json
{
  "prompts": [
    {
      "file": "src/prompts/summarize.ts",
      "line": 12,
      "preview": "const prompt = `Summarize {document} for {audience}`;",
      "reason": "template-variable",
      "confidence": "high",
      "delimiter": "single"
    },
    {
      "file": "src/emails/welcome.hbs",
      "line": 3,
      "preview": "<p>Hello {{name}}, welcome to {{product}}!</p>",
      "reason": "template-variable",
      "confidence": "high",
      "delimiter": "double"
    }
  ]
}
```

Use the delimiter field to:
- Enumerate variables correctly (don't treat `{{foo}}` as two `{foo}` tokens).
- Decide whether to convert before upload (Phase 1 above).
- Drive the [concepts/eval-criteria.md](./eval-criteria.md) → MVC step (one criterion per variable).

---

## Edge cases

- **Empty prompt** — no variables → tie (0/0) → `single` (canonical).
- **Mixed delimiters in one file** — majority wins, tied files default to `single`.
  Warn the user: their codebase probably has two prompt systems co-existing.
- **Nested braces** `{{{ foo }}}` — Handlebars triple-brace (no-escape). Currently
  matched by the double regex as `{{ foo }}`; outer `}` ignored. Fine for inference.

---

## Cross-references

- [SKILL.md](../../SKILL.md) → 5 rules + journey router
- [workflows/optimization.md](../workflows/optimization.md) → step 3 (delimiter drives variable enumeration) and step 15 (apply conversion)
- [concepts/eval-criteria.md](./eval-criteria.md) → MVC (Minimum Viable Context) — uses delimiter to enumerate input params

---

## CLI commands

```bash
# Discovery (no LLM cost, read-only)
mutagent explore --help                                          # read flags before first use (Rule 2)
mutagent explore --json                                          # scans codebase; emits "delimiter" field per prompt
mutagent prompts get <id> --json                                 # inspect uploaded prompt's stored form (incl. delimiter)

# Creation (no LLM cost, just storage)
mutagent prompts create --help                                   # read brace format rules before creating
mutagent prompts create --name "<name>" --raw "<prompt>" --json  # upload prompt (use single-brace {var} convention)
mutagent prompts create --name "<name>" --raw-file <path> --json # upload from file (preferred for multi-line prompts)

# Mutations
mutagent prompts update <id> --raw "<prompt>" --json             # replace stored prompt body
mutagent prompts delete <id> --json                              # delete prompt (idempotent; --force skips confirm)
```

**Flag glossary** (prompt-create-specific):
- `--raw "<text>"` -- inline prompt body. Use for short single-line prompts.
- `--raw-file <path>` -- read prompt body from file. Preferred for multi-line / templated prompts; preserves whitespace.
- `--name "<name>"` -- human-readable label (shows in dashboard + explore output).
- `--json` -- structured output (Rule 1: always use). Returns `_directive` (status_card) + `_links` + `_compat`.

**Cost note**: prompt creation/edit/delete commands incur ZERO LLM cost. Pure storage. Only `mutagent prompts optimize start` and `mutagent prompts playground` (interactive testing) incur LLM cost.

**Brace convention reminder**: use single-brace `{var}` for variables you'll later supply via dataset items. Use double-brace `{{literal}}` only when you need a literal `{var}` substring rendered (rare). The CLI's `mutagent explore` infers delimiter automatically -- see § "Delimiter inference" above for the rules.
