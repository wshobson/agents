# Godot SaveManager regression tests

These are headless Godot 4 tests for the SaveManager sample in
`plugins/game-development/skills/godot-gdscript-patterns/references/advanced-patterns.md`.

Run from the repository root with Godot 4.7.2 or newer:

```sh
godot --headless --path tools/tests/godot_save_validation --script res://test_save.gd
```

The test covers encrypted save and load, overwriting an existing save,
Windows destination-delete-then-rename-fails, partial restoration that leaves
a damaged primary file, recovery on a later load or save, invalid JSON number
syntax, trailing commas, and removing backup files on deletion.

A separate Python test checks that `save_manager_fixed.gd` exactly matches the
documentation example, so the fixture cannot silently become stale:

```sh
uv run --project plugins/plugin-eval --extra dev pytest -q tools/tests/test_godot_save_reference.py
```

Godot runtime execution is not part of the Python test. It must be run
separately before a pull request is considered validated.
