from pathlib import Path

from plugin_eval.snapshot import (
    SnapshotEntry,
    compare_snapshot,
    skill_digest,
)


def make_skill(root: Path, body: str, name: str = "s") -> Path:
    d = root / "p" / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Use when x.\n---\n{body}\n")
    return d


def test_digest_changes_with_content(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "one")
    first = skill_digest(d)
    (d / "SKILL.md").write_text((d / "SKILL.md").read_text() + "two\n")
    assert skill_digest(d) != first


def test_digest_covers_references(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "one")
    first = skill_digest(d)
    (d / "references").mkdir()
    (d / "references" / "x.md").write_text("detail")
    assert skill_digest(d) != first


def test_digest_tracks_siblings_only_for_cross_referencing_skills(tmp_path: Path) -> None:
    # The static layer resolves cross-references against sibling skill directories,
    # so a new sibling can change the score of a skill whose own files did not change.
    a = make_skill(tmp_path, "See skills/b for the details.", name="a")
    b = make_skill(tmp_path, "No references here.", name="b")
    a_before, b_before = skill_digest(a), skill_digest(b)
    make_skill(tmp_path, "one", name="c")
    assert skill_digest(a) != a_before
    assert skill_digest(b) == b_before


def test_digest_ignores_line_endings(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "one\ntwo")
    lf = skill_digest(d)
    md = d / "SKILL.md"
    md.write_bytes(md.read_bytes().replace(b"\n", b"\r\n"))
    assert skill_digest(d) == lf


def entry(digest: str, score: float) -> SnapshotEntry:
    return SnapshotEntry(
        digest=digest,
        static_score=score,
        sub_scores={"a": score},
        composite=score * 100,
        badge="Gold",
    )


def test_compare_skips_changed_content_and_flags_score_drift() -> None:
    saved = {"p/one": entry("d1", 0.8), "p/two": entry("d2", 0.8)}
    current = {"p/one": entry("d1", 0.7), "p/two": entry("CHANGED", 0.1)}
    result = compare_snapshot(saved, current)
    assert result.matched == 1
    assert result.stale == 1
    assert len(result.diffs) == 1
    assert "p/one" in result.diffs[0]
