#!/usr/bin/env python3
"""
vision.py — Example demonstrating multimodal image analysis with DeepSeek API.

Uses the experimental model `deepseek-v4-flash-vision-exp` to analyze images
via base64 encoding or external URLs.

Prerequisites:
    pip install openai

Usage:
    export DEEPSEEK_API_KEY="sk-..."
    python examples/python/vision.py
"""

import base64
import os
import sys
from openai import OpenAI


def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    # Example 1: Image via Public URL
    print("=== Analyzing Image via URL ===")
    response_url = client.chat.completions.create(
        model="deepseek-v4-flash-vision-exp",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is depicted in this image, and what are its key visual features?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/640px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                        },
                    },
                ],
            }
        ],
        max_tokens=500,
    )
    print(response_url.choices[0].message.content)
    print(f"\n[Usage: {response_url.usage}]\n")

    # Example 2: Local Image via Base64
    # (Create a small 1x1 test PNG data URI for demonstration)
    dummy_base64_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    print("=== Analyzing Local Image via Base64 Data URI ===")
    response_b64 = client.chat.completions.create(
        model="deepseek-v4-flash-vision-exp",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the dimensions and color of this 1x1 test image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{dummy_base64_png}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    print(response_b64.choices[0].message.content)
    print(f"\n[Usage: {response_b64.usage}]\n")


if __name__ == "__main__":
    main()
