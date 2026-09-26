"""Data models for synthetic trace prompts."""

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
