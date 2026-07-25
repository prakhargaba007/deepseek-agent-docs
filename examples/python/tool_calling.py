"""
tool_calling.py — Full tool call loop with DeepSeek.

The model requests tool execution; the caller runs the function and feeds
results back. The model then produces a natural language response.

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python tool_calling.py
"""

import json
import os
from openai import OpenAI


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. 'San Francisco, CA'",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the latest stock price for a ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol, e.g. 'AAPL'",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
]


# ── Simulated function implementations ───────────────────────────────────────

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulated weather API response."""
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "condition": "partly cloudy",
        "humidity": "65%",
    }


def get_stock_price(ticker: str) -> dict:
    """Simulated stock price response."""
    prices = {"AAPL": 189.50, "GOOG": 175.20, "MSFT": 415.80}
    return {
        "ticker": ticker,
        "price": prices.get(ticker, 100.00),
        "currency": "USD",
        "change": "+1.2%",
    }


def execute_tool(name: str, arguments: dict) -> str:
    if name == "get_weather":
        result = get_weather(**arguments)
    elif name == "get_stock_price":
        result = get_stock_price(**arguments)
    else:
        result = {"error": f"Unknown function: {name}"}
    return json.dumps(result)


# ── Agent loop ────────────────────────────────────────────────────────────────

def agent_loop(user_input: str, max_turns: int = 10) -> str:
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    messages = [{"role": "user", "content": user_input}]

    for turn in range(max_turns):
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message
        messages.append(message)

        # No tool calls — model has produced its final answer
        if not message.tool_calls:
            return message.content

        # Execute each tool call and append results
        print(f"[Turn {turn + 1}] Executing {len(message.tool_calls)} tool call(s)...")
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            print(f"  → {tool_call.function.name}({args})")
            result = execute_tool(tool_call.function.name, args)
            print(f"  ← {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "Max turns exceeded without a final answer."


def main():
    question = "What's the weather in Tokyo and the current price of AAPL stock?"
    print(f"User: {question}\n")
    answer = agent_loop(question)
    print(f"\nAssistant: {answer}")


if __name__ == "__main__":
    main()
