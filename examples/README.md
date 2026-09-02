# Code Examples

Runnable examples demonstrating DeepSeek API usage across multiple languages and use cases.

All examples use environment variables for API keys — never hardcode secrets.

## Setup

```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
```

## Examples

| Folder | Language | Examples |
|---|---|---|
| [`python/`](python/) | Python + OpenAI SDK | 8 examples (chat, streaming, thinking, tools, JSON, FIM, multi-turn, vision) |
| [`javascript/`](javascript/) | Node.js (ESM) | 3 examples (chat, streaming, tools) |
| [`typescript/`](typescript/) | TypeScript | 2 examples (chat, retry) |
| [`curl/`](curl/) | cURL (bash) | 4 examples (chat, streaming, FIM, vision) |
| [`anthropic_sdk/`](anthropic_sdk/) | Python + Anthropic SDK | 2 examples (chat, Claude Code setup) |

## Running Python Examples

```bash
pip install openai anthropic
python examples/python/basic_chat.py
```

## Running JavaScript Examples

```bash
npm install openai
node examples/javascript/basic_chat.js
```

## Running TypeScript Examples

```bash
npm install openai tsx
npx tsx examples/typescript/basic_chat.ts
```

## Running cURL Examples

```bash
chmod +x examples/curl/basic_chat.sh
./examples/curl/basic_chat.sh
```
