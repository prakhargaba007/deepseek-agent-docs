"""
fim_completion.py — Fill-in-the-Middle (FIM) code completion.

FIM lets you provide code before AND after the cursor, and the model fills
in what goes in the middle. Ideal for code completion tools.

Requirements:
  - Beta endpoint: base_url="https://api.deepseek.com/beta"
  - Non-thinking mode only
  - Max 4K output tokens

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python fim_completion.py
"""

import os
from openai import OpenAI


def fim_complete(prefix: str, suffix: str = "", max_tokens: int = 256) -> str:
    """Complete code between prefix and suffix using FIM."""
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/beta",  # Beta required for FIM
    )

    response = client.completions.create(
        model="deepseek-v4-pro",
        prompt=prefix,
        suffix=suffix if suffix else None,
        max_tokens=max_tokens,
        temperature=0.2,  # Low temperature for more deterministic code completion
    )

    return response.choices[0].text


def main():
    # Example 1: Complete a function body
    print("=== Example 1: Complete a function body ===\n")
    prefix = "def binary_search(arr: list, target: int) -> int:\n    \"\"\"\n    Search for target in sorted arr. Return index or -1.\n    \"\"\"\n    "
    suffix = "\n    return -1"

    completion = fim_complete(prefix, suffix)
    print(f"PREFIX:\n{prefix}")
    print(f"COMPLETION:\n{completion}")
    print(f"SUFFIX:\n{suffix}")

    # Example 2: Fill in a missing import
    print("\n\n=== Example 2: Fill in missing code ===\n")
    prefix = "import os\n"
    suffix = "\n\ndef main():\n    key = os.environ.get('API_KEY')\n    client = OpenAI(api_key=key)\n"

    completion = fim_complete(prefix, suffix)
    print(f"PREFIX:\n{prefix}")
    print(f"COMPLETION:\n{completion}")
    print(f"SUFFIX:\n{suffix}")


if __name__ == "__main__":
    main()
