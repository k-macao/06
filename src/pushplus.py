"""
PushPlus 推送模块
文档：http://www.pushplus.plus/doc/
支持：单人推送、一对多（群组 topic）、html 模板

一对多（默认）：
- 接口参数 `topic` = 群组编码；填了就把消息推给该群组内所有订阅者，不填仅发给自己。
- 本项目默认群组编码 `oai.1`（群名 oai.1），可用 config.yaml `pushplus_topic`、
  环境变量 `PUSHPLUS_TOPIC` 或 `python main.py --topic 群组编码` 覆盖；
  `python main.py --self-only` 可临时关掉一对多、只发给自己。
- 订阅方式：pushplus.plus →「发送消息 → 一对多消息」→ 群组 oai.1 → 生成二维码，
  订阅者微信扫码加入后才会收到推送。
- `channel=webhook` 时 `topic` 按官方文档无效，此时仍按单人/渠道配置发送。

常见问题速查：
- 2024-08 起未实名认证的用户无法发送（返回 905），请在 pushplus.plus 完成实名。
- 内容长度上限：实名用户 2 万字 / 会员 10 万字（超长会推送失败或被截断）。
- 相同内容 1 小时内最多 3 条；1 分钟最多 5 次请求。
- 接口是异步的：返回 200 只代表收到请求，实际送达以微信收到为准。
- 必须用微信关注 PushPlus 公众号，推送经公众号模板消息送达。
"""
import os
import requests
from .config import PUSHPLUS_URL, PUSHPLUS_TOKEN, PUSHPLUS_TOPIC

# 内容长度上限（按字符数计，含 HTML 标签）
CONTENT_LIMIT_FREE = 20_000    # 实名用户：2 万字
CONTENT_LIMIT_MEMBER = 100_000  # 会员：10 万字

# 错误码说明（见 https://www.pushplus.plus/doc/help/limit.html 与接口文档）
CODE_MESSAGES = {
    200: "✅ 推送成功（异步送达，实际以微信收到为准）",
    302: "未登录/登录失效，请重新登录 PushPlus",
    401: "请求未授权（开放接口未启用）",
    403: "请求 IP 未授权（开放接口白名单）",
    500: "PushPlus 系统异常，请稍后重试",
    600: "数据异常，操作失败",
    805: "无权查看",
    888: "积分不足，需要充值",
    900: "账号使用受限（今日请求次数过多，已停止推送，明日恢复）",
    903: "无效的用户令牌（token 不正确，请到 pushplus.plus 重新复制）",
    905: "账户未实名认证（2024-08 起必须实名才能发送，请到 pushplus.plus 完成实名）",
    999: "服务端验证错误（多为 token 无效或参数问题）",
    998: "内容超过 PushPlus 长度上限（会员 10 万字），已拒绝发送",
    997: "未配置 token，跳过推送",
}


def explain_code(code) -> str:
    return CODE_MESSAGES.get(code, f"未知返回码 {code}（请查询 PushPlus 文档）")


def resolve_topic(topic: str = None) -> str:
    """归一化一对多群组编码（接口参数 topic）。

    - `None`：用配置默认群组（config.yaml `pushplus_topic` / 环境变量 `PUSHPLUS_TOPIC`，默认 `oai.1`）
    - `""` / `none` / `off` / `self` / `-`：明确关闭一对多，只发给自己
    - 其他：使用该群组编码
    """
    raw = PUSHPLUS_TOPIC if topic is None else str(topic)
    raw = raw.strip()
    return "" if raw.lower() in ("", "none", "off", "self", "-") else raw


def send_pushplus(token: str, title: str, content: str, template: str = "html",
                  channel: str = "wechat", topic: str = None) -> dict:
    """
    发送 PushPlus
    - token: 你的 PushPlus token
    - title: 推送标题
    - content: html 或 markdown 内容
    - template: html / markdown / json
    - channel: wechat / webhook / cp / mail
    - topic: 一对多群组编码；None 用配置默认群组（oai.1），传 "" 则退化为单人推送
    返回接口 JSON 字典（附带 topic / mode 两个本地字段，便于日志与留档）。
    """
    token = token or PUSHPLUS_TOKEN or os.getenv("PUSHPLUS_TOKEN", "")
    if not token:
        print("[PushPlus] 未配置 token，跳过推送。请设置环境变量 PUSHPLUS_TOKEN 或在 config.yaml 中配置。")
        return {"code": 997, "msg": "no token", "skipped": True}

    # 长度守卫：超上限直接拒绝，避免微信收不到且白白消耗请求次数
    n = len(content)
    if n > CONTENT_LIMIT_MEMBER:
        print(f"[PushPlus] 内容 {n:,} 字符 > 上限 {CONTENT_LIMIT_MEMBER:,}（会员 10 万字），拒绝发送。"
              f"请改用摘要版（src/digest.py）或精简内容。")
        return {"code": 998, "msg": f"content too long: {n}", "skipped": True}

    group = resolve_topic(topic)
    mode = f"一对多·群组 {group}" if group else "单人·仅发给自己"
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
        "channel": channel,
    }
    if group:
        data["topic"] = group
        if channel == "webhook":
            print("[PushPlus] 提示：channel=webhook 时 topic（群组编码）按官方文档无效，实际只走 webhook 渠道")
    print(f"[PushPlus] 发送中... {mode} | title={title!r} content={n:,} 字符")
    try:
        resp = requests.post(PUSHPLUS_URL, json=data, timeout=15)
        j = resp.json()
        if not isinstance(j, dict):
            j = {"code": 500, "msg": f"非法响应: {j!r}"}
        code = j.get("code")
        j.setdefault("topic", group)
        j.setdefault("mode", mode)
        if code == 200:
            short_code = j.get("data") or ""
            print(f"[PushPlus] ✅ 已受理: {title} | {mode}"
                  f"{' | 流水号 ' + str(short_code) if short_code else ''}（异步送达，请查收微信）")
        else:
            print(f"[PushPlus] ❌ 推送失败 code={code}: {explain_code(code)} | {mode} | 原始返回: {j}")
        return j
    except Exception as ex:
        print(f"[PushPlus] 网络异常: {ex}")
        return {"code": 500, "msg": str(ex), "topic": group, "mode": mode}



