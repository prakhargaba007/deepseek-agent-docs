// basic_chat.js — Minimal DeepSeek chat completion (Node.js ESM)
//
// Usage:
//   export DEEPSEEK_API_KEY="sk-your-key"
//   npm install openai
//   node basic_chat.js

import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: "https://api.deepseek.com",
});

async function main() {
  const response = await client.chat.completions.create({
    model: "deepseek-v4-flash",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "What is the capital of France?" },
    ],
    maxTokens: 256,
  });

  const message = response.choices[0].message;
  console.log("Assistant:", message.content);
  console.log("\nUsage:", response.usage);
}

main().catch(console.error);
