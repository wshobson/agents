import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "eval_all.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False
    )


def test_non_quick_depth_is_rejected(tmp_path: Path) -> None:
    for depth in ("standard", "deep"):
        proc = run("--depth", depth, "--output-dir", str(tmp_path))
        assert proc.returncode == 2
        assert "static layer only" in proc.stderr


def test_quick_depth_still_accepted_in_help() -> None:
    proc = run("--help")
    assert proc.returncode == 0
    assert "--depth" in proc.stdout


def test_summary_has_no_interval_column(tmp_path: Path) -> None:
    proc = run("--only-changed", "plugin-eval", "--output-dir", str(tmp_path))
    assert proc.returncode == 0
    assert "95% CI" not in proc.stdout
    assert "| Plugin | Score | Badge | Confidence | Duration |" in proc.stdout
