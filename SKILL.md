---
name: deepseek-api
description: Reference guide for DeepSeek API integration, parameter specs, thinking mode, OpenAI/Anthropic SDK compatibility, FIM, tool calling, and code generation best practices.
---

# DeepSeek API Developer Skill

This skill provides comprehensive reference context for integrating DeepSeek models into codebases.

## Primary Documentation

For full API schema, endpoints, rate limits, SDK code examples, and edge cases, see [deepseek.md](deepseek.md).

## Quick Reference Summary

### Base URLs
- OpenAI Chat Completions: `https://api.deepseek.com`
- OpenAI Responses API: `https://api.deepseek.com` (`POST /responses`)
- Anthropic Compatible: `https://api.deepseek.com/anthropic`
- Beta Features (FIM, prefix): `https://api.deepseek.com/beta`

### Current Models (as of 2026.09.12)
- `deepseek-flash` (GA) — 1M context, 384K max output, 552B MoE asymmetric Causal Encoder-Decoder, native multimodal vision (JPEG, PNG, GIF, WebP), 2500 concurrency
- `deepseek-v4-pro` (GA) — 1M context, 384K max output, 1.6T MoE, frontier reasoning & complex code synthesis, 500 concurrency

> **Note**: Legacy models `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` were retired on 2026-09-10 and automatically route to `deepseek-flash`. Legacy names `deepseek-chat` and `deepseek-reasoner` were retired on 2026-07-24.

### Thinking Mode
- Default: **enabled** across V4 models
- Disable: `{"thinking": {"type": "disabled"}}`
- Effort levels: `"low"`, `"high"` (default), or `"max"` (agent/complex tasks)
- OpenAI SDK: pass via `extra_body={"thinking": {"type": "enabled"}}`
- In thinking mode, `top_p` lower bound is clamped to `0.95`. In non-thinking mode, `top_p` is fixed at `1.0`.

### Python (OpenAI SDK Compatible)
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "Hello"}],
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)
print(response.choices[0].message.content)
```

### Key Edge Cases (See Section 17 of deepseek.md)
- `reasoning_content` must be preserved in multi-turn context ONLY when tool calls occurred
- Multimodal images allowed only in `user`, `developer`, or tool output roles (capped at 1,024 tokens/img)
- Files API (`POST /files`) provides free image upload and referencing via `file_id:...`
- Beta features (FIM, prefix completion) require `base_url="https://api.deepseek.com/beta"`
- Any unknown Anthropic model name maps to `deepseek-flash`, not Pro
- Cache hits require EXACT prefix match — partial overlaps do not count
- Peak hours (01:00-04:00 & 06:00-10:00 UTC Mon-Fri) vs 50% discount during off-peak hours
- Server sends empty HTTP keep-alive lines during extended thinking to prevent gateway timeouts
