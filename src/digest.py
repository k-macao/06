"""
⚔️ 多空战场 · 精简摘要版战报生成器（专用于 PushPlus 微信推送）

排版风格：战斗竞技场 —— 血条 HP、军团花名册、猛攻/重击 TOP5、MVP 表彰
小符号体系：🐂🐻 阵营 · ⚔️🛡️🗡️ 武器 · 💥🔥💣 火力 · 🏆🥇👑 荣誉 · 📈📉 行情

背景：完整 report.html 会随已验证频道数量增长，可能超过 PushPlus 内容上限。
因此推送始终使用本模块生成的紧凑摘要版，完整版保留在仓库 output/report.html。

作者：章鱼 AI·全景分析
"""


def _esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- 小工具 ----------

def _badge(text, color, bg):
    """小型角标"""
    return (f"<span style='display:inline-block;padding:0 6px;margin:0 2px;"
            f"border:1px solid {color};color:{color};background:{bg};"
            f"border-radius:3px;font-size:10px;font-weight:bold'>{text}</span>")


def _hp_bar(pct, color):
    """章鱼风血条"""
    pct = max(0, min(100, pct))
    return (f"<div style='height:10px;background:#0a0a14;border:1px solid #44446a;"
            f"margin:2px 0 6px'>"
            f"<div style='width:{pct}%;height:100%;background:{color};"
            f"box-shadow:0 0 6px {color}'></div></div>")


def _sentiment_badge(sentiment):
    style = {
        "多头": ("#7CFC00", "#0d2015"),
        "空头": ("#ff6b6b", "#2a0d0d"),
        "中性": ("#ffd166", "#2a240d"),
    }.get(sentiment, ("#ffd166", "#2a240d"))
    return _badge(_esc(sentiment), style[0], style[1])


def _camp_meta(sentiment):
    """阵营 → (符号, 颜色, 名称)"""
    return {
        "多头阵营": ("🐂", "#7CFC00", "多头阵营"),
        "轻度偏多": ("🔺", "#a3e635", "偏多"),
        "均衡拉锯": ("⚖️", "#ffd166", "均衡拉锯"),
        "轻度偏空": ("🔻", "#ffa94d", "偏空"),
        "空头阵营": ("🐻", "#ff6b6b", "空头阵营"),
    }.get(sentiment, ("⚖️", "#ffd166", _esc(sentiment)))


# ---------- 主体 ----------

