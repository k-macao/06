"""
AI 多空分析引擎（离线启发式）
- 关键词+语境规则判定 多头( Bull ) / 空头( Bear ) / 中性( Neutral )
- 给出置信度、战斗力、理由与操作提示
- 支持中英文混合
"""
import re
import random
from datetime import datetime

BULL_KEYWORDS = [
    "多头", "看多", "上涨", "利好", "买入", "增持", "突破", "反弹", "牛市", "强劲", "增长", "超预期", "机会", "抄底", "持有", "推荐", "加仓", "新高", "加速", "扩张", "复苏", "降息", "回购", "分红",
    "bull", "buy", "long", "breakout", "rally", "growth", "upside", "upgrade", "surge", "rebound", "accumulate", "outperform", "beat", "all-time high"
]

BEAR_KEYWORDS = [
    "空头", "看空", "下跌", "利空", "卖出", "抛售", "暴跌", "崩盘", "泡沫", "风险", "警告", "衰退", "熊市", "压力", "做空", "减持", "清仓", "腰斩", "爆雷", "违约", "缩表", "加息", "通胀", "坏账",
    "bear", "sell", "short", "crash", "bubble", "risk", "warning", "recession", "downgrade", "plunge", "collapse", "default", "exposure", "tightening"
]

NEUTRAL_CUES = ["震荡", "观望", "中性", "分化", "博弈", "平衡", "横盘"]

def score_text(title: str, summary: str) -> dict:
    text = f"{title} {summary}".lower()
    # 中文不转 lower 影响不大
    bull_hits = sum(1 for k in BULL_KEYWORDS if k.lower() in text)
    bear_hits = sum(1 for k in BEAR_KEYWORDS if k.lower() in text)
    neutral_hits = sum(1 for k in NEUTRAL_CUES if k in text)

    # 特殊句式加权
    if "?" in title or "？" in title:
        neutral_hits += 0.5
    if "!" in title or "！" in title:
        # 感叹号往往偏情绪化，放大主导方向
        if bull_hits > bear_hits:
            bull_hits += 0.5
        elif bear_hits > bull_hits:
            bear_hits += 0.5

    total = bull_hits + bear_hits + neutral_hits
    if total == 0:
        # 无关键词则中性偏随机
        sentiment = "中性"
        confidence = 52 + random.randint(0, 8)
        bull_hits, bear_hits = 0.5, 0.5
    elif bull_hits > bear_hits + 0.5:
        sentiment = "多头"
        confidence = min(92, 62 + (bull_hits - bear_hits) * 9 + random.randint(0, 6))
    elif bear_hits > bull_hits + 0.5:
        sentiment = "空头"
        confidence = min(91, 60 + (bear_hits - bull_hits) * 9 + random.randint(0, 6))
    else:
        sentiment = "中性"
        confidence = 55 + random.randint(0, 12)

    # 战斗力 1-100
    if sentiment == "多头":
        power = int(confidence * 0.85 + random.randint(0, 10))
    elif sentiment == "空头":
        power = int(confidence * 0.83 + random.randint(0, 10))
    else:
        power = int(50 + random.randint(-8, 8))

    # 生成理由
    reason = build_reason(sentiment, title, summary, bull_hits, bear_hits)

    # 操作提示
    advice_map = {
        "多头": random.choice(["逢低分批建仓，设8%止损", "持有为主，关注量能是否跟随", "趋势未坏，回调即机会"]),
        "空头": random.choice(["降低仓位，等待恐慌释放", "空仓观望，勿接飞刀", "对冲为主，关注防御板块"]),
        "中性": random.choice(["高抛低吸，区间操作", "等待方向明朗再重仓", "均衡配置，攻守兼备"]),
    }

    return {
        "sentiment": sentiment,
        "confidence": int(confidence),
        "power": max(1, min(99, power)),
        "bull_hits": bull_hits,
        "bear_hits": bear_hits,
        "reason": reason,
        "advice": advice_map[sentiment]
    }

