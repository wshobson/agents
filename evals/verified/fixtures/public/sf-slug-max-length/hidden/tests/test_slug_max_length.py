import unittest

from textkit.slug import slugify


class MaxLengthTest(unittest.TestCase):
    def test_unchanged_without_limit(self):
        self.assertEqual(slugify("The Quick Brown Fox"), "the-quick-brown-fox")

    def test_cuts_at_word_boundary(self):
        self.assertEqual(slugify("The Quick Brown Fox", max_length=12), "the-quick")

    def test_exact_fit(self):
        self.assertEqual(slugify("The Quick Brown Fox", max_length=15), "the-quick-brown")

    def test_no_trailing_hyphen(self):
        self.assertFalse(slugify("ab cd ef", max_length=3).endswith("-"))
        self.assertEqual(slugify("ab cd ef", max_length=3), "ab")

    def test_long_first_word(self):
        self.assertEqual(slugify("Supercalifragilistic day", max_length=5), "super")

    def test_limit_longer_than_slug(self):
        self.assertEqual(slugify("Short", max_length=50), "short")

    def test_rejects_small_limit(self):
        with self.assertRaises(ValueError):
            slugify("anything", max_length=0)


if __name__ == "__main__":
    unittest.main()
