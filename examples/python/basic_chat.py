"""
basic_chat.py — Minimal DeepSeek chat completion example.

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python basic_chat.py
"""

import os
from openai import OpenAI


def main():
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-flash",  # Use deepseek-v4-pro for more complex tasks
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
        ],
        max_tokens=256,
    )

    print(response.choices[0].message.content)
    print(f"\n[Usage] prompt={response.usage.prompt_tokens}, "
          f"completion={response.usage.completion_tokens}, "
          f"total={response.usage.total_tokens}")
    print(f"[Cache] hits={response.usage.prompt_cache_hit_tokens}, "
          f"misses={response.usage.prompt_cache_miss_tokens}")


if __name__ == "__main__":
    main()