def send_report(html_path: str, title: str, token: str = None, summary: str = "",
                digest_html: str = None, full_link: str = "", topic: str = None) -> dict:
    """
    读取本地 html 报告并推送。
    - 若提供 digest_html（精简摘要版），直接推送摘要版（推荐，微信友好且不超限）
    - 否则推送完整 html；若完整 html 超过会员上限则拒绝并给出提示
    - topic: 一对多群组编码；None 用配置默认群组（oai.1），传 "" 则只发给自己
    """
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as ex:
        print(f"[PushPlus] 读取报告失败: {ex}")
        return {"code": 500, "msg": str(ex)}

    if digest_html:
        content = digest_html
        # 顶部加一行摘要横幅
        if summary:
            content = (f"<div style='background:#1a1a2e;color:#ffe066;padding:8px 10px;"
                       f"border:2px solid #fff;font-family:monospace;text-align:center;font-size:12px'>"
                       f"🐙 章鱼 AI·全景分析 | {summary}</div>" + content)
        return send_pushplus(token or PUSHPLUS_TOKEN, title, content, template="html", topic=topic)

    # 无摘要版时推送完整 html
    n = len(html)
    if n > CONTENT_LIMIT_MEMBER:
        print(f"[PushPlus] 完整报告 {n:,} 字符超过会员上限 {CONTENT_LIMIT_MEMBER:,}，拒绝发送。")
        return {"code": 998, "msg": f"report too long: {n}", "skipped": True}
    injected = (f"<div style='background:#1a1a2e;color:#ffe066;padding:12px;border:3px solid #fff;"
                f"font-family:monospace;text-align:center'>🐙 章鱼 AI·全景分析 | {summary}</div>" + html) if summary else html
    return send_pushplus(token or PUSHPLUS_TOKEN, title, injected, template="html", topic=topic)


def send_test_message(token: str = None, topic: str = None) -> dict:
    """发送一条测试消息，快速验证 token / 实名 / 关注 / 一对多群组是否正常。"""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token = token or PUSHPLUS_TOKEN or os.getenv("PUSHPLUS_TOKEN", "")
    if not token:
        print("[PushPlus] 未提供 token。用法: python -m src.pushplus --test <token> [群组编码]")
        return {"code": 997, "msg": "no token", "skipped": True}
    group = resolve_topic(topic)
    audience = f"群组 {group}（一对多，群内订阅者都会收到）" if group else "仅发给你自己（未启用一对多）"
    content = (
        "<div style='font-family:sans-serif;padding:12px;border:3px solid #333;background:#fff'>"
        f"<div style='font-size:18px;font-weight:bold'>✅ PushPlus 链路测试成功</div>"
        f"<div style='margin-top:8px;font-size:13px'>时间：{now}</div>"
        f"<div style='margin-top:4px;font-size:13px'>接收范围：{audience}</div>"
        f"<div style='margin-top:8px;font-size:13px'>若您收到本条消息，说明 token / 实名 / 公众号关注均正常，"
        f"战报推送可正常送达。</div>"
        "</div>")
    return send_pushplus(token, f"🐙 测试消息 {now}", content, template="html", topic=group)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--test":
        # 第 3 个参数可选：一对多群组编码；传 "" / self 表示只发给自己
        res = send_test_message(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None)
        sys.exit(0 if res.get("code") == 200 else 1)
    print("用法：")
    print("  python -m src.pushplus --test <token> [群组编码]   # 发送一条测试消息验证链路")
    print("  群组编码留空则用 config.yaml 的 pushplus_topic（默认 oai.1，一对多）；传 self 只发给自己")
