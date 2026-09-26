"""Tests for the per-trace trigger outcome and its descriptive counts."""

from typing import get_args

import pytest

from plugin_eval.traces.models import PromptRecord, TraceRecord
from plugin_eval.traces.triggering import TriggerOutcome, outcome_counts, trigger_outcome

TARGET = "postgresql-table-design"


def trace(
    routing: str = "should_trigger",
    skills_invoked: list[str] | None = None,
    *,
    is_error: bool = False,
    contaminated: bool = False,
) -> TraceRecord:
    prompt = PromptRecord.model_validate(
        {
            "id": "p001",
            "target_plugin": "database-design",
            "target_skill": TARGET,
            "explicitness": "names_topic",
            "routing": routing,
            "task_shape": "design",
            "query": "Design a PostgreSQL table for storing invoices.",
            "generator_model": "claude-opus-5",
        }
    )
    return TraceRecord(
        prompt=prompt,
        model="claude-opus-5-5",
        plugins_loaded=["database-design"],
        skills_invoked=skills_invoked or [],
        is_error=is_error,
        contaminated=contaminated,
    )


def test_should_trigger_with_target_invoked_is_hit() -> None:
    assert trigger_outcome(trace("should_trigger", ["other-skill", TARGET])) == "hit"


def test_should_trigger_without_target_is_missed() -> None:
    assert trigger_outcome(trace("should_trigger", ["other-skill"])) == "missed"
    assert trigger_outcome(trace("should_trigger", [])) == "missed"


@pytest.mark.parametrize("routing", ["near_miss", "off_topic"])
def test_non_trigger_routing_with_target_invoked_is_false_trigger(routing: str) -> None:
    assert trigger_outcome(trace(routing, [TARGET])) == "false_trigger"


@pytest.mark.parametrize("routing", ["near_miss", "off_topic"])
def test_non_trigger_routing_without_target_is_correct_abstain(routing: str) -> None:
    assert trigger_outcome(trace(routing, ["other-skill"])) == "correct_abstain"
    assert trigger_outcome(trace(routing, [])) == "correct_abstain"


def test_error_without_the_target_firing_is_error() -> None:
    assert trigger_outcome(trace("should_trigger", [], is_error=True)) == "error"
    assert trigger_outcome(trace("off_topic", ["other-skill"], is_error=True)) == "error"


def test_target_fired_then_hit_the_turn_cap_is_still_routed() -> None:
    fired = [f"database-design:{TARGET}"]
    assert trigger_outcome(trace("should_trigger", fired, is_error=True)) == "hit"
    assert trigger_outcome(trace("near_miss", fired, is_error=True)) == "false_trigger"


def test_namespaced_target_fires_and_a_same_named_distractor_does_not() -> None:
    assert trigger_outcome(trace("should_trigger", [f"database-design:{TARGET}"])) == "hit"
    distractor = [f"other-plugin:{TARGET}"]
    assert trigger_outcome(trace("should_trigger", distractor)) == "missed"
    assert trigger_outcome(trace("near_miss", distractor)) == "correct_abstain"


def test_contaminated_takes_precedence_over_error_and_routing() -> None:
    both = trace("should_trigger", [TARGET], is_error=True, contaminated=True)
    assert trigger_outcome(both) == "contaminated"
    assert trigger_outcome(trace("near_miss", [TARGET], contaminated=True)) == "contaminated"


def test_outcome_counts_on_mixed_list() -> None:
    traces = [
        trace("should_trigger", [TARGET]),
        trace("should_trigger", [TARGET]),
        trace("should_trigger", []),
        trace("near_miss", [TARGET]),
        trace("off_topic", []),
        trace("near_miss", []),
        trace("should_trigger", [], is_error=True),
        trace("should_trigger", [f"database-design:{TARGET}"], is_error=True),
    ]
    assert outcome_counts(traces) == {
        "hit": 3,
        "missed": 1,
        "false_trigger": 1,
        "correct_abstain": 2,
        "error": 1,
        "contaminated": 0,
    }


def test_outcome_counts_has_every_outcome_key_even_when_empty() -> None:
    counts = outcome_counts(iter([]))
    assert list(counts) == list(get_args(TriggerOutcome))
    assert set(counts.values()) == {0}