def build_reason(sentiment, title, summary, bull_hits, bear_hits):
    if sentiment == "多头":
        templates = [
            f"标题释放积极信号（“{title[:14]}…”），基本面或资金面出现边际改善，资金有做多动能。",
            f"内容强调增长/利好逻辑，搭配 {int(bull_hits)} 个多头关键词，短线情绪偏乐观。",
            f"作者暗示抄底窗口打开，配合量价或政策催化，利于多头发起进攻。",
        ]
    elif sentiment == "空头":
        templates = [
            f"标题直指风险（“{title[:14]}…”），警示抛售或衰退压力，防御姿态明显。",
            f"文中出现 {int(bear_hits)} 个空头关键词，指向泡沫/暴雷/缩表等利空因子。",
            f"作者对估值与流动性表示担忧，空头能量积聚，易形成下行共振。",
        ]
    else:
        templates = [
            f"内容呈现多空博弈，{int(bull_hits)} 多 vs {int(bear_hits)} 空，方向未明，需等待催化。",
            f"标题设问、观点平衡，强调震荡与分化，适合区间战术而非单边押注。",
            f"作者更偏客观复盘，缺乏明确方向指引，市场处于混沌期。",
        ]
    return random.choice(templates)

def analyze_kol_items(kol, items):
    """
    items: list of 3 dicts {title, summary, link, published}
    返回: list with added analysis + kol aggregate
    """
    analyzed = []
    bull = bear = neutral = 0
    total_conf = 0
    total_power = 0
    for it in items:
        res = score_text(it["title"], it["summary"])
        # 解析发布时间用于展示
        try:
            dt = datetime.fromisoformat(it["published"].replace("Z", "+00:00"))
            date_str = dt.strftime("%m-%d")
        except:
            date_str = it["published"][:10]
        analyzed.append({
            **it,
            "date_str": date_str,
            "sentiment": res["sentiment"],
            "confidence": res["confidence"],
            "power": res["power"],
            "reason": res["reason"],
            "advice": res["advice"]
        })
        total_conf += res["confidence"]
        total_power += res["power"]
        if res["sentiment"] == "多头":
            bull += 1
        elif res["sentiment"] == "空头":
            bear += 1
        else:
            neutral += 1

    # KOL 综合判断
    if bull > bear and bull >= 2:
        kol_sentiment = "多头阵营"
        kol_color = "bull"
    elif bear > bull and bear >= 2:
        kol_sentiment = "空头阵营"
        kol_color = "bear"
    elif bull == bear:
        kol_sentiment = "均衡拉锯"
        kol_color = "neutral"
    else:
        kol_sentiment = "轻度偏" + ("多" if bull > bear else "空")
        kol_color = "bull" if bull > bear else "bear"

    aggregate = {
        "kol_sentiment": kol_sentiment,
        "kol_color": kol_color,
        "bull_count": bull,
        "bear_count": bear,
        "neutral_count": neutral,
        "avg_confidence": int(total_conf / 3) if analyzed else 0,
        "avg_power": int(total_power / 3) if analyzed else 50,
        "battle_text": f"{bull}多 vs {bear}空 vs {neutral}中性"
    }

    return analyzed, aggregate

def global_battle_stats(all_analyzed_kols):
    """全市场多空能量汇总"""
    total_items = 0
    bull_items = 0
    bear_items = 0
    neutral_items = 0
    power_sum = 0
    for kol_id, data in all_analyzed_kols.items():
        for it in data["items"]:
            total_items += 1
            power_sum += it["power"]
            if it["sentiment"] == "多头":
                bull_items += 1
            elif it["sentiment"] == "空头":
                bear_items += 1
            else:
                neutral_items += 1
    if total_items == 0:
        return {"bull_ratio": 33, "bear_ratio": 33, "neutral_ratio": 34, "avg_power": 50, "dominant": "均衡"}
    bull_ratio = round(bull_items / total_items * 100)
    bear_ratio = round(bear_items / total_items * 100)
    neutral_ratio = 100 - bull_ratio - bear_ratio
    dominant = "多头" if bull_items > bear_items else "空头" if bear_items > bull_items else "均衡"
    return {
        "total": total_items,
        "bull": bull_items,
        "bear": bear_items,
        "neutral": neutral_items,
        "bull_ratio": bull_ratio,
        "bear_ratio": bear_ratio,
        "neutral_ratio": neutral_ratio,
        "avg_power": int(power_sum / total_items) if total_items else 50,
        "dominant": dominant
    }
