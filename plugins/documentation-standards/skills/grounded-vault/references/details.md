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

RAW = (Path.cwd() / "raw").resolve()
WIKI = Path("wiki")
HEADER = re.compile(r"^> (Raw|Fingerprint|Monitored|Status): (.*)$", re.M)
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")
NUMBER = re.compile(r"(?<![\w.,])\d[\d.,]*%?(?![\w.,])")
QUOTE = re.compile(r"[\"\u201c]([^\"\u201d]{8,})[\"\u201d]")  # shorter quoted words are not claims


def header(text: str) -> dict[str, str]:
    return {k: v.strip() for k, v in HEADER.findall(text)}


def prose(text: str) -> str:
    """Body text without the header block, headings, and fenced code."""
    kept, fenced = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced or line.startswith((">", "#")):
            continue
        kept.append(line)
    return "\n".join(kept)


def claims(text: str):
    """Yield (item, is_number, raw_links) for every figure or quotation in the prose."""
    for sentence in re.split(r"(?<=[.!?])\s+", prose(text)):
        links = [path for _, path in LINK.findall(sentence) if "raw/" in path]
        bare = LINK.sub(" ", sentence)  # link labels and paths are not claims
        for item in NUMBER.findall(bare):
            yield item, True, links
        for item in QUOTE.findall(bare):
            yield item, False, links


def raw_source(page: Path, rel: str) -> Path | None:
    """The raw file a link points at, or None when it escapes raw/ or is missing."""
    src = (page.parent / rel).resolve()
    return src if src.is_relative_to(RAW) and src.is_file() else None


def grounded(item: str, is_number: bool, sources: list[str], page: Path) -> bool:
    token = re.compile(r"(?<![\w.,])" + re.escape(item) + r"(?![\w.,])")
    for rel in sources:
        src = raw_source(page, rel)
        if src is None:
            continue
        text = src.read_text(errors="replace")
        if token.search(text) if is_number else item in text:
            return True
    return False


def drift(fingerprint: str, monitored: str) -> str:
    """Non-empty when monitored paths changed since the fingerprint, or git cannot tell."""
    sha = fingerprint.removeprefix("git:")
    paths = [p.strip() for p in monitored.split(",") if p.strip()]
    if not paths:
        return ""
    out = subprocess.run(
        ["git", "diff", "--stat", f"{sha}..HEAD", "--", *paths],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return f"git cannot compare {sha}: {out.stderr.strip() or 'unknown fingerprint'}"
    return out.stdout.strip()


def main(strict: bool) -> int:
    errors = 0
    for page in sorted(WIKI.rglob("*.md")):
        text = page.read_text()
        meta = header(text)
        if meta.get("Status", "Current") != "Current":
            continue
        if not meta.get("Fingerprint"):
            print(f"{page}: no Fingerprint header")
            errors += 1
        for item, is_number, sources in claims(text):
            if not sources:
                if strict:
                    print(f"{page}: {item!r} has no raw/ source link")
                    errors += 1
                continue
            if not grounded(item, is_number, sources, page):
                print(f"{page}: {item!r} not found in {', '.join(sources)}")
                errors += 1
        stat = drift(meta["Fingerprint"], meta.get("Monitored", "")) if meta.get("Fingerprint") else ""
        if stat:
            print(f"{page}: drifted since {meta['Fingerprint']}\n{stat}")
            errors += 1
    print(f"{errors} problem(s)")
    return 1 if (errors and strict) else 0


if __name__ == "__main__":
    sys.exit(main(strict="--strict" in sys.argv))
```

What it checks, and what it deliberately does not:

- Only the prose is scanned. The header block, headings, fenced code, and the labels and
  paths of Markdown links are excluded, so a source path such as `raw/adr/0007-jwt.md`
  never reads as a claim of `0007`.
- A number is grounded when it appears in a linked source as a whole token, so `15` does
  not match `150` or `2015`. A quotation must appear verbatim. Quoted phrases shorter than
  eight characters are not treated as claims; a two-word quote is not evidence of anything.
  Reformatted figures (`1,000` versus `1000`) fail on purpose; copy the source's form.
- A link must resolve inside `raw/`. A path that escapes it, or points at a file that is
  missing, is a miss, so a page cannot ground a claim on something outside the vault.
- Under `--strict`, a number or quotation with no `raw/` link in its sentence is an error.
  Without `--strict` it is skipped, which is the mode for a first pass over an old vault.
- Every current page needs a `Fingerprint:`. An empty `Monitored:` is allowed: a page
  compiled only from `raw/` has no code to drift against.
- Drift is a non-empty `git diff --stat` between the fingerprint and `HEAD` restricted to
  the monitored paths. When git cannot compare, for example after a history rewrite removed
  the fingerprint, that counts as drift too; recompile and stamp a fresh fingerprint.
- Archived and disputed pages are skipped; they are records, not claims.

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
