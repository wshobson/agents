"""Elo rating system for pairwise skill comparison."""

from __future__ import annotations

import random


class EloCalculator:
    def __init__(self, k_factor: int = 32) -> None:
        self.k_factor = k_factor

    def expected(self, rating_a: float, rating_b: float) -> float:
        """Expected score for player A against player B."""
        return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400))

    def update(self, rating: float, opponent_rating: float, actual: float) -> float:
        """Update rating after a single matchup."""
        exp = self.expected(rating, opponent_rating)
        return rating + self.k_factor * (actual - exp)

    def compute_rating(self, initial: float, matchups: list[tuple[float, float]]) -> float:
        """Compute final rating from (opponent_rating, actual_score) matchups."""
        rating = initial
        for opponent_rating, actual in matchups:
            rating = self.update(rating, opponent_rating, actual)
        return rating

    def compute_rating_with_ci(
        self,
        initial: float,
        matchups: list[tuple[float, float]],
        n_resamples: int = 500,
        seed: int | None = None,
    ) -> tuple[float, float, float]:
        """Compute rating with bootstrap CI by resampling matchups."""
        point_estimate = self.compute_rating(initial, matchups)

        if len(matchups) < 2:
            return point_estimate, point_estimate, point_estimate

        rng = random.Random(seed)
        ratings = []
        for _ in range(n_resamples):
            sample = [rng.choice(matchups) for _ in range(len(matchups))]
            ratings.append(self.compute_rating(initial, sample))

        ratings.sort()
        lower_idx = int(0.025 * n_resamples)
        upper_idx = int(0.975 * n_resamples) - 1
        return point_estimate, ratings[lower_idx], ratings[upper_idx]
