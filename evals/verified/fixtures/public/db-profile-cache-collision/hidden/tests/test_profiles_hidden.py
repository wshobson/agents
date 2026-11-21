import unittest

from app import cache, orgs, users


class CollisionTest(unittest.TestCase):
    def setUp(self):
        cache.clear()

    def test_org_then_user(self):
        self.assertEqual(orgs.load_profile(7)["kind"], "org")
        self.assertEqual(users.load_profile(7)["kind"], "user")

    def test_user_then_org(self):
        self.assertEqual(users.load_profile(7)["kind"], "user")
        self.assertEqual(orgs.load_profile(7)["kind"], "org")

    def test_cache_still_caches(self):
        first = users.load_profile(8)
        self.assertIs(users.load_profile(8), first)


if __name__ == "__main__":
    unittest.main()
