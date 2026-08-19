#!/usr/bin/env python3
"""eval-skill.py — Eval harness (Trụ 6): static check + test-set có version + trace verdict.

Dùng:
    python3 eval-skill.py <skill-dir> [--prompts <file.md>] [--record <file.json>]
    python3 eval-skill.py <skill-dir> --verify   # tổng kết record: pass rate + trigger rate

Chạy: 1) validate-skill.py (static) · 2) nạp test set (mặc định 5 loại hoặc file prompts)
       3) ghi eval-results.json (trace — re-run được, đo regression sau mỗi lần sửa skill).

BƯỚC TAY BẮT BUỘC (forward-test): với mỗi case, spawn agent MỚI (fork_context=false),
đưa prompt giả lập user thật, đối chiếu rubric (references/rubric.md), điền rubric + verdict
+ evidence vào eval-results.json — không lộ đáp án cho agent test. Xong chạy --verify để tổng kết.
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
VERSION = "1"


def default_prompts():
    return [
        "Tạo skill để <việc X> và kiểm tra nó chạy được (case chính)",
        "Cải thiện skill này tại <path> (case biên — skill có sẵn)",
        "Validate skill này tại <path> (case nhanh — 1 lệnh)",
        "Skill X báo lỗi khi chạy, debug giúp (case sai — error path)",
        "Tạo 5 skill cùng lúc cho 5 việc khác nhau (case lớn — scale)",
    ]


def load_prompts(f, root):
    if not f:
        return []
    text = f.read_text(encoding="utf-8")
    return [ln.strip().lstrip("- ").strip() for ln in text.splitlines() if ln.strip().startswith("- ")]


def _type(i):
    return ["chính", "biên", "nhanh", "sai", "lớn"][i] if i < 5 else "mở rộng"


def verify_run(record_file):
    if not record_file.exists():
        print(f"❌ Không có {record_file} — chạy eval-skill.py <skill-dir> trước (tạo record PENDING).")
        sys.exit(1)
    rec = json.loads(record_file.read_text(encoding="utf-8"))
    cases = rec.get("test_cases", [])
    n = len(cases)
    passed = [c for c in cases if c.get("verdict") == "PASS"]
    failed = [c for c in cases if c.get("verdict") == "FAIL"]
    pending = [c for c in cases if c.get("verdict") not in ("PASS", "FAIL")]
    no_rubric = [c for c in cases if not c.get("rubric")]
    edge = [c for c in cases if c.get("type") == "biên"]
    edge_pass = [c for c in edge if c.get("verdict") == "PASS"]
    print(f"📊 {rec.get('skill')} · test-set v{rec.get('version', '?')} · {rec.get('date')}")
    print(f"   Static validate: {'✅ PASS' if rec.get('static_pass') else '❌ FAIL'}")
    for c in cases:
        mark = "✅" if c.get("verdict") == "PASS" else ("❌" if c.get("verdict") == "FAIL" else "🔜")
        print(f"   {mark} #{c['id']} [{c.get('type', '?')}] {str(c.get('verdict')):8s} {str(c.get('prompt', ''))[:55]}")
    print(f"   — {len(passed)}/{n} PASS · {len(failed)} FAIL · {len(pending)} PENDING")
    if no_rubric:
        print(f"   ⚠️ {len(no_rubric)} case chưa khai rubric (bắt buộc pre-register — references/rubric.md)")
    if edge:
        pct = 100 * len(edge_pass) // len(edge)
        verdict = "✅" if pct >= 80 else "❌"
        print(f"   🎯 {verdict} Trigger rate (case biên): {len(edge_pass)}/{len(edge)} = {pct}% (mục tiêu ≥80%)")
    if pending:
        print("   🔜 Còn PENDING — điền verdict + evidence + rubric trong record rồi chạy lại --verify.")
        sys.exit(2)
    if failed or (edge and pct < 80):
        print("   ❌ Chưa đạt Definition of Done (eval-loop.md) — sửa skill rồi lặp lại.")
        sys.exit(3)
    print("   ✅ Đạt Definition of Done — sang bước handoff verify cho user.")


def main():
    if len(sys.argv) < 2:
        print("Dùng: python3 eval-skill.py <skill-dir> [--prompts <file.md>] [--record <file.json>] [--verify]")
        sys.exit(1)
    root = Path(sys.argv[1]).resolve()
    prompts_file = record_file = None
    verify = False
    args = sys.argv[2:]
    if "--prompts" in args:
        prompts_file = Path(args[args.index("--prompts") + 1])
    if "--record" in args:
        record_file = Path(args[args.index("--record") + 1])
    if "--verify" in args:
        verify = True
    if record_file is None:
        record_file = root / "eval-results.json"

    if verify:
        verify_run(record_file)
        return

    # 1. Static validate
    val = subprocess.run(
        [sys.executable, str(HERE / "validate-skill.py"), str(root)],
        capture_output=True, text=True)
    print(val.stdout)
    static_ok = "✅ PASS" in val.stdout

    # 2. Test set
    prompts = load_prompts(prompts_file, root) or default_prompts()

    # 3. Trace (versioned test set — re-run được)
    rec = {"skill": root.name, "version": VERSION, "date": date.today().isoformat(),
           "static_pass": static_ok,
           "test_cases": [{"id": i + 1, "type": _type(i), "prompt": p[:100],
                           "rubric": "", "verdict": "PENDING", "evidence": ""}
                          for i, p in enumerate(prompts)]}
    record_file.write_text(json.dumps(rec, ensure_ascii=False, indent=2))
    print(f"📄 Test set {len(prompts)} case ghi: {record_file}")
    print("🔜 BƯỚC TAY (bắt buộc): spawn agent MỚI cho từng case (không lộ đáp án),")
    print("   đối chiếu rubric (references/rubric.md), điền rubric + verdict + evidence trong record,")
    print("   rồi chạy: python3 eval-skill.py <skill-dir> --verify")


if __name__ == "__main__":
    main()
