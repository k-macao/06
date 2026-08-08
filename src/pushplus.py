"""
PushPlus 推送模块
文档：http://www.pushplus.plus/doc/
支持：单人推送、一对多、html 模板

常见问题速查：
- 2024-08 起未实名认证的用户无法发送（返回 905），请在 pushplus.plus 完成实名。
- 内容长度上限：实名用户 2 万字 / 会员 10 万字（超长会推送失败或被截断）。
- 相同内容 1 小时内最多 3 条；1 分钟最多 5 次请求。
- 接口是异步的：返回 200 只代表收到请求，实际送达以微信收到为准。
- 必须用微信关注 PushPlus 公众号，推送经公众号模板消息送达。
"""
import os
import requests
from .config import PUSHPLUS_URL, PUSHPLUS_TOKEN

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


def send_pushplus(token: str, title: str, content: str, template: str = "html",
                  channel: str = "wechat") -> dict:
    """
    发送 PushPlus
    - token: 你的 PushPlus token
    - title: 推送标题
    - content: html 或 markdown 内容
    - template: html / markdown / json
    - channel: wechat / webhook / cp / mail
    返回接口 JSON 字典。
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

    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
        "channel": channel,
    }
    print(f"[PushPlus] 发送中... title={title!r} content={n:,} 字符")
    try:
        resp = requests.post(PUSHPLUS_URL, json=data, timeout=15)
        j = resp.json()
        code = j.get("code")
        if code == 200:
            print(f"[PushPlus] ✅ 推送成功: {title}（异步送达，请查收微信）")
        else:
            print(f"[PushPlus] ❌ 推送失败 code={code}: {explain_code(code)} | 原始返回: {j}")
        return j
    except Exception as ex:
        print(f"[PushPlus] 网络异常: {ex}")
        return {"code": 500, "msg": str(ex)}


def send_report(html_path: str, title: str, token: str = None, summary: str = "",
                digest_html: str = None, full_link: str = "") -> dict:
    """
    读取本地 html 报告并推送。
    - 若提供 digest_html（精简摘要版），直接推送摘要版（推荐，微信友好且不超限）
    - 否则推送完整 html；若完整 html 超过会员上限则拒绝并给出提示
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
        return send_pushplus(token or PUSHPLUS_TOKEN, title, content, template="html")

    # 无摘要版时推送完整 html
    n = len(html)
    if n > CONTENT_LIMIT_MEMBER:
        print(f"[PushPlus] 完整报告 {n:,} 字符超过会员上限 {CONTENT_LIMIT_MEMBER:,}，拒绝发送。")
        return {"code": 998, "msg": f"report too long: {n}", "skipped": True}
    injected = (f"<div style='background:#1a1a2e;color:#ffe066;padding:12px;border:3px solid #fff;"
                f"font-family:monospace;text-align:center'>🐙 章鱼 AI·全景分析 | {summary}</div>" + html) if summary else html
    return send_pushplus(token or PUSHPLUS_TOKEN, title, injected, template="html")


def send_test_message(token: str = None) -> dict:
    """发送一条测试消息，快速验证 token / 实名 / 关注是否正常。"""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token = token or PUSHPLUS_TOKEN or os.getenv("PUSHPLUS_TOKEN", "")
    if not token:
        print("[PushPlus] 未提供 token。用法: python -m src.pushplus --test <token>")
        return {"code": 997, "msg": "no token", "skipped": True}
    content = (
        "<div style='font-family:sans-serif;padding:12px;border:3px solid #333;background:#fff'>"
        f"<div style='font-size:18px;font-weight:bold'>✅ PushPlus 链路测试成功</div>"
        f"<div style='margin-top:8px;font-size:13px'>时间：{now}</div>"
        f"<div style='font-size:13px'>若您收到本条消息，说明 token / 实名 / 公众号关注均正常，"
        f"战报推送可正常送达。</div>"
        "</div>")
    return send_pushplus(token, f"🐙 测试消息 {now}", content, template="html")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--test":
        res = send_test_message(sys.argv[2])
        sys.exit(0 if res.get("code") == 200 else 1)
    print("用法：")
    print("  python -m src.pushplus --test <token>   # 发送一条测试消息验证链路")
