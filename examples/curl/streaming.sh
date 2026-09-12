#!/usr/bin/env bash
# streaming.sh — DeepSeek streaming via cURL (Server-Sent Events)
#
# Tokens are printed to stdout as they arrive.
# The stream is terminated by "data: [DONE]".
#
# Usage:
#   export DEEPSEEK_API_KEY="sk-your-key"
#   chmod +x streaming.sh && ./streaming.sh

set -euo pipefail

: "${DEEPSEEK_API_KEY:?Error: DEEPSEEK_API_KEY is not set}"

echo "=== Streaming Response ==="

curl -sN https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {"role": "user", "content": "Count from 1 to 10 slowly."}
    ],
    "stream": true,
    "stream_options": {"include_usage": true},
    "max_tokens": 256
  }' | while IFS= read -r line; do
    # Skip empty lines and the [DONE] sentinel
    [[ -z "$line" || "$line" == "data: [DONE]" ]] && continue

    # Strip the "data: " prefix and extract the content delta
    json="${line#data: }"

    # Use python to extract delta.content (if present)
    python3 -c "
import json, sys
try:
    obj = json.loads('$json'.replace(\"'\", \"'\"))
    choices = obj.get('choices', [])
    if choices:
        delta = choices[0].get('delta', {})
        content = delta.get('content', '')
        if content:
            print(content, end='', flush=True)
    usage = obj.get('usage')
    if usage:
        print(f'\n\n[Usage] {usage}')
except:
    pass
" 2>/dev/null
done

echo
