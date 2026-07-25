"""
thinking_mode.py — DeepSeek thinking/reasoning mode with multi-turn conversation.

The model produces a chain-of-thought (reasoning_content) before the final answer (content).
In multi-turn conversations WITHOUT tool calls, reasoning_content can be omitted from history.

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python thinking_mode.py
"""

import os
from openai import OpenAI


def main():
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    messages = []

    # ── Turn 1 ────────────────────────────────────────────────────────────────
    print("=== Turn 1: Math Problem ===")
    messages.append({"role": "user", "content": "9.11 and 9.8 — which is greater?"})

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
        max_tokens=4096,
    )

    msg = response.choices[0].message

    print(f"\n[Reasoning]\n{msg.reasoning_content}")
    print(f"\n[Answer]\n{msg.content}")

    # Append assistant message to history.
    # Note: reasoning_content is included here but will be silently ignored
    # by the API in subsequent turns (when there are no tool calls).
    messages.append({
        "role": "assistant",
        "reasoning_content": msg.reasoning_content,
        "content": msg.content,
    })

    # ── Turn 2 ────────────────────────────────────────────────────────────────
    print("\n\n=== Turn 2: Follow-up ===")
    messages.append({"role": "user", "content": "How many R's are in 'strawberry'?"})

    response2 = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
        max_tokens=4096,
    )

    msg2 = response2.choices[0].message
    print(f"\n[Reasoning]\n{msg2.reasoning_content}")
    print(f"\n[Answer]\n{msg2.content}")


if __name__ == "__main__":
    main()
