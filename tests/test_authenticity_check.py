import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
from unittest.mock import Mock

from src.authenticity_check import _downgrade_mass_online_404s, check_online, run_audit


def _install_online_stubs(get_response):
    """Inject lightweight requests/feedparser so check_online can run without pip deps."""
    requests_mod = types.ModuleType("requests")
    requests_mod.RequestException = type("RequestException", (Exception,), {})
    requests_mod.get = lambda *a, **k: get_response
    feed = types.SimpleNamespace(entries=[])
    feedparser_mod = types.ModuleType("feedparser")
    feedparser_mod.parse = lambda *a, **k: feed
    return {
        "requests": requests_mod,
        "feedparser": feedparser_mod,
    }


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


class OnlineCheckTests(unittest.TestCase):
    """--online 复验在 YouTube 风控拦截下的行为：RSS 已抓取的频道不应被误判 FAIL。"""

    def setUp(self):
        self.kol = {
            "name": "Verified channel",
            "channel_url": "https://www.youtube.com/channel/UC1234567890123456789012",
            "channel_id": "UC1234567890123456789012",
        }
        self.rss_items = [{
            "source": "youtube_rss",
            "source_channel_id": "UC1234567890123456789012",
        }]

    def test_rss_404_is_warn_when_channel_was_already_rss_fetched(self):
        response = Mock(status_code=404)
        with mock.patch.dict(sys.modules, _install_online_stubs(response)):
            issues = check_online(self.kol, self.rss_items)
        self.assertFalse(any(i["level"] == "FAIL" for i in issues))
        self.assertTrue(any(i["code"] == "ONLINE" and "风控" in i["msg"] for i in issues))

    def test_rss_404_still_fails_when_channel_was_not_rss_fetched(self):
        cached_items = [{"source": "verified_cache", "source_channel_id": ""}]
        response = Mock(status_code=404)
        with mock.patch.dict(sys.modules, _install_online_stubs(response)):
            issues = check_online(self.kol, cached_items)
        self.assertTrue(any(i["level"] == "FAIL" and i["code"] == "ONLINE" for i in issues))

    def test_identity_mismatch_is_always_a_failure(self):
        # 200 但频道页身份与内容来源不一致：仍是硬 FAIL（与风控无关）。
        page = '{"externalId":"UC' + "B" * 22 + '"}'
        response = Mock(status_code=200, text=page, content=b"")
        with mock.patch.dict(sys.modules, _install_online_stubs(response)):
            issues = check_online(self.kol, self.rss_items)
        self.assertTrue(any(i["level"] == "FAIL" and "不一致" in i["msg"] for i in issues))


class MassOnline404Tests(unittest.TestCase):
    """大批频道同时在线 404 应被判定为 YouTube 风控拦截并降级，个别 404 仍保留 FAIL。"""

    def _result(self, online_fail_404=False):
        issues = []
        if online_fail_404:
            issues.append({"level": "FAIL", "code": "ONLINE", "msg": "RSS 404，channel_id 无效: UC1234567890123456789012"})
        return {"included": True, "issues": issues}

    def test_many_channels_404ing_at_once_is_downgraded(self):
        results = [self._result(online_fail_404=True) for _ in range(16)]
        results += [self._result() for _ in range(4)]
        self.assertGreater(_downgrade_mass_online_404s(results), 0)
        self.assertTrue(all(i["level"] == "WARN" for r in results for i in r["issues"]))

    def test_isolated_404_is_kept_as_fail(self):
        results = [self._result(online_fail_404=True)] + [self._result() for _ in range(19)]
        self.assertEqual(0, _downgrade_mass_online_404s(results))
        self.assertEqual("FAIL", results[0]["issues"][0]["level"])

    def test_non_404_failures_are_never_downgraded(self):
        results = [self._result() for _ in range(20)]
        results[0]["issues"] = [{"level": "FAIL", "code": "PROVENANCE", "msg": "改写标题"}]
        self.assertEqual(0, _downgrade_mass_online_404s(results))
        self.assertEqual("FAIL", results[0]["issues"][0]["level"])


if __name__ == "__main__":
    unittest.main()
