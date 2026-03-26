"""End-to-end tests using real plugins from the claude-agents repo."""

from pathlib import Path

import pytest

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig

REPO_ROOT = Path(__file__).parent.parent.parent.parent  # plugins/plugin-eval/tests -> claude-agents


@pytest.mark.skipif(
    not (REPO_ROOT / "plugins" / "observability-monitoring").exists(),
    reason="Real plugin directory not available",
)
class TestE2ERealPlugins:
    def test_score_real_skill_quick(self):
        skill_dir = (
            REPO_ROOT / "plugins" / "observability-monitoring" / "skills" / "distributed-tracing"
        )
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(skill_dir)

        assert result.composite is not None
        assert result.composite.score > 50  # known good skill
        assert len(result.layers) == 1

    def test_score_real_plugin_quick(self):
        plugin_dir = REPO_ROOT / "plugins" / "observability-monitoring"
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_plugin(plugin_dir)

        assert result.composite is not None
        assert result.composite.score > 40

    def test_score_agent_teams_quick(self):
        """Test a coordination-style plugin (shorter skills)."""
        skill_dir = REPO_ROOT / "plugins" / "agent-teams" / "skills" / "multi-reviewer-patterns"
        if not skill_dir.exists():
            pytest.skip("agent-teams plugin not available")
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(skill_dir)
        assert result.composite.score > 30
