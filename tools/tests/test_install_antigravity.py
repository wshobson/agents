"""Tests for safe Antigravity global install/uninstall helper."""

from __future__ import annotations

from pathlib import Path

from tools.install_antigravity import default_config_dir, install, uninstall


def _write_generated_antigravity(repo_root: Path) -> None:
    agents = repo_root / ".antigravity" / "agents" / "demo__agent"
    skills = repo_root / ".antigravity" / "skills" / "demo-hello"
    agents.mkdir(parents=True)
    skills.mkdir(parents=True)
    (agents / "agent.json").write_text('{"name": "demo__agent"}\n')
    (skills / "SKILL.md").write_text("---\nname: demo-hello\n---\n\nBody.\n")


def test_default_config_dir_prefers_antigravity_config_dir(tmp_path: Path):
    env = {
        "ANTIGRAVITY_CONFIG_DIR": str(tmp_path / "custom"),
    }
    assert default_config_dir(env) == tmp_path / "custom"


def test_install_creates_idempotent_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_antigravity(repo_root)

    first = install(repo_root=repo_root, config_dir=config_dir)
    second = install(repo_root=repo_root, config_dir=config_dir)

    assert first.ok
    assert first.linked == 2
    assert second.ok
    assert second.unchanged == 2
    assert (config_dir / "agents" / "demo__agent").is_symlink()
    assert (config_dir / "skills" / "demo-hello").is_symlink()


def test_install_refuses_to_overwrite_real_files(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_antigravity(repo_root)
    target = config_dir / "agents" / "demo__agent"
    target.parent.mkdir(parents=True)
    target.write_text("user file\n")

    report = install(repo_root=repo_root, config_dir=config_dir)

    assert not report.ok
    assert "not a symlink" in report.errors[0]
    assert target.read_text() == "user file\n"


def test_force_replaces_conflicting_symlink_only(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    other = tmp_path / "other_dir"
    other.mkdir()
    _write_generated_antigravity(repo_root)
    target = config_dir / "agents" / "demo__agent"
    target.parent.mkdir(parents=True)
    target.symlink_to(other, target_is_directory=True)

    blocked = install(repo_root=repo_root, config_dir=config_dir)
    forced = install(repo_root=repo_root, config_dir=config_dir, force=True)

    assert not blocked.ok
    assert forced.ok
    assert target.resolve() == (repo_root / ".antigravity" / "agents" / "demo__agent").resolve()


def test_uninstall_removes_only_repo_owned_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_antigravity(repo_root)
    assert install(repo_root=repo_root, config_dir=config_dir).ok

    unrelated_target = tmp_path / "unrelated_dir"
    unrelated_target.mkdir()
    unrelated = config_dir / "agents" / "unrelated"
    unrelated.symlink_to(unrelated_target, target_is_directory=True)
    real_file = config_dir / "skills" / "user.md"
    real_file.write_text("user\n")

    report = uninstall(repo_root=repo_root, config_dir=config_dir)

    assert report.removed == 2
    assert report.skipped == 2  # unrelated symlink + real file
    assert not (config_dir / "agents" / "demo__agent").exists()
    assert not (config_dir / "skills" / "demo-hello").exists()
    assert unrelated.is_symlink()
    assert real_file.is_file()
