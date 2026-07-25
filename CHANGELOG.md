# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (`YYYY.MM.DD`).

---

## [Unreleased]

### Added
- Nothing yet.

### Changed
- Nothing yet.

### Deprecated
- Nothing yet.

### Removed
- Nothing yet.

### Fixed
- Nothing yet.

---

## [2026.07.25] — 2026-07-25

### Added
- Initial public release of the DeepSeek API Agent-Optimized Markdown Documentation.
- `deepseek.md` — Complete 2,348-line single-file reference for the DeepSeek API (v2026.07.25).
- `README.md` — Professional README with badges, ToC, usage guide, and AI agent integration instructions.
- `CONTRIBUTING.md` — Full contributor guide with PR process, commit conventions, and documentation style.
- `CHANGELOG.md` — This file, following Keep a Changelog format.
- `SECURITY.md` — Security policy and responsible disclosure process.
- `VERSION` — CalVer version file (`2026.07.25`).
- `SKILL.md` — Agent skill file for Antigravity / Cursor / OpenHands skill directories.
- `llms.txt` — Standard `llms.txt` agent entry point.
- `examples/` — 17 runnable code examples across Python, JavaScript, TypeScript, cURL, and Anthropic SDK.
- `prompts/` — 7 AI agent prompt files for Cursor, Claude Code, Codex CLI, OpenHands, Roo Code, Continue, and generic agents.
- `scripts/` — 3 Python maintenance scripts: `validate_links.py`, `check_formatting.py`, `generate_toc.py`.
- `.github/ISSUE_TEMPLATE/bug_report.yml` — Structured bug report form.
- `.github/ISSUE_TEMPLATE/feature_request.yml` — Structured feature request form.
- `.github/PULL_REQUEST_TEMPLATE.md` — PR checklist template.
- `.github/workflows/markdown_lint.yml` — GitHub Actions workflow for Markdown linting.
- `.github/workflows/link_check.yml` — GitHub Actions workflow for weekly link validation.

### Documentation Coverage (deepseek.md v2026.07.25)
- Models: `deepseek-v4-pro`, `deepseek-v4-flash`
- Endpoints: Chat Completions, FIM Completion (Beta), List Models, Get User Balance
- Features: Thinking/Reasoning Mode, Multi-round Conversations, Streaming, Tool Calls, JSON Output, Context Caching, Chat Prefix Completion (Beta), FIM
- Compatibility: Full OpenAI SDK compatibility, Anthropic SDK compatibility
- Agent Integrations: Claude Code, GitHub Copilot, OpenCode
- Rate Limits, Error Codes, Token Usage, Best Practices, Production Examples

---

## Version History

| Version | Date | Summary |
|---|---|---|
| [2026.07.25] | 2026-07-25 | Initial public release |

---

[Unreleased]: https://github.com/prakhargaba007/deepseek-agent-docs/compare/v2026.07.25...HEAD
[2026.07.25]: https://github.com/prakhargaba007/deepseek-agent-docs/releases/tag/v2026.07.25
