import unittest

from pager.pages import page


class HiddenPagesTest(unittest.TestCase):
    def test_full_pages(self):
        items = list(range(10))
        self.assertEqual(page(items, 1, 3), [0, 1, 2])
        self.assertEqual(page(items, 2, 3), [3, 4, 5])

    def test_out_of_range(self):
        with self.assertRaises(IndexError):
            page(list(range(10)), 5, 3)

    def test_empty(self):
        self.assertEqual(page([], 1, 3), [])


if __name__ == "__main__":
    unittest.main()
