#!/usr/bin/env python3
"""Install generated Pi artifacts into the user's Pi config directory by symlink.

Pi discovers skills recursively under <config>/skills/, prompt templates flat under
<config>/prompts/, and the reference subagent extension reads agents flat under
<config>/agents/. So each plugin's skill directory, each prompt file, and each agent
file gets its own symlink. `pi install /path/to/agents/.pi` is the package
alternative for skills and prompts; agents have no package resource type, which is
why this helper exists.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_ROOT = REPO_ROOT / ".pi"


@dataclass
class InstallReport:
    linked: int = 0
    unchanged: int = 0
    removed: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def default_config_dir(env: dict[str, str] | None = None) -> Path:
    resolved: dict[str, str] = env if env is not None else dict(os.environ)
    if resolved.get("PI_CODING_AGENT_DIR"):
        return Path(resolved["PI_CODING_AGENT_DIR"]).expanduser()
    return Path.home() / ".pi" / "agent"


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def _generated_entries(repo_root: Path) -> list[tuple[Path, Path]]:
    """(source, relative destination) pairs: skill plugin dirs, prompt files, agent files."""
    root = repo_root / ".pi"
    if not root.is_dir():
        raise FileNotFoundError(
            f"No artifacts found under {root}; run `make generate HARNESS=pi` first"
        )
    entries: list[tuple[Path, Path]] = []
    skills = root / "skills"
    if skills.is_dir():
        for plugin_dir in sorted(p for p in skills.iterdir() if p.is_dir()):
            entries.append((plugin_dir, Path("skills") / plugin_dir.name))
    for sub in ("prompts", "agents"):
        d = root / sub
        if d.is_dir():
            for md in sorted(d.glob("*.md")):
                entries.append((md, Path(sub) / md.name))
    if not entries:
        raise FileNotFoundError(
            f"No skills, prompts, or agents found under {root}; run `make generate HARNESS=pi` first"
        )
    return entries


def _link_one(src: Path, dst: Path, *, force: bool, report: InstallReport) -> None:
    if dst.is_symlink():
        if dst.resolve(strict=False) == src:
            report.unchanged += 1
            return
        if not force:
            report.errors.append(
                f"{dst} already exists as a symlink to {dst.resolve(strict=False)}; "
                "rerun with FORCE=1 to replace symlink conflicts"
            )
            return
        dst.unlink()
    elif dst.exists():
        report.errors.append(f"{dst} already exists and is not a symlink; refusing to overwrite")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.symlink_to(src, target_is_directory=src.is_dir())
    report.linked += 1


def install(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
    force: bool = False,
) -> InstallReport:
    config_dir = (config_dir or default_config_dir()).expanduser()
    report = InstallReport()
    try:
        entries = _generated_entries(repo_root)
    except FileNotFoundError as exc:
        report.errors.append(str(exc))
        return report
    for src, rel in entries:
        _link_one(src.resolve(), config_dir / rel, force=force, report=report)
    return report


def uninstall(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
) -> InstallReport:
    config_dir = (config_dir or default_config_dir()).expanduser()
    generated_root = (repo_root / ".pi").resolve(strict=False)
    report = InstallReport()
    for sub in ("skills", "prompts", "agents"):
        target_dir = config_dir / sub
        if not target_dir.is_dir():
            continue
        for dst in sorted(target_dir.iterdir()):
            if not dst.is_symlink():
                report.skipped += 1
                continue
            if _is_relative_to(dst.resolve(strict=False), generated_root):
                dst.unlink()
                report.removed += 1
            else:
                report.skipped += 1
    return report


def _print_report(action: str, config_dir: Path, report: InstallReport) -> None:
    print(
        f"{action}: config={config_dir} linked={report.linked} unchanged={report.unchanged} "
        f"removed={report.removed} skipped={report.skipped}"
    )
    for error in report.errors:
        print(f"error: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall"))
    parser.add_argument("--config-dir", type=Path, default=None)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--force", action="store_true", help="Replace conflicting symlinks only")
    args = parser.parse_args()

    config_dir = (args.config_dir or default_config_dir()).expanduser()
    if args.action == "install":
        report = install(repo_root=args.repo_root, config_dir=config_dir, force=args.force)
    else:
        report = uninstall(repo_root=args.repo_root, config_dir=config_dir)
    _print_report(args.action, config_dir, report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