def build_digest(all_enriched, stats, report_date, inactive_kols=None,
                 engine="启发式", full_link="", author="章鱼 AI·全景分析"):
    """
    生成战斗风紧凑 HTML 摘要版。
    all_enriched: [{"kol": {...}, "aggregate": {...}, "items": [...]}, ...]
    stats: {"bull":..,"bear":..,"neutral":..,"bull_ratio":..,"bear_ratio":..,
            "avg_power":..,"dominant":..,"total":..}
    返回 HTML 字符串（不含 <html><body>，可直接嵌入 PushPlus html 模板）。
    """
    inactive_kols = inactive_kols or []
    total = stats.get("total") or sum(len(e["items"]) for e in all_enriched)

    # 1️⃣ 情报归类
    bull_items, bear_items = [], []
    for e in all_enriched:
        for it in e["items"]:
            it["_kol_name"] = e["kol"]["name"]
            if it.get("sentiment") == "多头":
                bull_items.append(it)
            elif it.get("sentiment") == "空头":
                bear_items.append(it)
    bull_items.sort(key=lambda x: x.get("power", 0), reverse=True)
    bear_items.sort(key=lambda x: x.get("power", 0), reverse=True)

    # 2️⃣ MVP 表彰
    def mvp(items):
        return items[0] if items else None

    bull_mvp, bear_mvp = mvp(bull_items), mvp(bear_items)

    # 3️⃣ 战场局势
    bull_r, bear_r = stats.get("bull_ratio", 0), stats.get("bear_ratio", 0)
    dominant = stats.get("dominant", "")
    if dominant == "空头":
        mood = "🌪️ 空头压制 · 恐慌气息弥漫"
    elif dominant == "多头":
        mood = "🔥 多头进攻 · 市场情绪回暖"
    else:
        mood = "🛡️ 多空胶着 · 全场观望蓄力"

    # 4️⃣ TOP5 战报条目
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    def rank_section(items, title_txt, icon, color, accent):
        if not items:
            return ""
        body = []
        for i, it in enumerate(items[:5]):
            name = _esc(it.get("_kol_name", ""))
            title = _esc(it.get("title", ""))
            reason = _esc(it.get("reason", ""))
            advice = _esc(it.get("advice", ""))
            conf, pow_ = it.get("confidence", "-"), it.get("power", "-")
            body.append(
                f"<div style='margin:6px 0;padding:7px 9px;background:#151528;"
                f"border:1px solid #33335c;border-left:4px solid {color}'>"
                f"<div style='font-size:12px'>{medals[i]} <b style='color:#f2f2ff'>{name}</b>"
                f"{_badge(f'置信{conf}%', '#9adcff', '#0d1526')}"
                f"{_badge(f'⚡{pow_}', color, '#0d1526')}</div>"
                f"<div style='font-size:13px;margin:3px 0;color:#f2f2ff'>{icon} {title}</div>"
                f"<div style='font-size:12px;color:#b9b9d6'>🧠 研判：{reason}</div>"
                f"<div style='font-size:12px;color:#ffe066'>🎯 战术：{advice}</div>"
                f"</div>")
        return (f"<div style='font-size:14px;font-weight:bold;margin:14px 0 4px;color:#fff;"
                f"border-left:5px solid {color};padding-left:8px'>{title_txt}"
                f"<span style='font-size:10px;color:#888;font-weight:normal'>（按 ⚡战力 排序）</span></div>"
                + "".join(body))

    # 5️⃣ 军团花名册（按阵营分组）
    camp_order = ["多头阵营", "轻度偏多", "均衡拉锯", "轻度偏空", "空头阵营"]
    camp_map = {}
    for e in all_enriched:
        camp_map.setdefault(e["aggregate"].get("kol_sentiment", "均衡拉锯"), []).append(e)

    roster = []
    for camp in camp_order:
        members = camp_map.get(camp)
        if not members:
            continue
        sym, color, label = _camp_meta(camp)
        avg_pow = sum(e["aggregate"].get("avg_power", 0) for e in members) // len(members)
        names = "、".join(f"{sym}{_esc(e['kol']['name'])}" for e in members)
        roster.append(
            f"<div style='margin:4px 0;padding:6px 8px;background:#151528;"
            f"border-left:3px solid {color}'>"
            f"<span style='font-size:12px;font-weight:bold;color:{color}'>{sym} {label}"
            f"</span>{_badge(f'{len(members)}家', color, '#0d1526')}"
            f"{_badge(f'⚡均战{avg_pow}', '#b9b9d6', '#0d1526')}"
            f"<div style='font-size:11px;color:#b9b9d6;margin-top:3px;line-height:1.7'>{names}</div>"
            f"</div>")

    # 6️⃣ 隔离/未验证名单（可能是停用、来源失效或暂不支持的平台，不等于沉寂）
    inactive_txt = ""
    if inactive_kols:
        names = "、".join(f"🛡️{_esc(k['name'])}" for k in inactive_kols)
        inactive_txt = (f"<div style='margin-top:10px;font-size:12px;color:#999;background:#1a1a2e;"
                        f"border:1px dashed #555;padding:6px 10px'>"
                        f"🛡️ 本次隔离/未验证（{len(inactive_kols)} 家）：{names}</div>")

    # 7️⃣ 完整版链接 / 提示
    if full_link:
        link_txt = (f"<div style='margin-top:10px;font-size:12px;color:#7CFC00;text-align:center'>"
                    f"📎 完整战报：<a href='{_esc(full_link)}' style='color:#7CFC00'>{_esc(full_link)}</a></div>")
    else:
        link_txt = (f"<div style='margin-top:10px;font-size:11px;color:#777;text-align:center'>"
                    f"微信推送使用战场摘要版；完整 HTML 见仓库 output/report.html</div>")

    mvp_txt = ""
    if bull_mvp or bear_mvp:
        parts = []
        if bull_mvp:
            p1 = _badge(f"⚡{bull_mvp.get('power', '-')}", "#7CFC00", "#0d1526")
            parts.append(f"🐂 多头MVP：{_esc(bull_mvp.get('_kol_name', ''))} {p1}")
        if bear_mvp:
            p2 = _badge(f"⚡{bear_mvp.get('power', '-')}", "#ff6b6b", "#0d1526")
            parts.append(f"🐻 空头MVP：{_esc(bear_mvp.get('_kol_name', ''))} {p2}")
        mvp_txt = ("<div style='display:flex;justify-content:space-around;flex-wrap:wrap;"
                   "background:#151528;border:2px solid #33335c;padding:6px 8px;margin:8px 0;"
                   "font-size:12px'>" + "&nbsp;&nbsp;".join(parts) + "</div>")

    # ---------- 组装 ----------
    html = f"""
<div style='font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#0f0f1a;color:#f2f2ff;padding:14px;border:4px solid #fff;box-shadow:4px 4px 0 #000'>

  <!-- ⚔️ 战斗横幅 -->
  <div style='text-align:center;background:#111122;border:3px double #ffe066;padding:10px 8px'>
    <div style='font-size:22px;font-weight:bold;color:#ffe066;letter-spacing:3px'>⚔️ 多空战场 · 章鱼战报 ⚔️</div>
    <div style='font-size:11px;color:#9adcff;margin:4px 0'>🐙 {_esc(author)} ｜ {_esc(report_date)}</div>
    <div style='font-size:13px;color:#fff;letter-spacing:1px'>🐂 BULL <span style='color:#ff6b6b'>⚡ VS ⚡</span> BEAR 🐻</div>
  </div>

  <!-- 🩸 军团状态 -->
  <div style='background:#151528;border:2px solid #33335c;padding:8px 12px;margin:10px 0;font-size:12px;color:#b9b9d6'>
    🧾 情报参战 <b style='color:#fff'>{total}</b> 条 ｜ ⚡ 平均战力 <b style='color:#fff'>{stats.get('avg_power','-')}</b> ｜ 引擎 {_esc(engine)}
  </div>

  <!-- ❤️‍🔥 HP 血条 -->
  <div style='background:#151528;border:2px solid #33335c;padding:8px 12px;margin:10px 0'>
    <div style='font-size:12px;color:#7CFC00'>🐂 多头军团 HP <b>{stats.get('bull',0)}</b> 条 · {bull_r}%</div>
    {_hp_bar(bull_r, '#7CFC00')}
    <div style='font-size:12px;color:#ff6b6b'>🐻 空头军团 HP <b>{stats.get('bear',0)}</b> 条 · {bear_r}%</div>
    {_hp_bar(bear_r, '#ff6b6b')}
    <div style='font-size:12px;color:#ffd166'>⚖️ 中立观望 <b>{stats.get('neutral',0)}</b> 条 · {stats.get('neutral_ratio',0)}%</div>
    {_hp_bar(stats.get('neutral_ratio', 0), '#ffd166')}
    <div style='font-size:12px;color:#ffe066;margin-top:4px'>👑 主导阵营：{_sentiment_badge(dominant)} {mood}</div>
  </div>

  <!-- 🏆 MVP -->
  {mvp_txt}

  <!-- 🔥 多头猛攻 TOP5 -->
  {rank_section(bull_items, '🔥 多头军团 · 猛攻 TOP5', '📈', '#7CFC00', '#7CFC00')}

  <!-- 💣 空头重击 TOP5 -->
  {rank_section(bear_items, '💣 空头军团 · 重击 TOP5', '📉', '#ff6b6b', '#ff6b6b')}

  <!-- 🛡️ 军团花名册 -->
  <div style='font-size:14px;font-weight:bold;margin:14px 0 4px;color:#fff;border-left:5px solid #ffd166;padding-left:8px'>
    🛡️ 军团花名册 <span style='font-size:10px;color:#888;font-weight:normal'>（{len(all_enriched)} 家参战）</span>
  </div>
  {''.join(roster)}

  {inactive_txt}
  {link_txt}

  <div style='margin-top:12px;font-size:10px;color:#666;text-align:center;line-height:1.7'>
    🗡️ 入报数据来源：YouTube 官方 RSS（其他平台在可信抓取器完成前保持隔离）<br>
    ⚠️ 本报告由 AI 启发式引擎生成，仅供研究与演示，不构成投资建议
  </div>
</div>
"""
    return html
