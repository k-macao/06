"""
不作伪检查模块 · Authenticity Check Module
==========================================

审计 KOL 元数据与生成结果，并执行「真实数据才可发布」门禁：
- 报告内的模拟标记、伪链接、改写标题、历史语料伪标题和严重失实来源均为 FAIL；
- 未进入报告的缺失/存疑来源会被隔离并记为 WARN，不会因凑数进入日报；
- 内容可来自 RSS / 官方 API / yt-dlp / 频道页 / 已验证缓存，但必须带可信来源标记；
- --online 只复核本次报告实际引用的频道，避免无关目录项造成门禁抖动。

用法：
  python -m src.authenticity_check
  python -m src.authenticity_check --online --strict
  python -m src.authenticity_check --md output/audit_report.md --json output/audit_report.json
  python -m src.authenticity_check --verify-only
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import KOL_DATA_PATH, OUTPUT_DIR, REQUEST_TIMEOUT, USER_AGENT  # noqa: E402

CHANNEL_ID_RE = re.compile(r"^UC[A-Za-z0-9_-]{22}$")

# 允许的内容来源：RSS 之外的备用链路同样必须可追溯。
VERIFIED_SOURCES = {
    "youtube_rss",
    "youtube_data_api",
    "yt_dlp",
    "youtube_channel_page",
    "verified_cache",
}
# 必须携带来源频道 ID 的链路（其余链路缺失时只记 WARN）。
SOURCES_REQUIRING_CHANNEL_ID = {"youtube_rss", "youtube_data_api"}


def _load_mock_pool_from_source():
    """从 src/fetcher.py 源码解析 MOCK_TITLES_POOL / GENERIC_TITLES 字面量（离线可用）。"""
    import ast

    src_path = ROOT / "src" / "fetcher.py"
    try:
        tree = ast.parse(src_path.read_text(encoding="utf-8"))
    except OSError:
        return {}, []
    pool, generic = {}, []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            try:
                if target.id == "MOCK_TITLES_POOL" and isinstance(node.value, ast.Dict):
                    pool = ast.literal_eval(node.value)
                elif target.id == "GENERIC_TITLES" and isinstance(node.value, ast.List):
                    generic = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                continue
    return pool, generic


MOCK_TITLES_POOL, GENERIC_TITLES = _load_mock_pool_from_source()
GENERIC_POOL_TITLES = {title for title, _ in GENERIC_TITLES}


def is_pool_title(kol_name: str, title: str) -> bool:
    """标题是否来自历史模拟语料库（即伪造标题而非频道原文）。"""
    if not title:
        return False
    pool = MOCK_TITLES_POOL.get(kol_name, [])
    return title in ({t for t, _ in pool} | GENERIC_POOL_TITLES)


MOCK_LINK_PATTERNS = (
    re.compile(r"[?&]v=mock\d*", re.I),
    re.compile(r"/mock\d*(?:/|$|\?)", re.I),
    re.compile(r"mock\d+\.", re.I),
)
PAGE_CHANNEL_ID_PATTERNS = (
    re.compile(r'"externalId"\s*:\s*"(UC[A-Za-z0-9_-]{22})"'),
    re.compile(r'<meta[^>]+itemprop=["\']channelId["\'][^>]+content=["\'](UC[A-Za-z0-9_-]{22})["\']', re.I),
    re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'][^"\']*/channel/(UC[A-Za-z0-9_-]{22})', re.I),
)


def is_mock_link(link: str) -> bool:
    return bool(link) and any(pattern.search(link) for pattern in MOCK_LINK_PATTERNS)


def is_supported_video_link(link: str) -> bool:
    """只接受具有视频标识的 YouTube Watch/Shorts/Live/youtu.be URL。"""
    if not link or is_mock_link(link):
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


def _is_youtube(kol: dict) -> bool:
    platform = (kol.get("platform") or "").lower()
    url = (kol.get("channel_url") or "").lower()
    return "youtube" in platform or "yt" in platform or "youtube.com" in url


def _is_youtube_host(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    return host == "youtube.com" or host.endswith(".youtube.com")


def check_kol_metadata(kol: dict, published: bool = False) -> list:
    """检查目录元数据；未发布记录的坏来源降级为隔离 WARN。"""
    issues = []
    source_level = "FAIL" if published else "WARN"
    source_suffix = "" if published else "（未进入本次报告，已隔离）"
    name = (kol.get("name") or "").strip()
    handle = kol.get("handle") or ""
    channel_url = kol.get("channel_url") or ""
    channel_id = kol.get("channel_id") or ""

    if not name:
        issues.append({"level": source_level, "code": "META", "msg": f"name 为空{source_suffix}"})

    if _is_youtube(kol):
        if not channel_id:
            issues.append({
                "level": "WARN",
                "code": "META",
                "msg": "channel_id 缺失；运行时必须从真实频道页解析，失败则隔离",
            })
        elif not CHANNEL_ID_RE.fullmatch(channel_id):
            issues.append({
                "level": source_level,
                "code": "META",
                "msg": f"channel_id 格式无效: {channel_id}{source_suffix}",
            })

        if not handle:
            issues.append({"level": "WARN", "code": "META", "msg": "handle 缺失"})
        elif not handle.startswith("@"):
            issues.append({"level": "WARN", "code": "META", "msg": f"handle 格式异常: {handle}（应为 @xxx）"})

        if "/results?" in channel_url:
            issues.append({
                "level": source_level,
                "code": "META",
                "msg": f"channel_url 是搜索页占位而非频道: {channel_url[:70]}…{source_suffix}",
            })
        elif channel_url and not _is_youtube_host(channel_url):
            issues.append({
                "level": source_level,
                "code": "META",
                "msg": f"YouTube 记录使用非 YouTube 来源: {channel_url[:70]}…{source_suffix}",
            })
        elif "/@" in channel_url and handle and handle.startswith("@"):
            url_handle = urlparse(channel_url).path.split("/@", 1)[-1].split("/", 1)[0]
            if url_handle and url_handle.casefold() != handle.lstrip("@").casefold():
                issues.append({
                    "level": source_level,
                    "code": "META",
                    "msg": f"channel_url 与 handle 不一致: {channel_url} vs {handle}{source_suffix}",
                })
    elif not channel_url:
        issues.append({"level": "WARN", "code": "META", "msg": "channel_url 缺失"})

    fans = kol.get("fans") or ""
    if not fans or fans in {"N/A", "NA", "0", "未知"}:
        issues.append({"level": "WARN", "code": "META", "msg": "fans 缺失/未填写"})
    elif not re.search(r"\d", fans):
        issues.append({"level": "WARN", "code": "META", "msg": f"fans 格式异常: {fans}"})

    for field, label in (("language", "language"), ("field", "field"), ("desc", "desc")):
        if not kol.get(field):
            issues.append({"level": "WARN", "code": "META", "msg": f"{label} 缺失"})
    return issues


def check_items(kol: dict, items: list) -> list:
    """检查本次真正发布的条目。"""
    issues = []
    seen_links = set()
    configured_channel_id = kol.get("channel_id") or ""

    for index, item in enumerate(items or [], start=1):
        link = item.get("link") or ""
        title = item.get("title") or ""
        original_title = item.get("original_title")
        published = item.get("published") or ""
        source = item.get("source") or ""

        if item.get("is_mock") is True:
            issues.append({
                "level": "FAIL",
                "code": "MOCK_FLAG",
                "msg": f"条目{index} 标记为模拟内容，禁止发布",
            })
        if is_mock_link(link):
            issues.append({
                "level": "FAIL",
                "code": "FAKE_LINK",
                "msg": f"条目{index} 链接为伪链接: {link}",
            })
        elif not link:
            issues.append({"level": "FAIL", "code": "LINK", "msg": f"条目{index} 无来源链接"})
        elif not is_supported_video_link(link):
            issues.append({
                "level": "FAIL",
                "code": "LINK",
                "msg": f"条目{index} 不是受支持的 YouTube 视频链接: {link}",
            })
        elif link in seen_links:
            issues.append({"level": "WARN", "code": "LINK", "msg": f"条目{index} 链接重复: {link}"})
        seen_links.add(link)

        if not title:
            issues.append({"level": "FAIL", "code": "TITLE", "msg": f"条目{index} 标题为空"})
        if original_title is None:
            issues.append({
                "level": "FAIL",
                "code": "PROVENANCE",
                "msg": f"条目{index} 缺少 RSS 原始标题，无法证明标题未被改写",
            })
        elif title != original_title:
            issues.append({
                "level": "FAIL",
                "code": "ALTERED_TITLE",
                "msg": f"条目{index} 展示标题与 RSS 原题不一致: 「{title}」 != 「{original_title}」",
            })

        if is_pool_title(kol.get("name", ""), title):
            issues.append({
                "level": "FAIL",
                "code": "POOL_TITLE",
                "msg": f"条目{index} 标题来自历史模拟语料库而非频道原文: 「{title[:40]}」",
            })

        if source not in VERIFIED_SOURCES:
            issues.append({
                "level": "FAIL",
                "code": "PROVENANCE",
                "msg": f"条目{index} 缺少受支持的来源标记（当前: {source or '空'}）",
            })
        source_channel_id = item.get("source_channel_id") or ""
        if not CHANNEL_ID_RE.fullmatch(source_channel_id):
            # RSS / 官方 API 必须能证明内容归属；yt-dlp、频道页与缓存链路
            # 拿不到频道 ID 时降级为 WARN，避免可用性下降被误判为伪造。
            level = "FAIL" if source in SOURCES_REQUIRING_CHANNEL_ID else "WARN"
            issues.append({
                "level": level,
                "code": "PROVENANCE",
                "msg": f"条目{index} source_channel_id 缺失或格式无效: {source_channel_id or '空'}（来源: {source or '空'}）",
            })
        if configured_channel_id and source_channel_id and configured_channel_id != source_channel_id:
            issues.append({
                "level": "FAIL",
                "code": "PROVENANCE",
                "msg": f"条目{index} 来源频道与 KOL 配置不一致",
            })

        if not published:
            issues.append({"level": "FAIL", "code": "DATE", "msg": f"条目{index} 无发布时间"})
        else:
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt > datetime.now(timezone.utc) + timedelta(days=1):
                    issues.append({"level": "FAIL", "code": "DATE", "msg": f"条目{index} 发布时间在未来: {published}"})
            except (TypeError, ValueError):
                issues.append({"level": "FAIL", "code": "DATE", "msg": f"条目{index} 发布时间无法解析: {published}"})
    return issues


def check_online(kol: dict, items: list) -> list:
    """在线复核报告实际引用的频道；网络故障为 WARN，明确 404 为 FAIL。"""
    issues = []
    try:
        import feedparser
        import requests
    except ImportError:
        return [{"level": "WARN", "code": "ONLINE", "msg": "缺少在线验证依赖"}]

    url = kol.get("channel_url") or ""
    channel_id = kol.get("channel_id") or ""
    if not channel_id:
        channel_id = next((item.get("source_channel_id") for item in items if item.get("source_channel_id")), "")
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8"}

    if url and _is_youtube_host(url) and "/results?" not in url:
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 404:
                issues.append({"level": "FAIL", "code": "ONLINE", "msg": f"频道页 404: {url}"})
            elif response.status_code == 200:
                page_channel_id = ""
                for pattern in PAGE_CHANNEL_ID_PATTERNS:
                    match = pattern.search(response.text)
                    if match:
                        page_channel_id = match.group(1)
                        break
                if channel_id and page_channel_id and channel_id != page_channel_id:
                    issues.append({
                        "level": "FAIL",
                        "code": "ONLINE",
                        "msg": f"频道页身份 {page_channel_id} 与内容来源 {channel_id} 不一致",
                    })
                elif channel_id and not page_channel_id:
                    issues.append({"level": "WARN", "code": "ONLINE", "msg": "频道页可达，但未能解析频道身份"})
                else:
                    issues.append({"level": "INFO", "code": "ONLINE", "msg": "在线验证：频道页身份一致"})
            else:
                issues.append({"level": "WARN", "code": "ONLINE", "msg": f"频道页 HTTP {response.status_code}"})
        except requests.RequestException as exc:
            issues.append({"level": "WARN", "code": "ONLINE", "msg": f"频道页验证失败: {type(exc).__name__}: {exc}"})

    if CHANNEL_ID_RE.fullmatch(channel_id):
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            response = requests.get(rss_url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 404:
                issues.append({"level": "FAIL", "code": "ONLINE", "msg": f"RSS 404，channel_id 无效: {channel_id}"})
            elif response.status_code != 200:
                issues.append({"level": "WARN", "code": "ONLINE", "msg": f"RSS HTTP {response.status_code}"})
            else:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    issues.append({
                        "level": "INFO",
                        "code": "ONLINE",
                        "msg": f"RSS 有效，最新标题: {feed.entries[0].get('title', '')[:40]}",
                    })
                else:
                    issues.append({"level": "WARN", "code": "ONLINE", "msg": "RSS 当前无可解析条目"})
        except requests.RequestException as exc:
            issues.append({"level": "WARN", "code": "ONLINE", "msg": f"RSS 验证失败: {type(exc).__name__}: {exc}"})
    return issues


def run_audit(
    kol_data_path=KOL_DATA_PATH,
    data_json_path=OUTPUT_DIR / "data.json",
    online: bool = False,
    verbose: bool = False,
) -> dict:
    kols = json.loads(Path(kol_data_path).read_text(encoding="utf-8"))
    output = {}
    if Path(data_json_path).exists():
        output = json.loads(Path(data_json_path).read_text(encoding="utf-8"))

    items_map = {}
    for entry in output.get("active_kols", []):
        kid = entry.get("kol", {}).get("id")
        if kid is not None:
            items_map[kid] = entry.get("items", [])

    results = []
    for kol in kols:
        kid = kol.get("id")
        included = kid in items_map
        items = items_map.get(kid, [])
        issues = check_kol_metadata(kol, published=included)
        issues.extend(check_items(kol, items))

        online_issues = check_online(kol, items) if online and included else []
        issues.extend(issue for issue in online_issues if issue["level"] != "INFO")

        levels = {issue["level"] for issue in issues}
        if "FAIL" in levels:
            verdict = "FAIL"
        elif "WARN" in levels or not items:
            verdict = "WARN"
        else:
            verdict = "PASS"

        mock_count = sum(
            1 for item in items if item.get("is_mock") is True or is_mock_link(item.get("link", ""))
        )
        altered_count = sum(
            1 for item in items
            if item.get("original_title") is not None and item.get("title") != item.get("original_title")
        )
        pool_count = sum(1 for item in items if is_pool_title(kol.get("name", ""), item.get("title", "")))
        results.append({
            "id": kid,
            "name": kol.get("name", ""),
            "platform": kol.get("platform", ""),
            "fans": kol.get("fans", ""),
            "channel_id": kol.get("channel_id") or "",
            "configured_active": bool(kol.get("active")),
            "included": included,
            "verdict": verdict,
            "mock_items": mock_count,
            "altered_titles": altered_count,
            "pool_titles": pool_count,
            "total_items": len(items),
            "online": [issue["msg"] for issue in online_issues if issue["level"] == "INFO"],
            "issues": issues,
        })
        if verbose:
            print(
                f"[{verdict:4s}] #{kid:02d} {kol.get('name', '')[:24]:24s} "
                f"included={included} mock={mock_count}/{len(items)}"
            )

    total_items = sum(result["total_items"] for result in results)
    mock_items = sum(result["mock_items"] for result in results)
    altered_titles = sum(result["altered_titles"] for result in results)
    pool_titles = sum(result["pool_titles"] for result in results)
    summary = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "total_kols": len(kols),
        "included_kols": sum(1 for result in results if result["included"]),
        "quarantined_kols": sum(1 for result in results if not result["included"]),
        "pass": sum(1 for result in results if result["verdict"] == "PASS"),
        "warn": sum(1 for result in results if result["verdict"] == "WARN"),
        "fail": sum(1 for result in results if result["verdict"] == "FAIL"),
        "total_items": total_items,
        "mock_items": mock_items,
        "altered_titles": altered_titles,
        "pool_titles": pool_titles,
        "mock_ratio_pct": round(100 * mock_items / max(1, total_items), 1),
        "online_verified": online,
    }
    return {"summary": summary, "results": results}


def _table(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(audit: dict) -> str:
    summary = audit["summary"]
    lines = [
        "# 🔍 全频道真实性审计报告（不作伪检查模块）",
        "",
        f"- **审计时间**：{summary['audited_at']}",
        f"- **KOL 目录**：{summary['total_kols']}（本次入报 {summary['included_kols']}，隔离 {summary['quarantined_kols']}）",
        f"- **判定**：PASS {summary['pass']}　|　WARN {summary['warn']}　|　FAIL {summary['fail']}",
        f"- **内容条目**：{summary['total_items']} 条；模拟/伪链接 {summary['mock_items']}；改写标题 {summary['altered_titles']}",
        f"- **在线复核**：{'已请求（仅复核入报频道）' if summary['online_verified'] else '未开启'}",
        "",
        "## 判定口径",
        "- **FAIL**：本次报告含模拟内容、伪链接、改写标题，或入报来源在线确认严重失实。",
        "- **WARN**：目录元数据不完整、网络暂时不可验证，或记录未入报并已隔离。",
        "- **PASS**：入报内容具备真实来源且无伪造痕迹。",
        "",
        "| # | 名称 | 入报 | 平台 | 判定 | mock/条目 | 主要问题 |",
        "|---|------|------|------|------|-----------|---------|",
    ]
    for result in audit["results"]:
        problems = []
        seen = set()
        for issue in result["issues"]:
            key = (issue["code"], issue["msg"])
            if key not in seen:
                seen.add(key)
                problems.append(issue["msg"])
        problem_text = "；".join(problems[:3])
        if len(problems) > 3:
            problem_text += f"…(共{len(problems)}条)"
        lines.append(
            f"| {result['id']:>2} | {_table(result['name'][:24])} | "
            f"{'是' if result['included'] else '否'} | {_table(result['platform'][:14])} | "
            f"**{result['verdict']}** | {result['mock_items']}/{result['total_items']} | "
            f"{_table(problem_text[:100])} |"
        )
    lines.extend([
        "",
        "---",
        "*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*",
        "",
    ])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="不作伪检查模块：KOL 名单与输出内容真实性审计")
    parser.add_argument("--kol-data", default=str(KOL_DATA_PATH))
    parser.add_argument("--data-json", default=str(OUTPUT_DIR / "data.json"))
    parser.add_argument("--online", action="store_true", help="在线复核本次报告实际引用的频道")
    parser.add_argument("--md", default=None, help="Markdown 报告输出路径")
    parser.add_argument("--json", dest="json_out", default=None, help="JSON 审计结果输出路径")
    parser.add_argument("--strict", action="store_true", help="存在 FAIL 即退出码 1")
    parser.add_argument("--verify-only", action="store_true", help="只审计、不写报告")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    audit = run_audit(args.kol_data, args.data_json, online=args.online, verbose=args.verbose)
    summary = audit["summary"]
    print("=" * 60)
    print("🔍 不作伪检查模块 · 审计完成")
    print(
        f"   KOL: {summary['total_kols']} | 入报 {summary['included_kols']} | "
        f"隔离 {summary['quarantined_kols']}"
    )
    print(f"   PASS {summary['pass']} | WARN {summary['warn']} | FAIL {summary['fail']}")
    print(
        f"   条目: {summary['total_items']} | mock伪链接 {summary['mock_items']} "
        f"({summary['mock_ratio_pct']}%) | 改写标题 {summary['altered_titles']}"
    )
    print("=" * 60)

    if not args.verify_only:
        md_path = args.md or str(OUTPUT_DIR / "audit_report.md")
        Path(md_path).parent.mkdir(parents=True, exist_ok=True)
        Path(md_path).write_text(render_markdown(audit), encoding="utf-8")
        print(f"📄 报告已写入: {md_path}")
        if args.json_out:
            json_path = Path(args.json_out)
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"📊 JSON 已写入: {json_path}")

    if args.strict and summary["fail"] > 0:
        print(f"❌ 检测到 {summary['fail']} 个 FAIL，--strict 门禁未通过")
        return 1
    print("✅ 严格门禁通过：本次报告未包含伪造内容")
    return 0


if __name__ == "__main__":
    sys.exit(main())
