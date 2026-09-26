"""Whether each trace's target skill fired as its prompt expected.

This is a descriptive feature of one trace, for the review app to show as a badge and to
cluster on. It is not an evaluator and computes no rates. If error analysis later confirms
mis-triggering as a failure mode, trigger_outcome becomes the code-based evaluator for it.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, get_args

from plugin_eval.traces.models import TraceRecord

TriggerOutcome = Literal[
    "hit", "missed", "false_trigger", "correct_abstain", "error", "contaminated"
]


def trigger_outcome(trace: TraceRecord) -> TriggerOutcome:
    """Classify one trace. Contamination wins over an error, and both win over routing."""
    if trace.contaminated:
        return "contaminated"
    if trace.is_error:
        return "error"
    fired = trace.prompt.target_skill in trace.skills_invoked
    if trace.prompt.routing == "should_trigger":
        return "hit" if fired else "missed"
    return "false_trigger" if fired else "correct_abstain"


def outcome_counts(traces: Iterable[TraceRecord]) -> dict[str, int]:
    """Count traces per outcome. Every outcome is a key, with 0 when no trace has it."""
    counts = dict.fromkeys(get_args(TriggerOutcome), 0)
    for trace in traces:
        counts[trigger_outcome(trace)] += 1
    return counts
