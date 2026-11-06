#!/usr/bin/env python3
"""Install the generated Qwen Code extension into the user's Qwen home by symlink.

Qwen Code loads extensions from `<qwen-home>/extensions/<name>/` and reads the
`qwen-extension.json` manifest inside. The adapter emits one extension holding
every plugin, so a single symlink is enough:

    ~/.qwen/extensions/qwen-code-workflows -> <repo>/.qwen/extensions/qwen-code-workflows

`qwen extensions link <path>` is the equivalent native command.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_ROOT = REPO_ROOT / ".qwen" / "extensions"
EXTENSION_NAME = "qwen-code-workflows"


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
    """Qwen's global home: `QWEN_HOME` wins, else `~/.qwen`."""
    resolved: dict[str, str] = env if env is not None else dict(os.environ)
    if resolved.get("QWEN_HOME"):
        return Path(resolved["QWEN_HOME"]).expanduser()
    return Path.home() / ".qwen"


def _is_relative_to(child: Path, parent: Path) -> bool:
    """Return whether the child path resolves inside the parent path."""
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def _generated_extension(repo_root: Path) -> Path:
    """Return the generated extension directory, or explain that it is missing."""
    source = repo_root / ".qwen" / "extensions" / EXTENSION_NAME
    if not source.is_dir():
        raise FileNotFoundError(
            f"No generated extension at {source}; run `make generate HARNESS=qwen` first"
        )
    if not (source / "qwen-extension.json").is_file():
        raise FileNotFoundError(
            f"{source} has no qwen-extension.json; run `make generate HARNESS=qwen` first"
        )
    return source


def install(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
    force: bool = False,
) -> InstallReport:
    """Symlink the generated extension into the user's Qwen home.

    An existing non-symlink target is never overwritten; a symlink that points
    somewhere else is only replaced when force=True.
    """
    config_dir = (config_dir or default_config_dir()).expanduser()
    report = InstallReport()
    try:
        source = _generated_extension(repo_root)
    except FileNotFoundError as exc:
        report.errors.append(str(exc))
        return report

    target = config_dir / "extensions" / EXTENSION_NAME
    if target.is_symlink():
        if target.resolve(strict=False) == source.resolve(strict=False):
            report.unchanged += 1
            return report
        if not force:
            report.errors.append(
                f"{target} already exists as a symlink to {target.resolve(strict=False)}; "
                "rerun with FORCE=1 to replace symlink conflicts"
            )
            return report
        target.unlink()
    elif target.exists():
        report.errors.append(f"{target} already exists and is not a symlink; refusing to overwrite")
        return report

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source.resolve(), target_is_directory=True)
    report.linked += 1
    return report


def uninstall(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
) -> InstallReport:
    """Remove the symlink this repository owns, leaving foreign targets alone."""
    config_dir = (config_dir or default_config_dir()).expanduser()
    generated_root = (repo_root / ".qwen" / "extensions").resolve(strict=False)
    report = InstallReport()
    target = config_dir / "extensions" / EXTENSION_NAME
    if not target.exists() and not target.is_symlink():
        return report
    if not target.is_symlink():
        report.skipped += 1
        return report
    if _is_relative_to(target.resolve(strict=False), generated_root):
        target.unlink()
        report.removed += 1
    else:
        report.skipped += 1
    return report


def _print_report(action: str, config_dir: Path, report: InstallReport) -> None:
    """Print a one-line summary of an install or uninstall action."""
    print(
        f"{action}: config={config_dir} linked={report.linked} unchanged={report.unchanged} "
        f"removed={report.removed} skipped={report.skipped}"
    )
    for error in report.errors:
        print(f"error: {error}")


def main() -> int:
    """Install or uninstall the generated Qwen Code extension."""
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
