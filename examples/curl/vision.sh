#!/usr/bin/env bash
# vision.sh — Multimodal image analysis using cURL and DeepSeek API
#
# Usage:
#   export DEEPSEEK_API_KEY="sk-..."
#   chmod +x examples/curl/vision.sh
#   ./examples/curl/vision.sh

set -euo pipefail

if [[ -z "${DEEPSEEK_API_KEY:-}" ]]; then
  echo "Error: DEEPSEEK_API_KEY environment variable is not set." >&2
  exit 1
fi

echo "=== Analyzing Image via cURL ==="

curl -s https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is depicted in this landscape photo?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/640px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ],
    "max_tokens": 500
  }' | (command -v jq >/dev/null && jq . || cat)
