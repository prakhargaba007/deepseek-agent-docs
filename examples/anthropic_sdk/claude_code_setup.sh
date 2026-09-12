#!/usr/bin/env bash
# claude_code_setup.sh — Configure Claude Code to use DeepSeek as the backend.
#
# Claude Code uses the Anthropic API format. DeepSeek's Anthropic-compatible
# endpoint lets you use Claude Code with DeepSeek models.
#
# Usage:
#   chmod +x claude_code_setup.sh
#   source ./claude_code_setup.sh
#   claude  # Start Claude Code

# ── Install Claude Code (if not already installed) ───────────────────────────
if ! command -v claude &> /dev/null; then
  echo "Installing Claude Code..."
  npm install -g @anthropic-ai/claude-code
fi

echo "Claude Code version: $(claude --version)"

# ── Configure environment variables ──────────────────────────────────────────
# IMPORTANT: Replace with your actual DeepSeek API key.
# Store this in your shell profile (~/.zshrc or ~/.bashrc) for persistence.

export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="${DEEPSEEK_API_KEY:?Please set DEEPSEEK_API_KEY}"

# Model routing:
# - Opus requests (complex tasks) → deepseek-v4-pro
# - Sonnet and Haiku (fast tasks) → deepseek-flash

export ANTHROPIC_MODEL="deepseek-flash"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-flash"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-flash"  # Subagents use Flash for speed
export CLAUDE_CODE_EFFORT_LEVEL="max"                   # Max reasoning effort

echo ""
echo "✅ Claude Code configured to use DeepSeek backend."
echo ""
echo "Environment:"
echo "  ANTHROPIC_BASE_URL     = ${ANTHROPIC_BASE_URL}"
echo "  ANTHROPIC_MODEL        = ${ANTHROPIC_MODEL}"
echo "  CLAUDE_CODE_EFFORT_LEVEL = ${CLAUDE_CODE_EFFORT_LEVEL}"
echo ""
echo "To persist these settings, add this file's exports to your ~/.zshrc or ~/.bashrc."
echo ""
echo "To start Claude Code in your project:"
echo "  cd /path/to/your-project"
echo "  claude"
