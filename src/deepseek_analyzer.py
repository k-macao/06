"""
DeepSeek 增强分析引擎
- 若 DEEPSEEK_API_KEY 存在，调用 DeepSeek Chat 进行真实多空研判
- 否则回退到本地启发式 analyzer.py
"""
import os
import json
import requests
import random
from datetime import datetime

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# 从环境变量读取
def get_deepseek_key():
    return os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_TOKEN") or ""

def call_deepseek_batch(items, kol_name, kol_field):
    """
    批量调用 DeepSeek：一次请求分析该 KOL 的 3 条内容
    items: list of {title, summary}
    返回: list of {sentiment, confidence, reason, advice} 或 None（失败回退）
    """
    api_key = get_deepseek_key()
    if not api_key:
        return None

    # 构造 prompt
    prompt_items = "\n".join([f"{i+1}. 标题：{it['title']}\n   摘要：{it['summary']}" for i, it in enumerate(items)])

    system_prompt = """你是章鱼 AI·全景分析的多空研判引擎，专注全球财经KOL内容分析。
任务：对给定的财经内容做多空判断。

要求：
- 对每条内容给出：sentiment（只能是 多头/空头/中性）、confidence（整数 50-95）、reason（中文 30-50字，点出关键多空因子）、advice（中文 10-15字操作建议）
- 多头信号：上涨、利好、买入、突破、牛市、增长、超预期、降息、回购等
- 空头信号：下跌、抛售、泡沫、风险、衰退、做空、暴跌、违约、缩表、加息等
- 若多空混杂或客观复盘则判中性
- 必须返回 JSON 数组，长度与输入条数一致，不要额外解释

示例输出：
[{"sentiment":"多头","confidence":78,"reason":"标题释放降息利好，资金面边际改善利于反弹","advice":"逢低分批建仓，设8%止损"},{"sentiment":"空头","confidence":82,"reason":"警示估值泡沫与抛售压力，防御姿态明显","advice":"降低仓位，等待恐慌释放"}]
"""

    item_count = len(items)
    user_prompt = f"""KOL：{kol_name}（领域：{kol_field}）
待分析内容（{item_count}条）：
{prompt_items}

请严格按 JSON 数组返回 {item_count} 个对象，每个对象含 sentiment/confidence/reason/advice。
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1500,
        "response_format": {"type": "json_object"}
    }

    try:
        resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        j = resp.json()
        content = j["choices"][0]["message"]["content"]
        # content 可能是 {"result": [...]} 或直接 [...]
        parsed = json.loads(content)
        # 兼容不同返回结构
        if isinstance(parsed, dict):
            # 尝试找数组字段
            for v in parsed.values():
                if isinstance(v, list) and len(v) == len(items):
                    parsed = v
                    break
        if not isinstance(parsed, list):
            raise ValueError(f"DeepSeek返回非数组: {content[:200]}")
        # 校验并补全
        results = []
        for idx, obj in enumerate(parsed[:len(items)]):
            sentiment = obj.get("sentiment", "中性")
            if sentiment not in ["多头", "空头", "中性"]:
                sentiment = "中性"
            confidence = int(obj.get("confidence", 65))
            confidence = max(50, min(95, confidence))
            reason = obj.get("reason", "")[:80] or "AI综合研判"
            advice = obj.get("advice", "")[:30] or ("持有为主" if sentiment=="多头" else "降低仓位" if sentiment=="空头" else "区间操作")
            results.append({"sentiment": sentiment, "confidence": confidence, "reason": reason, "advice": advice})
        # 若数量不足，用启发式补齐
        while len(results) < len(items):
            results.append({"sentiment": "中性", "confidence": 58, "reason": "AI未返回，降级为中性研判", "advice": "观望等待方向"})
        print(f"[DeepSeek] ✅ {kol_name} 成功：{[r['sentiment'] for r in results]}")
        return results
    except Exception as ex:
        print(f"[DeepSeek] ⚠️ {kol_name} 失败回退启发式: {ex}")
        return None

def analyze_with_deepseek_or_fallback(kol, items):
    """
    封装：优先 DeepSeek，失败则用本地启发式
    返回同样结构的 analyzed + aggregate，且 power 基于 confidence 计算
    """
    # 先尝试 DeepSeek 批量
    deep_results = call_deepseek_batch(items, kol["name"], kol["field"])

    from .analyzer import score_text  # 延迟导入避免循环
    analyzed = []
    bull = bear = neutral = 0
    total_conf = 0
    total_power = 0

    for i, it in enumerate(items):
        if deep_results:
            dr = deep_results[i]
            sentiment = dr["sentiment"]
            confidence = dr["confidence"]
            reason = dr["reason"]
            advice = dr["advice"]
            # power 按置信度映射
            if sentiment == "多头":
                power = int(confidence * 0.85 + random.randint(0, 10))
            elif sentiment == "空头":
                power = int(confidence * 0.83 + random.randint(0, 10))
            else:
                power = int(50 + random.randint(-8, 8))
            power = max(1, min(99, power))
        else:
            # 回退启发式
            res = score_text(it["title"], it["summary"])
            sentiment = res["sentiment"]
            confidence = res["confidence"]
            power = res["power"]
            reason = res["reason"]
            advice = res["advice"]

        # 日期
        try:
            dt = datetime.fromisoformat(it["published"].replace("Z", "+00:00"))
            date_str = dt.strftime("%m-%d")
        except:
            date_str = it["published"][:10]

        analyzed.append({
            **it,
            "date_str": date_str,
            "sentiment": sentiment,
            "confidence": confidence,
            "power": power,
            "reason": reason,
            "advice": advice,
            "engine": "deepseek" if deep_results else "heuristic"
        })
        total_conf += confidence
        total_power += power
        if sentiment == "多头":
            bull += 1
        elif sentiment == "空头":
            bear += 1
        else:
            neutral += 1

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

    analyzed_count = len(analyzed)
    aggregate = {
        "kol_sentiment": kol_sentiment,
        "kol_color": kol_color,
        "bull_count": bull,
        "bear_count": bear,
        "neutral_count": neutral,
        "avg_confidence": int(total_conf / analyzed_count) if analyzed_count else 0,
        "avg_power": int(total_power / analyzed_count) if analyzed_count else 50,
        "battle_text": f"{bull}多 vs {bear}空 vs {neutral}中性"
    }

    return analyzed, aggregate
