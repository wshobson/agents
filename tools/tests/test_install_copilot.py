"""Tests for safe Copilot global install/uninstall helper."""

from __future__ import annotations

import sys
from pathlib import Path

from tools.install_copilot import default_config_dir, install, main, uninstall


def _write_generated_copilot(repo_root: Path) -> None:
    agents = repo_root / ".copilot" / "agents"
    skills = repo_root / ".copilot" / "skills" / "demo-hello"
    commands = repo_root / ".copilot" / "commands" / "demo"
    agents.mkdir(parents=True)
    skills.mkdir(parents=True)
    commands.mkdir(parents=True)
    (agents / "demo__agent.agent.md").write_text("agent\n")
    (skills / "SKILL.md").write_text("---\nname: demo-hello\n---\n\nBody.\n")
    (commands / "index.md").write_text("---\ndescription: demo\n---\n\nEntry.\n")
    (commands / "say-hi.md").write_text("---\ndescription: hi\n---\n\nHi.\n")


def test_default_config_dir_prefers_copilot_config_dir(tmp_path: Path):
    env = {
        "COPILOT_CONFIG_DIR": str(tmp_path / "custom"),
        "XDG_CONFIG_HOME": str(tmp_path / "xdg"),
    }
    assert default_config_dir(env) == tmp_path / "custom"


def test_default_config_dir_uses_xdg_config_home(tmp_path: Path):
    assert default_config_dir({"XDG_CONFIG_HOME": str(tmp_path / "xdg")}) == (
        tmp_path / "xdg" / "copilot"
    )


def test_install_creates_idempotent_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_copilot(repo_root)

    first = install(repo_root=repo_root, config_dir=config_dir)
    second = install(repo_root=repo_root, config_dir=config_dir)

    assert first.ok
    assert first.linked == 3
    assert second.ok
    assert second.unchanged == 3
    assert (config_dir / "agents" / "demo__agent.agent.md").is_symlink()
    assert (config_dir / "skills" / "demo-hello").is_symlink()
    assert (config_dir / "demo" / "commands").is_symlink()


def test_install_refuses_to_overwrite_real_files(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_copilot(repo_root)
    target = config_dir / "agents" / "demo__agent.agent.md"
    target.parent.mkdir(parents=True)
    target.write_text("user file\n")

    report = install(repo_root=repo_root, config_dir=config_dir)

    assert not report.ok
    assert "not a symlink" in report.errors[0]
    assert target.read_text() == "user file\n"


def test_force_replaces_conflicting_symlink_only(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    other = tmp_path / "other.agent.md"
    other.write_text("other\n")
    _write_generated_copilot(repo_root)
    target = config_dir / "agents" / "demo__agent.agent.md"
    target.parent.mkdir(parents=True)
    target.symlink_to(other)

    blocked = install(repo_root=repo_root, config_dir=config_dir)
    forced = install(repo_root=repo_root, config_dir=config_dir, force=True)

    assert not blocked.ok
    assert forced.ok
    assert (
        target.resolve() == (repo_root / ".copilot" / "agents" / "demo__agent.agent.md").resolve()
    )


def test_main_does_not_clear_caches_on_failed_install(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_copilot(repo_root)

    # Conflict: a real (non-symlink) file already at the install destination.
    target = config_dir / "agents" / "demo__agent.agent.md"
    target.parent.mkdir(parents=True)
    target.write_text("user file\n")

    pkg_dir = config_dir / "pkg"
    pkg_dir.mkdir(parents=True)
    pkg_sentinel = pkg_dir / "sentinel.txt"
    pkg_sentinel.write_text("pkg\n")

    marketplace_cache_dir = config_dir / "marketplace-cache"
    marketplace_cache_dir.mkdir(parents=True)
    marketplace_sentinel = marketplace_cache_dir / "sentinel.txt"
    marketplace_sentinel.write_text("marketplace\n")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "install_copilot.py",
            "install",
            "--repo-root",
            str(repo_root),
            "--config-dir",
            str(config_dir),
        ],
    )

    result = main()

    assert result != 0
    assert pkg_sentinel.exists()
    assert marketplace_sentinel.exists()


def test_main_clears_caches_on_successful_install(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_copilot(repo_root)

    pkg_dir = config_dir / "pkg"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "sentinel.txt").write_text("pkg\n")

    marketplace_cache_dir = config_dir / "marketplace-cache"
    marketplace_cache_dir.mkdir(parents=True)
    (marketplace_cache_dir / "sentinel.txt").write_text("marketplace\n")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "install_copilot.py",
            "install",
            "--repo-root",
            str(repo_root),
            "--config-dir",
            str(config_dir),
        ],
    )

    result = main()

    assert result == 0
    assert not pkg_dir.exists()
    assert not marketplace_cache_dir.exists()


def test_uninstall_removes_only_repo_owned_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_copilot(repo_root)
    assert install(repo_root=repo_root, config_dir=config_dir).ok

    unrelated_target = tmp_path / "unrelated.agent.md"
    unrelated_target.write_text("unrelated\n")
    unrelated = config_dir / "agents" / "unrelated.agent.md"
    unrelated.symlink_to(unrelated_target)
    real_file = config_dir / "skills" / "user.md"
    real_file.write_text("user\n")

    report = uninstall(repo_root=repo_root, config_dir=config_dir)

    assert report.ok
    assert report.removed == 3
    assert not (config_dir / "agents" / "demo__agent.agent.md").exists()
    assert unrelated.is_symlink()
    assert real_file.read_text() == "user\n"
