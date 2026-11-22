import unittest

from app import cache, orgs, users


class ProfilesTest(unittest.TestCase):
    def setUp(self):
        cache.clear()

    def test_user(self):
        self.assertEqual(users.load_profile(7)["name"], "Ada")

    def test_org(self):
        self.assertEqual(orgs.load_profile(7)["name"], "Acme")


if __name__ == "__main__":
    unittest.main()
