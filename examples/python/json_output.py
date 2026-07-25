"""
json_output.py — Structured JSON extraction using DeepSeek's response_format.

Requirements:
  1. Set response_format={"type": "json_object"}
  2. Include the word "json" in the prompt
  3. Provide an example schema in the prompt

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python json_output.py
"""

import json
import os
from openai import OpenAI


def extract_entities(text: str) -> dict:
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data extraction assistant. "
                    "Always respond with valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": f"""Extract the following information as JSON from the text below.

Text:
{text}

Return a JSON object matching this exact schema:
{{
  "persons": [
    {{"name": "string", "role": "string or null"}}
  ],
  "organizations": ["string"],
  "locations": ["string"],
  "dates": ["string"],
  "key_events": ["string"]
}}""",
            },
        ],
        response_format={"type": "json_object"},
        max_tokens=1024,
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


def main():
    samples = [
        (
            "John Smith was appointed as CTO of Acme Corp on March 15, 2024 "
            "at their headquarters in Austin, Texas."
        ),
        (
            "Google and Microsoft announced a joint research initiative in "
            "Seattle on November 1, 2023, led by Dr. Sarah Chen and Dr. James Park."
        ),
    ]

    for i, text in enumerate(samples, 1):
        print(f"\n=== Sample {i} ===")
        print(f"Input: {text}\n")
        result = extract_entities(text)
        print("Output:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
