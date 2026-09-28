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


def test_default_config_dir_defaults_to_gemini_config_dir():
    assert default_config_dir({}) == Path.home() / ".gemini" / "config"


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


def _legacy_link(repo_root: Path, legacy_dir: Path, name: str = "demo") -> Path:
    link = legacy_dir / "plugins" / name
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(repo_root / ".antigravity" / "plugins" / name)
    return link


def test_install_moves_repo_links_out_of_the_legacy_dir(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    legacy_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)
    old = _legacy_link(repo_root, legacy_dir)
    unrelated_target = tmp_path / "unrelated-plugin"
    unrelated_target.mkdir()
    unrelated = legacy_dir / "plugins" / "unrelated"
    unrelated.symlink_to(unrelated_target)

    report = install(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=legacy_dir)

    assert report.ok
    assert report.linked == 1
    assert report.migrated == 1
    assert (config_dir / "plugins" / "demo").is_symlink()
    assert not old.is_symlink()
    assert unrelated.is_symlink()


def test_install_keeps_legacy_link_when_new_link_fails(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    legacy_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)
    old = _legacy_link(repo_root, legacy_dir)
    (config_dir / "plugins" / "demo").mkdir(parents=True)

    report = install(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=legacy_dir)

    assert not report.ok
    assert report.migrated == 0
    assert old.is_symlink()


def test_install_ignores_legacy_dir_when_it_is_the_config_dir(tmp_path: Path):
    """ANTIGRAVITY_CONFIG_DIR pointed at the old path must not unlink the new links."""
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)

    report = install(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=config_dir)

    assert report.ok
    assert report.migrated == 0
    assert (config_dir / "plugins" / "demo").is_symlink()


def test_install_ignores_legacy_plugins_dir_that_aliases_the_new_one(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    legacy_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)
    (config_dir / "plugins").mkdir(parents=True)
    legacy_dir.mkdir()
    (legacy_dir / "plugins").symlink_to(config_dir / "plugins")

    report = install(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=legacy_dir)

    assert report.ok
    assert report.migrated == 0
    assert (config_dir / "plugins" / "demo").is_symlink()


def test_install_removes_legacy_links_for_plugins_no_longer_generated(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    legacy_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)
    gone = _legacy_link(repo_root, legacy_dir, name="removed-plugin")

    report = install(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=legacy_dir)

    assert report.ok
    assert report.migrated == 1
    assert not gone.is_symlink()


def test_failed_install_keeps_legacy_links_for_removed_plugins(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    legacy_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)
    gone = _legacy_link(repo_root, legacy_dir, name="removed-plugin")
    (config_dir / "plugins" / "demo").mkdir(parents=True)

    report = install(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=legacy_dir)

    assert not report.ok
    assert gone.is_symlink()


def test_uninstall_also_removes_repo_links_from_the_legacy_dir(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    legacy_dir = tmp_path / "antigravity-cli"
    _write_generated_antigravity(repo_root)
    old = _legacy_link(repo_root, legacy_dir)

    report = uninstall(repo_root=repo_root, config_dir=config_dir, legacy_config_dir=legacy_dir)

    assert report.ok
    assert report.removed == 1
    assert not old.is_symlink()


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
