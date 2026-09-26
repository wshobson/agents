from pathlib import Path

import pytest

from plugin_eval.snapshot import (
    SnapshotComparison,
    build_snapshot,
    compare_snapshot,
    load_snapshot,
)

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "evals" / "static-score-snapshot.json"


@pytest.fixture(scope="module")
def comparison() -> SnapshotComparison:
    # Scoring every skill takes a few seconds, so both tests share one run.
    return compare_snapshot(load_snapshot(SNAPSHOT), build_snapshot(ROOT / "plugins"))


def test_static_scores_match_snapshot_for_unchanged_skills(comparison: SnapshotComparison) -> None:
    assert not comparison.diffs, (
        "Static scores changed for skills whose content did not change. If the scoring change "
        "is intended, run `make eval-snapshot` and commit the result.\n"
        + "\n".join(comparison.diffs)
    )


def test_snapshot_is_not_stale(comparison: SnapshotComparison) -> None:
    total = comparison.matched + comparison.stale
    assert comparison.matched >= total * 0.5, (
        f"Only {comparison.matched} of {total} skills still match the snapshot. "
        "Run `make eval-snapshot` and commit the result."
    )
