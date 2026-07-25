# DeepSeek API — Claude Code Instructions

Place this content in your `CLAUDE.md` file at the project root.

---

## DeepSeek API

This project integrates with the DeepSeek API. When writing or modifying
any code that calls the DeepSeek API:

**Always read `deepseek.md` before writing any implementation.**

The file `deepseek.md` in this repository contains the complete, current
API reference including:
- All model names and their capabilities
- All endpoint URLs and HTTP methods  
- All request/response parameters with types and defaults
- Thinking mode behavior and `reasoning_content` handling
- Tool calling, streaming, JSON output, FIM, context caching
- Error codes and retry strategies
- OpenAI and Anthropic SDK compatibility details
- Hidden details and edge cases (Section 17)

### Quick Reference

```bash
# Environment setup
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<deepseek-api-key>
export ANTHROPIC_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

### Rules

- **DO** use `deepseek-v4-pro` and `deepseek-v4-flash` as model names
- **DO NOT** use `deepseek-chat` or `deepseek-reasoner` (deprecated)
- **DO NOT** hardcode API keys
- When using thinking mode with OpenAI SDK, always pass via `extra_body`
- For beta features (FIM, prefix completion), use `base_url="https://api.deepseek.com/beta"`
