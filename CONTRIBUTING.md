# Contributing to DeepSeek API Agent-Optimized Documentation

Thank you for your interest in contributing! This project aims to be **the** definitive community-maintained Markdown reference for the DeepSeek API — readable by both humans and AI agents.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Repository Setup](#repository-setup)
- [Ways to Contribute](#ways-to-contribute)
- [Documentation Style Guide](#documentation-style-guide)
- [Updating the Documentation](#updating-the-documentation)
- [Pull Request Process](#pull-request-process)
- [Commit Conventions](#commit-conventions)
- [Reporting Issues](#reporting-issues)
- [Recommended Labels](#recommended-labels)

---

## Code of Conduct

Be kind, respectful, and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) code of conduct. Violations may result in removal from the project.

---

## Repository Setup

No build step is required — this is a documentation-only repository.

```bash
# 1. Fork and clone the repository
git clone https://github.com/prakhargaba007/deepseek-agent-docs.git
cd deepseek-agent-docs

# 2. (Optional) Set up Python for running maintenance scripts
python3 -m venv .venv
source .venv/bin/activate
pip install requests markdown-it-py

# 3. Run the validation scripts before submitting a PR
python scripts/validate_links.py
python scripts/check_formatting.py
```

---

## Ways to Contribute

| Type | Description |
|---|---|
| 🐛 Bug fix | Fix incorrect API information, broken examples, or bad links |
| 📝 Documentation | Improve explanations, add missing examples, clarify edge cases |
| ✨ New feature | Add a new example file, agent prompt, or maintenance script |
| 🔄 Documentation update | Sync `deepseek.md` with the latest official DeepSeek API docs |
| 🌐 Translation | Add translated versions (e.g., `deepseek.zh.md`) |

---

## Documentation Style Guide

### Markdown Formatting

- Use **ATX-style headings** (`#`, `##`, `###`) — no underline-style headings.
- Use a **single blank line** between sections.
- Use **fenced code blocks** with a language identifier: ` ```python `, ` ```bash `, ` ```json `.
- Tables should have aligned columns (use `|---|---| ` separators).
- Use **bold** for UI elements, parameter names, and key terms.
- Use `code` (backticks) for all file paths, command names, and API parameters.
- Avoid HTML tags in Markdown except when absolutely necessary.

### Writing Style

- Write in **plain English**. Avoid jargon.
- Use the **active voice**: "The model returns..." not "A response is returned by...".
- Keep sentences short (≤ 25 words when possible).
- Use **present tense**: "This parameter controls..." not "This parameter will control...".
- Always include a practical example after explaining a concept.
- Preserve **all technical accuracy** — never paraphrase API behavior without verifying against the official docs.

### Code Examples

- All code examples must be **runnable** (or clearly marked as pseudo-code).
- Use `os.environ.get("DEEPSEEK_API_KEY")` for API keys — never hardcode them.
- Add comments for non-obvious lines.
- Use the current model names: `deepseek-v4-pro` or `deepseek-v4-flash`.
- Include `import` statements and all necessary setup code.

---

## Updating the Documentation

The `deepseek.md` file is the heart of this project. To update it:

1. **Check the official docs** at [api-docs.deepseek.com](https://api-docs.deepseek.com).
2. **Identify changes**: new models, new parameters, deprecated features, pricing changes, etc.
3. **Update `deepseek.md`**: Make the minimal diff needed to reflect the change accurately.
4. **Update the version header** at the top of `deepseek.md`:
   ```markdown
   > Version: 1.0.0 | Last crawled: [Month Year]
   ```
5. **Update `VERSION`**: Change to the new `YYYY.MM.DD` date.
6. **Update `CHANGELOG.md`**: Add an entry under `[Unreleased]` describing what changed.
7. **Run validation scripts**:
   ```bash
   python scripts/validate_links.py
   python scripts/check_formatting.py
   ```

### Do NOT:
- Modify technical information without verifying against official docs.
- Remove sections even if you believe they are redundant.
- Reformat code examples unless there's a clear correctness issue.

---

## Pull Request Process

1. **Fork** the repository and create a branch:
   ```bash
   git checkout -b docs/update-tool-calling-examples
   ```

2. **Make your changes** following the style guide above.

3. **Run the validation scripts**:
   ```bash
   python scripts/validate_links.py
   python scripts/check_formatting.py
   ```

4. **Commit** following the commit conventions below.

5. **Push** your branch and open a Pull Request against `main`.

6. **Fill out the PR template** completely.

7. A maintainer will review within **7 days**. We may request changes or ask clarifying questions.

8. Once approved, a maintainer will merge your PR and update the changelog.

### PR Size Guidelines

- Keep PRs **focused**: one logical change per PR.
- If updating `deepseek.md`, include only the relevant sections, not a full rewrite.
- Large changes (e.g., full documentation sync) should be discussed in an issue first.

---

## Commit Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|---|---|
| `docs` | Changes to `deepseek.md` or any other `.md` file |
| `feat` | New example file, prompt, or script |
| `fix` | Correcting inaccurate information or broken code |
| `chore` | CI/CD, tooling, GitHub Actions, `.gitignore`, etc. |
| `refactor` | Restructuring files without changing content |
| `style` | Formatting fixes (whitespace, table alignment) |

### Examples

```bash
git commit -m "docs(deepseek.md): update model pricing for v4-pro"
git commit -m "feat(examples): add TypeScript streaming example"
git commit -m "fix(deepseek.md): correct FIM max_tokens limit to 4K"
git commit -m "chore(ci): add weekly link check workflow"
```

---

## Reporting Issues

Use the GitHub issue templates:

- **🐛 Bug Report** — incorrect API info, broken examples, bad links
- **✨ Feature Request** — new examples, new agent prompts, new scripts

### Good Bug Reports Include:

1. Which section of `deepseek.md` is incorrect
2. What the documentation currently says
3. What the official documentation (or actual API behavior) says
4. A link to the official source if available

### Good Feature Requests Include:

1. A clear use case ("As a developer using X tool, I need...")
2. What files would need to be created or changed
3. Any references to existing patterns in the repo

---

## Recommended Labels

Maintainers use these labels on issues and PRs:

| Label | Description |
|---|---|
| `documentation` | Changes to `.md` files |
| `bug` | Incorrect or misleading information |
| `enhancement` | New example, prompt, or script |
| `outdated` | Documentation that no longer matches official API |
| `good first issue` | Simple, well-scoped issue for new contributors |
| `help wanted` | Maintainers need community assistance |
| `duplicate` | This issue/PR already exists |
| `wontfix` | Out of scope for this project |
| `needs-verification` | Needs checking against official docs before merging |

---

## Questions?

Open a [Discussion](../../discussions) or ask in the issue thread. We're happy to help!
