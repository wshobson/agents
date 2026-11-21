from pathlib import Path

p = Path("report/cli.py")
s = p.read_text()
s = s.replace("import argparse\n", "import argparse\nimport json\n")
s = s.replace(
    '    parser.add_argument("results", help="lines of name=pass|fail")\n',
    '    parser.add_argument("results", help="lines of name=pass|fail")\n'
    '    parser.add_argument("--json", action="store_true")\n',
)
s = s.replace(
    '    out.write(f"{summary.passed}/{summary.total} passed\\n")\n',
    """    if args.json:
        failed = sorted(summary.failed_names)
        payload = {
            "total": summary.total,
            "passed": summary.passed,
            "failed": len(failed),
            "failed_names": failed,
        }
        out.write(json.dumps(payload) + "\\n")
        return 0 if not failed else 1
    out.write(f"{summary.passed}/{summary.total} passed\\n")
""",
)
p.write_text(s)
print("Added --json.")
