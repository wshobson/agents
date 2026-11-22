import unittest

from pager.pages import page, page_count


class PagesTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(page_count(10, 3), 4)
        self.assertEqual(page_count(0, 3), 1)

    def test_last_page(self):
        self.assertEqual(page(list(range(9)), 3, 3), [6, 7, 8])


if __name__ == "__main__":
    unittest.main()
