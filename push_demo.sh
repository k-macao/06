#!/bin/bash
# PushPlus 推送演示脚本
# 用法：PUSHPLUS_TOKEN=xxx bash push_demo.sh
# 或：bash push_demo.sh your_token_here

TOKEN=${1:-$PUSHPLUS_TOKEN}

if [ -z "$TOKEN" ]; then
  echo "⚠️  未提供 PushPlus Token"
  echo "获取方式：http://www.pushplus.plus/push1.html"
  echo "用法：PUSHPLUS_TOKEN=xxx python main.py"
  echo "或：python main.py --token xxx"
  echo ""
  echo "当前演示：仅本地生成，不推送"
  python main.py --no-push
  exit 0
fi

echo "🐙 使用 Token: ${TOKEN:0:6}****** 推送中..."
PUSHPLUS_TOKEN=$TOKEN python main.py
