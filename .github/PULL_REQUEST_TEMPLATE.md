## Description

<!-- A clear and concise description of what this PR changes and why. -->

## Type of Change

- [ ] 🐛 Bug fix — Corrects inaccurate API information
- [ ] 📝 Documentation update — Updates deepseek.md with new/changed API behavior
- [ ] ✨ New feature — Adds a new example, prompt, or script
- [ ] 🔧 Maintenance — CI, tooling, or repository configuration
- [ ] 🌐 Translation — Adds a translated version of deepseek.md
- [ ] 🎨 Style — Formatting or structural improvements (no content changes)

## Affected Files

<!-- List the files you changed. -->

- [ ] `deepseek.md`
- [ ] `README.md`
- [ ] `examples/...`
- [ ] `prompts/...`
- [ ] `scripts/...`
- [ ] `.github/...`
- [ ] Other: ___

## Checklist

### For deepseek.md Changes

- [ ] The change is verified against the [official DeepSeek API docs](https://api-docs.deepseek.com)
- [ ] I have included a link to the official source in this PR description
- [ ] I have updated the version header in `deepseek.md`
- [ ] I have updated the `VERSION` file
- [ ] I have added a CHANGELOG entry under `[Unreleased]`
- [ ] `python scripts/validate_links.py` passes (if links were added/changed)
- [ ] `python scripts/check_formatting.py` passes

### For Code Example Changes

- [ ] The example is runnable (tested locally or clearly marked as pseudo-code)
- [ ] API keys are stored in environment variables (`os.environ.get("DEEPSEEK_API_KEY")`)
- [ ] Current model names are used (`deepseek-v4-pro` or `deepseek-v4-flash`)
- [ ] The example has a docstring/comment explaining what it demonstrates

### General

- [ ] My commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) format
- [ ] I have read [CONTRIBUTING.md](CONTRIBUTING.md)

## Source / Reference

<!-- If this PR updates API information, link to the official source. -->

Official documentation source: <!-- https://api-docs.deepseek.com/... -->

## Additional Notes

<!-- Any other information reviewers should know. -->
