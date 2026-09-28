#!/usr/bin/env python3
"""Install generated Antigravity artifacts into the user's agy plugins directory."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_ROOT = REPO_ROOT / ".antigravity"


@dataclass
class InstallReport:
    linked: int = 0
    unchanged: int = 0
    removed: int = 0
    migrated: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def default_config_dir(env: dict[str, str] | None = None) -> Path:
    resolved: dict[str, str] = env if env is not None else dict(os.environ)
    if resolved.get("ANTIGRAVITY_CONFIG_DIR"):
        return Path(resolved["ANTIGRAVITY_CONFIG_DIR"]).expanduser()
    return Path.home() / ".gemini" / "config"


def default_legacy_config_dir() -> Path:
    """The directory installs used before agy moved plugins to ``~/.gemini/config``."""
    return Path.home() / ".gemini" / "antigravity-cli"


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def _generated_plugins(repo_root: Path) -> list[Path]:
    generated_root = repo_root / ".antigravity" / "plugins"
    if not generated_root.is_dir():
        raise FileNotFoundError(
            f"No artifacts found under {generated_root}; "
            "run `make generate HARNESS=antigravity` first"
        )
    plugins = sorted(p for p in generated_root.iterdir() if p.is_dir())
    if not plugins:
        raise FileNotFoundError(
            f"No plugin directories found under {generated_root}; "
            "run `make generate HARNESS=antigravity` first"
        )
    return plugins


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


def _legacy_plugins_dir(config_dir: Path, legacy_config_dir: Path | None) -> Path | None:
    """Return the old plugins dir to clean, or None when it is the config dir itself."""
    if legacy_config_dir is None:
        return None
    legacy = legacy_config_dir.expanduser()
    if legacy.resolve(strict=False) == config_dir.resolve(strict=False):
        return None
    return legacy / "plugins"


def _is_repo_link(path: Path, generated_root: Path) -> bool:
    return path.is_symlink() and _is_relative_to(path.resolve(strict=False), generated_root)


def install(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
    legacy_config_dir: Path | None = None,
    force: bool = False,
) -> InstallReport:
    """Link each generated plugin into ``config_dir``.

    A repo-owned link for the same plugin in ``legacy_config_dir`` is removed once the
    new link is in place, so an upgrade does not leave the plugin installed twice.
    """
    config_dir = (config_dir or default_config_dir()).expanduser()
    legacy_plugins = _legacy_plugins_dir(config_dir, legacy_config_dir)
    generated_root = (repo_root / ".antigravity" / "plugins").resolve(strict=False)
    report = InstallReport()
    try:
        plugins = _generated_plugins(repo_root)
    except FileNotFoundError as exc:
        report.errors.append(str(exc))
        return report

    for src in plugins:
        dst = config_dir / "plugins" / src.name
        _link_one(src.resolve(), dst, force=force, report=report)
        if legacy_plugins is None or dst.resolve(strict=False) != src.resolve():
            continue
        old = legacy_plugins / src.name
        if _is_repo_link(old, generated_root):
            old.unlink()
            report.migrated += 1
    return report


def _remove_repo_links(target_dir: Path, generated_root: Path, report: InstallReport) -> None:
    if not target_dir.is_dir():
        return
    for dst in sorted(target_dir.iterdir()):
        if _is_repo_link(dst, generated_root):
            dst.unlink()
            report.removed += 1
        else:
            report.skipped += 1


def uninstall(
    *,
    repo_root: Path = REPO_ROOT,
    config_dir: Path | None = None,
    legacy_config_dir: Path | None = None,
) -> InstallReport:
    config_dir = (config_dir or default_config_dir()).expanduser()
    legacy_plugins = _legacy_plugins_dir(config_dir, legacy_config_dir)
    generated_root = (repo_root / ".antigravity" / "plugins").resolve(strict=False)
    report = InstallReport()

    _remove_repo_links(config_dir / "plugins", generated_root, report)
    if legacy_plugins is not None:
        _remove_repo_links(legacy_plugins, generated_root, report)
    return report


def _print_report(action: str, config_dir: Path, report: InstallReport) -> None:
    print(
        f"{action}: config={config_dir} linked={report.linked} unchanged={report.unchanged} "
        f"removed={report.removed} migrated={report.migrated} skipped={report.skipped}"
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
    # Only a default install can have used the old default, so leave the old
    # directory alone when the caller chose a config dir.
    uses_default = args.config_dir is None and not os.environ.get("ANTIGRAVITY_CONFIG_DIR")
    legacy_config_dir = default_legacy_config_dir() if uses_default else None
    if args.action == "install":
        report = install(
            repo_root=args.repo_root,
            config_dir=config_dir,
            legacy_config_dir=legacy_config_dir,
            force=args.force,
        )
    else:
        report = uninstall(
            repo_root=args.repo_root,
            config_dir=config_dir,
            legacy_config_dir=legacy_config_dir,
        )
    _print_report(args.action, config_dir, report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
