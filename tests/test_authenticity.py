import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.analyzer import global_battle_stats
from src.authenticity_check import check_items, check_kol_metadata, run_audit
from src.fetcher import enrich_with_real_content, is_active_kol


class FetcherAuthenticityTests(unittest.TestCase):
    def setUp(self):
        self.kol = {
            "id": 1,
            "name": "Example",
            "platform": "YouTube",
            "channel_url": "https://www.youtube.com/@example",
            "channel_id": "UCexample",
            "handle": "@example",
            "fans": "1W+",
            "language": "中文",
            "field": "财经",
            "desc": "Example channel",
        }

    def test_real_enrichment_does_not_fill_missing_slots_with_mock_data(self):
        source = [{
            "title": "A real title",
            "link": "https://www.youtube.com/watch?v=real-id",
            "published": "2026-08-15T00:00:00+00:00",
            "summary": "A real summary",
        }]
        items = enrich_with_real_content(self.kol, source)
        self.assertEqual(1, len(items))
        self.assertFalse(items[0]["is_mock"])
        self.assertEqual(source[0]["link"], items[0]["link"])

    def test_failed_network_verification_does_not_use_static_active_flag(self):
        kol = {**self.kol, "active": True}
        with patch("src.fetcher.parse_last_update_from_rss", return_value=(None, [])), patch(
            "src.fetcher.scrape_channel_page", return_value=None
        ):
            active, last_update, items = is_active_kol(kol)
        self.assertFalse(active)
        self.assertIsNone(last_update)
        self.assertEqual([], items)


class AuditTests(unittest.TestCase):
    def test_empty_global_stats_keep_the_normal_result_schema(self):
        stats = global_battle_stats({})
        self.assertEqual(0, stats["total"])
        self.assertEqual(0, stats["bull"])
        self.assertEqual("无可验证内容", stats["dominant"])

    def test_explicit_mock_marker_is_a_failure_even_without_mock_url_pattern(self):
        issues = check_items(
            {"name": "Example"},
            [{"title": "Invented", "link": "https://example.com/item", "is_mock": True}],
        )
        self.assertIn("FAIL", {issue["level"] for issue in issues})

    def test_mixed_platform_instagram_url_is_not_a_youtube_domain_failure(self):
        kol = {
            "name": "Mixed creator",
            "platform": "IG/YT",
            "channel_url": "https://www.instagram.com/example",
            "handle": "@example",
            "fans": "1W+",
            "language": "中文",
            "field": "财经",
            "desc": "Mixed-platform creator",
        }
        failures = [i for i in check_kol_metadata(kol) if i["level"] == "FAIL"]
        self.assertEqual([], failures)

    def test_clean_output_passes_strict_failure_condition(self):
        kols = [{
            "id": 1,
            "name": "Example",
            "platform": "YouTube",
            "channel_url": "https://www.youtube.com/@example",
            "channel_id": "UCexample",
            "handle": "@example",
            "fans": "1W+",
            "language": "中文",
            "field": "财经",
            "desc": "Example channel",
            "active": True,
        }]
        output = {"active_kols": [{"kol": {"id": 1}, "items": [{
            "title": "A real title",
            "link": "https://www.youtube.com/watch?v=real-id",
            "published": "2026-08-15T00:00:00+00:00",
            "is_mock": False,
        }]}]}
        with tempfile.TemporaryDirectory() as directory:
            kol_path = Path(directory) / "kols.json"
            output_path = Path(directory) / "data.json"
            kol_path.write_text(json.dumps(kols), encoding="utf-8")
            output_path.write_text(json.dumps(output), encoding="utf-8")
            audit = run_audit(kol_path, output_path)
        self.assertEqual(0, audit["summary"]["fail"])
        self.assertEqual(1, audit["summary"]["pass"])


if __name__ == "__main__":
    unittest.main()
