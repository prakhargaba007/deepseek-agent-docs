# Agent Prompts

Ready-to-use prompts for popular AI coding agents. These prompts instruct the agent to use `deepseek.md` as its authoritative source for the DeepSeek API, instead of web searches or training data.

## How to Use

1. Find the prompt file for your tool.
2. Copy its contents into the appropriate location for your tool.
3. Make sure `deepseek.md` is accessible from your project root.

## Prompt Files

| File | Tool | Where to Place |
|---|---|---|
| [`antigravity.md`](antigravity.md) | Antigravity | Copy `SKILL.md` + `deepseek.md` to `~/.gemini/config/skills/deepseek-api/` |
| [`cursor.md`](cursor.md) | Cursor | `.cursor/rules/deepseek.mdc` or `.cursorrules` |
| [`claude_code.md`](claude_code.md) | Claude Code | `CLAUDE.md` in your project root |
| [`codex_cli.md`](codex_cli.md) | Codex CLI | Pass as `--instructions` or system prompt |
| [`openhands.md`](openhands.md) | OpenHands | Microagent instructions |
| [`roo_code.md`](roo_code.md) | Roo Code | `.roo/rules/deepseek.md` |
| [`continue.md`](continue.md) | Continue | `.continue/config.json` system message |
| [`generic_agent.md`](generic_agent.md) | Any agent | Copy into system prompt |
