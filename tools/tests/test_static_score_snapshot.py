from pathlib import Path

from plugin_eval.snapshot import build_snapshot, compare_snapshot, load_snapshot

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "evals" / "static-score-snapshot.json"


def test_static_scores_match_snapshot_for_unchanged_skills() -> None:
    saved = load_snapshot(SNAPSHOT)
    current = build_snapshot(ROOT / "plugins")
    result = compare_snapshot(saved, current)
    assert not result.diffs, (
        "Static scores changed for skills whose content did not change. If the scoring change "
        "is intended, run `make eval-snapshot` and commit the result.\n" + "\n".join(result.diffs)
    )


def test_snapshot_is_not_stale() -> None:
    saved = load_snapshot(SNAPSHOT)
    current = build_snapshot(ROOT / "plugins")
    result = compare_snapshot(saved, current)
    total = result.matched + result.stale
    assert result.matched >= total * 0.5, (
        f"Only {result.matched} of {total} skills still match the snapshot. "
        "Run `make eval-snapshot` and commit the result."
    )
