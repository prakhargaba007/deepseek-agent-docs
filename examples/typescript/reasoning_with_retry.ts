// reasoning_with_retry.ts — Thinking mode + exponential backoff retry (TypeScript)
//
// Usage:
//   export DEEPSEEK_API_KEY="sk-your-key"
//   npm install openai tsx
//   npx tsx reasoning_with_retry.ts

import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY!,
  baseURL: "https://api.deepseek.com",
});

// ── Retry with exponential backoff ────────────────────────────────────────────

async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 4,
  baseDelayMs = 1000
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      if (attempt === maxRetries) throw error;

      const isRetryable =
        error.status === 429 || // Rate limit
        error.status === 500 || // Server error
        error.status === 503;   // Service unavailable

      if (!isRetryable) throw error;

      const delay = baseDelayMs * Math.pow(2, attempt) + Math.random() * 500;
      console.warn(`[Retry ${attempt + 1}/${maxRetries}] ${error.message}. Waiting ${Math.round(delay)}ms...`);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error("Unreachable");
}

// ── Thinking mode completion ──────────────────────────────────────────────────

interface ThinkingResult {
  reasoning: string;
  answer: string;
  usage: OpenAI.CompletionUsage | undefined;
}

async function thinkAndRespond(prompt: string): Promise<ThinkingResult> {
  const response = await withRetry(() =>
    client.chat.completions.create({
      model: "deepseek-v4-pro",
      messages: [{ role: "user", content: prompt }],
      reasoning_effort: "high",
      // @ts-ignore — DeepSeek-specific parameter via extra_body
      extra_body: { thinking: { type: "enabled" } },
      max_tokens: 8192,
    })
  );

  const message = response.choices[0].message as any;
  return {
    reasoning: message.reasoning_content ?? "",
    answer: message.content ?? "",
    usage: response.usage,
  };
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
  const problem = `
    A farmer has 17 sheep. All but 9 die. How many sheep does he have left?
  `.trim();

  console.log(`Problem: ${problem}\n`);

  const result = await thinkAndRespond(problem);

  console.log("=== Chain of Thought ===");
  console.log(result.reasoning || "(no reasoning returned)");

  console.log("\n=== Answer ===");
  console.log(result.answer);

  if (result.usage) {
    console.log(`\n=== Token Usage ===`);
    console.log(
      `Prompt: ${result.usage.prompt_tokens} | ` +
      `Completion: ${result.usage.completion_tokens} | ` +
      `Total: ${result.usage.total_tokens}`
    );
  }
}

main().catch(console.error);
