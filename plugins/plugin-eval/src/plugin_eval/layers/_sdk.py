"""Shared helper for reading Claude Agent SDK message streams.

Both the judge and Monte Carlo layers consume the same `query()` message stream
(assistant text blocks + a terminal result message). This centralizes that
walk so the two layers can't drift on how SDK message types are handled.
"""

from __future__ import annotations

from typing import Any, NamedTuple


class SdkOutput(NamedTuple):
    """Extracted view of one SDK message stream."""

    text: str  # concatenated assistant TextBlock text
    result: str | None  # ResultMessage.result, if present (fallback text)
    errored: bool  # a ResultMessage reported is_error
    usage: dict[str, Any] | None  # ResultMessage.usage, if it was a dict


def collect_sdk_output(messages: list) -> SdkOutput:
    """Walk SDK messages → assistant text, result fallback, error flag, usage."""
    from claude_agent_sdk import (  # type: ignore[import-untyped]
        AssistantMessage,
        ResultMessage,
        TextBlock,
    )

    text = ""
    result: str | None = None
    errored = False
    usage: dict[str, Any] | None = None
    for message in messages:
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text += block.text
        elif isinstance(message, ResultMessage):
            if message.is_error:
                errored = True
            if message.result:
                result = message.result
            if isinstance(message.usage, dict):
                usage = message.usage
    return SdkOutput(text=text, result=result, errored=errored, usage=usage)


def usage_total_tokens(usage: dict[str, Any] | None) -> int:
    """Total token count from an SDK usage dict.

    The SDK's `usage` exposes separate `*_tokens` fields (input/output/cache),
    not a single `total_tokens`. Prefer an explicit `total_tokens` if a future
    SDK provides one, otherwise sum the component `*_tokens` fields.
    """
    if not usage:
        return 0
    total = usage.get("total_tokens")
    if isinstance(total, int):
        return total
    return sum(n for k, n in usage.items() if k.endswith("_tokens") and isinstance(n, int))
