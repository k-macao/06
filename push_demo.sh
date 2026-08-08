#!/bin/bash
# PushPlus 推送演示脚本
# 用法：
#   bash push_demo.sh test [token]        # 发送一条测试消息，快速验证 token/实名/关注
#   bash push_demo.sh [token]             # 完整流水线 + 推送战报（摘要版）
# 或设置环境变量 PUSHPLUS_TOKEN

TOKEN=${1:-$PUSHPLUS_TOKEN}

if [ "$1" = "test" ]; then
  TOKEN=${2:-$PUSHPLUS_TOKEN}
  if [ -z "$TOKEN" ]; then
    echo "⚠️  未提供 Token：bash push_demo.sh test <你的token>"
    echo "获取方式：http://www.pushplus.plus/push1.html"
    exit 1
  fi
  echo "🐙 发送测试消息 Token: ${TOKEN:0:6}****** ..."
  python3 -m src.pushplus --test "$TOKEN"
  exit $?
fi

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
