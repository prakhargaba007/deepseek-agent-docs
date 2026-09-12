"""
basic_chat.py — Using the Anthropic SDK with DeepSeek.

The DeepSeek API supports the Anthropic message format at:
  https://api.deepseek.com/anthropic

Claude model names are automatically mapped:
  claude-opus*   → deepseek-v4-pro
  claude-haiku*  → deepseek-flash
  claude-sonnet* → deepseek-flash

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    pip install anthropic
    python basic_chat.py
"""

import os
from anthropic import Anthropic


def main():
    client = Anthropic(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/anthropic",
    )

    # Use a Claude model name — it will be mapped to deepseek-v4-pro
    message = client.messages.create(
        model="claude-opus-4-20250514",  # Maps to deepseek-v4-pro
        max_tokens=1024,
        system="You are a helpful coding assistant.",
        messages=[
            {
                "role": "user",
                "content": "Write a Python one-liner to flatten a nested list.",
            }
        ],
    )

    print("Model (as mapped):", message.model)
    print("Response:", message.content[0].text)
    print("\nUsage:")
    print(f"  Input tokens : {message.usage.input_tokens}")
    print(f"  Output tokens: {message.usage.output_tokens}")


if __name__ == "__main__":
    main()
