"""Tests for the Pi global install/uninstall helper."""

from __future__ import annotations

from pathlib import Path

from tools.install_pi import default_config_dir, install, uninstall


def _write_generated_pi(repo_root: Path) -> None:
    root = repo_root / ".pi"
    (root / "skills" / "demo" / "hello").mkdir(parents=True)
    (root / "skills" / "demo" / "hello" / "SKILL.md").write_text(
        "---\nname: hello\ndescription: Use when testing.\n---\n\nBody.\n"
    )
    (root / "prompts").mkdir(parents=True)
    (root / "prompts" / "demo__say-hi.md").write_text("---\ndescription: d\n---\n\nHi $ARGUMENTS\n")
    (root / "agents").mkdir(parents=True)
    (root / "agents" / "demo__greeter.md").write_text(
        "---\nname: greeter\ndescription: Use when greeting.\n---\n\nYou greet.\n"
    )


def test_default_config_dir_prefers_pi_coding_agent_dir(tmp_path: Path):
    env = {"PI_CODING_AGENT_DIR": str(tmp_path / "custom")}
    assert default_config_dir(env) == tmp_path / "custom"


def test_default_config_dir_defaults_to_home_pi_agent():
    assert default_config_dir({}) == Path.home() / ".pi" / "agent"


def test_install_links_skill_dirs_prompt_files_and_agent_files(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_pi(repo_root)

    first = install(repo_root=repo_root, config_dir=config_dir)
    second = install(repo_root=repo_root, config_dir=config_dir)

    assert first.ok and first.linked == 3
    assert second.ok and second.unchanged == 3 and second.linked == 0
    assert (config_dir / "skills" / "demo").is_symlink()
    assert (config_dir / "skills" / "demo" / "hello" / "SKILL.md").is_file()
    assert (config_dir / "prompts" / "demo__say-hi.md").is_symlink()
    assert (config_dir / "agents" / "demo__greeter.md").is_symlink()


def test_install_refuses_to_overwrite_real_files(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_pi(repo_root)
    (config_dir / "prompts").mkdir(parents=True)
    (config_dir / "prompts" / "demo__say-hi.md").write_text("user file\n")

    report = install(repo_root=repo_root, config_dir=config_dir)

    assert not report.ok
    assert "not a symlink" in report.errors[0]
    assert (config_dir / "prompts" / "demo__say-hi.md").read_text() == "user file\n"


def test_install_force_replaces_only_symlink_conflicts(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_pi(repo_root)
    (config_dir / "agents").mkdir(parents=True)
    (config_dir / "agents" / "demo__greeter.md").symlink_to(tmp_path / "elsewhere.md")
    (config_dir / "prompts").mkdir(parents=True)
    (config_dir / "prompts" / "demo__say-hi.md").write_text("user file\n")

    without_force = install(repo_root=repo_root, config_dir=config_dir)
    with_force = install(repo_root=repo_root, config_dir=config_dir, force=True)

    assert not without_force.ok
    assert any("FORCE=1" in e for e in without_force.errors)
    assert (config_dir / "agents" / "demo__greeter.md").resolve() == (
        repo_root / ".pi" / "agents" / "demo__greeter.md"
    ).resolve()
    # Force replaces the symlink conflict, but a real file is still refused.
    assert not with_force.ok
    assert any("not a symlink" in e for e in with_force.errors)
    assert (config_dir / "prompts" / "demo__say-hi.md").read_text() == "user file\n"


def test_uninstall_removes_only_repo_owned_symlinks(tmp_path: Path):
    repo_root = tmp_path / "repo"
    config_dir = tmp_path / "config"
    _write_generated_pi(repo_root)
    install(repo_root=repo_root, config_dir=config_dir)
    (config_dir / "prompts" / "mine.md").write_text("keep me\n")
    (config_dir / "skills" / "other").symlink_to(tmp_path / "other-skills")

    report = uninstall(repo_root=repo_root, config_dir=config_dir)

    assert report.removed == 3
    assert (config_dir / "prompts" / "mine.md").is_file()
    assert (config_dir / "skills" / "other").is_symlink()
    assert not (config_dir / "agents" / "demo__greeter.md").exists()


def test_install_without_generated_tree_reports_error(tmp_path: Path):
    report = install(repo_root=tmp_path / "repo", config_dir=tmp_path / "config")
    assert not report.ok
    assert "make generate HARNESS=pi" in report.errors[0]
