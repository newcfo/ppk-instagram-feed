import datetime as dt
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "build_feed", pathlib.Path(__file__).with_name("build_feed.py")
)
feed_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feed_module)


class TestBuildFeed(unittest.TestCase):
    def setUp(self):
        self.feed = {
            "username": "perfectpotion.kr",
            "posts": [
                {
                    "permalink": f"https://www.instagram.com/p/SHORT{i}/",
                    "timestamp": f"2026-11-{16-i:02d}T10:00:00+0000",
                    "sizes": {
                        "medium": {
                            "mediaUrl": f"https://cdn2.behold.pictures/assets/{i}.webp"
                        }
                    },
                    "altText": f"Post {i}"
                }
                for i in range(6)
            ],
        }

    def test_six(self):
        payload = feed_module.build_payload(
            self.feed, now=dt.datetime(2026, 11, 17, tzinfo=dt.timezone.utc)
        )
        self.assertEqual(len(payload["posts"]), 6)
        self.assertTrue(payload["posts"][0]["url"].endswith("SHORT0/"))
        self.assertIn("window.PPK_INSTAGRAM_WEEKLY", feed_module.build_js(payload))

    def test_wrong_user_rejected(self):
        self.feed["username"] = "stranger"
        with self.assertRaises(ValueError):
            feed_module.build_payload(self.feed)

    def test_short_rejected(self):
        self.feed["posts"] = self.feed["posts"][:4]
        with self.assertRaises(ValueError):
            feed_module.build_payload(self.feed)

    def test_bad_thumbnail_rejected(self):
        self.feed["posts"][0]["sizes"]["medium"]["mediaUrl"] = "https://evil.example/1.png"
        with self.assertRaises(ValueError):
            feed_module.build_payload(self.feed)


if __name__ == "__main__":
    unittest.main()
