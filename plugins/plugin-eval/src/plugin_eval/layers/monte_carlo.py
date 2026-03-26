"""Layer 3: Monte Carlo simulation — statistical reliability testing via repeated runs."""

from __future__ import annotations

import asyncio
import statistics
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from plugin_eval.models import LayerResult
from plugin_eval.parser import ParsedSkill, parse_skill
from plugin_eval.stats import (
    bootstrap_ci,
    clopper_pearson_ci,
    coefficient_of_variation,
    wilson_score_ci,
)

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class SimResult:
    """Result of a single simulation run."""

    activated: bool
    quality_score: float
    tokens: int
    duration_ms: int
    errored: bool = False
    prompt: str = ""


@dataclass
class MonteCarloConfig:
    """Configuration for Monte Carlo simulation runs."""

    n_runs: int = 50
    concurrency: int = 4
    auth: str = "max"
    seed: int = 42
    progress_callback: Callable[[int, int], None] | None = None


# ---------------------------------------------------------------------------
# Single simulation runner
# ---------------------------------------------------------------------------


async def run_simulation(skill_content: str, prompt: str, auth: str) -> SimResult:
    """Run a single simulation via Agent SDK. Returns SimResult. On error, errored=True."""
    try:
        import claude_agent_sdk as sdk  # type: ignore[import-untyped]

        result_text = ""
        activated = False
        tokens = 0

        import time

        start = time.monotonic()

        async for event in sdk.stream(
            prompt,
            system=f"You are evaluating a skill. Apply the skill if appropriate.\n\n{skill_content}",
        ):
            if hasattr(event, "text"):
                result_text += event.text
                activated = True
            if hasattr(event, "usage"):
                tokens = getattr(event.usage, "total_tokens", 0)

        duration_ms = int((time.monotonic() - start) * 1000)

        # Estimate quality score from response length and coherence heuristic
        quality_score = min(1.0, len(result_text) / 500) if activated else 0.0

        return SimResult(
            activated=activated,
            quality_score=quality_score,
            tokens=tokens,
            duration_ms=duration_ms,
            prompt=prompt,
        )

    except Exception:
        return SimResult(
            activated=False,
            quality_score=0.0,
            tokens=0,
            duration_ms=0,
            errored=True,
            prompt=prompt,
        )


# ---------------------------------------------------------------------------
# Analyzer
# ---------------------------------------------------------------------------


