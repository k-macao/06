"""
PushPlus 推送模块
文档：http://www.pushplus.plus/doc/
支持：单人推送、一对多、html 模板
"""
import os
import requests
from .config import PUSHPLUS_URL, PUSHPLUS_TOKEN

def send_pushplus(token: str, title: str, content: str, template: str = "html", channel: str = "wechat"):
    """
    发送 PushPlus
    - token: 你的 PushPlus token
    - title: 推送标题
    - content: html 或 markdown 内容
    - template: html / markdown / json
    - channel: wechat / webhook / cp / mail
    """
    token = token or PUSHPLUS_TOKEN or os.getenv("PUSHPLUS_TOKEN", "")
    if not token:
        print("[PushPlus] 未配置 token，跳过推送。请设置环境变量 PUSHPLUS_TOKEN 或在 config.yaml 中配置。")
        return {"code": 999, "msg": "no token", "skipped": True}

    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
        "channel": channel
    }
    try:
        resp = requests.post(PUSHPLUS_URL, json=data, timeout=12)
        j = resp.json()
        if j.get("code") == 200:
            print(f"[PushPlus] 推送成功: {title}")
        else:
            print(f"[PushPlus] 推送返回: {j}")
        return j
    except Exception as ex:
        print(f"[PushPlus] 异常: {ex}")
        return {"code": 500, "msg": str(ex)}

def send_report(html_path: str, title: str, token: str = None, summary: str = ""):
    """读取本地 html 报告并推送（PushPlus 对 content 长度有限制，超长会截断，建议同时提供链接）"""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        # PushPlus html 模式直接渲染 html
        # 为避免超长，先尝试直接推送；若失败降级为摘要+链接
        # 这里增加一个顶部摘要
        injected = f"<div style='background:#1a1a2e;color:#ffe066;padding:12px;border:3px solid #fff;font-family:monospace;text-align:center'>🐙 章鱼 AI·全景分析 | {summary}</div>" + html if summary else html
        return send_pushplus(token or PUSHPLUS_TOKEN, title, injected, template="html")
    except Exception as ex:
        print(f"[PushPlus] send_report error: {ex}")
        return {"code": 500, "msg": str(ex)}
