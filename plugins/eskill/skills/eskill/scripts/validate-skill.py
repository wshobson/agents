#!/usr/bin/env python3
"""validate-skill.py — Kiểm tra Agent Skill theo spec agentskills.io + kinh nghiệm eskill.

Chạy:
    python3 validate-skill.py <skill-dir>                       # validate cơ bản
    python3 validate-skill.py <skill-dir> --leak                # + quét rò rỉ thương mại
    python3 validate-skill.py <skill-dir> --leak --brand "name1,name2"   # + quét brand/dịch vụ nội bộ

Check: frontmatter (name/description) · quy tắc name (khớp thư mục) · description ≤1024 ·
SKILL.md < 500 dòng · refs 1 cấp + file tồn tại · (--leak) secret/path/brand/chat_id.
"""
import re
import sys
from pathlib import Path

FAILS = 0

def ok(msg):
    print(f"  ✅ {msg}")

def bad(msg):
    global FAILS
    FAILS += 1
    print(f"  ❌ {msg}")

def main():
    if len(sys.argv) < 2:
        print("Dùng: python3 validate-skill.py <skill-dir> [--leak] [--brand \"a,b\"]")
        sys.exit(1)
    root = Path(sys.argv[1]).resolve()
    leak = "--leak" in sys.argv
    brands = []
    if "--brand" in sys.argv:
        i = sys.argv.index("--brand")
        if i + 1 < len(sys.argv):
            brands = [b.strip().lower() for b in sys.argv[i + 1].split(",") if b.strip()]
    skill = root / "SKILL.md"

    if not skill.exists():
        bad(f"thiếu SKILL.md trong {root}")
        sys.exit(1)
    ok("có SKILL.md")

    text = skill.read_text(encoding="utf-8")

    # ── Frontmatter ──
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        bad("thiếu YAML frontmatter (--- name/description ---)")
    else:
        fm = m.group(1)
        has_name = re.search(r"^name\s*:\s*\S+", fm, re.M)
        has_desc = re.search(r"^description\s*:", fm, re.M)
        if has_name and has_desc:
            ok("frontmatter có name + description")
        else:
            bad("frontmatter thiếu name hoặc description")

        nm = re.search(r"^name\s*:\s*(\S+)", fm, re.M)
        if nm:
            name = nm.group(1)
            if re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
                ok(f"name hợp lệ: {name}")
            else:
                bad(f"name sai quy tắc (chữ thường + gạch nối): {name}")
            if root.name != name:
                bad(f"name ({name}) KHÔNG khớp tên thư mục ({root.name})")
            else:
                ok(f"name = thư mục ({root.name})")

        desc = re.search(r"^description\s*:\s*(.+)$", fm, re.M)
        if desc and len(desc.group(1)) > 1024:
            bad(f"description > 1024 ký tự ({len(desc.group(1))})")

    # ── Body < 500 dòng ──
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    n_lines = len(body.splitlines())
    if n_lines > 500:
        bad(f"SKILL.md > 500 dòng ({n_lines}) — đẩy chi tiết xuống references/")
    else:
        ok(f"SKILL.md {n_lines} dòng (< 500)")

    # ── Refs 1 cấp + tồn tại ──
    refs = re.findall(r"\]\(([^)]+)\)", body)
    deep = [r for r in refs if r.startswith(("../", "../../", "/"))]
    for r in deep:
        bad(f"ref ngoài skill hoặc > 1 cấp: {r}")
    local = [r for r in refs if r.startswith(("references/", "scripts/", "assets/"))]
    missing = [r for r in local if not (root / r).exists()]
    for r in missing:
        bad(f"ref hỏng (file không tồn tại): {r}")
    if local and not missing and not deep:
        ok(f"{len(local)} ref cục bộ — 1 cấp + tồn tại")

    # ── Leak mode ──
    if leak:
        patterns = {
            "token bot": r"bot\d{8,}:[A-Za-z0-9_-]{20,}",
            "API key": r"(sk-[A-Za-z0-9]{16,}|api[_-]?key\s*=\s*['\"]?[A-Za-z0-9]{12,}|AKIA[A-Z0-9]{16})",
            "path cá nhân": r"/(Users|home)/",
            "chat_id dài": r"\b\d{9,11}\b",
            "access token Meta": r"EAA[A-Za-z0-9]{20,}",
        }
        hits = set()
        for label, pat in patterns.items():
            for mm in re.finditer(pat, text, re.IGNORECASE):
                hits.add(f"{label}: {mm.group(0)[:20]}…")
        if hits:
            bad(f"RÒ RỈ ({len(hits)}): " + " · ".join(sorted(hits)))
        else:
            ok("không rò rỉ secret/path/chat_id")

        if brands:
            low = text.lower()
            found = [b for b in brands if b in low]
            if found:
                bad(f"RÒ RỈ brand/dịch vụ nội bộ: {', '.join(found)}")
            else:
                ok(f"không dính brand nội bộ ({', '.join(brands)})")

    print(f"\nKẾT QUẢ: {'❌ FAIL' if FAILS else '✅ PASS'} ({FAILS} lỗi)")
    sys.exit(1 if FAILS else 0)

if __name__ == "__main__":
    main()
