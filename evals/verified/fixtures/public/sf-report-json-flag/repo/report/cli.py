import argparse
import sys

from report.summary import summarize


def main(argv=None, out=sys.stdout):
    parser = argparse.ArgumentParser(prog="report")
    parser.add_argument("results", help="lines of name=pass|fail")
    args = parser.parse_args(argv)
    with open(args.results, encoding="utf-8") as handle:
        summary = summarize(handle.read())
    out.write(f"{summary.passed}/{summary.total} passed\n")
    for name in summary.failed_names:
        out.write(f"FAIL {name}\n")
    return 0 if not summary.failed_names else 1
