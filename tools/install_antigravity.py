#!/usr/bin/env python3
"""Install generated Antigravity artifacts into the user's Antigravity config directory."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_ROOT = REPO_ROOT / ".antigravity"
ARTIFACT_GLOBS = {
    "agents": "*",
    "skills": "*",
    "workflows": "*.md",
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
    env = env or os.environ
    if env.get("ANTIGRAVITY_CONFIG_DIR"):
        return Path(env["ANTIGRAVITY_CONFIG_DIR"]).expanduser()
    return Path.home() / ".gemini" / "antigravity-cli"


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def _generated_artifacts(repo_root: Path) -> list[tuple[str, Path]]:
    generated_root = repo_root / ".antigravity"
    artifacts: list[tuple[str, Path]] = []
    for subdir, pattern in ARTIFACT_GLOBS.items():
        source_dir = generated_root / subdir
        if not source_dir.is_dir():
            continue
        for src in sorted(source_dir.glob(pattern)):
            if subdir in {"agents", "skills"} and not src.is_dir():
                continue
            if subdir == "workflows" and not src.is_file():
                continue
            artifacts.append((subdir, src.resolve()))
    if not artifacts:
        raise FileNotFoundError(
            f"No artifacts found under {generated_root}; "
            "run `make generate HARNESS=antigravity` first"
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
        dst = config_dir / subdir / src.name
        _link_one(src, dst, force=force, report=report)
    return report


def uninstall(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
) -> InstallReport:
    config_dir = (config_dir or default_config_dir()).expanduser()
    generated_root = (repo_root / ".antigravity").resolve(strict=False)
    report = InstallReport()

    for subdir in ARTIFACT_GLOBS:
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


def list_installed(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
) -> InstallReport:
    config_dir = (config_dir or default_config_dir()).expanduser()
    generated_root = (repo_root / ".antigravity").resolve(strict=False)
    report = InstallReport()

    for subdir in ARTIFACT_GLOBS:
        target_dir = config_dir / subdir
        if not target_dir.is_dir():
            continue
        for dst in sorted(target_dir.iterdir()):
            if not dst.is_symlink():
                continue
            target = dst.resolve(strict=False)
            if _is_relative_to(target, generated_root):
                print(f"  linked:  {subdir}/{dst.name} -> {target}")
                report.linked += 1
            else:
                print(f"  foreign: {subdir}/{dst.name} -> {target}")
    return report


def _print_report(action: str, config_dir: Path, report: InstallReport) -> None:
    if action == "list":
        print(
            f"{action}: config={config_dir} repo-owned={report.linked} foreign={report.skipped}"
        )
    else:
        print(
            f"{action}: config={config_dir} linked={report.linked} unchanged={report.unchanged} "
            f"removed={report.removed} skipped={report.skipped}"
        )
    for error in report.errors:
        print(f"error: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall", "list"))
    parser.add_argument("--config-dir", type=Path, default=None)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--force", action="store_true", help="Replace conflicting symlinks only"
    )
    args = parser.parse_args()

    if args.config_dir:
        targets = [args.config_dir.expanduser()]
    else:
        home = Path.home()
        targets = [
            home / ".gemini" / "antigravity-cli",
            home / ".gemini" / "antigravity-ide",
            home / ".gemini" / "antigravity",
        ]

    ok = True
    for target in targets:
        if args.action == "install":
            report = install(
                repo_root=args.repo_root, config_dir=target, force=args.force
            )
        elif args.action == "list":
            report = list_installed(repo_root=args.repo_root, config_dir=target)
        else:
            report = uninstall(repo_root=args.repo_root, config_dir=target)
        _print_report(args.action, target, report)
        if not report.ok:
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
