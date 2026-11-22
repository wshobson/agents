"""Data models for Verified test cases and run results.

`RunResult` is the record written for every run. Its JSON Schema is committed at
scorecards/result.schema.json, and a test keeps that file in step with this model.
"""

from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class CaseKind(StrEnum):
    ORDINARY = "ordinary"
    MULTI_FILE = "multi_file"
    TRAP = "trap"
    STOP_AND_ASK = "stop_and_ask"


class Visibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class CaseSpec(BaseModel):
    """One test case, read from <case>/case.json.

    A case directory holds `repo/` (the project the agent starts from) and `hidden/` (test
    files copied in only after the agent finishes). Commands run from the workspace root.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    workflow: str
    kind: CaseKind
    language: str
    task: str = Field(description="The request given to the agent, word for word.")
    test_command: list[str] = Field(min_length=1)
    build_command: list[str] | None = None
    protected_paths: list[str] = Field(
        default_factory=list,
        description="Files the agent must not delete or edit, such as existing tests.",
    )
    ask_terms: list[str] = Field(
        default_factory=list,
        description=(
            "For a stop-and-ask case: phrases, any one of which the question must contain "
            "(case-insensitive). Pick phrases that appear only when the conflict is named, so "
            "a generic approval prompt or a summary of the wrong fix does not count as asking."
        ),
    )


class RunResult(BaseModel):
    """The outcome of one agent run on one case."""

    model_config = ConfigDict(extra="forbid")

    workflow: str
    workflow_version: str
    harness: str
    harness_version: str
    model: str
    case_id: str
    case_visibility: Visibility
    passed: bool
    failed_checks: list[str] = Field(default_factory=list)
    error: str | None = Field(
        default=None,
        description="Why the harness failed, for a run whose failed_checks is harness_error.",
    )
    tokens_in: int | None = Field(default=None, ge=0)
    tokens_out: int | None = Field(default=None, ge=0)
    cost_usd: float | None = Field(default=None, ge=0)
    wall_seconds: float = Field(ge=0)
    run_at: str = Field(description="ISO 8601 time in UTC, for example 2026-12-01T14:00:00Z.")
    runner_version: str


def load_case(case_dir: Path) -> CaseSpec:
    spec = CaseSpec.model_validate_json((case_dir / "case.json").read_text(encoding="utf-8"))
    if spec.id != case_dir.name:
        raise ValueError(f"case id {spec.id!r} does not match its directory {case_dir.name!r}")
    for sub in ("repo", "hidden"):
        if not (case_dir / sub).is_dir():
            raise ValueError(f"case {spec.id} is missing its {sub}/ directory")
    return spec


def result_schema() -> dict:
    schema = RunResult.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://github.com/wshobson/agents/scorecards/result.schema.json"
    return schema


def result_schema_text() -> str:
    return json.dumps(result_schema(), indent=2, sort_keys=True) + "\n"
