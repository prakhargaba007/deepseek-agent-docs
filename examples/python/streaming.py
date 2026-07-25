"""
streaming.py — DeepSeek streaming chat with usage statistics.

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python streaming.py
"""

import os
from openai import OpenAI


def main():
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    stream = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "user", "content": "Explain how HTTPS works in simple terms."},
        ],
        stream=True,
        stream_options={"include_usage": True},  # Get usage stats in final chunk
        max_tokens=512,
    )

    print("=== Response ===")
    full_response = ""

    for chunk in stream:
        # Content delta
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            print(content, end="", flush=True)

        # Usage stats arrive in a final chunk where choices is empty
        if chunk.usage:
            print(f"\n\n=== Token Usage ===")
            print(f"Prompt tokens   : {chunk.usage.prompt_tokens}")
            print(f"Completion tokens: {chunk.usage.completion_tokens}")
            print(f"Total tokens    : {chunk.usage.total_tokens}")

    print()


if __name__ == "__main__":
    main()
