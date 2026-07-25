// tool_calling.js — Tool/function calling with DeepSeek (Node.js ESM)
//
// Usage:
//   export DEEPSEEK_API_KEY="sk-your-key"
//   npm install openai
//   node tool_calling.js

import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: "https://api.deepseek.com",
});

// ── Tool definitions ──────────────────────────────────────────────────────────

const tools = [
  {
    type: "function",
    function: {
      name: "get_weather",
      description: "Get the current weather for a city.",
      parameters: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "City name, e.g. 'London'",
          },
        },
        required: ["location"],
      },
    },
  },
];

// ── Simulated tool execution ──────────────────────────────────────────────────

function executeTool(name, args) {
  if (name === "get_weather") {
    return JSON.stringify({
      location: args.location,
      temperature: 18,
      unit: "celsius",
      condition: "cloudy",
    });
  }
  return JSON.stringify({ error: `Unknown function: ${name}` });
}

// ── Agent loop ────────────────────────────────────────────────────────────────

async function agentLoop(userMessage, maxTurns = 10) {
  const messages = [{ role: "user", content: userMessage }];

  for (let turn = 0; turn < maxTurns; turn++) {
    const response = await client.chat.completions.create({
      model: "deepseek-v4-flash",
      messages,
      tools,
      toolChoice: "auto",
    });

    const message = response.choices[0].message;
    messages.push(message);

    if (!message.toolCalls || message.toolCalls.length === 0) {
      return message.content;
    }

    console.log(`[Turn ${turn + 1}] Executing ${message.toolCalls.length} tool call(s)...`);

    for (const toolCall of message.toolCalls) {
      const args = JSON.parse(toolCall.function.arguments);
      console.log(`  → ${toolCall.function.name}(${JSON.stringify(args)})`);
      const result = executeTool(toolCall.function.name, args);
      console.log(`  ← ${result}`);

      messages.push({
        role: "tool",
        toolCallId: toolCall.id,
        content: result,
      });
    }
  }

  return "Max turns exceeded.";
}

async function main() {
  const question = "What's the weather like in London?";
  console.log(`User: ${question}\n`);
  const answer = await agentLoop(question);
  console.log(`\nAssistant: ${answer}`);
}

main().catch(console.error);
