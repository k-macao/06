#!/usr/bin/env python3
"""
全球财经金融 KOL 精选名单 · 多空全景战报
作者：章鱼 AI·全景分析
流程：
  1. 排查 53 个 KOL 存活状态（90天内有更新）
  2. 抓取活跃名单最近 3 条内容（RSS + HTML + Mock 中文）
  3. AI 多空分析（DeepSeek LLM 优先，回退启发式）
  4. 生成像素风 HTML 战报
  5. 推送 PushPlus（自动转为微信友好的精简摘要版）

用法：
  python main.py --no-push      # 仅生成，不推送
  python main.py --push-only    # 仅推送（复用上次 output/data.json，常用于补推/重推）
  python main.py --token XXX    # 完整流水线 + 推送（指定 token）
"""
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

from src.fetcher import scan_kols
from src.analyzer import analyze_kol_items, global_battle_stats
from src.deepseek_analyzer import analyze_with_deepseek_or_fallback, get_deepseek_key
from src.report_generator import generate_report
from src.pushplus import send_report, explain_code
from src.digest import build_digest
from src.config import OUTPUT_DIR

# 完整报告超长时降级为摘要版的阈值（PushPlus 会员上限 10 万字）
FULL_HTML_LIMIT = 100_000


def run(push: bool = True, token: str = None, push_only: bool = False):
    print("=" * 60)
    print("🐙 章鱼 AI·全景分析 | 全球财经 KOL 多空战场 启动")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    if push_only:
        # ---- 仅推送模式：复用上次生成的结果 ----
        json_path = OUTPUT_DIR / "data.json"
        if not json_path.exists():
            print(f"❌ 未找到 {json_path}，请先运行 python main.py --no-push 生成报告")
            return False
        dump = json.loads(json_path.read_text(encoding="utf-8"))
        all_enriched = dump["active_kols"]
        stats = dump["meta"]["stats"]
        inactive_kols = dump["inactive_kols"]
        report_date = dump["meta"]["date"]
        engine = dump["meta"]["engine"]
        print(f"📂 复用上次生成结果：{report_date} | 存活 {dump['meta']['active_count']} 家")
    else:
        # 1. 排查
        print("\n[1/4] 🔍 排查 KOL 存活状态（阈值 90 天）...")
        active_kols, inactive_kols, enriched_map = scan_kols(verbose=True)

        print(f"\n📊 排查完成：存活 {len(active_kols)} / 沉寂 {len(inactive_kols)} / 总数 {len(active_kols)+len(inactive_kols)}")
        if inactive_kols:
            print("💤 沉寂名单：", ", ".join([k["name"] for k in inactive_kols]))

        # 2+3. 分析 - 优先 DeepSeek
        has_ds = bool(get_deepseek_key())
        engine_name = "DeepSeek + 启发式" if has_ds else "启发式（未检测到 DEEPSEEK_API_KEY）"
        print(f"\n[2/4] 🧠 AI 多空分析中（每 KOL 3 条）... 引擎: {engine_name}")
        if has_ds:
            print(f"   🔑 DeepSeek Key: {get_deepseek_key()[:8]}*** 已就绪，逐KOL调用 LLM")
        all_enriched = []
        all_analyzed_for_stats = {}
        for kol in active_kols:
            items = enriched_map[kol["id"]]
            if has_ds:
                analyzed_items, agg = analyze_with_deepseek_or_fallback(kol, items)
            else:
                analyzed_items, agg = analyze_kol_items(kol, items)
            all_enriched.append({
                "kol": kol,
                "items": analyzed_items,
                "aggregate": agg
            })
            all_analyzed_for_stats[kol["id"]] = {"items": analyzed_items}
            # 打印简要
            eng = analyzed_items[0].get("engine", "heuristic") if analyzed_items else "heuristic"
            print(f"  #{kol['id']:02d} {kol['name']:20s} → {agg['kol_sentiment']} ({agg['battle_text']})  avg_conf={agg['avg_confidence']}% [{eng}]")

        stats = global_battle_stats(all_analyzed_for_stats)
        print(f"\n⚔️ 全市场战况：🐂 {stats['bull']} ({stats['bull_ratio']}%) vs 🐻 {stats['bear']} ({stats['bear_ratio']}%) vs ⚖️ {stats['neutral']} ({stats['neutral_ratio']}%) → 主导: {stats['dominant']}")

        # 4. 生成报告
        print("\n[3/4] 🎮 生成像素风战报...")
        report_date = datetime.now().strftime("%Y年%m月%d日")
        html_path = OUTPUT_DIR / "report.html"
        json_path = OUTPUT_DIR / "data.json"

        generate_report(all_enriched, stats, html_path, report_date)

        # 同时保存 JSON 数据
        dump = {
            "meta": {
                "author": "章鱼 AI·全景分析",
                "title": "全球财经金融 KOL 精选名单 · 多空全景战报",
                "date": report_date,
                "generated_at": datetime.now().isoformat(),
                "active_count": len(active_kols),
                "inactive_count": len(inactive_kols),
                "total": len(active_kols)+len(inactive_kols),
                "stats": stats,
                "engine": engine_name
            },
            "active_kols": [
                {
                    "kol": e["kol"],
                    "aggregate": e["aggregate"],
                    "items": e["items"]
                } for e in all_enriched
            ],
            "inactive_kols": inactive_kols
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dump, f, ensure_ascii=False, indent=2)
        print(f"[data] 已保存: {json_path}")
        engine = engine_name
        inactive_kols = inactive_kols

    # 5. 推送
    if push:
        html_path = OUTPUT_DIR / "report.html"
        print("\n[4/4] 📨 推送 PushPlus（自动使用精简摘要版，微信友好）...")
        title = f"🐙像素战场·KOL多空战报 {report_date} | 存活{len(all_enriched)}/{len(all_enriched)+len(inactive_kols)} 主导:{stats['dominant']}"
        summary = f"存活{len(all_enriched)}家 · 🐂{stats['bull']} vs 🐻{stats['bear']} | {engine} | 平均战斗力{stats['avg_power']}"

        # 生成摘要版（完整 HTML 约 18 万字符，超 PushPlus 上限，微信推送用摘要版）
        digest_html = build_digest(
            all_enriched, stats, report_date,
            inactive_kols=inactive_kols, engine=engine,
        )
        print(f"   📄 摘要版字符数: {len(digest_html):,}（上限: 100,000/会员）")
        res = send_report(str(html_path), title, token=token, summary=summary, digest_html=digest_html)
        print(f"PushPlus 结果: {res}")
        code = res.get("code")
        # 将推送结果写回 data.json（随 Artifact 上传，便于 CI 留档核查）
        try:
            d2 = json.loads(json_path.read_text(encoding="utf-8"))
            d2.setdefault("meta", {})["push_result"] = {
                "code": res.get("code"),
                "msg": res.get("msg", ""),
                "pushed_at": datetime.now().isoformat(),
            }
            json_path.write_text(json.dumps(d2, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[data] 推送结果写回失败: {e}")
        if code == 200:
            print("   📱 请检查微信『PushPlus』公众号的模板消息（需先关注 PushPlus 服务号并实名认证）")
            return True
        else:
            print(f"   ❌ 推送失败: {explain_code(code)}")
            if code in (903, 905, 302, 888, 900):
                print("   💡 处理建议：")
                print("      - 903/999: 到 https://www.pushplus.plus 重新复制 token，更新仓库 Secret PUSHPLUS_TOKEN")
                print("      - 905: 到 pushplus.plus 完成实名认证（微信扫码）")
                print("      - 未收到但返回 200: 确认微信已关注『PushPlus』公众号，并发送'请求次数'查询")
            return False
    else:
        print("\n[4/4] 📨 已跳过推送（--no-push）")

    print("\n✅ 全部完成！报告路径:", (OUTPUT_DIR / "report.html").resolve())
    print("   本地预览: python -m http.server --directory output 8000")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="章鱼 AI·KOL 多空战报")
    parser.add_argument("--no-push", action="store_true", help="跳过 PushPlus 推送")
    parser.add_argument("--push-only", action="store_true", help="仅推送（复用上次生成的 output/data.json）")
    parser.add_argument("--token", type=str, default=None, help="PushPlus token，覆盖环境变量")
    args = parser.parse_args()
    ok = run(push=not args.no_push, token=args.token, push_only=args.push_only)
    # 推送失败时退出码非 0，让 CI（GitHub Actions）能红起来而不是假绿
    sys.exit(0 if ok else 1)
