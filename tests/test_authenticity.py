import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from src.analyzer import global_battle_stats
from src.authenticity_check import check_items, check_kol_metadata, run_audit
from src.fetcher import (
    _find_initial_data,
    _youtube_video_id,
    enrich_items_with_transcripts,
    enrich_with_real_content,
    fetch_from_ytdlp,
    fetch_transcript_summary,
    is_active_kol,
    load_verified_cache,
    scrape_channel_items,
)


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

    def test_transcript_fallback_fills_only_missing_summary(self):
        snippets = [Mock(text="First verified caption."), Mock(text="Second caption.")]
        with patch("youtube_transcript_api.YouTubeTranscriptApi.fetch", return_value=snippets):
            items = enrich_items_with_transcripts([{
                "title": "Real video",
                "link": "https://www.youtube.com/watch?v=caption123",
                "summary": "",
            }], self.kol)
        self.assertEqual("First verified caption. Second caption.", items[0]["summary"])
        self.assertEqual("youtube_transcript_api", items[0]["summary_source"])

    def test_transcript_does_not_overwrite_source_description(self):
        with patch("src.fetcher.fetch_transcript_summary") as transcript:
            items = enrich_items_with_transcripts([{
                "link": "https://youtu.be/real123",
                "summary": "Original source description",
            }], self.kol)
        transcript.assert_not_called()
        self.assertEqual("Original source description", items[0]["summary"])

    def test_video_id_parser_supports_youtube_url_forms(self):
        self.assertEqual("abc", _youtube_video_id("https://www.youtube.com/watch?v=abc"))
        self.assertEqual("short1", _youtube_video_id("https://youtube.com/shorts/short1"))
        self.assertEqual("tiny1", _youtube_video_id("https://youtu.be/tiny1"))

    def test_ytdlp_fallback_extracts_metadata_without_downloading(self):
        timestamp = int(datetime.now(timezone.utc).timestamp())
        result = {"entries": [{
            "id": "ytdlp123",
            "title": "yt-dlp real title",
            "timestamp": timestamp,
            "description": "Real metadata",
        }]}
        downloader = Mock()
        downloader.__enter__ = Mock(return_value=downloader)
        downloader.__exit__ = Mock(return_value=False)
        downloader.extract_info.return_value = result
        with patch("yt_dlp.YoutubeDL", return_value=downloader) as ydl:
            last_update, items = fetch_from_ytdlp(self.kol["channel_url"])
        self.assertIsNotNone(last_update)
        self.assertEqual("yt_dlp", items[0]["source"])
        self.assertEqual("https://www.youtube.com/watch?v=ytdlp123", items[0]["link"])
        self.assertTrue(ydl.call_args.args[0]["skip_download"])

    def test_channel_page_fallback_extracts_traceable_video(self):
        initial_data = {
            "contents": [{"videoRenderer": {
                "videoId": "real123",
                "title": {"runs": [{"text": "Real page title"}]},
                "publishedTimeText": {"simpleText": "2 days ago"},
                "descriptionSnippet": {"runs": [{"text": "Real description"}]},
            }}]
        }
        response = Mock(text="var ytInitialData = " + json.dumps(initial_data) + ";")
        response.raise_for_status.return_value = None
        with patch("src.fetcher.requests.get", return_value=response):
            last_update, items = scrape_channel_items(self.kol["channel_url"])
        self.assertIsNotNone(last_update)
        self.assertEqual("https://www.youtube.com/watch?v=real123", items[0]["link"])
        self.assertEqual("youtube_channel_page", items[0]["source"])

    def test_cache_loader_rejects_mock_entries(self):
        output = {"active_kols": [{"kol": {"id": 1}, "items": [
            {"title": "Fake", "link": "https://example.com/?v=mock0", "is_mock": True},
            {"title": "Real", "link": "https://example.com/real", "published": "2026-08-15T00:00:00Z"},
        ]}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            path.write_text(json.dumps(output), encoding="utf-8")
            cached = load_verified_cache(path)
        self.assertEqual(["Real"], [item["title"] for item in cached[1]])

    def test_recent_verified_cache_is_the_last_live_fallback(self):
        cached = [{
            "title": "Previously verified",
            "link": "https://www.youtube.com/watch?v=cached123",
            "published": datetime.now(timezone.utc).isoformat(),
            "summary": "Previously verified summary",
            "source": "verified_cache",
        }]
        with patch("src.fetcher.parse_last_update_from_rss", return_value=(None, [])), patch(
            "src.fetcher.fetch_from_youtube_api", return_value=(None, [])
        ), patch("src.fetcher.fetch_from_ytdlp", return_value=(None, [])), patch(
            "src.fetcher.scrape_channel_items", return_value=(None, [])
        ):
            active, _, items = is_active_kol(self.kol, cached_items=cached)
        self.assertTrue(active)
        self.assertEqual("verified_cache", items[0]["source"])

    def test_failed_network_verification_does_not_use_static_active_flag(self):
        kol = {**self.kol, "active": True}
        with patch("src.fetcher.parse_last_update_from_rss", return_value=(None, [])), patch(
            "src.fetcher.fetch_from_youtube_api", return_value=(None, [])
        ), patch("src.fetcher.fetch_from_ytdlp", return_value=(None, [])), patch(
            "src.fetcher.scrape_channel_items", return_value=(None, [])
        ), patch("src.fetcher.scrape_channel_page", return_value=None):
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
