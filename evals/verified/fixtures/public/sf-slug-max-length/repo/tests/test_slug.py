import unittest

from textkit.slug import slugify


class SlugifyTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_accents(self):
        self.assertEqual(slugify("Crème Brûlée"), "creme-brulee")

    def test_empty(self):
        self.assertEqual(slugify("  !!  "), "")


if __name__ == "__main__":
    unittest.main()
