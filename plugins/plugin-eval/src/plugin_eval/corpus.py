"""Gold standard corpus management for Elo ranking."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from plugin_eval.parser import parse_skill


@dataclass
class CorpusEntry:
    name: str
    path: str
    category: str
    line_count: int
    elo_rating: float = 1500.0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "category": self.category,
            "line_count": self.line_count,
            "elo_rating": self.elo_rating,
        }


class Corpus:
    def __init__(self, corpus_dir: Path) -> None:
        self.corpus_dir = corpus_dir
        self.entries: list[CorpusEntry] = []
        self._load()

    @classmethod
    def init_from_source(cls, plugins_dir: Path, corpus_dir: Path) -> Corpus:
        """Index all skills from a plugins directory into a corpus."""
        corpus_dir.mkdir(parents=True, exist_ok=True)

        entries = []
        for plugin_dir in sorted(plugins_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue
            skills_dir = plugin_dir / "skills"
            if not skills_dir.exists():
                continue
            for skill_dir in sorted(skills_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    try:
                        skill = parse_skill(skill_dir)
                        entries.append(
                            CorpusEntry(
                                name=skill.name,
                                path=str(skill_dir),
                                category=plugin_dir.name,
                                line_count=skill.line_count,
                            )
                        )
                    except Exception:
                        continue

        index = [e.to_dict() for e in entries]
        (corpus_dir / "index.json").write_text(json.dumps(index, indent=2))

        corpus = cls(corpus_dir)
        return corpus

    @property
    def size(self) -> int:
        return len(self.entries)

    def list_skills(self) -> list[CorpusEntry]:
        return self.entries

    def select_references(
        self,
        category: str | None = None,
        line_count: int | None = None,
        n: int = 5,
    ) -> list[CorpusEntry]:
        """Select reference skills for Elo comparison."""
        candidates = self.entries

        if category:
            same_cat = [e for e in candidates if e.category == category]
            if same_cat:
                candidates = same_cat

        if line_count:
            margin = line_count * 0.3
            sized = [e for e in candidates if abs(e.line_count - line_count) <= margin]
            if sized:
                candidates = sized

        candidates = sorted(candidates, key=lambda e: abs(e.elo_rating - 1500))
        return candidates[:n]

    def update_rating(self, name: str, new_rating: float) -> None:
        for entry in self.entries:
            if entry.name == name:
                entry.elo_rating = new_rating
                break
        self._save()

    def _load(self) -> None:
        index_path = self.corpus_dir / "index.json"
        if index_path.exists():
            data = json.loads(index_path.read_text())
            self.entries = [
                CorpusEntry(
                    name=e["name"],
                    path=e["path"],
                    category=e["category"],
                    line_count=e["line_count"],
                    elo_rating=e.get("elo_rating", 1500.0),
                )
                for e in data
            ]

    def _save(self) -> None:
        index = [e.to_dict() for e in self.entries]
        (self.corpus_dir / "index.json").write_text(json.dumps(index, indent=2))
