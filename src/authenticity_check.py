"""
不作伪检查模块 · Authenticity Check Module
==========================================
对 KOL 名单（kol_data.json）与生成结果（output/data.json）做真实性/防伪检查：

  [元数据层]  channel_id 是否缺失（缺失 = 抓取必然走 Mock 兜底）、handle/channel_url
              是否一致、fans/language/field/desc 是否为空或异常。
  [内容层]    条目链接是否为 `?v=mock` 伪链接（100% 伪造）、标题是否来自
              fetcher 的 MOCK_TITLES_POOL 语料（非频道原文）、发布日期是否在未来、
              同一 KOL 内链接是否重复。
  [在线层]    (--online, 需要网络, 适合 CI) 抓取频道页 HTTP 状态、订阅数、
              用 channel_id 拉 RSS 取真实最新条目。

用法：
  python -m src.authenticity_check                 # 离线全量审计（默认）
  python -m src.authenticity_check --online        # 尝试在线验证（CI/有网环境）
  python -m src.authenticity_check --md 审计报告.md --json audit.json
  python -m src.authenticity_check --strict        # 存在伪造即退出码 1（CI 门禁）
  python -m src.authenticity_check --verify-only   # 只审计不写报告文件

判定：
  FAIL  = 检测到伪造内容（mock 链接等）或在线验证确认元数据严重失实
  WARN  = 元数据不完整（如 channel_id 缺失、fans 缺失）→ 无法证明真实，需要人工核
  PASS  = 无伪造痕迹且元数据完整（--online 时还要求在线验证通过）
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import KOL_DATA_PATH, OUTPUT_DIR  # noqa: E402

# ---- 加载 fetcher 的模拟语料库（不依赖 requests/feedparser，直接用 AST 解析源码） ----
def _load_mock_pool_from_source():
    """从 src/fetcher.py 源码解析 MOCK_TITLES_POOL / GENERIC_TITLES 字典字面量。"""
    import ast
    src_path = ROOT / "src" / "fetcher.py"
    try:
        tree = ast.parse(src_path.read_text(encoding="utf-8"))
        pool, generic = {}, []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == "MOCK_TITLES_POOL" and isinstance(node.value, ast.Dict):
                        try:
                            pool = ast.literal_eval(node.value)
                        except Exception:
                            pool = {}
                    if isinstance(tgt, ast.Name) and tgt.id == "GENERIC_TITLES" and isinstance(node.value, ast.List):
                        try:
                            generic = ast.literal_eval(node.value)
                        except Exception:
                            generic = []
        return pool, generic
    except Exception:
        return {}, []

# 优先用源码解析（离线可用）；失败再尝试 import（CI 有依赖时）
try:
    from src.fetcher import MOCK_TITLES_POOL as _P, GENERIC_TITLES as _G  # noqa: E402
    MOCK_TITLES_POOL, GENERIC_TITLES = _P, _G
except Exception:
    MOCK_TITLES_POOL, GENERIC_TITLES = _load_mock_pool_from_source()

# ---------------------------------------------------------------------------
# 伪造特征定义
# ---------------------------------------------------------------------------
MOCK_LINK_PATTERNS = [
    re.compile(r"[?&]v=mock\d*", re.I),       # ?v=mock0 / ?v=mock1
    re.compile(r"/mock\d*(/|$|\?)", re.I),    # /mock0
    re.compile(r"mock\d+\.", re.I),           # mock0.xxx
]
GENERIC_POOL_TITLES = {t for t, _ in GENERIC_TITLES}


def is_mock_link(link: str) -> bool:
    if not link:
        return False
    return any(p.search(link) for p in MOCK_LINK_PATTERNS)


def is_pool_title(kol_name: str, title: str) -> bool:
    """标题是否来自语料库（伪造标题，非频道原文）"""
    if not title:
        return False
    pool = MOCK_TITLES_POOL.get(kol_name, [])
    pool_titles = {t for t, _ in pool} | GENERIC_POOL_TITLES
    return title in pool_titles


# ---------------------------------------------------------------------------
# 元数据层检查
# ---------------------------------------------------------------------------
def check_kol_metadata(kol: dict) -> list:
    issues = []
    name = kol.get("name", "").strip()
    platform = (kol.get("platform") or "").lower()
    handle = kol.get("handle") or ""
    channel_url = kol.get("channel_url") or ""
    channel_id = kol.get("channel_id") or ""

    if not name:
        issues.append({"level": "FAIL", "code": "META", "msg": "name 为空"})
    # 混合平台（如 IG/YT）的主链接可以合法指向 Instagram；只有链接本身
    # 指向 YouTube，或平台明确只有 YouTube 时，才套用 YouTube 元数据规则。
    youtube_url = "youtube.com" in channel_url or "youtu.be" in channel_url
    youtube_only = platform.strip() == "youtube"
    if youtube_url or youtube_only:
        if not channel_id:
            issues.append({"level": "WARN", "code": "META", "msg": "channel_id 缺失 → 无法通过 RSS 抓取和验证内容"})
        if not handle:
            issues.append({"level": "WARN", "code": "META", "msg": "handle 缺失"})
        if handle and not handle.startswith("@"):
            issues.append({"level": "WARN", "code": "META", "msg": f"handle 格式异常: {handle}（应为 @xxx）"})
        if channel_url and handle and ("@" + handle.lstrip("@")) not in channel_url and handle.lstrip("@") not in channel_url:
            issues.append({"level": "WARN", "code": "META", "msg": f"channel_url 与 handle 不一致: {channel_url} vs {handle}"})
        # YouTube 搜索结果不是频道来源，不能作为链接占位。
        if "/results?search_query=" in channel_url or "/results?q=" in channel_url:
            issues.append({"level": "FAIL", "code": "META", "msg": f"channel_url 是 YouTube 搜索页占位（非真实频道链接）: {channel_url[:70]}…"})
        elif channel_url and not youtube_url:
            issues.append({"level": "FAIL", "code": "META", "msg": f"platform=YouTube 但 channel_url 非 YouTube 域名: {channel_url[:70]}…"})
    elif not channel_url:
        issues.append({"level": "WARN", "code": "META", "msg": "channel_url 缺失"})

    fans = kol.get("fans") or ""
    if not fans or fans in ("N/A", "NA", "0", "未知"):
        issues.append({"level": "WARN", "code": "META", "msg": "fans 缺失/未填写"})
    elif re.fullmatch(r"\d+W\+?", fans):  # 形如 5W+ 正常
        pass
    elif re.fullmatch(r"\d+(\.\d+)?[KMW]\+?", fans):
        pass
    elif not re.search(r"\d", fans):
        issues.append({"level": "WARN", "code": "META", "msg": f"fans 格式异常: {fans}"})

    if not kol.get("language"):
        issues.append({"level": "WARN", "code": "META", "msg": "language 缺失"})
    if not kol.get("field"):
        issues.append({"level": "WARN", "code": "META", "msg": "field 缺失"})
    if not kol.get("desc"):
        issues.append({"level": "WARN", "code": "META", "msg": "desc 缺失"})
    return issues


# ---------------------------------------------------------------------------
# 内容层检查（伪造检测核心）
# ---------------------------------------------------------------------------
def check_items(kol: dict, items: list) -> list:
    issues = []
    name = kol.get("name", "")
    links = []
    for i, it in enumerate(items or []):
        link = it.get("link") or ""
        title = it.get("title") or ""
        published = it.get("published") or ""

        if it.get("is_mock") is True or is_mock_link(link):
            issues.append({
                "level": "FAIL",
                "code": "FAKE_LINK",
                "msg": f"条目{i+1} 被标记为 mock 或使用伪链接: {link or '（空）'}",
            })
        elif not link:
            issues.append({"level": "WARN", "code": "LINK", "msg": f"条目{i+1} 无链接"})
        elif link in links:
            issues.append({"level": "WARN", "code": "LINK", "msg": f"条目{i+1} 链接重复: {link}"})
        links.append(link)

        if is_pool_title(name, title):
            issues.append({
                "level": "WARN",
                "code": "FAKE_TITLE",
                "msg": f"条目{i+1} 标题来自模拟语料库（非频道原文）: 「{title}」",
            })

        if published:
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt > datetime.now(timezone.utc) + timedelta(days=1):
                    issues.append({"level": "WARN", "code": "DATE", "msg": f"条目{i+1} 发布时间在未来: {published}"})
            except ValueError:
                issues.append({"level": "WARN", "code": "DATE", "msg": f"条目{i+1} 发布时间无法解析: {published}"})
    return issues


# ---------------------------------------------------------------------------
# 在线层检查（--online，需要网络；适合 GitHub Actions/CI）
# ---------------------------------------------------------------------------
def check_online(kol: dict) -> list:
    """尝试用 requests 验证：频道页 HTTP 状态 / 订阅数 / RSS 最新条目。
    沙箱无网时自动跳过并标注为「未在线验证」。"""
    issues = []
    try:
        import requests
    except ImportError:
        issues.append({"level": "WARN", "code": "ONLINE", "msg": "未安装 requests，跳过在线验证"})
        return issues

    url = kol.get("channel_url") or ""
    channel_id = kol.get("channel_id") or ""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
               "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8"}

    if url:
        try:
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code == 404:
                issues.append({"level": "FAIL", "code": "ONLINE", "msg": f"频道页 404：{url}（频道可能不存在或 handle 错误）"})
            elif r.status_code == 200:
                m = re.search(r'"subscriberCountText":\{"simpleText":"([^"]+)"', r.text)
                if m:
                    issues.append({"level": "INFO", "code": "ONLINE", "msg": f"在线验证：频道可达，订阅数 {m.group(1)}"})
                else:
                    issues.append({"level": "INFO", "code": "ONLINE", "msg": "在线验证：频道可达（未能解析订阅数）"})
            else:
                issues.append({"level": "WARN", "code": "ONLINE", "msg": f"频道页 HTTP {r.status_code}"})
        except Exception as e:
            issues.append({"level": "WARN", "code": "ONLINE", "msg": f"在线验证失败: {type(e).__name__}: {e}"})

    if channel_id:
        try:
            import feedparser
            feed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
            if feed.entries:
                latest = feed.entries[0].get("published", "?")
                issues.append({"level": "INFO", "code": "ONLINE", "msg": f"RSS 有效，最新发布: {latest} | 标题: {feed.entries[0].get('title', '')[:40]}"})
            else:
                issues.append({"level": "WARN", "code": "ONLINE", "msg": "RSS 无条目（channel_id 可能无效）"})
        except Exception as e:
            issues.append({"level": "WARN", "code": "ONLINE", "msg": f"RSS 检查失败: {type(e).__name__}: {e}"})
    return issues


# ---------------------------------------------------------------------------
# 全量审计
# ---------------------------------------------------------------------------
def run_audit(kol_data_path=KOL_DATA_PATH, data_json_path=OUTPUT_DIR / "data.json",
              online=False, verbose=False) -> dict:
    kols = json.loads(Path(kol_data_path).read_text(encoding="utf-8"))
    output = {}
    if Path(data_json_path).exists():
        output = json.loads(Path(data_json_path).read_text(encoding="utf-8"))

    # 建立 kol_id -> items 的映射（只对活跃且在输出中的 KOL）
    items_map = {}
    for entry in output.get("active_kols", []):
        kid = entry.get("kol", {}).get("id")
        items_map[kid] = entry.get("items", [])

    results = []
    for kol in kols:
        kid = kol.get("id")
        issues = check_kol_metadata(kol)
        items = items_map.get(kid, [])
        items_issues = check_items(kol, items)
        issues += items_issues

        online_issues = []
        if online:
            online_issues = check_online(kol)
            issues += [i for i in online_issues if i["level"] != "INFO"]

        levels = {i["level"] for i in issues}
        if "FAIL" in levels:
            verdict = "FAIL"
        elif "WARN" in levels or not items:
            verdict = "WARN"
        else:
            verdict = "PASS"

        mock_count = sum(1 for it in items if it.get("is_mock") is True or is_mock_link(it.get("link", "")))
        pool_count = sum(1 for it in items if is_pool_title(kol.get("name", ""), it.get("title", "")))
        online_info = [i["msg"] for i in online_issues if i["level"] == "INFO"]

        results.append({
            "id": kid,
            "name": kol.get("name", ""),
            "platform": kol.get("platform", ""),
            "fans": kol.get("fans", ""),
            "channel_id": kol.get("channel_id") or "",
            "active": bool(kol.get("active")),
            "verdict": verdict,
            "mock_items": mock_count,
            "pool_titles": pool_count,
            "total_items": len(items),
            "online": online_info,
            "issues": issues,
        })
        if verbose:
            print(f"[{verdict:4s}] #{kid:02d} {kol.get('name','')[:24]:24s} mock={mock_count}/{len(items)}")

    summary = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "total_kols": len(kols),
        "pass": sum(1 for r in results if r["verdict"] == "PASS"),
        "warn": sum(1 for r in results if r["verdict"] == "WARN"),
        "fail": sum(1 for r in results if r["verdict"] == "FAIL"),
        "total_items": sum(r["total_items"] for r in results),
        "mock_items": sum(r["mock_items"] for r in results),
        "pool_titles": sum(r["pool_titles"] for r in results),
        "mock_ratio_pct": round(100 * sum(r["mock_items"] for r in results) / max(1, sum(r["total_items"] for r in results)), 1),
        "online_verified": online,
    }
    return {"summary": summary, "results": results}


# ---------------------------------------------------------------------------
# Markdown 报告生成
# ---------------------------------------------------------------------------
def render_markdown(audit: dict) -> str:
    s = audit["summary"]
    lines = [
        "# 🔍 全频道真实性审计报告（不作伪检查模块）",
        "",
        f"- **审计时间**：{s['audited_at']}",
        f"- **KOL 总数**：{s['total_kols']}　|　**PASS**：{s['pass']}　|　**WARN**：{s['warn']}　|　**FAIL**：{s['fail']}",
        f"- **内容条目**：共 {s['total_items']} 条，其中**伪链接（mock）{s['mock_items']} 条（{s['mock_ratio_pct']}%）**，语料库标题 {s['pool_titles']} 条",
        f"- **在线验证**：{'开启' if s['online_verified'] else '未开启（离线审计，建议 CI 中 --online 复核）'}",
        "",
        "## 判定口径",
        "- **FAIL**：检测到伪造内容（伪链接等）或在线验证确认元数据严重失实",
        "- **WARN**：元数据不完整（channel_id/fans 缺失等）→ 无法证明真实，需人工核",
        "- **PASS**：无伪造痕迹且元数据完整（在线模式还要求验证通过）",
        "",
        "| # | 名称 | 平台 | fans | channel_id | 判定 | mock/总条目 | 主要问题 |",
        "|---|------|------|------|-----------|------|-----------|---------|",
    ]
    for r in audit["results"]:
        problems = []
        seen = set()
        for i in r["issues"]:
            key = i["code"] + ":" + i["msg"][:30]
            if key not in seen:
                seen.add(key)
                problems.append(i["msg"])
        prob_str = "；".join(problems[:3])
        if len(problems) > 3:
            prob_str += f"…(共{len(problems)}条)"
        lines.append(
            f"| {r['id']:>2} | {r['name'][:22]} | {r['platform'][:12]} | {r['fans'][:8]} | "
            f"{r['channel_id'][:12] if r['channel_id'] else '—'} | **{r['verdict']}** | "
            f"{r['mock_items']}/{r['total_items']} | {prob_str[:80]} |"
        )
    lines += ["", "---", "*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="不作伪检查模块：KOL 名单与输出内容真实性审计")
    ap.add_argument("--kol-data", default=str(KOL_DATA_PATH))
    ap.add_argument("--data-json", default=str(OUTPUT_DIR / "data.json"))
    ap.add_argument("--online", action="store_true", help="尝试在线验证（需网络，适合 CI）")
    ap.add_argument("--md", default=None, help="Markdown 报告输出路径（默认 output/audit_report.md）")
    ap.add_argument("--json", dest="json_out", default=None, help="JSON 审计结果输出路径")
    ap.add_argument("--strict", action="store_true", help="存在 FAIL 即退出码 1（CI 门禁）")
    ap.add_argument("--verify-only", action="store_true", help="只审计、不写报告文件")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    audit = run_audit(args.kol_data, args.data_json, online=args.online, verbose=args.verbose)
    s = audit["summary"]
    print("=" * 60)
    print("🔍 不作伪检查模块 · 审计完成")
    print(f"   KOL: {s['total_kols']} | PASS {s['pass']} | WARN {s['warn']} | FAIL {s['fail']}")
    print(f"   条目: {s['total_items']} | mock伪链接 {s['mock_items']} ({s['mock_ratio_pct']}%) | 语料标题 {s['pool_titles']}")
    print("=" * 60)

    if not args.verify_only:
        md_path = args.md or str(OUTPUT_DIR / "audit_report.md")
        Path(md_path).parent.mkdir(parents=True, exist_ok=True)
        Path(md_path).write_text(render_markdown(audit), encoding="utf-8")
        print(f"📄 报告已写入: {md_path}")
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"📊 JSON 已写入: {args.json_out}")

    if args.strict and s["fail"] > 0:
        print(f"❌ 检测到 {s['fail']} 个 FAIL（伪造/严重失实），--strict 门禁未通过")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
