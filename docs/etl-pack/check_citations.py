"""Verify every `path:line` "fragment" citation in pack.md: file exists, line exists,
fragment appears on that line. Paths resolve under plugins/ then repo root."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
text = (root / "docs/etl-pack/pack.md").read_text()
cite = re.compile(r"`([\w./-]+\.md):(\d+)`(?:\s+\"((?:[^\"\\]|\\.)+)\")?")
bad = n = 0
for m in cite.finditer(text):
    n += 1
    rel, line, frag = m.group(1), int(m.group(2)), m.group(3)
    path = next((p for p in (root / "plugins" / rel, root / rel) if p.is_file()), None)
    if not path:
        print("MISSING FILE", rel); bad += 1; continue
    lines = path.read_text().splitlines()
    if line > len(lines):
        print("NO LINE", rel, line); bad += 1; continue
    if frag:
        frag = frag.replace('\\"', '"')
        if frag not in lines[line - 1]:
            print(f"FRAGMENT MISS {rel}:{line}\n  want: {frag}\n  have: {lines[line-1].strip()[:120]}"); bad += 1
print(f"{n} citations, {bad} bad")
sys.exit(1 if bad else 0)
