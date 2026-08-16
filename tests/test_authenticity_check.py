import json
from pathlib import Path
import tempfile
import unittest

from src.authenticity_check import run_audit


class AuthenticityAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.kol_path = root / "kols.json"
        self.data_path = root / "data.json"
        self.kols = [
            {
                "id": 1,
                "name": "Verified channel",
                "handle": "@verified",
                "channel_url": "https://www.youtube.com/@verified",
                "channel_id": "UC1234567890123456789012",
                "platform": "YouTube",
                "fans": "10W+",
                "language": "中文",
                "field": "财经",
                "desc": "test",
                "active": True,
            },
            {
                "id": 2,
                "name": "Quarantined placeholder",
                "handle": "placeholder",
                "channel_url": "https://www.youtube.com/results?search_query=placeholder",
                "channel_id": None,
                "platform": "YouTube",
                "fans": "N/A",
                "language": "中文",
                "field": "财经",
                "desc": "test",
                "active": True,
            },
        ]
        self.real_item = {
            "title": "A real RSS title",
            "original_title": "A real RSS title",
            "link": "https://www.youtube.com/watch?v=abcdefghijk",
            "published": "2026-08-15T00:00:00+00:00",
            "summary": "RSS summary",
            "source": "youtube_rss",
            "source_channel_id": "UC1234567890123456789012",
            "is_mock": False,
        }
        self.kol_path.write_text(json.dumps(self.kols), encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_output(self, item):
        payload = {
            "active_kols": [{"kol": self.kols[0], "items": [item]}],
            "inactive_kols": [self.kols[1]],
        }
        self.data_path.write_text(json.dumps(payload), encoding="utf-8")

    def test_quarantined_bad_metadata_does_not_fail_clean_report(self):
        self.write_output(self.real_item)
        audit = run_audit(self.kol_path, self.data_path)
        self.assertEqual(0, audit["summary"]["fail"])
        self.assertEqual(1, audit["summary"]["included_kols"])
        self.assertEqual("PASS", audit["results"][0]["verdict"])
        self.assertEqual("WARN", audit["results"][1]["verdict"])

    def test_mock_item_fails(self):
        item = {
            **self.real_item,
            "link": "https://www.youtube.com/@verified?v=mock0",
            "is_mock": True,
        }
        self.write_output(item)
        audit = run_audit(self.kol_path, self.data_path)
        self.assertEqual(1, audit["summary"]["fail"])
        codes = {issue["code"] for issue in audit["results"][0]["issues"]}
        self.assertIn("MOCK_FLAG", codes)
        self.assertIn("FAKE_LINK", codes)

    def test_rewritten_rss_title_fails(self):
        item = {**self.real_item, "title": "Invented headline"}
        self.write_output(item)
        audit = run_audit(self.kol_path, self.data_path)
        self.assertEqual(1, audit["summary"]["fail"])
        self.assertEqual(1, audit["summary"]["altered_titles"])

    def test_unverifiable_provenance_fails(self):
        item = {
            **self.real_item,
            "link": "https://example.com/video",
            "source": "",
            "source_channel_id": "",
        }
        self.write_output(item)
        audit = run_audit(self.kol_path, self.data_path)
        self.assertEqual(1, audit["summary"]["fail"])
        codes = {issue["code"] for issue in audit["results"][0]["issues"]}
        self.assertIn("LINK", codes)
        self.assertIn("PROVENANCE", codes)


if __name__ == "__main__":
    unittest.main()