class MonteCarloAnalyzer:
    """Statistical reliability testing via repeated simulated runs."""

    def __init__(self, config: MonteCarloConfig) -> None:
        self.config = config
        self._sem = asyncio.Semaphore(config.concurrency)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def analyze_skill(self, skill_or_dir: Path | ParsedSkill) -> LayerResult:
        """Generate prompts, run N simulations, compute statistics, return LayerResult."""
        skill = skill_or_dir if isinstance(skill_or_dir, ParsedSkill) else parse_skill(skill_or_dir)
        skill_content = skill.raw_content

        prompts = await self._generate_prompts(skill.name, skill.description)

        # Repeat prompts to reach n_runs
        repeated: list[str] = []
        while len(repeated) < self.config.n_runs:
            repeated.extend(prompts)
        prompts_to_run = repeated[: self.config.n_runs]

        results = await self._run_all(skill_content, prompts_to_run)
        stats = self._compute_statistics(results)

        triggering = stats["triggering"]
        output_consistency = stats["output_consistency"]
        failure_rate = stats["failure_rate"]
        token_efficiency = stats["token_efficiency"]

        activation_rate = triggering.get("activation_rate", 0.0)
        cv = output_consistency.get("cv", 1.0)
        p_fail = failure_rate.get("p_fail", 1.0)
        efficiency_norm = token_efficiency.get("efficiency_norm", 0.0)

        # Composite: 0.40 * trigger_reliability + 0.30 * (1-cv) + 0.20 * (1-p_fail) + 0.10 * efficiency_norm
        score = (
            0.40 * activation_rate
            + 0.30 * (1.0 - min(1.0, cv))
            + 0.20 * (1.0 - p_fail)
            + 0.10 * efficiency_norm
        )
        score = max(0.0, min(1.0, score))

        sub_scores: dict = {
            "triggering": triggering,
            "output_consistency": output_consistency,
            "failure_rate": failure_rate,
            "token_efficiency": token_efficiency,
        }

        metadata: dict = {
            "n_runs": len(results),
            "n_activated": sum(1 for r in results if r.activated),
            "n_errored": sum(1 for r in results if r.errored),
        }

        return LayerResult(
            layer="monte_carlo",
            score=score,
            sub_scores=sub_scores,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # Prompt generation
    # ------------------------------------------------------------------

    async def _generate_prompts(self, name: str, description: str) -> list[str]:
        """Use Haiku to generate 15 varied prompts. Falls back to basic variants."""
        try:
            from plugin_eval.layers.judge import query_llm

            model = "claude-haiku-4-5-20251001"
            system = (
                "You are generating test prompts for a Claude Code skill. "
                "Respond ONLY with a JSON array of strings — no explanation, no markdown fences."
            )
            prompt = (
                f"Generate 15 varied user prompts that would trigger this skill:\n\n"
                f"Name: {name}\n"
                f"Description: {description}\n\n"
                f'Return a JSON array of 15 strings. Example: ["prompt 1", "prompt 2", ...]'
            )
            result = await query_llm(prompt, system=system, model=model)
            if isinstance(result, list) and len(result) >= 5:
                return [str(p) for p in result[:15]]
        except Exception:
            pass

        # Fallback: generate basic variants from description
        return self._fallback_prompts(name, description)

    def _fallback_prompts(self, name: str, description: str) -> list[str]:
        """Generate basic prompt variants when LLM is unavailable."""
        base = description.split(".")[0].strip() if description else name
        variants = [
            f"Please help me with {name}.",
            f"I need to {base.lower()}.",
            f"Can you {base.lower()}?",
            f"Help me {base.lower()}.",
            f"Run {name} for me.",
            f"Use {name} to help with my task.",
            f"I want to {base.lower()}.",
            f"Execute {name}.",
            f"Apply {name}.",
            f"Invoke {name} now.",
            f"Start {name}.",
            f"Please execute {name} on this.",
            f"I'd like to use {name}.",
            f"Trigger {name}.",
            f"Activate {name} for this request.",
        ]
        return variants[:15]

    # ------------------------------------------------------------------
    # Running simulations
    # ------------------------------------------------------------------

    async def _run_all(self, skill_content: str, prompts: list[str]) -> list[SimResult]:
        """Run all simulations with semaphore throttling."""
        completed = 0
        total = len(prompts)

        async def run_one(prompt: str) -> SimResult:
            nonlocal completed
            async with self._sem:
                result = await run_simulation(skill_content, prompt, self.config.auth)
                completed += 1
                if self.config.progress_callback:
                    self.config.progress_callback(completed, total)
                return result

        tasks = [run_one(p) for p in prompts]
        return list(await asyncio.gather(*tasks))

    # ------------------------------------------------------------------
    # Statistical analysis
    # ------------------------------------------------------------------

    def _compute_statistics(self, results: list[SimResult]) -> dict:
        """Compute statistical measures from simulation results."""
        n = len(results)
        if n == 0:
            return {
                "triggering": {"activation_rate": 0.0},
                "output_consistency": {"mean_quality": 0.0, "std_dev": 0.0, "cv": 1.0},
                "failure_rate": {"p_fail": 1.0},
                "token_efficiency": {"median": 0, "efficiency_norm": 0.0},
            }

        # --- Triggering ---
        n_activated = sum(1 for r in results if r.activated)
        activation_rate = n_activated / n
        wi_lower, wi_upper = wilson_score_ci(n_activated, n)

        triggering: dict = {
            "activation_rate": activation_rate,
            "wilson_lower": wi_lower,
            "wilson_upper": wi_upper,
            "n_activated": n_activated,
            "n_total": n,
        }

        # --- Output consistency (non-errored, activated runs) ---
        quality_scores = [r.quality_score for r in results if r.activated and not r.errored]
        if quality_scores:
            mean_quality = statistics.mean(quality_scores)
            std_dev = statistics.pstdev(quality_scores) if len(quality_scores) > 1 else 0.0
            cv = coefficient_of_variation(quality_scores) if len(quality_scores) > 1 else 0.0
            if len(quality_scores) > 1:
                bs_lower, bs_upper = bootstrap_ci(quality_scores, seed=self.config.seed)
            else:
                bs_lower, bs_upper = quality_scores[0], quality_scores[0]
        else:
            mean_quality = 0.0
            std_dev = 0.0
            cv = 0.0
            bs_lower, bs_upper = 0.0, 0.0

        output_consistency: dict = {
            "mean_quality": mean_quality,
            "std_dev": std_dev,
            "cv": cv,
            "bootstrap_lower": bs_lower,
            "bootstrap_upper": bs_upper,
        }

        # --- Failure rate ---
        n_errored = sum(1 for r in results if r.errored)
        p_fail = n_errored / n
        cp_lower, cp_upper = clopper_pearson_ci(n_errored, n)

        failure_rate: dict = {
            "p_fail": p_fail,
            "cp_lower": cp_lower,
            "cp_upper": cp_upper,
            "n_errored": n_errored,
        }

        # --- Token efficiency ---
        all_tokens = [r.tokens for r in results if not r.errored]
        if all_tokens:
            sorted_tokens = sorted(all_tokens)
            mid = len(sorted_tokens) // 2
            if len(sorted_tokens) % 2 == 0:
                median_tokens = (sorted_tokens[mid - 1] + sorted_tokens[mid]) / 2
            else:
                median_tokens = float(sorted_tokens[mid])

            q1_idx = len(sorted_tokens) // 4
            q3_idx = (3 * len(sorted_tokens)) // 4
            q1 = float(sorted_tokens[q1_idx])
            q3 = float(sorted_tokens[min(q3_idx, len(sorted_tokens) - 1)])
            iqr = q3 - q1

            # Count outliers: tokens > Q3 + 1.5*IQR
            outlier_threshold = q3 + 1.5 * iqr
            n_outliers = sum(1 for t in all_tokens if t > outlier_threshold)

            # Normalize efficiency: lower tokens = better, cap at 8000 tokens
            TOKEN_CAP = 8000.0
            efficiency_norm = max(0.0, 1.0 - median_tokens / TOKEN_CAP)
        else:
            median_tokens = 0.0
            iqr = 0.0
            n_outliers = 0
            efficiency_norm = 0.0

        token_efficiency: dict = {
            "median": median_tokens,
            "iqr": iqr,
            "outlier_count": n_outliers,
            "efficiency_norm": efficiency_norm,
        }

        return {
            "triggering": triggering,
            "output_consistency": output_consistency,
            "failure_rate": failure_rate,
            "token_efficiency": token_efficiency,
        }
