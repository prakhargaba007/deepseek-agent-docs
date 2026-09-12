# DeepSeek API — Codex CLI Instructions

Pass this as your `--instructions` flag or system prompt when running Codex CLI.

---

You are working in a project that integrates with the DeepSeek API.

Before writing any code that calls the DeepSeek API:

1. Read the file `deepseek.md` in the current repository. It is the
   authoritative reference for the DeepSeek API. Do NOT use your training
   data or perform web searches for DeepSeek API information.

2. Always use the current model names:
   - `deepseek-flash` — primary model (DeepSeek-V4.1-Flash) for fast responses, coding, vision, and agent workflows
   - `deepseek-v4-pro` — for complex reasoning and deep STEM proofs

3. Use the correct base URL / endpoint:
   - OpenAI Chat Completions & Responses API: `https://api.deepseek.com` (use `POST /responses` for Codex-style agents)
   - Beta features: `https://api.deepseek.com/beta`
   - Anthropic-compatible: `https://api.deepseek.com/anthropic`

4. When using the OpenAI SDK, pass `thinking` via `extra_body`:
   ```python
   extra_body={"thinking": {"type": "enabled"}}
   ```

5. Always store API keys in environment variables (`DEEPSEEK_API_KEY`).

6. For error handling: implement exponential backoff for 429, 500, 503.

7. Refer to Section 17 of `deepseek.md` for undocumented edge cases
   before assuming default behavior.
