from datetime import datetime, timezone
import unittest
from unittest.mock import Mock, patch

from src import fetcher


class FetcherTests(unittest.TestCase):
    def test_search_page_is_not_a_channel(self):
        self.assertFalse(
            fetcher.is_youtube_channel_url(
                "https://www.youtube.com/results?search_query=not-a-channel"
            )
        )
        self.assertTrue(fetcher.is_youtube_channel_url("https://www.youtube.com/@real"))

    def test_disabled_record_is_never_probed(self):
        kol = {"active": False}
        with patch.object(fetcher, "resolve_channel_id") as resolve:
            active, last_dt, items = fetcher.is_active_kol(kol)
        self.assertFalse(active)
        self.assertIsNone(last_dt)
        self.assertEqual([], items)
        resolve.assert_not_called()

    def test_configured_channel_id_must_match_handle_page(self):
        configured = "UC" + "A" * 22
        resolved = "UC" + "B" * 22
        response = Mock(text=f'{{"externalId":"{resolved}"}}')
        response.raise_for_status.return_value = None
        kol = {
            "name": "Mismatched",
            "channel_url": "https://www.youtube.com/@mismatched",
            "channel_id": configured,
        }
        with patch.object(fetcher.requests, "get", return_value=response):
            self.assertIsNone(fetcher.resolve_channel_id(kol))

    def test_rss_parser_preserves_source_fields(self):
        channel_id = "UC" + "A" * 22
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://www.youtube.com/xml/schemas/2015">
          <entry>
            <yt:videoId>abcdefghijk</yt:videoId>
            <yt:channelId>{channel_id}</yt:channelId>
            <title>Official title</title>
            <link rel="alternate" href="https://www.youtube.com/watch?v=abcdefghijk"/>
            <published>2026-08-15T00:00:00+00:00</published>
            <updated>2026-08-15T00:00:00+00:00</updated>
          </entry>
        </feed>""".encode()
        response = Mock(content=xml)
        response.raise_for_status.return_value = None
        with patch.object(fetcher.requests, "get", return_value=response):
            last_dt, items = fetcher.parse_last_update_from_rss(channel_id)
        self.assertEqual(datetime(2026, 8, 15, tzinfo=timezone.utc), last_dt)
        self.assertEqual("Official title", items[0]["title"])
        self.assertEqual("Official title", items[0]["original_title"])
        self.assertEqual(channel_id, items[0]["source_channel_id"])
        self.assertFalse(items[0]["is_mock"])

    def test_scan_publishes_only_verified_items_without_padding(self):
        kol = {
            "id": 1,
            "name": "Real",
            "platform": "YouTube",
            "fans": "1W+",
            "language": "en",
            "active": True,
        }
        item = {
            "title": "Real title",
            "original_title": "Real title",
            "summary": "Real summary",
            "link": "https://www.youtube.com/watch?v=abcdefghijk",
            "published": "2026-08-15T00:00:00+00:00",
            "source": "youtube_rss",
            "source_channel_id": "UC1234567890123456789012",
            "is_mock": False,
        }
        with patch.object(
            fetcher,
            "is_active_kol",
            return_value=(True, datetime(2026, 8, 15, tzinfo=timezone.utc), [item]),
        ):
            active, inactive, item_map = fetcher.scan_kols([kol], verbose=False)
        self.assertEqual([kol], active)
        self.assertEqual([], inactive)
        self.assertEqual(1, len(item_map[1]))
        self.assertFalse(item_map[1][0]["is_mock"])
        self.assertEqual("Real title", item_map[1][0]["title"])

    def test_mock_link_is_filtered_from_enrichment(self):
        kol = {"language": "中文"}
        item = {
            "title": "Fake",
            "link": "https://www.youtube.com/@fake?v=mock0",
            "published": "2026-08-15T00:00:00+00:00",
            "is_mock": True,
        }
        self.assertEqual([], fetcher.enrich_with_verified_content(kol, [item]))


if __name__ == "__main__":
    unittest.main()
