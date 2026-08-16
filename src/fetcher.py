"""
KOL 真实性优先的内容抓取器。

生产报告只接受可验证的 YouTube RSS 条目：
1. 使用已配置的 channel_id，或从真实频道页解析 channel_id；
2. 拉取 YouTube 官方 RSS；
3. 仅把带真实标题、视频链接和发布时间的条目交给下游。

任何抓取失败、搜索结果页、非支持平台或被人工停用的记录都会被隔离，绝不
用模拟标题、模拟日期或伪链接补位。可用性下降应表现为「未验证/不入报」，而
不应伪造成一份看似完整的日报。
"""
from datetime import datetime, timezone
import html
import json
import re
from urllib.parse import parse_qs, urlparse

import feedparser
import requests

from .config import (
    ACTIVE_THRESHOLD_DAYS,
    KOL_DATA_PATH,
    REQUEST_TIMEOUT,
    USER_AGENT,
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
}
CHANNEL_ID_RE = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
CHANNEL_ID_PATTERNS = (
    re.compile(r'"externalId"\s*:\s*"(UC[A-Za-z0-9_-]{22})"'),
    re.compile(r'"channelId"\s*:\s*"(UC[A-Za-z0-9_-]{22})"'),
    re.compile(r'"browseId"\s*:\s*"(UC[A-Za-z0-9_-]{22})"'),
    re.compile(r'<meta[^>]+itemprop=["\']channelId["\'][^>]+content=["\'](UC[A-Za-z0-9_-]{22})["\']', re.I),
    re.compile(r'youtube\.com/channel/(UC[A-Za-z0-9_-]{22})'),
)
MOCK_LINK_RE = re.compile(r"(?:[?&]v=mock\d*|/mock\d*(?:/|$|\?)|mock\d+\.)", re.I)


def is_youtube_channel_url(url: str) -> bool:
    """只接受 YouTube 真实频道 URL，明确拒绝搜索结果页。"""
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    host = (parsed.hostname or "").lower()
    if host != "youtube.com" and not host.endswith(".youtube.com"):
        return False
    if parsed.path.rstrip("/") == "/results":
        return False
    return parsed.path.startswith(("/@", "/channel/", "/c/", "/user/"))


def is_real_video_link(link: str) -> bool:
    """验证 RSS 条目的链接是 YouTube 视频链接而不是伪造占位链接。"""
    if not link or MOCK_LINK_RE.search(link):
        return False
    try:
        parsed = urlparse(link)
    except ValueError:
        return False
    host = (parsed.hostname or "").lower()
    path_parts = [part for part in parsed.path.split("/") if part]
    if host == "youtu.be":
        return bool(path_parts)
    if host != "youtube.com" and not host.endswith(".youtube.com"):
        return False
    if parsed.path == "/watch":
        return bool(parse_qs(parsed.query).get("v", [""])[0])
    return len(path_parts) >= 2 and path_parts[0] in {"shorts", "live"}


def _channel_id_from_url(url: str) -> str | None:
    if not is_youtube_channel_url(url):
        return None
    match = re.search(r"/channel/(UC[A-Za-z0-9_-]{22})(?:/|$)", urlparse(url).path)
    return match.group(1) if match else None


