#!/usr/bin/env python3
"""Install generated Copilot artifacts into the user's Copilot config directory."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_ROOT = REPO_ROOT / ".copilot"
ARTIFACT_GLOBS = {
    "agents": "*.agent.md",
    "skills": "*",
    "commands": "*",
}


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
    if resolved.get("COPILOT_CONFIG_DIR"):
        return Path(resolved["COPILOT_CONFIG_DIR"]).expanduser()
    if resolved.get("XDG_CONFIG_HOME"):
        return Path(resolved["XDG_CONFIG_HOME"]).expanduser() / "copilot"
    return Path.home() / ".copilot"


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def _generated_artifacts(repo_root: Path) -> list[tuple[str, Path]]:
    generated_root = repo_root / ".copilot"
    artifacts: list[tuple[str, Path]] = []
    for subdir, pattern in ARTIFACT_GLOBS.items():
        source_dir = generated_root / subdir
        if not source_dir.is_dir():
            continue  # optional dir (commands, etc.) — may not exist
        for src in sorted(source_dir.glob(pattern)):
            if subdir == "skills" and not src.is_dir():
                continue
            if subdir in {"agents"} and not src.is_file():
                continue
            if subdir in {"commands"} and not src.is_dir():
                continue
            artifacts.append((subdir, src.resolve()))
    if not artifacts:
        raise FileNotFoundError(
            f"No artifacts found under {generated_root}; "
            "run `make generate HARNESS=copilot` first"
        )
    return artifacts


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
        report.errors.append(
            f"{dst} already exists and is not a symlink; refusing to overwrite"
        )
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
        artifacts = _generated_artifacts(repo_root)
    except FileNotFoundError as exc:
        report.errors.append(str(exc))
        return report

    for subdir, src in artifacts:
        if subdir == "commands":
            # For commands, extract plugin name and symlink to ~/.copilot/<plugin>/commands/
            # src is like .copilot/commands/comprehensive-review, symlink to ~/.copilot/comprehensive-review/commands
            plugin_name = src.name
            dst = config_dir / plugin_name / "commands"
            _link_one(src, dst, force=force, report=report)
        else:
            dst = config_dir / subdir / src.name
            _link_one(src, dst, force=force, report=report)
    return report


def _clear_copilot_cache(config_dir: Path) -> list[str]:
    """Clear Copilot CLI caches to force artifact discovery reload."""
    cache_dirs = [
        config_dir / "pkg",
        config_dir / "marketplace-cache",
    ]
    cleared = []
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            import shutil

            shutil.rmtree(cache_dir, ignore_errors=True)
            cleared.append(str(cache_dir))
    return cleared


def uninstall(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
) -> InstallReport:
    config_dir = (config_dir or default_config_dir()).expanduser()
    generated_root = (repo_root / ".copilot").resolve(strict=False)
    report = InstallReport()

    for subdir in ARTIFACT_GLOBS:
        if subdir == "commands":
            # commands are installed at config/<plugin>/commands/ (not config/commands/)
            if not config_dir.is_dir():
                continue
            for candidate in sorted(config_dir.iterdir()):
                commands_dir = candidate / "commands"
                if commands_dir.is_symlink():
                    target = commands_dir.resolve(strict=False)
                    if _is_relative_to(target, generated_root):
                        commands_dir.unlink()
                        report.removed += 1
                    else:
                        report.skipped += 1
            continue
        target_dir = config_dir / subdir
        if not target_dir.is_dir():
            continue
        for dst in sorted(target_dir.iterdir()):
            if not dst.is_symlink():
                report.skipped += 1
                continue
            target = dst.resolve(strict=False)
            if _is_relative_to(target, generated_root):
                dst.unlink()
                report.removed += 1
            else:
                report.skipped += 1
    return report


def _print_report(
    action: str,
    config_dir: Path,
    report: InstallReport,
    *,
    cache_cleared: list[str] | None = None,
) -> None:
    print(
        f"{action}: config={config_dir} linked={report.linked} unchanged={report.unchanged} "
        f"removed={report.removed} skipped={report.skipped}"
    )
    if cache_cleared:
        print(f"cache: cleared {len(cache_cleared)} cache dir(s)")
    for error in report.errors:
        print(f"error: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall"))
    parser.add_argument("--config-dir", type=Path, default=None)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--force", action="store_true", help="Replace conflicting symlinks only"
    )
    args = parser.parse_args()

    config_dir = (args.config_dir or default_config_dir()).expanduser()
    cache_cleared = None
    if args.action == "install":
        report = install(
            repo_root=args.repo_root, config_dir=config_dir, force=args.force
        )
        cache_cleared = _clear_copilot_cache(config_dir)
    else:
        report = uninstall(repo_root=args.repo_root, config_dir=config_dir)
    _print_report(args.action, config_dir, report, cache_cleared=cache_cleared)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
