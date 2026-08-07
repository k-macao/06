#!/usr/bin/env python3
"""
全球财经金融 KOL 精选名单 · 多空全景战报
作者：章鱼 AI·全景分析
流程：
  1. 排查 53 个 KOL 存活状态（90天内有更新）
  2. 抓取活跃名单最近 3 条内容（RSS + HTML + Mock 中文）
  3. AI 多空分析（启发式引擎）
  4. 生成像素风 HTML 战报
  5. 推送 PushPlus
"""
import json
import argparse
from pathlib import Path
from datetime import datetime

from src.fetcher import scan_kols
from src.analyzer import analyze_kol_items, global_battle_stats
from src.report_generator import generate_report
from src.pushplus import send_report
from src.config import OUTPUT_DIR

def run(push: bool = True, token: str = None):
    print("="*60)
    print("🐙 章鱼 AI·全景分析 | 全球财经 KOL 多空战场 启动")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 1. 排查
    print("\n[1/4] 🔍 排查 KOL 存活状态（阈值 90 天）...")
    active_kols, inactive_kols, enriched_map = scan_kols(verbose=True)

    print(f"\n📊 排查完成：存活 {len(active_kols)} / 沉寂 {len(inactive_kols)} / 总数 {len(active_kols)+len(inactive_kols)}")
    if inactive_kols:
        print("💤 沉寂名单：", ", ".join([k["name"] for k in inactive_kols]))

    # 2+3. 分析
    print("\n[2/4] 🧠 AI 多空分析中（每 KOL 3 条）...")
    all_enriched = []
    all_analyzed_for_stats = {}
    for kol in active_kols:
        items = enriched_map[kol["id"]]
        analyzed_items, agg = analyze_kol_items(kol, items)
        all_enriched.append({
            "kol": kol,
            "items": analyzed_items,
            "aggregate": agg
        })
        all_analyzed_for_stats[kol["id"]] = {"items": analyzed_items}
        # 打印简要
        print(f"  #{kol['id']:02d} {kol['name']:20s} → {agg['kol_sentiment']} ({agg['battle_text']})  avg_conf={agg['avg_confidence']}%")

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
            "stats": stats
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

    # 5. 推送
    if push:
        print("\n[4/4] 📨 推送 PushPlus...")
        title = f"🐙像素战场·KOL多空战报 {report_date} | 存活{len(active_kols)}/{len(active_kols)+len(inactive_kols)} 主导:{stats['dominant']}"
        summary = f"存活{len(active_kols)}家 · 🐂{stats['bull']} vs 🐻{stats['bear']} | 平均战斗力{stats['avg_power']}"
        res = send_report(str(html_path), title, token=token, summary=summary)
        print(f"PushPlus 结果: {res}")
    else:
        print("\n[4/4] 📨 已跳过推送（--no-push）")

    print("\n✅ 全部完成！报告路径:", html_path.resolve())
    print("   本地预览: python -m http.server --directory output 8000")
    return html_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="章鱼 AI·KOL 多空战报")
    parser.add_argument("--no-push", action="store_true", help="跳过 PushPlus 推送")
    parser.add_argument("--token", type=str, default=None, help="PushPlus token，覆盖环境变量")
    args = parser.parse_args()
    run(push=not args.no_push, token=args.token)
