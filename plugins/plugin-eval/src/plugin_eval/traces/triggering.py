"""Whether each trace's target skill fired as its prompt expected.

This is a descriptive feature of one trace, for the review app to show as a badge and to
cluster on. It is not an evaluator and computes no rates. If error analysis later confirms
mis-triggering as a failure mode, trigger_outcome becomes the code-based evaluator for it.

A contaminated trace is always "contaminated". Otherwise, once the target skill fired, the
Skill call has settled routing, so the outcome is "hit" or "false_trigger" even when the
session later ended in an error, for example at the turn cap. A trace is "error" only when
it ended in an error and the target did not fire.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, get_args

from plugin_eval.traces.models import TraceRecord

TriggerOutcome = Literal[
    "hit", "missed", "false_trigger", "correct_abstain", "error", "contaminated"
]


def target_fired(trace: TraceRecord) -> bool:
    """Whether the trace invoked its target skill.

    skills_invoked keeps each Skill call's input as given, so a plugin skill appears as
    "plugin:skill". A call matches the target by its full name, or by its bare name when it
    has no namespace. The same bare name in another plugin does not match.
    """
    prompt = trace.prompt
    names = {f"{prompt.target_plugin}:{prompt.target_skill}", prompt.target_skill}
    return any(name in names for name in trace.skills_invoked)


def trigger_outcome(trace: TraceRecord) -> TriggerOutcome:
    """Classify one trace. See the module docstring for the order of the rules."""
    if trace.contaminated:
        return "contaminated"
    fired = target_fired(trace)
    if fired:
        return "hit" if trace.prompt.routing == "should_trigger" else "false_trigger"
    if trace.is_error:
        return "error"
    return "missed" if trace.prompt.routing == "should_trigger" else "correct_abstain"


def outcome_counts(traces: Iterable[TraceRecord]) -> dict[str, int]:
    """Count traces per outcome. Every outcome is a key, with 0 when no trace has it."""
    counts = dict.fromkeys(get_args(TriggerOutcome), 0)
    for trace in traces:
        counts[trigger_outcome(trace)] += 1
    return counts
