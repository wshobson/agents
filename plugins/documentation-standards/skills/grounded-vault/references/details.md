# Grounded vault: details

Deep material for the `grounded-vault` skill. `SKILL.md` carries the convention; this file
carries the scripts, templates, and edge cases.

## Vault check script

`scripts/check_vault.py` walks every page under `wiki/`, verifies each linked claim against
its raw source, and compares each fingerprint with the current tree. It uses only the standard
library and `git`.

```python
#!/usr/bin/env python3
"""Grounding and drift checks for a grounded vault. Run from the vault root."""

import re
import subprocess
import sys
from pathlib import Path

WIKI = Path("wiki")
HEADER = re.compile(r"^> (Raw|Fingerprint|Monitored|Status): (.*)$", re.M)
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")
NUMBER = re.compile(r"\b\d[\d.,%]*\b")
QUOTE = re.compile(r"[\"“]([^\"”]{8,})[\"”]")


def header(text: str) -> dict[str, str]:
    return {k: v.strip() for k, v in HEADER.findall(text)}


def claims(text: str):
    """Yield (figure_or_quote, raw_path) for every sentence that links a raw source."""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        links = [p for _, p in LINK.findall(sentence) if "raw/" in p]
        if not links:
            continue
        for item in NUMBER.findall(sentence) + QUOTE.findall(sentence):
            yield item, links


def grounded(item: str, sources: list[str], page: Path) -> bool:
    for rel in sources:
        src = (page.parent / rel).resolve()
        if src.is_file() and item in src.read_text(errors="replace"):
            return True
    return False


def drifted(fingerprint: str, monitored: str) -> str:
    sha = fingerprint.removeprefix("git:")
    paths = [p.strip() for p in monitored.split(",") if p.strip()]
    if not sha or not paths:
        return ""
    out = subprocess.run(
        ["git", "diff", "--stat", f"{sha}..HEAD", "--", *paths],
        capture_output=True, text=True, check=False,
    )
    return out.stdout.strip()


def main(strict: bool) -> int:
    errors = 0
    for page in sorted(WIKI.rglob("*.md")):
        text = page.read_text()
        meta = header(text)
        if meta.get("Status", "Current") != "Current":
            continue
        for item, sources in claims(text):
            if not grounded(item, sources, page):
                print(f"{page}: {item!r} not found in {', '.join(sources)}")
                errors += 1
        if meta.get("Fingerprint") and meta.get("Monitored"):
            stat = drifted(meta["Fingerprint"], meta["Monitored"])
            if stat:
                print(f"{page}: drifted since {meta['Fingerprint']}\n{stat}")
                errors += 1
    print(f"{errors} problem(s)")
    return 1 if (errors and strict) else 0


if __name__ == "__main__":
    sys.exit(main(strict="--strict" in sys.argv))
```

What it checks, and what it deliberately does not:

- Only sentences that link a `raw/` file are checked, so prose without a source link is not
  silently accepted as grounded; the reviewer sees it has no link. Add a lint for unlinked
  numbers if the vault is large enough to need it.
- A number or quote is grounded when it appears verbatim in any of the sentence's linked
  sources. Reformatted figures (1,000 versus 1000) fail on purpose; copy the source's form.
- Archived and disputed pages are skipped; they are records, not claims.
- Drift is a non-empty `git diff --stat` between the fingerprint and `HEAD` restricted to the
  monitored paths. A fingerprint that no longer exists in the repository (after a history
  rewrite) makes `git` fail; treat that as drift and recompile.

## Batching the drift check

For a vault with many pages, collect fingerprints first and run one `git diff` per distinct
fingerprint rather than one per page:

```bash
grep -rh '^> Fingerprint: git:' wiki | sort -u | sed 's/^> Fingerprint: git://' \
  | while read -r sha; do
      echo "== $sha"; git diff --stat "$sha..HEAD" -- $(grep -rl "git:$sha" wiki \
        | xargs grep -h '^> Monitored:' | sed 's/^> Monitored: //' | tr ',' '\n' | sort -u)
    done
```

## Templates

`index.md`:

```markdown
# Vault index

| Page | Status | Fingerprint | Sources |
|---|---|---|---|
| [Authentication architecture](wiki/auth-architecture.md) | Current | git:5b237fa | raw/notes/auth-v1.md, raw/adr/0007-jwt.md |
```

`log.md`, one line per change, newest last:

```markdown
2026-09-01 compile wiki/auth-architecture.md from raw/adr/0007-jwt.md at git:5b237fa
2026-09-14 archive wiki/session-store.md: Outdated, src/auth/session.ts changed after git:5b237fa
```

Pre-commit hook (`.git/hooks/pre-commit`):

```bash
#!/bin/sh
python3 scripts/check_vault.py --strict || {
  echo "vault check failed; fix the claim or the fingerprint before committing" >&2
  exit 1
}
```

The same command runs as a CI step on pull requests so the gate holds for every contributor.

## Edge cases

- **Renamed or deleted monitored files.** `git diff` reports the deletion as a change, which
  is correct: the page describes something that moved. Recompile with the new paths in
  `Monitored:`.
- **Binary sources** (PDFs, images). Store the binary in `raw/` and add a sibling text
  extraction (`report.pdf` and `report.pdf.txt`) produced once by a deterministic tool. Link
  claims to the text file so the grounding check can read it.
- **External URLs.** A URL is not immutable. Save a dated snapshot into `raw/` and link the
  snapshot; keep the URL in the snapshot's first line for attribution.
- **Multiple repositories.** Fingerprint with `git:<repo-name>@<sha>` and keep one vault per
  repository, or one vault whose `Monitored:` paths are prefixed by repository. The check
  script above assumes a single repository.
- **Large raw files.** Verbatim search is linear in file size; it stays fast up to tens of
  megabytes. Split larger exports by date when ingesting.

## Reference implementation

`llm-wiki-loop` (MIT, <https://github.com/PALAN-K/llm-wiki-loop>) scaffolds this layout with
`npx llm-wiki-loop init`, ships a stricter `check_evidence.py`, and adds an event-driven
garbage collector and a step that promotes repeated fixes in `log.md` into agent skills. Read
it for the full loop; nothing in this skill requires it. The pattern was proposed for this
catalog by its author in wshobson/agents issue #673.
