// basic_chat.ts — Fully typed DeepSeek chat completion (TypeScript)
//
// Usage:
//   export DEEPSEEK_API_KEY="sk-your-key"
//   npm install openai tsx
//   npx tsx basic_chat.ts

import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY!,
  baseURL: "https://api.deepseek.com",
});

interface ChatOptions {
  model?: string;
  systemPrompt?: string;
  maxTokens?: number;
}

async function chat(
  userMessage: string,
  options: ChatOptions = {}
): Promise<string> {
  const {
    model = "deepseek-flash",
    systemPrompt = "You are a helpful assistant.",
    maxTokens = 1024,
  } = options;

  const response = await client.chat.completions.create({
    model,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userMessage },
    ],
    max_tokens: maxTokens,
  });

  const content = response.choices[0].message.content;
  if (!content) throw new Error("Empty response from model");

  return content;
}

async function main(): Promise<void> {
  const result = await chat(
    "Write a one-line TypeScript function that reverses a string.",
    {
      model: "deepseek-flash",
      systemPrompt: "You are an expert TypeScript developer. Be concise.",
    }
  );

  console.log("Answer:", result);
}

main().catch(console.error);
