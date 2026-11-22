"""Ensure the Godot runtime fixture matches the documented SaveManager example."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "plugins/game-development/skills/godot-gdscript-patterns/references/advanced-patterns.md"
FIXTURE = ROOT / "tools/tests/godot_save_validation/save_manager_fixed.gd"


def test_godot_save_example_fixture_matches_docs() -> None:
    source = DOC.read_text(encoding="utf-8")
    marker = "```gdscript\n# save_manager.gd (Autoload)\n"
    assert source.count(marker) == 1
    example = source.split(marker, 1)[1].split("\n```", 1)[0].strip() + "\n"
    assert FIXTURE.read_text(encoding="utf-8") == example
