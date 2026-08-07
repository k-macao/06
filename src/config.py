import os
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
KOL_DATA_PATH = ROOT / "kol_data.json"
OUTPUT_DIR = ROOT / "output"
TEMPLATE_DIR = ROOT / "templates"

# PushPlus 配置
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "")
PUSHPLUS_URL = "http://www.pushplus.plus/send"
# 也支持从 config.yaml 读取
CONFIG_YAML = ROOT / "config.yaml"

# 抓取配置
ACTIVE_THRESHOLD_DAYS = 90  # 90天内有更新视为活跃
REQUEST_TIMEOUT = 12
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 报告配置
REPORT_TITLE = "全球财经金融 KOL 精选名单 · 多空全景战报"
AUTHOR = "章鱼 AI·全景分析"
REPORT_DATE_FORMAT = "%Y年%m月%d日"

def load_kols():
    with open(KOL_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
