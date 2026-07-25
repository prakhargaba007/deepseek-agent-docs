# Security Policy

## Supported Versions

This repository contains **documentation only** (no executable server code). There are no known security vulnerabilities in the documentation itself.

| Version | Supported |
|---|---|
| Latest (main branch) | ✅ |

## Reporting a Vulnerability

If you discover a security issue **in this repository** (e.g., a malicious script, a compromised dependency in a GitHub Action, or a link pointing to a phishing site), please **do not open a public issue**.

Instead, report it privately:

1. Go to the [Security tab](../../security) of this repository.
2. Click **"Report a vulnerability"**.
3. Fill out the form with as much detail as possible.

We will acknowledge your report within **72 hours** and work to resolve it as quickly as possible.

## Security Considerations for API Key Usage

The examples in this repository use environment variables for API keys. **Never:**

- Hardcode API keys in source files
- Commit `.env` files containing secrets to version control
- Share your DeepSeek API key publicly

Always store your `DEEPSEEK_API_KEY` in environment variables:

```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
```

Or use a secrets manager in production environments.

## Scope

This security policy covers:
- The repository files and GitHub Actions workflows
- The example scripts under `examples/`
- The scripts under `scripts/`

It does **not** cover:
- The DeepSeek platform itself (report to api-service@deepseek.com)
- Third-party integrations listed in the documentation
