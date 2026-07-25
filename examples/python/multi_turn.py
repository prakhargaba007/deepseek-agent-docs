"""
multi_turn.py — Multi-turn conversation manager.

The DeepSeek API is stateless. This example shows how to manage conversation
history client-side by appending all messages before each request.

Usage:
    export DEEPSEEK_API_KEY="sk-your-key"
    python multi_turn.py
"""

import os
from typing import List, Dict, Optional
from openai import OpenAI


class ConversationManager:
    """Manages a stateful multi-turn conversation with DeepSeek."""

    def __init__(
        self,
        model: str = "deepseek-v4-flash",
        system_prompt: Optional[str] = None,
        max_history_turns: int = 20,
    ):
        self.client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
        self.model = model
        self.system_prompt = system_prompt or "You are a helpful assistant."
        self.max_history_turns = max_history_turns
        self.history: List[Dict] = []

    def chat(self, user_message: str) -> str:
        """Send a message and get a response."""
        self.history.append({"role": "user", "content": user_message})

        # Trim history to prevent context window overflow
        if len(self.history) > self.max_history_turns * 2:
            # Keep the last N turns (each turn = user + assistant = 2 messages)
            self.history = self.history[-(self.max_history_turns * 2):]

        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.history

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2048,
        )

        assistant_content = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_content})

        return assistant_content

    def reset(self):
        """Clear conversation history."""
        self.history = []


def main():
    bot = ConversationManager(
        model="deepseek-v4-flash",
        system_prompt="You are a knowledgeable travel guide. Be concise.",
    )

    # Simulate a multi-turn travel planning conversation
    turns = [
        "What are the top 3 things to do in Kyoto, Japan?",
        "Which of those is best for a first-time visitor?",
        "How long should I plan to spend there?",
        "What's the best time of year to go?",
    ]

    for i, user_input in enumerate(turns, 1):
        print(f"\n[Turn {i}] User: {user_input}")
        response = bot.chat(user_input)
        print(f"[Turn {i}] Assistant: {response}")

    print(f"\n[Total history: {len(bot.history)} messages]")


if __name__ == "__main__":
    main()
