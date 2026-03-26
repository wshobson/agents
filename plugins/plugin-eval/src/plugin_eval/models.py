"""Data models for PluginEval evaluation results."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, computed_field, field_validator


class Depth(StrEnum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"
    THOROUGH = "thorough"

    @property
    def confidence_label(self) -> str:
        return {
            Depth.QUICK: "Estimated",
            Depth.STANDARD: "Assessed",
            Depth.DEEP: "Certified",
            Depth.THOROUGH: "Certified+",
        }[self]

    @property
    def layers(self) -> list[str]:
        return {
            Depth.QUICK: ["static"],
            Depth.STANDARD: ["static", "judge"],
            Depth.DEEP: ["static", "judge", "monte_carlo"],
            Depth.THOROUGH: ["static", "judge", "monte_carlo"],
        }[self]


class EvalConfig(BaseModel):
    depth: Depth = Depth.STANDARD
    concurrency: int = Field(default=4, ge=1, le=20)
    model_tier: str = "auto"
    output_format: str = "json"
    verbose: bool = False
    corpus_path: str | None = None
    auth: str = "max"
    judges: int = Field(default=1, ge=1, le=5)
    monte_carlo_n: int | None = None


class AntiPattern(BaseModel):
    flag: str
    description: str
    severity: float = Field(default=0.05, ge=0.0, le=0.5)


class StaticSubScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=1.0)
    details: dict[str, Any] = Field(default_factory=dict)


class DimensionScore(BaseModel):
    name: str
    weight: float = Field(ge=0.0, le=1.0)
    score: float = Field(ge=0.0, le=1.0)
    ci_lower: float | None = None
    ci_upper: float | None = None
    grade: str | None = None
    evidence: list[str] = Field(default_factory=list)

    @computed_field
    @property
    def weighted_score(self) -> float:
        return self.weight * self.score

    @field_validator("score", "ci_lower", "ci_upper", mode="before")
    @classmethod
    def clamp_score(cls, v: float | None) -> float | None:
        if v is None:
            return v
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Score must be between 0 and 1, got {v}")
        return v


class LayerResult(BaseModel):
    layer: str
    score: float = Field(ge=0.0, le=1.0)
    sub_scores: dict[str, Any] = Field(default_factory=dict)
    anti_patterns: list[AntiPattern] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EloMatchup(BaseModel):
    opponent: str
    opponent_elo: float
    result: str
    score: float = Field(ge=0.0, le=1.0)
    position_bias_check: str = "not_checked"

    @field_validator("result")
    @classmethod
    def validate_result(cls, v: str) -> str:
        if v not in ("win", "loss", "draw"):
            raise ValueError(f"Result must be win/loss/draw, got {v}")
        return v


class EloResult(BaseModel):
    rating: float = 1500.0
    ci_lower: float | None = None
    ci_upper: float | None = None
    corpus_percentile: float | None = None
    matches: list[EloMatchup] = Field(default_factory=list)
    closest_comparable: str | None = None
    dimensional_wins: list[str] = Field(default_factory=list)
    dimensional_losses: list[str] = Field(default_factory=list)


class Badge(StrEnum):
    PLATINUM = "platinum"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    NO_BADGE = "no_badge"

    @classmethod
    def from_scores(cls, composite: float, elo: float | None) -> Badge:
        thresholds = [
            (cls.PLATINUM, 90, 1600),
            (cls.GOLD, 80, 1500),
            (cls.SILVER, 70, 1400),
            (cls.BRONZE, 60, 1300),
        ]
        for badge, score_min, elo_min in thresholds:
            if composite >= score_min and (elo is None or elo >= elo_min):
                return badge
        return cls.NO_BADGE

    @property
    def stars(self) -> str:
        return {
            Badge.PLATINUM: "★★★★★",
            Badge.GOLD: "★★★★",
            Badge.SILVER: "★★★",
            Badge.BRONZE: "★★",
            Badge.NO_BADGE: "—",
        }[self]


class CompositeResult(BaseModel):
    score: float = Field(ge=0.0, le=100.0)
    ci_lower: float | None = None
    ci_upper: float | None = None
    anti_pattern_penalty: float = Field(default=1.0, ge=0.5, le=1.0)
    dimensions: list[DimensionScore] = Field(default_factory=list)
    badge: Badge = Badge.NO_BADGE
    confidence_label: str = "Estimated"


class PluginEvalResult(BaseModel):
    plugin_path: str
    timestamp: str
    config: EvalConfig
    layers: list[LayerResult] = Field(default_factory=list)
    composite: CompositeResult | None = None
    elo: EloResult | None = None
    model_usage: dict[str, int] = Field(default_factory=dict)
    total_duration_ms: int | None = None
