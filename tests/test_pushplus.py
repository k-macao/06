import unittest
from unittest.mock import Mock, patch

from src import pushplus
from src.config import DEFAULT_PUSHPLUS_TOPIC


def _ok_response():
    resp = Mock()
    resp.json.return_value = {"code": 200, "msg": "请求成功", "data": "3cbc5eab19fe512e80677540fbde332a"}
    return resp


class TopicResolutionTests(unittest.TestCase):
    def test_default_topic_is_the_oai_1_group(self):
        self.assertEqual(DEFAULT_PUSHPLUS_TOPIC, "oai.1")
        self.assertEqual(pushplus.PUSHPLUS_TOPIC, "oai.1")
        self.assertEqual(pushplus.resolve_topic(), "oai.1")

    def test_explicit_topic_overrides_default(self):
        self.assertEqual(pushplus.resolve_topic("other.group"), "other.group")

    def test_self_only_aliases_disable_one_to_many(self):
        for value in ("", "  ", "none", "OFF", "self", "-"):
            self.assertEqual(pushplus.resolve_topic(value), "")

    def test_none_means_use_configured_group(self):
        self.assertEqual(pushplus.resolve_topic(None), "oai.1")


class OneToManyPayloadTests(unittest.TestCase):
    def test_payload_carries_topic_by_default(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post:
            res = pushplus.send_pushplus("tok", "标题", "<p>内容</p>")
        self.assertEqual(res["code"], 200)
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["topic"], "oai.1")
        self.assertEqual(payload["channel"], "wechat")
        self.assertEqual(payload["template"], "html")
        self.assertEqual(res["mode"], "一对多·群组 oai.1")

    def test_topic_override_reaches_payload(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post:
            pushplus.send_pushplus("tok", "标题", "<p>内容</p>", topic="vip.group")
        self.assertEqual(post.call_args.kwargs["json"]["topic"], "vip.group")

    def test_self_only_omits_topic(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post:
            res = pushplus.send_pushplus("tok", "标题", "<p>内容</p>", topic="")
        self.assertNotIn("topic", post.call_args.kwargs["json"])
        self.assertEqual(res["mode"], "单人·仅发给自己")

    def test_webhook_channel_still_sends_topic_with_warning(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post:
            pushplus.send_pushplus("tok", "标题", "<p>内容</p>", channel="webhook")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["channel"], "webhook")
        self.assertEqual(payload["topic"], "oai.1")

    def test_oversize_content_is_rejected_before_any_request(self):
        with patch.object(pushplus.requests, "post") as post:
            res = pushplus.send_pushplus("tok", "标题", "x" * 100_001)
        self.assertEqual(res["code"], 998)
        post.assert_not_called()

    def test_missing_token_skips_push(self):
        with patch.object(pushplus.requests, "post") as post, \
                patch.object(pushplus, "PUSHPLUS_TOKEN", ""), \
                patch.dict(pushplus.os.environ, {}, clear=True):
            res = pushplus.send_pushplus("", "标题", "<p>内容</p>")
        self.assertEqual(res["code"], 997)
        post.assert_not_called()

    def test_non_dict_response_is_normalized(self):
        resp = Mock()
        resp.json.return_value = ["not", "a", "dict"]
        with patch.object(pushplus.requests, "post", return_value=resp):
            res = pushplus.send_pushplus("tok", "标题", "<p>内容</p>")
        self.assertEqual(res["code"], 500)
        self.assertEqual(res["topic"], "oai.1")


class SendReportTopicTests(unittest.TestCase):
    def test_send_report_threads_topic_into_payload(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post, \
                patch("builtins.open", unittest.mock.mock_open(read_data="<html>报告</html>")):
            res = pushplus.send_report("output/report.html", "战报", token="tok",
                                       digest_html="<p>摘要</p>", topic="oai.1")
        self.assertEqual(res["code"], 200)
        self.assertEqual(post.call_args.kwargs["json"]["topic"], "oai.1")

    def test_send_report_self_only(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post, \
                patch("builtins.open", unittest.mock.mock_open(read_data="<html>报告</html>")):
            pushplus.send_report("output/report.html", "战报", token="tok",
                                 digest_html="<p>摘要</p>", topic="")
        self.assertNotIn("topic", post.call_args.kwargs["json"])


if __name__ == "__main__":
    unittest.main()


class TestMessageTopicTests(unittest.TestCase):
    def test_test_message_uses_configured_group(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post:
            pushplus.send_test_message("tok")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["topic"], "oai.1")
        self.assertIn("oai.1", payload["content"])

    def test_test_message_self_only(self):
        with patch.object(pushplus.requests, "post", return_value=_ok_response()) as post:
            pushplus.send_test_message("tok", "self")
        self.assertNotIn("topic", post.call_args.kwargs["json"])
