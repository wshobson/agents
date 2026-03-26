import pytest

from plugin_eval.elo import EloCalculator


class TestEloCalculator:
    def test_expected_score(self):
        calc = EloCalculator(k_factor=32)
        assert calc.expected(1500, 1500) == pytest.approx(0.5)
        assert calc.expected(1600, 1500) > 0.5
        assert calc.expected(1400, 1500) < 0.5

    def test_update_win(self):
        calc = EloCalculator(k_factor=32)
        new_rating = calc.update(1500, 1500, actual=1.0)
        assert new_rating > 1500
        assert new_rating == pytest.approx(1516.0)

    def test_update_loss(self):
        calc = EloCalculator(k_factor=32)
        new_rating = calc.update(1500, 1500, actual=0.0)
        assert new_rating < 1500

    def test_update_draw(self):
        calc = EloCalculator(k_factor=32)
        new_rating = calc.update(1500, 1500, actual=0.5)
        assert new_rating == pytest.approx(1500.0)

    def test_compute_rating_from_matchups(self):
        calc = EloCalculator(k_factor=32)
        matchups = [
            (1540, 1.0),
            (1500, 0.0),
            (1460, 1.0),
        ]
        final = calc.compute_rating(1500, matchups)
        assert final > 1500

    def test_bootstrap_ci(self):
        calc = EloCalculator(k_factor=32)
        matchups = [
            (1540, 1.0),
            (1500, 0.0),
            (1460, 1.0),
            (1520, 0.5),
        ]
        rating, lower, upper = calc.compute_rating_with_ci(1500, matchups, seed=42)
        assert lower <= rating <= upper or lower == upper
