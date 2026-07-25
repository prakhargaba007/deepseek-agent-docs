// streaming.js — DeepSeek streaming with SSE (Node.js ESM)
//
// Usage:
//   export DEEPSEEK_API_KEY="sk-your-key"
//   npm install openai
//   node streaming.js

import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: "https://api.deepseek.com",
});

async function main() {
  const stream = await client.chat.completions.create({
    model: "deepseek-v4-flash",
    messages: [
      { role: "user", content: "Explain the event loop in JavaScript." },
    ],
    stream: true,
    streamOptions: { includeUsage: true },
    maxTokens: 512,
  });

  process.stdout.write("Assistant: ");

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
      process.stdout.write(content);
    }
    if (chunk.usage) {
      console.log("\n\nUsage:", chunk.usage);
    }
  }

  console.log();
}

main().catch(console.error);
