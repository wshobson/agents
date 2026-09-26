"""Per-skill static score snapshot, keyed by a hash of each skill's content.

The snapshot records what the static layer scores every skill in the repo at
quick depth. An entry whose skill content changed is skipped, so editing a skill
never fails a check. An entry whose content did not change but whose numbers did
points at a change in the scoring code, which is what the snapshot exists to catch.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig

# A frozen copy of the parser's cross-reference pattern. The digest must not call
# scoring code. If it did, a change to that code would move the digest as well as
# the score, and the snapshot would report the skill as stale instead of failing.
_REFERENCE_PATTERN = re.compile(
    r"(?<![\w-])((?:skill|skills|sub-skills)/[a-z0-9-]+(?:/[a-z0-9-]+)*)"
)


class SnapshotEntry(BaseModel):
    digest: str
    static_score: float
    sub_scores: dict[str, float]
    composite: float
    badge: str


@dataclass
class SnapshotComparison:
    matched: int = 0
    stale: int = 0
    diffs: list[str] = field(default_factory=list)


def skill_digest(skill_dir: Path) -> str:
    """Return a sha256 hex digest over every file under the skill directory.

    CRLF line endings are hashed as LF, because the parser reads text with
    universal newlines and scores both the same. When SKILL.md cross-references
    other skills, each reference is hashed with whether it exists next to the
    skill and inside the skill, because the static layer lowers the score when
    it finds neither. The digest finds references with its own copy of the
    pattern, so a change to the parser cannot hide a change in the score.
    """
    files = sorted(
        (p for p in skill_dir.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(skill_dir).as_posix(),
    )
    h = hashlib.sha256()
    for path in files:
        h.update(path.relative_to(skill_dir).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes().replace(b"\r\n", b"\n"))
        h.update(b"\0")
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8") if skill_md.is_file() else ""
    refs = sorted(
        {
            ref.split("/", 1)[1] if ref.startswith(("skill/", "skills/")) else ref
            for ref in _REFERENCE_PATTERN.findall(text)
        }
    )
    if refs:
        h.update(b"\0cross-references\0")
        for ref in refs:
            beside = int((skill_dir.parent / ref).exists())
            inside = int((skill_dir / ref).exists())
            h.update(f"{ref}\0{beside}{inside}\0".encode())
    return h.hexdigest()


def build_snapshot(plugins_dir: Path) -> dict[str, SnapshotEntry]:
    """Score every skill under plugins_dir the way `plugin-eval score --depth quick` does."""
    engine = EvalEngine(EvalConfig(depth=Depth.QUICK))
    snap: dict[str, SnapshotEntry] = {}
    for skill_md in sorted(plugins_dir.glob("*/skills/*/SKILL.md")):
        skill_dir = skill_md.parent
        result = engine.evaluate_skill(skill_dir)
        static = next(lr for lr in result.layers if lr.layer == "static")
        composite = result.composite
        assert composite is not None  # evaluate_skill always builds a composite
        snap[f"{skill_dir.parent.parent.name}/{skill_dir.name}"] = SnapshotEntry(
            digest=skill_digest(skill_dir),
            static_score=static.score,
            sub_scores={name: float(value) for name, value in static.sub_scores.items()},
            composite=composite.score,
            badge=composite.badge.value,
        )
    return snap


def compare_snapshot(
    saved: dict[str, SnapshotEntry],
    current: dict[str, SnapshotEntry],
    tol: float = 1e-9,
) -> SnapshotComparison:
    """Compare entries whose content is unchanged and report any whose numbers moved.

    An entry is stale when its digest differs or it exists on only one side. A
    stale entry is counted and otherwise skipped.
    """
    result = SnapshotComparison()
    for key in sorted(saved.keys() | current.keys()):
        old, new = saved.get(key), current.get(key)
        if old is None or new is None or old.digest != new.digest:
            result.stale += 1
            continue
        result.matched += 1
        changes = _entry_changes(old, new, tol)
        if changes:
            result.diffs.append(f"{key}: " + "; ".join(changes))
    return result


def _entry_changes(old: SnapshotEntry, new: SnapshotEntry, tol: float) -> list[str]:
    numbers: list[tuple[str, float | None, float | None]] = [
        ("static_score", old.static_score, new.static_score),
        ("composite", old.composite, new.composite),
    ]
    for name in sorted(old.sub_scores.keys() | new.sub_scores.keys()):
        numbers.append((f"sub_scores.{name}", old.sub_scores.get(name), new.sub_scores.get(name)))

    changes = [
        f"{label} {_fmt(before)} -> {_fmt(after)}"
        for label, before, after in numbers
        if before is None or after is None or abs(before - after) > tol
    ]
    if old.badge != new.badge:
        changes.append(f"badge {old.badge} -> {new.badge}")
    return changes


def _fmt(value: float | None) -> str:
    return "missing" if value is None else f"{value:.6g}"


def load_snapshot(path: Path) -> dict[str, SnapshotEntry]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {key: SnapshotEntry.model_validate(value) for key, value in data.items()}


def write_snapshot(path: Path, snap: dict[str, SnapshotEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {key: entry.model_dump() for key, entry in snap.items()}
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
