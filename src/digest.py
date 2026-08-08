"""
精简摘要版战报生成器（专用于 PushPlus 微信推送）

背景：完整 report.html 约 18.6 万字符，远超 PushPlus 内容上限
（实名用户 2 万字 / 会员 10 万字），推送到微信会被拒绝或截断。
因此推送时改用本模块生成的紧凑摘要版（约 1-2 万字符），
完整版保留在仓库 output/report.html。

作者：章鱼 AI·全景分析
"""


def _esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _sentiment_badge(sentiment: str) -> str:
    style = {
        "多头": "background:#1b4332;color:#7CFC00;border-color:#7CFC00",
        "空头": "background:#4a0e0e;color:#ff6b6b;border-color:#ff6b6b",
        "中性": "background:#3a3a4a;color:#ffd166;border-color:#ffd166",
    }.get(sentiment, "background:#3a3a4a;color:#ffd166;border-color:#ffd166")
    return (f"<span style='display:inline-block;padding:1px 8px;border:2px solid;"
            f"border-radius:2px;font-size:11px;font-weight:bold;{style}'>{_esc(sentiment)}</span>")


def build_digest(all_enriched, stats, report_date, inactive_kols=None,
                 engine="启发式", full_link="", author="章鱼 AI·全景分析"):
    """
    生成适合微信阅读的紧凑 HTML 摘要版。
    all_enriched: [{"kol": {...}, "aggregate": {...}, "items": [...]}, ...]
    stats: {"bull":..,"bear":..,"neutral":..,"bull_ratio":..,"bear_ratio":..,
            "avg_power":..,"dominant":..,"total":..}
    返回 HTML 字符串（不含 <html><body>，可直接嵌入 PushPlus html 模板）。
    """
    inactive_kols = inactive_kols or []
    total = stats.get("total") or sum(len(e["items"]) for e in all_enriched)

    # —— 多空火力 TOP5 / 空头施压 TOP5 ——
    bull_items, bear_items, neutral_items = [], [], []
    for e in all_enriched:
        for it in e["items"]:
            it["_kol_name"] = e["kol"]["name"]
            (bull_items if it.get("sentiment") == "多头"
             else bear_items if it.get("sentiment") == "空头"
             else neutral_items).append(it)
    bull_items.sort(key=lambda x: x.get("power", 0), reverse=True)
    bear_items.sort(key=lambda x: x.get("power", 0), reverse=True)

    def item_row(it):
        name = _esc(it.get("_kol_name", ""))
        title = _esc(it.get("title", ""))
        reason = _esc(it.get("reason", ""))
        advice = _esc(it.get("advice", ""))
        conf = it.get("confidence", "-")
        pow_ = it.get("power", "-")
        return (
            f"<div style='margin:6px 0;padding:8px 10px;background:#151528;"
            f"border:1px solid #33335c;border-left:3px solid #7CFC00'>"
            f"<div style='color:#9adcff;font-size:12px'>👤 {name} · 置信 {conf}% · 战力 {pow_}</div>"
            f"<div style='font-size:13px;margin:3px 0;color:#f2f2ff'>{title}</div>"
            f"<div style='font-size:12px;color:#b9b9d6'>🧠 {reason}</div>"
            f"<div style='font-size:12px;color:#ffe066'>🎯 {advice}</div>"
            f"</div>"
        )

    def rank_list(items, title_txt, border_color):
        if not items:
            return f"<div style='color:#888'>暂无</div>"
        body = "".join(item_row(it) for it in items[:5])
        return (f"<div style='font-size:14px;font-weight:bold;margin:14px 0 4px;"
                f"color:#fff;border-left:4px solid {border_color};padding-left:8px'>{title_txt}</div>{body}")

    # —— KOL 一览表 ——
    rows = []
    for e in all_enriched:
        kol, agg = e["kol"], e["aggregate"]
        badge = _sentiment_badge(agg.get("kol_sentiment", "中性"))
        rows.append(
            f"<tr><td style='padding:4px 6px;font-size:12px;color:#f2f2ff'>"
            f"{_esc(kol['name'])}</td>"
            f"<td style='padding:4px 6px;font-size:11px;color:#9adcff'>{_esc(kol.get('platform',''))}</td>"
            f"<td style='padding:4px 6px;font-size:11px;color:#b9b9d6'>{_esc(kol.get('fans',''))}</td>"
            f"<td style='padding:4px 6px;text-align:center'>{badge}</td>"
            f"<td style='padding:4px 6px;font-size:11px;color:#888'>{_esc(agg.get('battle_text',''))}</td>"
            f"</tr>")
    kol_table = (
        f"<div style='font-size:14px;font-weight:bold;margin:14px 0 4px;color:#fff;"
        f"border-left:4px solid #ffd166;padding-left:8px'>📋 存活 KOL 一览（{len(all_enriched)} 家）</div>"
        f"<table style='width:100%;border-collapse:collapse;background:#151528'>"
        f"<tr style='color:#9adcff;font-size:11px'><th align='left'>名称</th><th align='left'>平台</th>"
        f"<th align='left'>粉丝</th><th>阵营</th><th align='right'>多空</th></tr>"
        + "".join(rows) +
        f"</table>")

    # —— 沉寂名单 ——
    inactive_txt = ""
    if inactive_kols:
        names = "、".join(_esc(k["name"]) for k in inactive_kols)
        inactive_txt = (f"<div style='margin-top:10px;font-size:12px;color:#999;background:#1a1a2e;"
                        f"border:1px dashed #555;padding:6px 10px'>💤 沉寂（已剔除）：{names}</div>")

    # —— 完整版链接 ——
    link_txt = ""
    if full_link:
        link_txt = (f"<div style='margin-top:10px;font-size:12px;color:#7CFC00;text-align:center'>"
                    f"📎 完整版 HTML 战报：<a href='{_esc(full_link)}' style='color:#7CFC00'>{_esc(full_link)}</a></div>")
    else:
        link_txt = (f"<div style='margin-top:10px;font-size:11px;color:#777;text-align:center'>"
                    f"完整版（18万字符）体积超微信限制，已自动转为摘要版；完整 HTML 见仓库 output/report.html</div>")

    html = f"""
<div style='font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#0f0f1a;color:#f2f2ff;padding:14px;border:4px solid #fff;box-shadow:4px 4px 0 #000'>
  <div style='text-align:center;font-size:20px;font-weight:bold;color:#ffe066;letter-spacing:2px'>🐙 像素战场 · KOL 多空战报</div>
  <div style='text-align:center;font-size:12px;color:#9adcff;margin:4px 0'>{_esc(report_date)} · {_esc(author)}</div>

  <div style='display:flex;justify-content:space-between;background:#151528;border:2px solid #33335c;padding:8px 12px;margin:10px 0'>
    <span style='font-size:13px'>存活 <b style='color:#7CFC00'>{stats.get('active_count', len(all_enriched))}</b>/{len(all_enriched)+len(inactive_kols)} 家</span>
    <span style='font-size:13px'>🐂 <b style='color:#7CFC00'>{stats.get('bull',0)}</b> vs 🐻 <b style='color:#ff6b6b'>{stats.get('bear',0)}</b> vs ⚖️ <b style='color:#ffd166'>{stats.get('neutral',0)}</b></span>
    <span style='font-size:13px'>主导 <b style='color:#ffe066'>{_esc(stats.get('dominant',''))}</b></span>
  </div>

  <div style='background:#1a1a2e;border:2px solid #33335c;padding:8px 12px;margin:10px 0;font-size:12px;color:#b9b9d6'>
    参战内容 {total} 条 · 平均战斗力 {stats.get('avg_power','-')} · 引擎：{_esc(engine)}
  </div>

  {rank_list(bull_items[:5], '🔥 多头火力 TOP5', '#7CFC00')}
  {rank_list(bear_items[:5], '💣 空头施压 TOP5', '#ff6b6b')}

  {kol_table}
  {inactive_txt}
  {link_txt}

  <div style='margin-top:12px;font-size:10px;color:#666;text-align:center;line-height:1.6'>
    数据来源：YouTube / TikTok / IG / Reddit / TradingView 公开页<br>
    本报告由 AI 启发式引擎生成，仅供研究与演示，不构成投资建议
  </div>
</div>
"""
    return html
