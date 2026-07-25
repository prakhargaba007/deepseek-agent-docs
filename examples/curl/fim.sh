#!/usr/bin/env bash
# fim.sh — Fill-in-the-Middle (FIM) completion via cURL
#
# FIM requires the Beta endpoint: https://api.deepseek.com/beta
# Max output: 4K tokens. Non-thinking mode only.
#
# Usage:
#   export DEEPSEEK_API_KEY="sk-your-key"
#   chmod +x fim.sh && ./fim.sh

set -euo pipefail

: "${DEEPSEEK_API_KEY:?Error: DEEPSEEK_API_KEY is not set}"

echo "=== FIM Completion ==="
echo "Prefix: 'def fibonacci(n):\\n    '"
echo "Suffix: '\\n    return result'"
echo ""

curl -s https://api.deepseek.com/beta/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-v4-pro",
    "prompt": "def fibonacci(n):\n    ",
    "suffix": "\n    return result",
    "max_tokens": 256,
    "temperature": 0.2,
    "stream": false
  }' | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('Completion:')
print(data['choices'][0]['text'])
print()
print('Usage:', data.get('usage', {}))
"
