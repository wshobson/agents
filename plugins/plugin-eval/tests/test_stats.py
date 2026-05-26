import pytest

from plugin_eval.stats import (
    bootstrap_ci,
    clopper_pearson_ci,
    cohens_kappa,
    coefficient_of_variation,
    wilson_score_ci,
)


class TestWilsonScore:
    def test_perfect_activation(self):
        lower, upper = wilson_score_ci(successes=50, trials=50, confidence=0.95)
        assert lower > 0.90
        assert upper == pytest.approx(1.0, abs=0.01)

    def test_half_activation(self):
        lower, upper = wilson_score_ci(successes=25, trials=50, confidence=0.95)
        assert lower < 0.50
        assert upper > 0.50
        assert lower > 0.35
        assert upper < 0.65

    def test_zero_trials_raises(self):
        with pytest.raises(ValueError):
            wilson_score_ci(successes=0, trials=0)

    def test_successes_exceed_trials_raises(self):
        with pytest.raises(ValueError):
            wilson_score_ci(successes=10, trials=5)


class TestBootstrapCI:
    def test_tight_data(self):
        data = [0.80, 0.82, 0.81, 0.83, 0.79, 0.80, 0.82, 0.81]
        lower, upper = bootstrap_ci(data, confidence=0.95, n_resamples=1000, seed=42)
        assert lower > 0.78
        assert upper < 0.84
        assert lower < upper

    def test_single_value(self):
        lower, upper = bootstrap_ci([0.5], confidence=0.95, n_resamples=100, seed=42)
        assert lower == pytest.approx(0.5)
        assert upper == pytest.approx(0.5)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            bootstrap_ci([], confidence=0.95)


class TestClopperPearson:
    def test_zero_failures(self):
        lower, upper = clopper_pearson_ci(failures=0, trials=50, confidence=0.95)
        assert lower == 0.0
        assert upper < 0.10

    def test_some_failures(self):
        lower, upper = clopper_pearson_ci(failures=2, trials=50, confidence=0.95)
        assert lower < 0.04
        assert upper > 0.04
        assert upper < 0.15

    def test_zero_trials_raises(self):
        with pytest.raises(ValueError):
            clopper_pearson_ci(failures=0, trials=0)


class TestCoefficientOfVariation:
    def test_low_variation(self):
        data = [0.80, 0.82, 0.81, 0.83, 0.79]
        cv = coefficient_of_variation(data)
        assert cv < 0.05

    def test_high_variation(self):
        data = [0.20, 0.90, 0.10, 0.95, 0.50]
        cv = coefficient_of_variation(data)
        assert cv > 0.40

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            coefficient_of_variation([])


class TestCohensKappa:
    def test_perfect_agreement(self):
        rater1 = [1, 2, 3, 4, 5]
        rater2 = [1, 2, 3, 4, 5]
        k = cohens_kappa(rater1, rater2)
        assert k == pytest.approx(1.0)

    def test_no_agreement(self):
        rater1 = [1, 2, 3, 4, 5]
        rater2 = [5, 4, 3, 2, 1]
        k = cohens_kappa(rater1, rater2)
        assert k < 0.0

    def test_mismatched_length_raises(self):
        with pytest.raises(ValueError):
            cohens_kappa([1, 2], [1, 2, 3])
