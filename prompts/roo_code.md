# DeepSeek API — Roo Code Instructions

Place this file at `.roo/rules/deepseek.md` in your project root.
Roo Code will automatically load it as a context rule.

---

## DeepSeek API Context Rule

**Priority**: HIGH  
**Scope**: Any file containing DeepSeek API calls

### Rule

When you encounter or are asked to write code that calls the DeepSeek API:

1. **Source of truth**: Read `deepseek.md` in the repository root before
   making any assumptions about the API. Your training data may contain
   outdated DeepSeek API information.

2. **Model names** (always verify against deepseek.md):
   - `deepseek-flash` — fast, cost-effective tasks, vision support, 2500 concurrency limit
   - `deepseek-v4-pro` — complex tasks, deep reasoning, STEM/code proofs, 500 concurrency limit
   - ❌ Do NOT use retired models: `deepseek-v4-flash`, `deepseek-v4-flash-vision-exp`, `deepseek-chat`, `deepseek-reasoner`

3. **OpenAI SDK thinking mode**: The `thinking` parameter is NOT a standard
   OpenAI parameter. Always pass it via `extra_body`:
   ```python
   extra_body={"thinking": {"type": "enabled"}}
   ```

4. **Beta endpoint**: Required for FIM and prefix completion features:
   ```python
   base_url="https://api.deepseek.com/beta"
   ```

5. **reasoning_content in multi-turn**:
   - Without tool calls: `reasoning_content` can be omitted from history
   - With tool calls: `reasoning_content` MUST be included in all subsequent turns

6. **Retry strategy**: Implement exponential backoff for 429, 500, 503 errors.

### Pattern Detection

Apply these rules when you see:
- `deepseek` in any import, URL, or string
- `base_url="https://api.deepseek.com"` in Python/JS/TS code
- `DEEPSEEK_API_KEY` environment variable references
- Model names starting with `deepseek-`
