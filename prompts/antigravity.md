# DeepSeek API — Antigravity Instructions

Antigravity uses the **skill directory** system. This repository already ships with
a ready-made skill file (`SKILL.md`) that you can drop into your skill directories.

---

## Option 1: Global Skill (available in all projects)

```bash
# Create the skill directory
mkdir -p ~/.gemini/config/skills/deepseek-api

# Copy the skill files
cp SKILL.md ~/.gemini/config/skills/deepseek-api/SKILL.md
cp deepseek.md ~/.gemini/config/skills/deepseek-api/deepseek.md
```

Antigravity will automatically discover the skill and load `deepseek.md`
as context whenever you work on DeepSeek API code.

---

## Option 2: Project-Scoped Skill

```bash
# Create the skill directory inside your project
mkdir -p .agents/skills/deepseek-api

# Copy the skill files
cp SKILL.md .agents/skills/deepseek-api/SKILL.md
cp deepseek.md .agents/skills/deepseek-api/deepseek.md
```

---

## Option 3: System Prompt

If you prefer to pass context manually, use this as your system prompt:

```
You are working on a project that integrates with the DeepSeek API.

Before writing any DeepSeek API code, read the file `deepseek.md` in the
repository root. It is the authoritative reference. Do not use training data
or web searches for DeepSeek API model names, parameters, or behavior.

Key facts:
- Models: deepseek-v4-pro (complex tasks), deepseek-v4-flash (fast/cheap)
- Base URL: https://api.deepseek.com
- Beta features: https://api.deepseek.com/beta
- Anthropic format: https://api.deepseek.com/anthropic
- Thinking mode: pass via extra_body={"thinking": {"type": "enabled"}} (OpenAI SDK)
- Never use: deepseek-chat or deepseek-reasoner (deprecated 2026-07-24)
- Edge cases: see Section 17 of deepseek.md
```

---

## How the Skill File Works

The `SKILL.md` at the root of this repository is an Antigravity skill definition:

```yaml
---
name: deepseek-api
description: Reference guide for DeepSeek API integration, parameter specs,
             thinking mode, OpenAI/Anthropic SDK compatibility, FIM, tool calling,
             and code generation best practices.
---
```

Antigravity reads this frontmatter and automatically surfaces the skill when
your task involves DeepSeek API code. The body of `SKILL.md` provides a
quick reference summary, while `deepseek.md` (referenced inside it) provides
the full specification.

---

## Verifying It Works

Once the skill is installed, ask Antigravity:

```
What are the current DeepSeek model names and their pricing?
```

It should answer using the data in `deepseek.md` rather than its training data.
