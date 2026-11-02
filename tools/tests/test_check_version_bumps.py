"""Tests for tools/check_version_bumps.py, run against throwaway git repos."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from tools.check_version_bumps import find_problems


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _write(repo: Path, rel: str, content: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _set_version(repo: Path, plugin: str, version: str | None) -> None:
    manifest: dict = {"name": plugin}
    if version is not None:
        manifest["version"] = version
    _write(repo, f"plugins/{plugin}/.claude-plugin/plugin.json", json.dumps(manifest))


def _commit(repo: Path, message: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repo whose `main` holds one plugin, `demo` at 1.2.3, checked out on a branch."""
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "test@example.com")
    _git(tmp_path, "config", "user.name", "Test")
    _git(tmp_path, "config", "commit.gpgsign", "false")
    _set_version(tmp_path, "demo", "1.2.3")
    _write(tmp_path, "plugins/demo/skills/s/SKILL.md", "v1\n")
    _commit(tmp_path, "base")
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    return tmp_path


def test_content_change_without_bump_fails(repo: Path):
    _write(repo, "plugins/demo/skills/s/SKILL.md", "v2\n")
    _commit(repo, "edit skill")

    problems = find_problems(repo, "main")
    assert len(problems) == 1
    assert problems[0].startswith("demo: version 1.2.3 is not above 1.2.3, but")
    assert "plugins/demo/skills/s/SKILL.md" in problems[0]


def test_content_change_with_patch_bump_passes(repo: Path):
    _write(repo, "plugins/demo/skills/s/SKILL.md", "v2\n")
    _set_version(repo, "demo", "1.2.4")
    _commit(repo, "edit skill and bump")

    assert find_problems(repo, "main") == []


@pytest.mark.parametrize("version", ["1.2.2", "1.2.3", "0.9.9"])
def test_version_must_be_strictly_greater(repo: Path, version: str):
    _write(repo, "plugins/demo/skills/s/SKILL.md", "v2\n")
    _set_version(repo, "demo", version)
    _commit(repo, "edit skill")

    assert len(find_problems(repo, "main")) == 1


def test_versions_compare_numerically_not_as_strings(repo: Path):
    _write(repo, "plugins/demo/skills/s/SKILL.md", "v2\n")
    _set_version(repo, "demo", "1.2.10")
    _commit(repo, "edit skill")

    assert find_problems(repo, "main") == []


def test_non_semver_version_fails(repo: Path):
    _write(repo, "plugins/demo/skills/s/SKILL.md", "v2\n")
    _set_version(repo, "demo", "1.3")
    _commit(repo, "edit skill")

    assert find_problems(repo, "main") == ["demo: version '1.3' is not MAJOR.MINOR.PATCH"]


@pytest.mark.parametrize("rel", ["uv.lock", "tools/package-lock.json", ".codex-plugin/plugin.json"])
def test_exempt_paths_need_no_bump(repo: Path, rel: str):
    _write(repo, f"plugins/demo/{rel}", "changed\n")
    _commit(repo, "lockfile refresh")

    assert find_problems(repo, "main") == []


def test_dependency_manifest_change_needs_bump(repo: Path):
    _write(repo, "plugins/demo/pyproject.toml", "[project]\n")
    _commit(repo, "raise a dependency floor")

    assert len(find_problems(repo, "main")) == 1


def test_new_plugin_needs_no_bump(repo: Path):
    _set_version(repo, "fresh", "1.0.0")
    _write(repo, "plugins/fresh/agents/a.md", "agent\n")
    _commit(repo, "add plugin")

    assert find_problems(repo, "main") == []


def test_removed_plugin_needs_no_bump(repo: Path):
    _git(repo, "rm", "-q", "-r", "plugins/demo")
    _commit(repo, "remove plugin")

    assert find_problems(repo, "main") == []


def test_directory_without_manifest_is_ignored(repo: Path):
    _git(repo, "checkout", "-q", "main")
    _write(repo, "plugins/loose/README.md", "v1\n")
    _commit(repo, "loose dir")
    _git(repo, "checkout", "-q", "feature")
    _git(repo, "merge", "-q", "main")
    _write(repo, "plugins/loose/README.md", "v2\n")
    _commit(repo, "edit loose dir")

    assert find_problems(repo, "main") == []


def test_versionless_plugin_needs_no_bump(repo: Path):
    _git(repo, "checkout", "-q", "main")
    _set_version(repo, "demo", None)
    _commit(repo, "track commits instead of versions")
    _git(repo, "checkout", "-q", "feature")
    _git(repo, "merge", "-q", "main")
    _write(repo, "plugins/demo/skills/s/SKILL.md", "v2\n")
    _commit(repo, "edit skill")

    assert find_problems(repo, "main") == []


def test_only_changes_since_the_merge_base_count(repo: Path):
    """A plugin edited on main after the branch point is not this branch's change."""
    _git(repo, "checkout", "-q", "main")
    _set_version(repo, "other", "1.0.0")
    _commit(repo, "add other")
    _write(repo, "plugins/other/agents/a.md", "main-only edit\n")
    _commit(repo, "edit other on main")
    _git(repo, "checkout", "-q", "feature")

    assert find_problems(repo, "main") == []


def test_file_moved_between_plugins_needs_both_bumped(repo: Path):
    _git(repo, "checkout", "-q", "main")
    _set_version(repo, "other", "1.0.0")
    _commit(repo, "add other")
    _git(repo, "checkout", "-q", "feature")
    _git(repo, "merge", "-q", "main")
    (repo / "plugins" / "other" / "skills").mkdir()
    _git(repo, "mv", "plugins/demo/skills/s", "plugins/other/skills/s")
    _commit(repo, "move skill")

    problems = find_problems(repo, "main")
    assert [p.split(":")[0] for p in problems] == ["demo", "other"]
