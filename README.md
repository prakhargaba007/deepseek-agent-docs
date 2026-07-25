<div align="center">

# 🤖 DeepSeek API — Agent-Optimized Documentation

**The definitive community-maintained Markdown reference for the DeepSeek API.**  
*Designed to be loaded by AI coding agents instead of crawling the web.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2026.07.25-green.svg)](VERSION)
[![Documentation](https://img.shields.io/badge/deepseek.md-2%2C348%20lines-orange.svg)](deepseek.md)
[![Last Updated](https://img.shields.io/badge/last%20updated-July%202026-lightgrey.svg)](CHANGELOG.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/deepseek-api-docs?style=social)](https://github.com/YOUR_USERNAME/deepseek-api-docs)

[📄 View Documentation](deepseek.md) · [🚀 Quick Start](#-quick-start) · [🤖 AI Agent Usage](#-ai-agent-usage) · [💡 Examples](examples/) · [🤝 Contributing](CONTRIBUTING.md)

</div>

---

## 🎯 Why This Exists

When you're building with the DeepSeek API, your AI coding agent has two options:

| Without This Repo | With This Repo |
|---|---|
| ❌ Crawls the web (slow, unreliable) | ✅ Reads a local file (instant) |
| ❌ Relies on stale training data | ✅ Gets current, accurate API specs |
| ❌ Misses edge cases and gotchas | ✅ Includes hidden details & edge cases |
| ❌ Wrong model names, deprecated params | ✅ Up-to-date model names & pricing |
| ❌ Inconsistent code examples | ✅ Runnable, tested examples |

Just drop [`deepseek.md`](deepseek.md) into your project (or point your agent to it), and your agent will use it as its authoritative source for the DeepSeek API — no web searches required.

---

## ✨ Features

- 📄 **Single File** — The entire DeepSeek API in one Markdown file (`deepseek.md`, ~75 KB)
- 🧠 **Thinking Mode Coverage** — Full docs for `reasoning_effort`, chain-of-thought, multi-turn behavior
- 🔄 **OpenAI + Anthropic Compatibility** — Exact migration steps for both SDKs
- ⚡ **All Endpoints** — Chat Completions, FIM (Beta), List Models, User Balance
- 🛠️ **Tool Calling** — Standard and strict mode with JSON Schema examples
- 💾 **Context Caching** — How it works, when cache hits/misses occur, cost impact
- 🤖 **Agent Integrations** — Claude Code, GitHub Copilot, OpenCode configuration
- 🎯 **Production-Ready** — Rate limits, error handling, retry strategies, best practices
- 🧩 **17 Code Examples** — Python, JavaScript, TypeScript, cURL, Anthropic SDK
- 💬 **7 Agent Prompts** — Ready-to-use prompts for Cursor, Claude Code, Codex CLI, and more
- 🔍 **Hidden Details** — Edge cases, undocumented caveats, compatibility quirks

---

## 📋 Table of Contents

- [Why This Exists](#-why-this-exists)
- [Features](#-features)
- [Supported Models](#-supported-models)
- [Supported APIs](#-supported-apis)
- [Quick Start](#-quick-start)
- [AI Agent Usage](#-ai-agent-usage)
- [Repository Structure](#-repository-structure)
- [Example Prompts](#-example-prompts)
- [Examples Overview](#-examples-overview)
- [Updating the Documentation](#-updating-the-documentation)
- [Versioning](#-versioning)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)
- [Disclaimer](#-disclaimer)

---

## 🤖 Supported Models

| Model | Context | Max Output | Thinking | Tools | Best For |
|---|---|---|---|---|---|
| `deepseek-v4-pro` | 1M tokens | 384K tokens | ✅ Default on | ✅ | Complex reasoning, coding, agent tasks |
| `deepseek-v4-flash` | 1M tokens | 384K tokens | ✅ Default on | ✅ | Fast responses, cost-sensitive apps |

> **Deprecated names** (removed 2026-07-24): `deepseek-chat` → `deepseek-v4-flash`, `deepseek-reasoner` → `deepseek-v4-flash` (thinking mode)

---

## 🔌 Supported APIs

| Endpoint | Method | Description |
|---|---|---|
| `/chat/completions` | `POST` | Primary chat/reasoning endpoint |
| `/completions` (Beta) | `POST` | FIM (Fill-in-the-Middle) for code completion |
| `/models` | `GET` | List available models |
| `/user/balance` | `GET` | Check account balance |

**Compatibility:**
- ✅ OpenAI SDK (Python + Node.js) — drop-in with `base_url` swap
- ✅ Anthropic SDK (Python) — with `base_url` and model name mapping
- ✅ Claude Code, OpenCode, GitHub Copilot agent integrations

---

## 🚀 Quick Start

**Install the OpenAI SDK:**
```bash
pip install openai       # Python
npm install openai       # Node.js / TypeScript
```

**Set your API key:**
```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
```

**Your first call:**
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

For more examples, see the [`examples/`](examples/) folder.

---

## 🤖 AI Agent Usage

### Option 1: Copy `deepseek.md` into your project

The simplest and most reliable approach. Copy the file anywhere in your codebase:

```bash
# Into your docs folder
cp deepseek.md ./docs/deepseek.md

# Or into your agent skills directory
cp deepseek.md .agents/skills/deepseek/deepseek.md
```

Then tell your agent to reference it:
> "When writing code that calls the DeepSeek API, always refer to `docs/deepseek.md` as your source of truth."

---

### Option 2: Use as an Agent Skill

Copy `SKILL.md` into your agent's skill directory. Compatible with Antigravity, Cursor, OpenHands, and any agent that supports skill directories.

```bash
# Antigravity / Cursor global skills
cp SKILL.md ~/.gemini/config/skills/deepseek/SKILL.md
cp deepseek.md ~/.gemini/config/skills/deepseek/deepseek.md

# Project-scoped skills
mkdir -p .agents/skills/deepseek
cp SKILL.md .agents/skills/deepseek/SKILL.md
cp deepseek.md .agents/skills/deepseek/deepseek.md
```

---

### Option 3: Cursor Rules

Add to your `.cursor/rules/deepseek.mdc` or `.cursorrules`:

```markdown
When writing or reviewing code that integrates with the DeepSeek API,
ALWAYS refer to the file at `deepseek.md` in this repository as your
primary source of truth. Do NOT rely on your training data or web searches
for DeepSeek API specifications, model names, or parameter behavior.
```

---

### Option 4: Direct URL (Online Agents)

For agents that can fetch URLs or support `llms.txt`:

```
# Raw file URL
https://raw.githubusercontent.com/YOUR_USERNAME/deepseek-api-docs/main/deepseek.md

# llms.txt entry point
https://YOUR_USERNAME.github.io/deepseek-api-docs/llms.txt
```

---

### Option 5: Tool-Specific Prompts

Ready-to-use agent prompts are in the [`prompts/`](prompts/) folder:

| Tool | Prompt File |
|---|---|
| Cursor | [prompts/cursor.md](prompts/cursor.md) |
| Claude Code | [prompts/claude_code.md](prompts/claude_code.md) |
| Codex CLI | [prompts/codex_cli.md](prompts/codex_cli.md) |
| OpenHands | [prompts/openhands.md](prompts/openhands.md) |
| Roo Code | [prompts/roo_code.md](prompts/roo_code.md) |
| Continue | [prompts/continue.md](prompts/continue.md) |
| Generic Agent | [prompts/generic_agent.md](prompts/generic_agent.md) |

---

## 📂 Repository Structure

```text
deepseek-api-docs/
│
├── deepseek.md              # 📄 The main documentation (2,348 lines)
├── README.md                # This file
├── SKILL.md                 # Agent skill definition
├── llms.txt                 # Standard llms.txt entry point
├── CONTRIBUTING.md          # Contributor guide
├── CHANGELOG.md             # Version history
├── SECURITY.md              # Security policy
├── VERSION                  # Current version (CalVer: YYYY.MM.DD)
├── LICENSE                  # MIT License
│
├── examples/                # 💡 Runnable code examples
│   ├── README.md
│   ├── python/              # Python + OpenAI SDK examples
│   ├── javascript/          # Node.js examples
│   ├── typescript/          # TypeScript examples
│   ├── curl/                # cURL shell examples
│   └── anthropic_sdk/       # Anthropic SDK examples
│
├── prompts/                 # 💬 Ready-to-use AI agent prompts
│   ├── README.md
│   ├── cursor.md
│   ├── claude_code.md
│   ├── codex_cli.md
│   ├── openhands.md
│   ├── roo_code.md
│   ├── continue.md
│   └── generic_agent.md
│
├── scripts/                 # 🔧 Maintenance scripts
│   ├── README.md
│   ├── validate_links.py    # Check all HTTP links in deepseek.md
│   ├── check_formatting.py  # Validate markdown structure
│   └── generate_toc.py      # Auto-generate table of contents
│
└── .github/                 # ⚙️ GitHub configuration
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   └── feature_request.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        ├── markdown_lint.yml
        └── link_check.yml
```

---

## 💬 Example Prompts

### For Cursor (`.cursorrules`)

```
When writing or debugging code that calls the DeepSeek API:
1. Open and read deepseek.md first.
2. Use ONLY the model names, endpoints, and parameter names documented there.
3. Do NOT guess at parameter behavior — check the Parameters Reference section.
4. For thinking mode, always pass thinking via extra_body when using the OpenAI SDK.
```

### For Claude Code

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=sk-your-key
export ANTHROPIC_MODEL=deepseek-v4-pro
```

Then in your project's `CLAUDE.md`:
```
For all DeepSeek API code, read deepseek.md before writing any implementation.
```

See the full [`prompts/`](prompts/) directory for tool-specific instructions.

---

## 🗂️ Examples Overview

| File | Language | What It Demonstrates |
|---|---|---|
| [`python/basic_chat.py`](examples/python/basic_chat.py) | Python | Basic chat completion |
| [`python/streaming.py`](examples/python/streaming.py) | Python | Streaming with usage stats |
| [`python/thinking_mode.py`](examples/python/thinking_mode.py) | Python | Thinking mode + multi-turn |
| [`python/tool_calling.py`](examples/python/tool_calling.py) | Python | Full tool call loop |
| [`python/json_output.py`](examples/python/json_output.py) | Python | Structured JSON extraction |
| [`python/fim_completion.py`](examples/python/fim_completion.py) | Python | Fill-in-the-Middle (Beta) |
| [`python/multi_turn.py`](examples/python/multi_turn.py) | Python | Multi-turn conversation |
| [`javascript/basic_chat.js`](examples/javascript/basic_chat.js) | JavaScript | Basic chat (ESM) |
| [`javascript/streaming.js`](examples/javascript/streaming.js) | JavaScript | Streaming |
| [`javascript/tool_calling.js`](examples/javascript/tool_calling.js) | JavaScript | Tool calling |
| [`typescript/basic_chat.ts`](examples/typescript/basic_chat.ts) | TypeScript | Typed chat completion |
| [`typescript/reasoning_with_retry.ts`](examples/typescript/reasoning_with_retry.ts) | TypeScript | Thinking mode + retry logic |
| [`curl/basic_chat.sh`](examples/curl/basic_chat.sh) | cURL | Minimal API call |
| [`curl/streaming.sh`](examples/curl/streaming.sh) | cURL | SSE streaming |
| [`curl/fim.sh`](examples/curl/fim.sh) | cURL | FIM completion |
| [`anthropic_sdk/basic_chat.py`](examples/anthropic_sdk/basic_chat.py) | Python | Anthropic SDK with DeepSeek |
| [`anthropic_sdk/claude_code_setup.sh`](examples/anthropic_sdk/claude_code_setup.sh) | Bash | Claude Code env setup |

---

## 🔄 Updating the Documentation

When DeepSeek releases new API features or model updates:

1. Check [api-docs.deepseek.com](https://api-docs.deepseek.com) for changes.
2. Update `deepseek.md` with the new information.
3. Update the version header in `deepseek.md` and the `VERSION` file.
4. Add a `CHANGELOG.md` entry.
5. Open a PR — see [CONTRIBUTING.md](CONTRIBUTING.md) for the full process.

Run the validation scripts to check your changes:

```bash
python scripts/validate_links.py
python scripts/check_formatting.py
```

---

## 📌 Versioning

This project uses **Calendar Versioning** (`YYYY.MM.DD`):

```
2026.07.25   ← Date the documentation was last synchronized
```

CalVer is chosen over SemVer because the version number communicates the most important piece of information for a documentation repository: **when it was last updated**. This helps developers quickly assess staleness.

Git tags follow the pattern `v2026.07.25`.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Found incorrect info?** → [Open a Bug Report](../../issues/new?template=bug_report.yml)
2. **Want to add an example?** → [Open a Feature Request](../../issues/new?template=feature_request.yml)
3. **Ready to contribute?** → Read [CONTRIBUTING.md](CONTRIBUTING.md)

**Great first issues** are tagged with [`good first issue`](../../labels/good%20first%20issue).

### GitHub Topics

This repository is tagged with:
`deepseek` · `deepseek-api` · `llm` · `ai-agent` · `markdown` · `documentation` · `openai-compatible` · `anthropic-compatible` · `cursor` · `claude-code` · `codex` · `openhands` · `continue` · `roo-code` · `llms-txt`

---

## 📜 License

Distributed under the [MIT License](LICENSE). You are free to use, modify, and distribute this documentation in any project, including commercial ones.

---

## 🙏 Credits

- **Documentation source**: [api-docs.deepseek.com](https://api-docs.deepseek.com) (official DeepSeek API documentation)
- **Maintainer**: [Prakhar](https://github.com/YOUR_USERNAME)
- **Contributors**: See [Contributors](../../graphs/contributors)

---

## ⚠️ Disclaimer

> **This is an unofficial, community-maintained resource.**
>
> The official DeepSeek API documentation at [api-docs.deepseek.com](https://api-docs.deepseek.com) is always the authoritative source of truth. This repository aims to mirror it accurately, but there may be a lag between official updates and updates here.
>
> Always verify critical API behavior against the official documentation before deploying to production.
>
> This project is not affiliated with, endorsed by, or sponsored by DeepSeek.

---

<div align="center">

**⭐ If this saved you time, please star the repository! ⭐**

[Report Issue](../../issues/new?template=bug_report.yml) · [Request Feature](../../issues/new?template=feature_request.yml) · [View Documentation](deepseek.md)

</div>
