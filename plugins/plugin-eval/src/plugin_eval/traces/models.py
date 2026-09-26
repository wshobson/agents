"""Data models for synthetic trace prompts and the traces they produce."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

Explicitness = Literal["names_topic", "describes_problem", "vague"]
Routing = Literal["should_trigger", "near_miss", "off_topic"]
TaskShape = Literal["design", "write_code", "review_snippet", "explain"]


class PromptTuple(BaseModel):
    """One combination of dimension values that defines a test prompt."""

    id: str
    target_plugin: str
    target_skill: str
    explicitness: Explicitness
    routing: Routing
    task_shape: TaskShape


class PromptRecord(PromptTuple):
    """A tuple with the user message an LLM wrote for it."""

    query: str
    generator_model: str


class ToolCall(BaseModel):
    """One tool call in a trace, paired with its result."""

    name: str
    input_summary: str  # JSON of the input, truncated to 2,000 characters
    result_summary: str = ""  # tool result text, truncated to 4,000 characters
    is_error: bool = False


class Step(BaseModel):
    """One assistant action in a trace: a text block or a tool call."""

    kind: Literal["assistant_text", "tool_call"]
    text: str | None = None
    tool: ToolCall | None = None


class TraceRecord(BaseModel):
    """One headless Claude Code session run for one prompt.

    skills_available is the init event's skill list as reported, so plugin skills carry
    their namespace ("plugin:skill"). skills_invoked holds the skill input of each Skill tool
    call as given, in order, so plugin skills carry their namespace there too. Use
    triggering.target_fired to tell whether the target fired. contaminated is True when the
    session saw a skill, tool, plugin, or MCP server that the runner did not load, when a
    loaded skill was missing, when a hook ran, or when the stream had no init event.
    contamination_reasons names each cause, for example "unexpected skill: x".
    """

    prompt: PromptRecord
    model: str
    plugins_loaded: list[str]
    skills_available: list[str] = []
    skills_invoked: list[str] = []
    steps: list[Step] = []
    final_text: str = ""
    cost_usd: float = 0.0
    num_turns: int = 0
    duration_ms: int = 0
    is_error: bool = False
    error: str | None = None
    contaminated: bool = False
    contamination_reasons: list[str] = []
    claude_version: str = ""
    # How far cost_usd went past the per-trace cap. Claude Code checks --max-budget-usd
    # between turns, so the turn that crosses the cap still completes.
    over_cap_usd: float = 0.0
