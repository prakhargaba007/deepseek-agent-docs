# DeepSeek API — Cursor Rules

Place this file at `.cursor/rules/deepseek.mdc` in your project root,
or append it to your `.cursorrules` file.

---

## DeepSeek API Reference

When writing, reviewing, or debugging any code that integrates with the
DeepSeek API, you MUST follow these rules:

1. **Read `deepseek.md` first.** Before writing any DeepSeek API code,
   open and read the file `deepseek.md` in this repository. It is the
   authoritative reference for all model names, endpoints, parameters,
   and behavior.

2. **Use current model names.** The correct model IDs are:
   - `deepseek-flash` — primary model (DeepSeek-V4.1-Flash) for fast responses, coding, vision, and high concurrency (2500)
   - `deepseek-v4-pro` — for deep reasoning, STEM proofs, and complex agent tasks (500 concurrency)
   Do NOT use retired models (`deepseek-v4-flash`, `deepseek-v4-flash-vision-exp`, `deepseek-chat`, `deepseek-reasoner`).

3. **Use the correct base URL.**
   - Standard: `https://api.deepseek.com`
   - Beta features (FIM, prefix completion): `https://api.deepseek.com/beta`
   - Anthropic format: `https://api.deepseek.com/anthropic`

4. **Thinking mode requires `extra_body`.** When using the OpenAI SDK,
   the `thinking` parameter must be passed via `extra_body`:
   ```python
   extra_body={"thinking": {"type": "enabled"}}
   ```

5. **Never hardcode API keys.** Always use environment variables:
   ```python
   api_key=os.environ.get("DEEPSEEK_API_KEY")
   ```

6. **Do NOT guess at parameter behavior.** If you are unsure about a
   parameter, look it up in Section 5 (Parameters Reference) of `deepseek.md`.

7. **Check edge cases in Section 17.** The "Hidden Details & Edge Cases"
   section documents undocumented caveats and compatibility quirks.