def resolve_channel_id(kol: dict) -> str | None:
    """从真实频道 URL 验证 channel_id；配置与页面不一致时失败关闭。"""
    configured = (kol.get("channel_id") or "").strip()
    configured = configured if CHANNEL_ID_RE.fullmatch(configured) else ""
    channel_url = (kol.get("channel_url") or "").strip()
    if not is_youtube_channel_url(channel_url):
        return None

    # /channel/UC... 已把身份编码在 URL 中，无需额外页面请求。
    from_url = _channel_id_from_url(channel_url)
    if from_url:
        if configured and configured != from_url:
            print(f"[channel] {kol.get('name', '?')} 配置 channel_id 与 URL 不一致")
            return None
        return from_url

    # @handle、/c/ 与 /user/ 必须从页面确认身份，即使已有配置值也不能盲信。
    try:
        response = requests.get(
            channel_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[channel] {kol.get('name', '?')} 无法验证 channel_id: {exc}")
        return None

    page = html.unescape(response.text)
    for pattern in CHANNEL_ID_PATTERNS:
        match = pattern.search(page)
        if match:
            resolved = match.group(1)
            if configured and configured != resolved:
                print(f"[channel] {kol.get('name', '?')} 配置 channel_id 与频道页不一致")
                return None
            return resolved
    print(f"[channel] {kol.get('name', '?')} 页面未找到 channel_id")
    return None


def _entry_datetime(entry) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return None
    try:
        return datetime(*parsed[:6], tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def parse_last_update_from_rss(channel_id: str):
    """通过 YouTube 官方 RSS 获取最多三条可验证内容。"""
    if not CHANNEL_ID_RE.fullmatch(channel_id or ""):
        return None, []

    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        response = requests.get(
            rss_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[RSS] {channel_id} 请求失败: {exc}")
        return None, []

    feed = feedparser.parse(response.content)
    items = []
    for entry in feed.entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        published = _entry_datetime(entry)
        if not title or not published or not is_real_video_link(link):
            continue
        items.append({
            "title": title,
            "original_title": title,
            "link": link,
            "published": published.isoformat(),
            "summary": (entry.get("summary") or "")[:220],
            "source": "youtube_rss",
            "source_channel_id": channel_id,
            "is_mock": False,
        })
        if len(items) == 3:
            break

    if not items:
        detail = getattr(feed, "bozo_exception", "RSS 无有效条目")
        print(f"[RSS] {channel_id} 无有效条目: {detail}")
        return None, []
    return _entry_datetime(feed.entries[0]) or datetime.fromisoformat(items[0]["published"]), items


def is_active_kol(kol: dict, threshold_days: int = ACTIVE_THRESHOLD_DAYS):
    """仅当官方 RSS 含阈值内的真实条目时，才判为可发布。"""
    # active=false 是人工隔离开关，必须优先于线上探测，避免重复/存疑频道回流。
    if kol.get("active") is False:
        return False, None, []

    channel_id = resolve_channel_id(kol)
    if not channel_id:
        return False, None, []

    last_dt, items = parse_last_update_from_rss(channel_id)
    if not last_dt or not items:
        return False, None, []
    age_days = (datetime.now(timezone.utc) - last_dt).days
    return age_days <= threshold_days, last_dt, items


def enrich_with_verified_content(kol: dict, real_items: list) -> list:
    """补充展示字段，不改写 RSS 的标题、摘要、链接或日期。"""
    enriched = []
    for item in real_items[:3]:
        if item.get("is_mock") or not is_real_video_link(item.get("link", "")):
            continue
        enriched.append({
            **item,
            "title": item["title"],
            "original_title": item["title"],
            "lang": kol.get("language", ""),
            "source": "youtube_rss",
            "is_mock": False,
        })
    return enriched


def scan_kols(kol_list=None, verbose: bool = True):
    """扫描名单，返回有真实内容的频道、隔离记录和真实条目映射。"""
    if kol_list is None:
        with open(KOL_DATA_PATH, "r", encoding="utf-8") as file:
            kol_list = json.load(file)

    active_kols = []
    inactive_kols = []
    enriched_map = {}
    for kol in kol_list:
        active, last_dt, items = is_active_kol(kol)
        verified_items = enrich_with_verified_content(kol, items) if active else []
        active = active and bool(verified_items)
        last_str = last_dt.strftime("%Y-%m-%d") if last_dt else "未知"
        if verbose:
            if active:
                status = "✅已验证"
            elif kol.get("active") is False:
                status = "⏸️已停用"
            else:
                status = "⚠️未验证"
            print(
                f"{status} [{kol['id']:02d}] {kol['name']:20s} | "
                f"{kol['platform']:12s} | 最近: {last_str} | {kol['fans']}"
            )
        if active:
            active_kols.append(kol)
            enriched_map[kol["id"]] = verified_items
        else:
            inactive_kols.append(kol)
    return active_kols, inactive_kols, enriched_map


if __name__ == "__main__":
    verified, quarantined, item_map = scan_kols()
    print(f"\n已验证: {len(verified)} / 总数: {len(verified) + len(quarantined)}")
    for record in verified[:2]:
        print(record["name"], item_map[record["id"]])
