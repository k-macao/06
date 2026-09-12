#!/bin/bash
# PushPlus 推送演示脚本
# 用法：
#   bash push_demo.sh test [token] [群组编码]   # 发送一条测试消息，验证 token/实名/关注/一对多群组
#   bash push_demo.sh [token]                   # 完整流水线 + 推送战报（摘要版）
# 或设置环境变量 PUSHPLUS_TOKEN / PUSHPLUS_TOPIC
# 一对多：默认群组编码取 config.yaml 的 pushplus_topic（群名 oai.1）；
#         传 self 作为群组编码 = 只发给自己（关闭一对多）

TOKEN=${1:-$PUSHPLUS_TOKEN}
TOPIC=${PUSHPLUS_TOPIC:-}

if [ "$1" = "test" ]; then
  TOKEN=${2:-$PUSHPLUS_TOKEN}
  TOPIC=${3:-$PUSHPLUS_TOPIC}
  if [ -z "$TOKEN" ]; then
    echo "⚠️  未提供 Token：bash push_demo.sh test <你的token> [群组编码]"
    echo "获取方式：http://www.pushplus.plus/push1.html"
    exit 1
  fi
  echo "🐙 发送测试消息 Token: ${TOKEN:0:6}****** | 群组: ${TOPIC:-（config.yaml 默认 oai.1）} ..."
  if [ -n "$TOPIC" ]; then
    python3 -m src.pushplus --test "$TOKEN" "$TOPIC"
  else
    python3 -m src.pushplus --test "$TOKEN"
  fi
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

echo "🐙 使用 Token: ${TOKEN:0:6}****** 推送中 | 群组: ${TOPIC:-（config.yaml 默认 oai.1）} ..."
if [ -n "$TOPIC" ]; then
  PUSHPLUS_TOKEN=$TOKEN python main.py --topic "$TOPIC"
else
  PUSHPLUS_TOKEN=$TOKEN python main.py
fi
