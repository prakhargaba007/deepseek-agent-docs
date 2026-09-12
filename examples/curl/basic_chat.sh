#!/usr/bin/env bash
# basic_chat.sh — Minimal DeepSeek API call with cURL
#
# Usage:
#   export DEEPSEEK_API_KEY="sk-your-key"
#   chmod +x basic_chat.sh && ./basic_chat.sh

set -euo pipefail

: "${DEEPSEEK_API_KEY:?Error: DEEPSEEK_API_KEY is not set}"

curl -s https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user",   "content": "What is 2 + 2?"}
    ],
    "max_tokens": 128,
    "stream": false
  }' | python3 -m json.tool
