"""Tests for safe OpenCode global install/uninstall helper."""

from __future__ import annotations

from pathlib import Path

from tools.install_opencode import default_config_dir, install, uninstall


def _write_generated_opencode(repo_root: Path) -> None:
    agents = repo_root / ".opencode" / "agents"
    commands = repo_root / ".opencode" / "commands"
    skills = repo_root / ".opencode" / "skills" / "demo-hello"
    agents.mkdir(parents=True)
    commands.mkdir(parents=True)
    skills.mkdir(parents=True)
    (agents / "demo__agent.md").write_text("agent\n")
    (commands / "demo__command.md").write_text("command\n")
    (skills / "SKILL.md").write_text("---\nname: demo-hello\n---\n\nBody.\n")


def test_default_config_dir_prefers_opencode_config_dir(tmp_path: Path):
    env = {
        "OPENCODE_CONFIG_DIR": str(tmp_path / "custom"),
        "XDG_CONFIG_HOME": str(tmp_path / "xdg"),
    }
    assert default_config_dir(env) == tmp_path / "custom"


def test_default_config_dir_uses_xdg_config_home(tmp_path: Path):
    assert default_config_dir({"XDG_CONFIG_HOME": str(tmp_path / "xdg")}) == (
        tmp_path / "xdg" / "opencode"
    )


def test_install_creates_idempotent_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_opencode(repo_root)

    first = install(repo_root=repo_root, config_dir=config_dir)
    second = install(repo_root=repo_root, config_dir=config_dir)

    assert first.ok
    assert first.linked == 3
    assert second.ok
    assert second.unchanged == 3
    assert (config_dir / "agents" / "demo__agent.md").is_symlink()
    assert (config_dir / "commands" / "demo__command.md").is_symlink()
    assert (config_dir / "skills" / "demo-hello").is_symlink()


def test_install_refuses_to_overwrite_real_files(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_opencode(repo_root)
    target = config_dir / "agents" / "demo__agent.md"
    target.parent.mkdir(parents=True)
    target.write_text("user file\n")

    report = install(repo_root=repo_root, config_dir=config_dir)

    assert not report.ok
    assert "not a symlink" in report.errors[0]
    assert target.read_text() == "user file\n"


def test_force_replaces_conflicting_symlink_only(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    other = tmp_path / "other.md"
    other.write_text("other\n")
    _write_generated_opencode(repo_root)
    target = config_dir / "agents" / "demo__agent.md"
    target.parent.mkdir(parents=True)
    target.symlink_to(other)

    blocked = install(repo_root=repo_root, config_dir=config_dir)
    forced = install(repo_root=repo_root, config_dir=config_dir, force=True)

    assert not blocked.ok
    assert forced.ok
    assert target.resolve() == (repo_root / ".opencode" / "agents" / "demo__agent.md").resolve()


def test_uninstall_removes_only_repo_owned_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_opencode(repo_root)
    assert install(repo_root=repo_root, config_dir=config_dir).ok

    unrelated_target = tmp_path / "unrelated.md"
    unrelated_target.write_text("unrelated\n")
    unrelated = config_dir / "agents" / "unrelated.md"
    unrelated.symlink_to(unrelated_target)
    real_file = config_dir / "commands" / "user.md"
    real_file.write_text("user\n")

    report = uninstall(repo_root=repo_root, config_dir=config_dir)

    assert report.ok
    assert report.removed == 3
    assert not (config_dir / "agents" / "demo__agent.md").exists()
    assert unrelated.is_symlink()
    assert real_file.read_text() == "user\n"
