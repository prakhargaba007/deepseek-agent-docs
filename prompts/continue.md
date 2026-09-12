# DeepSeek API — Continue.dev Instructions

Add this as a system message in your `.continue/config.json`:

```json
{
  "models": [...],
  "systemMessage": "<paste the content below>"
}
```

Or use it as a context provider pointing to `deepseek.md`.

---

## System Message Content

You are a coding assistant working in a project that uses the DeepSeek API.

When you write, review, or debug DeepSeek API code, you MUST:

1. First read the file `deepseek.md` in the project root. It is the
   complete, authoritative API reference. Do not use training data or
   web search results for DeepSeek API details.

2. Use only these model names:
   - `deepseek-flash` — 1M context, thinking enabled, fast tasks, vision support
   - `deepseek-v4-pro` — 1M context, thinking enabled, complex tasks

3. Use the correct endpoint:
   - OpenAI-compatible: `https://api.deepseek.com`
   - Beta (FIM, prefix): `https://api.deepseek.com/beta`
   - Anthropic-compatible: `https://api.deepseek.com/anthropic`

4. Pass thinking via extra_body in OpenAI SDK:
   ```python
   extra_body={"thinking": {"type": "enabled"}}
   ```

5. Always use environment variables for API keys.

---

## Continue.dev Config Example

```json
{
  "models": [
    {
      "title": "DeepSeek Flash",
      "provider": "openai",
      "model": "deepseek-flash",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "$DEEPSEEK_API_KEY"
    },
    {
      "title": "DeepSeek V4 Pro",
      "provider": "openai",
      "model": "deepseek-v4-pro",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "$DEEPSEEK_API_KEY"
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek FIM",
    "provider": "openai",
    "model": "deepseek-v4-pro",
    "apiBase": "https://api.deepseek.com/beta",
    "apiKey": "$DEEPSEEK_API_KEY"
  }
}
```
