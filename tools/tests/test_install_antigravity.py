"""Tests for safe Antigravity global install/uninstall helper."""

from __future__ import annotations

from pathlib import Path

from tools.install_antigravity import default_config_dir, install, uninstall


def _write_generated_antigravity(repo_root: Path) -> None:
    plugin_dir = repo_root / ".antigravity" / "plugins" / "demo"
    (plugin_dir / "skills" / "hello").mkdir(parents=True)
    (plugin_dir / "agents").mkdir(parents=True)
    (plugin_dir / "plugin.json").write_text('{"name": "demo", "description": "Demo"}\n')
    (plugin_dir / "skills" / "hello" / "SKILL.md").write_text(
        "---\nname: hello\ndescription: Use when testing.\n---\n\nBody.\n"
    )
    (plugin_dir / "agents" / "greeter.md").write_text(
        "---\nname: greeter\ndescription: Use for testing.\nmodel: pro\nsubagent: true\n---\n\nBody.\n"
    )


def test_default_config_dir_prefers_antigravity_config_dir(tmp_path: Path):
    env = {"ANTIGRAVITY_CONFIG_DIR": str(tmp_path / "custom")}
    assert default_config_dir(env) == tmp_path / "custom"


def test_default_config_dir_defaults_to_gemini_antigravity_cli():
    assert default_config_dir({}) == Path.home() / ".gemini" / "antigravity-cli"


def test_install_creates_idempotent_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_antigravity(repo_root)

    first = install(repo_root=repo_root, config_dir=config_dir)
    second = install(repo_root=repo_root, config_dir=config_dir)

    assert first.ok
    assert first.linked == 1
    assert second.ok
    assert second.unchanged == 1
    assert (config_dir / "plugins" / "demo").is_symlink()
    assert (config_dir / "plugins" / "demo" / "plugin.json").is_file()


def test_install_refuses_to_overwrite_real_files(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_antigravity(repo_root)
    target = config_dir / "plugins" / "demo"
    target.mkdir(parents=True)
    (target / "existing.txt").write_text("user file\n")

    report = install(repo_root=repo_root, config_dir=config_dir)

    assert not report.ok
    assert "not a symlink" in report.errors[0]
    assert (target / "existing.txt").read_text() == "user file\n"


def test_force_replaces_conflicting_symlink_only(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    other = tmp_path / "other-plugin"
    other.mkdir()
    _write_generated_antigravity(repo_root)
    target = config_dir / "plugins" / "demo"
    target.parent.mkdir(parents=True)
    target.symlink_to(other)

    blocked = install(repo_root=repo_root, config_dir=config_dir)
    forced = install(repo_root=repo_root, config_dir=config_dir, force=True)

    assert not blocked.ok
    assert forced.ok
    assert target.resolve() == (repo_root / ".antigravity" / "plugins" / "demo").resolve()


def test_uninstall_removes_only_repo_owned_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_antigravity(repo_root)
    assert install(repo_root=repo_root, config_dir=config_dir).ok

    unrelated_target = tmp_path / "unrelated-plugin"
    unrelated_target.mkdir()
    unrelated = config_dir / "plugins" / "unrelated"
    unrelated.symlink_to(unrelated_target)
    real_dir = config_dir / "plugins" / "real"
    real_dir.mkdir()

    report = uninstall(repo_root=repo_root, config_dir=config_dir)

    assert report.ok
    assert report.removed == 1
    assert not (config_dir / "plugins" / "demo").exists()
    assert unrelated.is_symlink()
    assert real_dir.is_dir()


def test_install_errors_when_nothing_generated(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"

    report = install(repo_root=repo_root, config_dir=config_dir)

    assert not report.ok
    assert "No artifacts found" in report.errors[0]


def test_uninstall_no_op_when_nothing_installed(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"

    report = uninstall(repo_root=repo_root, config_dir=config_dir)

    assert report.ok
    assert report.removed == 0
