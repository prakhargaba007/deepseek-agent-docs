# DeepSeek API — Complete Developer Reference

> **Based on official documentation at [api-docs.deepseek.com](https://api-docs.deepseek.com)**
>
> Version: 1.0.0 | Last crawled: July 2026

---

## Table of Contents

- [1. Overview & Quick Start](#1-overview--quick-start)
- [2. Authentication](#2-authentication)
- [3. Models & Pricing](#3-models--pricing)
- [4. API Endpoints](#4-api-endpoints)
  - [4.1 Chat Completions](#41-chat-completions)
  - [4.2 FIM Completion (Beta)](#42-fim-completion-beta)
  - [4.3 List Models](#43-list-models)
  - [4.4 Get User Balance](#44-get-user-balance)
- [5. Parameters Reference](#5-parameters-reference)
- [6. Features](#6-features)
  - [6.1 Thinking / Reasoning Mode](#61-thinking--reasoning-mode)
  - [6.2 Multi-round Conversations](#62-multi-round-conversations)
  - [6.3 Streaming](#63-streaming)
  - [6.4 Tool Calls](#64-tool-calls)
  - [6.5 JSON Output (Structured Output)](#65-json-output-structured-output)
  - [6.6 Context Caching](#66-context-caching)
  - [6.7 Chat Prefix Completion (Beta)](#67-chat-prefix-completion-beta)
  - [6.8 FIM (Fill-in-the-Middle)](#68-fim-fill-in-the-middle)
- [7. OpenAI Compatibility](#7-openai-compatibility)
- [8. Anthropic API Compatibility](#8-anthropic-api-compatibility)
- [9. Agent Integrations](#9-agent-integrations)
- [10. Rate Limits & Isolation](#10-rate-limits--isolation)
- [11. Error Codes & Handling](#11-error-codes--handling)
- [12. Token Usage](#12-token-usage)
- [13. SDK Examples](#13-sdk-examples)
- [14. Best Practices](#14-best-practices)
- [15. Production Examples](#15-production-examples)
- [16. Changelog](#16-changelog)
- [17. Hidden Details & Edge Cases](#17-hidden-details--edge-cases)

---

## 1. Overview & Quick Start

The DeepSeek API provides access to the DeepSeek family of large language models via endpoints compatible with both **OpenAI** and **Anthropic** API formats. By modifying your SDK configuration, you can use existing OpenAI or Anthropic SDKs or software compatible with those APIs to access the DeepSeek API.

### Base URLs

| Parameter | Value |
|---|---|
| base_url (OpenAI format) | `https://api.deepseek.com` |
| base_url (Anthropic format) | `https://api.deepseek.com/anthropic` |
| Beta features base_url | `https://api.deepseek.com/beta` |

### Minimum Request

A minimal chat completion request requires:
- A valid API key
- A model name
- A list of messages

### Your First API Call (cURL)

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "stream": false
      }'
```

### Your First API Call (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"}
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)
```

### Your First API Call (Node.js / JavaScript)

```javascript
// Please install OpenAI SDK first: `npm install openai`
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env['DEEPSEEK_API_KEY'],
    baseURL: "https://api.deepseek.com",
});

async function main() {
    const response = await client.chat.completions.create({
        model: "deepseek-v4-pro",
        messages: [
            { role: "system", content: "You are a helpful assistant" },
            { role: "user", content: "Hello" },
        ],
        stream: false,
    });
    console.log(response.choices[0].message.content);
}
main();
```

---

## 2. Authentication

### API Keys

The DeepSeek API uses Bearer token authentication via HTTP headers.

- **Security Scheme**: HTTP Bearer Auth
- **Header format**: `Authorization: Bearer ${DEEPSEEK_API_KEY}`
- **Key prefix**: API keys start with `sk-`

### Obtaining an API Key

1. Visit the [DeepSeek Platform](https://platform.deepseek.com/api_keys)
2. Create a new API key
3. Copy the key and store it securely

### Key Management Best Practices

- Store keys in environment variables, never in code
- Use different keys for different environments (dev, staging, production)
- Rotate keys periodically
- Monitor key usage on the DeepSeek Platform dashboard

---

## 3. Models & Pricing

### Current Models

| Model | Context Length | Max Output | Thinking Support | Tool Support | Streaming | Recommended For |
|---|---|---|---|---|---|---|
| `deepseek-v4-pro` | 1M tokens | 384K tokens | Yes (default: enabled) | Yes | Yes | Complex reasoning, coding, agent tasks, production workloads |
| `deepseek-v4-flash` | 1M tokens | 384K tokens | Yes (default: enabled) | Yes | Yes | Fast responses, simple agent tasks, cost-sensitive applications |

### Model Details

**DeepSeek-V4-Pro**
- 1.6T total parameters, 49B active parameters (MoE)
- Performance rivaling top closed-source models
- Enhanced agentic capabilities
- Rich world knowledge
- World-class reasoning in Math/STEM/Coding

**DeepSeek-V4-Flash**
- 284B total parameters, 13B active parameters (MoE)
- Reasoning capabilities closely approach V4-Pro
- Performs on par with V4-Pro on simple agent tasks
- Smaller parameter size, faster response times
- Highly cost-effective

### Deprecated Model Names

> **Warning**: The following model names will be deprecated on **2026/07/24 15:59 UTC**.

| Legacy Name | Maps To | Mode |
|---|---|---|
| `deepseek-chat` | `deepseek-v4-flash` | Non-thinking mode |
| `deepseek-reasoner` | `deepseek-v4-flash` | Thinking mode |

For compatibility, these legacy names currently correspond to the non-thinking mode and thinking mode of `deepseek-v4-flash`, respectively. You should migrate to `deepseek-v4-flash` or `deepseek-v4-pro` before the deprecation date.

### Pricing (Per 1M Tokens)

| | deepseek-v4-flash | deepseek-v4-pro |
|---|---|---|
| **Input (Cache Hit)** | $0.0028 | $0.003625 |
| **Input (Cache Miss)** | $0.14 | $0.435 |
| **Output** | $0.28 | $0.87 |
| **Concurrency Limit** | 2500 | 500 |

### Deduction Rules

- Expense = number of tokens x price
- Fees are deducted from your topped-up balance or granted balance
- Granted balance is used first when both balances are available
- Prices may vary; DeepSeek reserves the right to adjust them
- Regularly check the pricing page for the most recent information

---

## 4. API Endpoints

### 4.1 Chat Completions

**Create Chat Completion**

| Property | Value |
|---|---|
| HTTP Method | `POST` |
| URL | `/chat/completions` |
| Authentication | Bearer token via `Authorization` header |
| Content-Type | `application/json` |

**Purpose**: Creates a model response for the given chat conversation. This is the primary endpoint for interacting with DeepSeek models.

#### Request Body

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `messages` | array[object] | Yes | - | A list of messages comprising the conversation. Minimum 1 message. |
| `model` | string | Yes | - | Model ID: `deepseek-v4-flash` or `deepseek-v4-pro` |
| `thinking` | object | No | `{"type": "enabled"}` | Controls thinking/non-thinking mode. `{"type": "enabled"}` or `{"type": "disabled"}` |
| `reasoning_effort` | string | No | `"high"` | Reasoning effort: `"high"` or `"max"` |
| `max_tokens` | integer | No | - | Maximum tokens in the generated response |
| `temperature` | number | No | - | Sampling temperature (not supported in thinking mode) |
| `top_p` | number | No | - | Nucleus sampling parameter (not supported in thinking mode) |
| `presence_penalty` | number | No | - | Deprecated / no effect in thinking mode |
| `frequency_penalty` | number | No | - | Deprecated / no effect in thinking mode |
| `stream` | boolean | No | `false` | Whether to stream partial progress |
| `stream_options` | object | No | - | Options for streaming. Set `{"include_usage": true}` to get usage in the final chunk |
| `stop` | string or array[string] | No | - | Up to 16 sequences where the API will stop generating |
| `tools` | array[object] | No | - | Tool definitions (functions the model may call) |
| `tool_choice` | string or object | No | - | Controls tool calling behavior |
| `response_format` | object | No | - | For JSON output: `{"type": "json_object"}` |
| `user` | string | No | - | user_id for rate limit isolation and content safety |
| `frequency_penalty` | - | - | - | **Deprecated.** Will not take effect. |
| `presence_penalty` | - | - | - | **Deprecated.** Will not take effect. |

#### Message Object Types

**System Message**
```json
{
  "content": "string (required) - The contents of the system message",
  "role": "system (required)",
  "name": "string (optional) - Differentiates participants of the same role"
}
```

**User Message**
```json
{
  "content": "string (required) - The contents of the user message",
  "role": "user (required)",
  "name": "string (optional)"
}
```

**Assistant Message**
```json
{
  "content": "string or null (required) - The contents of the assistant message",
  "role": "assistant (required)",
  "name": "string (optional)",
  "prefix": "boolean (optional, Beta) - Set true to force the model to start its answer with the supplied prefix. Requires base_url=https://api.deepseek.com/beta",
  "reasoning_content": "string or null (optional, Beta) - CoT input for prefix completion. Requires prefix=true",
  "tool_calls": "array[object] (optional) - Tool calls made by the assistant"
}
```

**Tool Message**
```json
{
  "content": "string (required) - The contents of the tool message",
  "role": "tool (required)",
  "tool_call_id": "string (required) - Tool call this message is responding to"
}
```

#### Thinking Parameter

```json
{
  "thinking": {
    "type": "enabled"  // or "disabled"
  },
  "reasoning_effort": "high"  // or "max"
}
```

The `thinking` toggle defaults to `enabled`. When using the OpenAI SDK, you must pass the `thinking` parameter within `extra_body`.

#### Response Schema

```json
{
  "id": "string - A unique identifier for the completion",
  "object": "string - Always 'chat.completion'",
  "created": "integer - Unix timestamp of creation",
  "model": "string - The model used",
  "choices": [
    {
      "index": "integer",
      "message": {
        "role": "string",
        "content": "string or null",
        "reasoning_content": "string or null - Chain-of-thought content (thinking mode only)"
      },
      "finish_reason": "string - 'stop', 'length', 'content_filter', or 'insufficient_system_resource'"
    }
  ],
  "usage": {
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "total_tokens": "integer",
    "prompt_cache_hit_tokens": "integer - Tokens served from context cache",
    "prompt_cache_miss_tokens": "integer - Tokens that missed the cache"
  }
}
```

**finish_reason values:**
| Value | Description |
|---|---|
| `stop` | Model hit a natural stop point or a provided stop sequence |
| `length` | Maximum number of tokens specified in the request was reached |
| `content_filter` | Content omitted due to a flag from content filters |
| `insufficient_system_resource` | Request interrupted due to insufficient resources in the inference system |

#### Example Response (Non-streaming)

```json
{
  "id": "chatcmpl-1234567890abcdef",
  "object": "chat.completion",
  "created": 1728000000,
  "model": "deepseek-v4-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?",
        "reasoning_content": null
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 10,
    "total_tokens": 25,
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 15
  }
}
```

#### Streaming Behavior

When `stream: true`, the API returns Server-Sent Events (SSE). Tokens are sent as `data:` events as they become available, terminated by a `data: [DONE]` message.

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [{"role": "user", "content": "Count from 1 to 5"}],
        "stream": true
      }'
```

Streaming response format:
```
data: {"choices":[{"delta":{"content":"1"},"index":0}]}

data: {"choices":[{"delta":{"content":"2"},"index":0}]}

...

data: {"choices":[{"delta":{},"finish_reason":"stop","index":0}]}

data: [DONE]
```

When `stream_options: {"include_usage": true}` is set, an additional chunk with usage statistics is sent before `[DONE]`:
```json
data: {"usage": {...}, "choices": []}
data: [DONE]
```

---

### 4.2 FIM Completion (Beta)

**Create FIM Completion**

| Property | Value |
|---|---|
| HTTP Method | `POST` |
| URL | `/completions` |
| Authentication | Bearer token |
| Content-Type | `application/json` |
| Beta flag | Must set `base_url="https://api.deepseek.com/beta"` |

**Purpose**: Fill-in-the-Middle completion — provide a prefix and optional suffix, and the model completes the content in between. Commonly used for code completion.

#### Request Body

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `model` | string | Yes | - | `deepseek-v4-pro` |
| `prompt` | string | Yes | `"Once upon a time, "` | The prompt to generate completions for |
| `suffix` | string | No | - | The suffix that comes after the completion of inserted text |
| `max_tokens` | integer | No | - | Maximum tokens in the completion (max: 4K) |
| `temperature` | number | No | - | Sampling temperature |
| `top_p` | number | No | - | Nucleus sampling |
| `stop` | string or array[string] | No | - | Up to 16 stop sequences |
| `stream` | boolean | No | `false` | Whether to stream |
| `stream_options` | object | No | - | Same as Chat Completions |
| `echo` | boolean | No | - | Echo back the prompt in addition to the completion |
| `logprobs` | integer | No | - | Include log probabilities |
| `frequency_penalty` | - | - | - | **Deprecated** |
| `presence_penalty` | - | - | - | **Deprecated** |

**Limits:**
- Maximum tokens for FIM completion: **4K tokens**
- Only supported in non-thinking mode

#### Response Schema

```json
{
  "id": "string - Unique identifier",
  "object": "string - Always 'text_completion'",
  "choices": [
    {
      "finish_reason": "string - 'stop', 'length', 'content_filter', or 'insufficient_system_resource'",
      "index": "integer",
      "logprobs": "object or null",
      "text": "string - The generated completion text"
    }
  ],
  "usage": {
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "total_tokens": "integer"
  }
}
```

---

### 4.3 List Models

**Lists Models**

| Property | Value |
|---|---|
| HTTP Method | `GET` |
| URL | `/models` |
| Authentication | Bearer token |

**Purpose**: Lists the currently available models with basic information.

#### Response Schema

```json
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-v4-flash",
      "object": "model",
      "owned_by": "deepseek"
    },
    {
      "id": "deepseek-v4-pro",
      "object": "model",
      "owned_by": "deepseek"
    }
  ]
}
```

#### Example Request

```bash
curl https://api.deepseek.com/models \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}"
```

---

### 4.4 Get User Balance

**Get User Balance**

| Property | Value |
|---|---|
| HTTP Method | `GET` |
| URL | `/user/balance` |
| Authentication | Bearer token |

**Purpose**: Get the user's current balance information.

#### Response Schema

```json
{
  "is_available": "boolean - Whether the balance is sufficient for API calls",
  "balance_infos": [
    {
      "currency": "string - 'CNY' or 'USD'",
      "total_balance": "string - Total available balance (granted + topped-up)",
      "granted_balance": "string - Total not-expired granted balance",
      "topped_up_balance": "string - Total topped-up balance"
    }
  ]
}
```

#### Example Request

```bash
curl https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}"
```

#### Example Response

```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

---

## 5. Parameters Reference

### `messages` (array, required)

A list of messages comprising the conversation. The minimum number of messages is 1. Each message is an object with a `role` and `content`. Supported roles: `system`, `user`, `assistant`, `tool`.

**Interaction with other parameters:**
- When the last message has `role: "assistant"` and `prefix: true`, the model completes from that prefix
- When `response_format: {"type": "json_object"}`, the system or user prompt should include the word "json"

### `model` (string, required)

Valid values: `deepseek-v4-flash`, `deepseek-v4-pro`.

The model determines capabilities, pricing, and concurrency limits.

### `thinking` (object, optional)

Controls the thinking mode toggle.

```json
{"type": "enabled"}   // thinking mode (default)
{"type": "disabled"}  // non-thinking mode
```

**When using the OpenAI SDK**, pass this via `extra_body`:
```python
extra_body={"thinking": {"type": "enabled"}}
```

### `reasoning_effort` (string, optional)

Controls the reasoning effort when thinking mode is enabled.

| Value | Behavior |
|---|---|
| `"high"` | Default effort for regular requests |
| `"max"` | Effort for complex agent requests (Claude Code, OpenCode sets this automatically) |
| `"low"` | Mapped to `"high"` for compatibility |
| `"medium"` | Mapped to `"high"` for compatibility |
| `"xhigh"` | Mapped to `"max"` for compatibility |

### `max_tokens` (integer, optional)

The maximum number of tokens that can be generated in the response.

### `temperature` (number, optional)

Sampling temperature. **Not supported in thinking mode** — setting it will have no effect but will not trigger an error.

### `top_p` (number, optional)

Nucleus sampling parameter. **Not supported in thinking mode** — same behavior as temperature.

### `presence_penalty` / `frequency_penalty` (number, optional)

**Deprecated parameters.** These no longer have any effect if passed to the API.

### `stream` (boolean, optional, default: false)

Whether to stream partial progress. When `true`, tokens are sent as SSE events.

### `stream_options` (object, optional)

Only applicable when `stream: true`. Set `{"include_usage": true}` to receive usage statistics in the final chunk before `[DONE]`.

### `stop` (string or array[string], optional)

Up to 16 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.

### `tools` (array[object], optional)

Function/tool definitions that the model may call. Each tool follows the JSON Schema format with a `type` (must be `"function"`) and `function` object containing `name`, `description`, and `parameters`.

### `tool_choice` (string or object, optional)

Controls tool calling behavior:
- `"auto"` (default) — model decides whether to call tools
- `"none"` — model will not call any tool
- `{"type": "function", "function": {"name": "function_name"}}` — force a specific tool

### `response_format` (object, optional)

For JSON output: `{"type": "json_object"}`. When enabled, the prompt must include the word "json" and provide an example of the desired JSON format.

### `user` (string, optional)

A user_id for fine-grained management of different users under the same account. Used for:
- Content safety isolation
- KVCache isolation
- Scheduling isolation
- Per-user concurrency limits (for users with increased quotas)

---

## 6. Features

### 6.1 Thinking / Reasoning Mode

**What it does**: Before outputting the final answer, the model first produces a chain-of-thought (CoT) reasoning to improve accuracy.

**Why it exists**: To enhance the quality of responses by allowing the model to "think through" problems before answering.

**When to use it**: For complex reasoning tasks (math, logic, coding, analysis), multi-step agent workflows, or any scenario where response quality matters more than raw speed.

**When NOT to use it**: For simple, deterministic responses (e.g., greetings, simple classifications) where the overhead of reasoning adds latency and cost with no benefit.

**Performance implications**: Thinking mode generates more tokens (both reasoning and final output), increasing latency and cost. The `reasoning_effort` parameter controls this tradeoff.

**Cost implications**: Higher reasoning effort = more reasoning tokens = higher cost. Complex tasks may consume significantly more tokens compared to non-thinking mode.

#### Control Parameters

| Control | OpenAI Format | Anthropic Format |
|---|---|---|
| Toggle | `"thinking": {"type": "enabled/disabled"}` | Same (via extra_body) |
| Effort | `"reasoning_effort": "high/max"` | `"output_config": {"effort": "high/max"}` |

#### Input and Output Parameters

In thinking mode, the following parameters are **not supported** (they have no effect but will not error):
- `temperature`
- `top_p`
- `presence_penalty`
- `frequency_penalty`

The chain-of-thought content is returned via the **`reasoning_content`** parameter, at the same level as `content` in the response message.

#### Multi-turn Behavior with reasoning_content

**Without tool calls**: The intermediate assistant's `reasoning_content` does NOT need to participate in context concatenation. If passed to the API in subsequent turns, it will be ignored.

**With tool calls**: The intermediate assistant's `reasoning_content` MUST participate in context concatenation and MUST be passed back to the API in all subsequent user interaction turns.

#### Example (Non-streaming with Thinking)

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-api-key>",
    base_url="https://api.deepseek.com"
)

# Turn 1
messages = [
    {"role": "user", "content": "9.11 and 9.8, which is greater?"}
]
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

# Turn 2 - The reasoning_content will be ignored by the API
messages.append(response.choices[0].message)
messages.append({
    'role': 'user',
    'content': "How many Rs are there in the word 'strawberry'?"
})
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
)
```

#### Example (Streaming with Thinking)

```python
from openai import OpenAI

client = OpenAI(api_key="<your-key>", base_url="https://api.deepseek.com")

# Turn 1
messages = [
    {"role": "user", "content": "9.11 and 9.8, which is greater?"}
]
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    stream=True,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
)

reasoning_content = ""
content = ""
for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
    else:
        content += chunk.choices[0].delta.content

# Turn 2 - reasoning_content will be ignored by the API
messages.append({
    "role": "assistant",
    "reasoning_content": reasoning_content,
    "content": content
})
messages.append({
    "role": "user",
    "content": "How many Rs are there in the word 'strawberry'?"
})
```

---

### 6.2 Multi-round Conversations

**What it does**: Enables multi-turn conversations by concatenating history.

**Why it exists**: The DeepSeek `/chat/completions` API is "stateless" — the server does not record conversation context. Users must include all previous messages with each request.

**How to implement**: With each new turn:
1. Append the model's previous response to the messages array
2. Append the new user question
3. Send the complete message history with each request

#### Example

**Round 1:**
```json
[
  {"role": "user", "content": "What is the capital of China?"}
]
```

**Round 2:**
```json
[
  {"role": "user", "content": "What is the capital of China?"},
  {"role": "assistant", "content": "The capital of China is Beijing."},
  {"role": "user", "content": "What is the capital of the United States?"}
]
```

---

### 6.3 Streaming

**What it does**: Returns partial progress via Server-Sent Events (SSE) as tokens are generated.

**Why it exists**: Reduces perceived latency in interactive applications (chat UIs, real-time coding assistants).

**When to use it**: Chat interfaces, real-time code completion, any application where the user expects immediate feedback.

**When NOT to use it**: Batch processing, data extraction pipelines, or when you need the complete response to parse structured output.

#### Behavior with reasoning_content

When streaming in thinking mode, the `reasoning_content` field is populated with chain-of-thought tokens as they are generated, before the final `content` begins streaming.

#### Usage Statistics in Streaming

Set `stream_options: {"include_usage": true}` to receive token usage in a final chunk before `data: [DONE]`.

---

### 6.4 Tool Calls

**What it does**: Allows the model to request the execution of external functions/tools, enabling integration with external APIs, databases, and services.

**Why it exists**: Extends model capabilities beyond text generation by enabling interactions with external systems.

**Supported in**: Both thinking mode and non-thinking mode (thinking mode support added in DeepSeek-V3.2).

#### Non-thinking Mode

The model outputs a JSON object specifying which function to call and with what parameters. The caller executes the function and returns results in a tool message.

```python
from openai import OpenAI

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(api_key="<your-key>", base_url="https://api.deepseek.com")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply a location first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [
    {"role": "user", "content": "How's the weather in Hangzhou, Zhejiang?"}
]
message = send_messages(messages)
print(f"User>\t{messages[0]['content']}")
print(f"Model>\t{message}")
```

**Execution flow:**
1. User asks a question
2. Model returns a function call (e.g., `get_weather({"location": "Hangzhou"})`)
3. Caller executes the function and provides results
4. Model responds in natural language with the results

> **Important**: The model itself does not execute functions. The caller must implement function execution.

#### Thinking Mode with Tool Calls

From DeepSeek-V3.2 onward, tool use is supported in thinking mode. When a tool call occurs in thinking mode, the `reasoning_content` **must** be included in context for subsequent turns.

#### strict Mode (Beta)

**What it does**: In strict mode, the model strictly adheres to the format requirements of the Function's JSON schema when outputting a tool call.

**Requirements to use strict mode:**
1. Use `base_url="https://api.deepseek.com/beta"` to enable Beta features
2. In the `tools` parameter, all functions must set `strict: true`
3. The server validates the JSON Schema — invalid schemas return errors

**Example tool definition with strict mode:**
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "strict": true,
    "description": "Get weather of a location, the user should supply a location first.",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        }
      },
      "required": ["location"],
      "additionalProperties": false
    }
  }
}
```

**Supported JSON Schema types in strict mode:**
| Type | Description |
|---|---|
| `object` | Nested structure with `properties`, `required`, `additionalProperties` |
| `string` | Text values |
| `number` | Numeric values |
| `integer` | Whole numbers |
| `boolean` | True/false values |
| `array` | Lists of items (with `items` schema) |
| `enum` | Enumerated values |
| `anyOf` | Multiple possible type schemas |

**object** — Defines a nested structure:
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"}
  },
  "required": ["name", "age"],
  "additionalProperties": false
}
```

**string with constraints** — Supports `format`, `pattern`, `description`:
```json
{
  "type": "object",
  "properties": {
    "user_email": {
      "type": "string",
      "description": "The user's email address",
      "format": "email"
    },
    "zip_code": {
      "type": "string",
      "description": "Six digit postal code",
      "pattern": "^\\\\d{6}$"
    }
  }
}
```

**integer with range**:
```json
{
  "type": "object",
  "properties": {
    "score": {
      "type": "integer",
      "description": "A number from 1-5, higher is better",
      "minimum": 1,
      "maximum": 5
    }
  },
  "required": ["score"],
  "additionalProperties": false
}
```

**array with item schema**:
```json
{
  "type": "object",
  "properties": {
    "keywords": {
      "type": "array",
      "description": "Five keywords of the article, sorted by importance",
      "items": {
        "type": "string",
        "description": "A concise and accurate keyword or phrase."
      }
    }
  },
  "required": ["keywords"],
  "additionalProperties": false
}
```

**enum**:
```json
{
  "type": "object",
  "properties": {
    "order_status": {
      "type": "string",
      "description": "Ordering status",
      "enum": ["pending", "processing", "shipped", "cancelled"]
    }
  }
}
```

**anyOf** — Multiple possible types:
```json
{
  "type": "object",
  "properties": {
    "account": {
      "anyOf": [
        {"type": "string", "format": "email", "description": "Email address"},
        {"type": "string", "pattern": "^\\\\d{11}$", "description": "11-digit phone number"}
      ]
    }
  }
}
```

**Nested $ref (strict mode supports $def):**
```json
{
  "type": "object",
  "properties": {
    "report_date": {"type": "string", "description": "The date when the report was published"},
    "authors": {
      "type": "array",
      "description": "The authors of the report",
      "items": {"$ref": "#/$def/author"}
    }
  },
  "required": ["report_date", "authors"],
  "additionalProperties": false,
  "$def": {
    "author": {
      "type": "object",
      "properties": {
        "name": {"type": "string", "description": "author's name"},
        "institution": {"type": "string", "description": "author's institution"},
        "email": {"type": "string", "format": "email", "description": "author's email"}
      },
      "additionalProperties": false,
      "required": ["name", "institution", "email"]
    }
  }
}
```

---

### 6.5 JSON Output (Structured Output)

**What it does**: Ensures the model outputs valid JSON strings, enabling reliable structured output parsing.

**Why it exists**: Many applications need machine-parseable structured data from the model.

**How to enable:**
1. Set `response_format: {"type": "json_object"}` in the request
2. Include the word "json" in the system or user prompt
3. Provide an example of the desired JSON format in the prompt
4. Set `max_tokens` reasonably to prevent truncation

**Limitations:**
- The API may occasionally return empty content (being optimized)
- You may need to modify the prompt to mitigate empty responses

**Example:**
```python
from openai import OpenAI

client = OpenAI(api_key="<your-key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
        {"role": "user", "content": "Extract the name, age, and city from: 'John is 30 years old and lives in New York.' Return as JSON."}
    ],
    response_format={"type": "json_object"}
)

print(response.choices[0].message.content)
# {"name": "John", "age": 30, "city": "New York"}
```

---

### 6.6 Context Caching

**What it does**: The DeepSeek API Context Caching on Disk Technology automatically caches overlapping prefixes across requests, reducing cost for repeated or similar requests.

**Why it exists**: To reduce costs and latency for applications where system prompts, few-shot examples, or long document prefixes are reused across requests.

**How it works:**
- Enabled by default for all users — no code changes needed
- Each request triggers construction of a hard disk cache
- Subsequent requests with overlapping prefixes benefit from cache hits
- Cache hits are billed at a significantly lower rate (see [Pricing](#pricing))

#### Cache Persistence and Hit Rules

A cache hit requires that the corresponding prefix has already been "persisted" (written to the disk cache). Due to the Sliding Window Attention mechanism, each cached prefix is an **independent, complete unit**. A subsequent request can only hit the cache if it **fully matches** a cache prefix unit.

**When cache prefixes are persisted:**

1. **Persistence at request boundaries**: Each request produces two cache prefix units at the end position of the user input and the end position of the model output. Subsequent requests can hit the cache if they fully match these units.

2. **Common prefix detection persistence**: When the system detects a common prefix across multiple requests, it persists that common prefix as an independent cache prefix unit. Subsequent requests can hit the cache if they fully reuse that cache prefix unit.

3. **Persistence at fixed token intervals**: For long inputs or long outputs, the system carves out cache prefix units at fixed token intervals to prevent long prefixes from being uncacheable.

**Example 1 (Cache Hit):**
```
Request 1: A + B
Request 2: A + B + C
```
Result: Request 2 fully matches the cache prefix unit A + B, hitting the cache for A + B.

**Example 2 (Cache Miss):**
```
Request 1: A + B
Request 2: A + C
```
Result: Request 2 cannot hit the cache because A + C does not fully match the first round's cache prefix unit (A + B).

**Example with shared system prompt:**
```
Request 1: [long system prompt about financial analysis] + "Please summarize the key information"
Request 2: [same long system prompt] + "Please analyze the profitability"
```
Result: If the system detects the common prefix of the long system prompt across requests, it will persist and cache it. Request 2 reuses that common prefix and hits the cache for it.

#### Usage Tracking

The response includes cache metrics:
```json
"usage": {
  "prompt_cache_hit_tokens": 500,
  "prompt_cache_miss_tokens": 200
}
```

#### Cost Implications

| | Cache Hit | Cache Miss |
|---|---|---|
| deepseek-v4-flash input | $0.0028/1M tokens | $0.14/1M tokens |
| deepseek-v4-pro input | $0.003625/1M tokens | $0.435/1M tokens |

Cache hits offer approximately **50x** cost reduction for input tokens.

---

### 6.7 Chat Prefix Completion (Beta)

**What it does**: Provides an assistant prefix message for the model to complete. The user supplies the beginning of an assistant response, and the model fills in the rest.

**Why it exists**: Enables use cases where you want the model to start from a specific point (e.g., completing a code block after a known prefix).

**Requirements:**
- The last message in the `messages` list must have `role: "assistant"`
- Set `prefix: true` on the last assistant message
- Use `base_url="https://api.deepseek.com/beta"` to enable Beta features
- Can combine with `stop` parameter to prevent additional output

**Example:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-key>",
    base_url="https://api.deepseek.com/beta"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers"},
        {"role": "assistant", "content": "```python\n", "prefix": True}
    ],
    stop=["```"],
    max_tokens=512
)
```

---

### 6.8 FIM (Fill-in-the-Middle)

**What it does**: Given a prefix (and optional suffix), the model completes the content in between.

**Why it exists**: Essential for code completion — given the code before and after the cursor position, the model fills in what should go in between.

**Requirements:**
- Use `base_url="https://api.deepseek.com/beta"` to enable Beta features
- Max tokens: 4K
- Supported in non-thinking mode only

**Example:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-key>",
    base_url="https://api.deepseek.com/beta"
)

response = client.completions.create(
    model="deepseek-v4-pro",
    prompt="def fibonacci(n):\n    ",
    suffix="\n    return result",
    max_tokens=128
)
```

**Integration with Continue.dev:**
[Continue](https://continue.dev) is a VS Code plugin that supports code completion via DeepSeek. Refer to [this guide](https://github.com/deepseek-ai/awesome-deepseek-integration/blob/main/docs/continue/README_cn.md) for configuration.

---

## 7. OpenAI Compatibility

The DeepSeek API is fully compatible with the **OpenAI Chat Completions API format**. You can use the OpenAI SDK (`openai` Python package, `openai` npm package) with minimal configuration changes.

### Configuration Differences

| Parameter | OpenAI | DeepSeek |
|---|---|---|
| `base_url` | `https://api.openai.com/v1` | `https://api.deepseek.com` |
| `api_key` | OpenAI API key | DeepSeek API key |
| `model` | `gpt-4`, `gpt-3.5-turbo`, etc. | `deepseek-v4-pro`, `deepseek-v4-flash` |
| Thinking mode | Not natively supported | Via `extra_body: {"thinking": {...}}` |
| `reasoning_effort` | Not supported | Via direct parameter |

### Migration Steps

1. Change `base_url` to `https://api.deepseek.com`
2. Replace API key with a DeepSeek API key
3. Change model to `deepseek-v4-pro` or `deepseek-v4-flash`
4. (Optional) Add `extra_body: {"thinking": {"type": "enabled"}}` for thinking mode
5. (Optional) Add `reasoning_effort` parameter

### Forward Compatibility

DeepSeek supports most OpenAI request parameters. Unsupported or deprecated parameters (like `frequency_penalty`, `presence_penalty` in thinking mode) are silently ignored rather than rejected, ensuring compatibility with existing OpenAI-based tools and libraries.

### Limitations vs OpenAI

| Feature | OpenAI | DeepSeek |
|---|---|---|
| Vision/Images | Yes (GPT-4V) | No (text-only; see agent integrations for proxy workaround) |
| TTS / Speech | Yes | Not documented |
| Embeddings | Yes | Not documented |
| Fine-tuning | Yes | Not documented |
| Moderation | Yes | Not documented |
| Assistants API | Yes | Not documented |

---

## 8. Anthropic API Compatibility

The DeepSeek API also supports the **Anthropic API format** at `https://api.deepseek.com/anthropic`.

### Configuration

```
base_url: https://api.deepseek.com/anthropic
api_key:  <DeepSeek API key (starts with sk-)>
```

### Model Mapping

When using the Anthropic API, Claude model names are automatically mapped:

| Claude Model Pattern | Mapped To |
|---|---|
| `claude-opus*` | `deepseek-v4-pro` |
| `claude-haiku*` | `deepseek-v4-flash` |
| `claude-sonnet*` | `deepseek-v4-flash` |
| Any unsupported name | `deepseek-v4-flash` |

This mapping is useful for tools like Claude Desktop APP developer mode — just change the `base_url` and `api_key`.

### Compatibility Details

**HTTP Headers:**
| Field | Support Status |
|---|---|
| `anthropic-beta` | Ignored |
| `anthropic-version` | Ignored |
| `x-api-key` | Fully Supported |

**Message Fields:**
Most Anthropic message fields are supported with equivalent DeepSeek functionality.

**Thinking Mode via Anthropic Format:**
```json
{
  "output_config": {
    "effort": "high"
  }
}
```

### Using the Anthropic SDK

#### Python
```python
from anthropic import Anthropic

client = Anthropic(
    api_key="<deepseek-api-key>",
    base_url="https://api.deepseek.com/anthropic"
)

message = client.messages.create(
    model="claude-opus-4-20250514",  # mapped to deepseek-v4-pro
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, world"}
    ]
)
print(message.content[0].text)
```

#### Environment Variables
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<deepseek-api-key>
```

> **Note**: When you pass an unsupported model name to the DeepSeek Anthropic API, it will automatically map to `deepseek-v4-flash`.

---

## 9. Agent Integrations

DeepSeek integrates with popular AI agent and coding assistant tools. These are third-party integrations listed for developer reference. DeepSeek does not guarantee effectiveness or security.

### Claude Code

[Claude Code](https://github.com/anthropics/claude-code) is an AI coding assistant that runs in the terminal.

**Environment variables for Claude Code:**
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<deepseek-api-key>
export ANTHROPIC_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

**Installation from scratch:**
```bash
npm install -g @anthropic-ai/claude-code
claude --version
# Configure env vars as above
cd /path/to/my-project
claude
```

### GitHub Copilot

A VS Code extension that adds DeepSeek V4 Pro & Flash into the Copilot Chat model picker.

**Requirements:**
- VS Code 1.116 or later
- GitHub Copilot subscription (free tier works)
- DeepSeek V4 for Copilot Chat extension (from GitHub)

**Configuration:**
1. Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Run **DeepSeek: Set API Key** and paste your key
3. Open Copilot Chat (`Cmd+Shift+I` / `Ctrl+Shift+I`)
4. Click the model picker and choose **DeepSeek V4 Pro** or **DeepSeek V4 Flash**

**Vision support**: DeepSeek V4 is text-only, but the extension proxies images through another Copilot model (Claude, GPT-4o) before sending to DeepSeek.

### OpenCode

[OpenCode](https://github.com/sst/opencode) is an open-source AI coding assistant (version >= v1.14.24 recommended).

**Configuration:**
1. Run `opencode`
2. Type `/connect`, enter `deepseek`, select the provider
3. Enter your DeepSeek API key
4. Select the DeepSeek-V4-Pro model

---

## 10. Rate Limits & Isolation

### Concurrency Limits

| Model | Concurrency Limit |
|---|---|
| `deepseek-v4-pro` | 500 |
| `deepseek-v4-flash` | 2500 |

- A request counts as one concurrent connection from the time it is sent until the model response is complete
- Concurrency limits are calculated at the **account level**, regardless of which API Key is used
- Requests within the limit receive a response; requests exceeding the limit receive HTTP 429
- To request higher concurrency, submit a [capacity expansion request](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnda9jNKvhyYr8xb843xLEzc). There is no additional cost.

### user_id Isolation

The `user` parameter (`user_id`) enables fine-grained management of different end-users under the same account.

**Functions of user_id:**
- **Content Safety Isolation**: Distinguishes user identities for content safety handling
- **KVCache Isolation**: Isolates KVCache for privacy management
- **Scheduling Isolation**: Schedules users separately

**Concurrency behavior with user_id:**
- For regular API users: all user_id values are combined for concurrency limit calculation
- For users with increased quotas: total concurrency is limited per account AND per user_id
- Per-user_id limits: deepseek-v4-pro = 500, deepseek-v4-flash = 2500
- An empty id is treated as a special user_id
- Exceeding the per-user_id limit returns HTTP 429

**Setting user_id:**
```python
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[...],
    user="user_abc_123"  # Must be a string
)
```

---

## 11. Error Codes & Handling

### Error Reference

| Code | Name | Cause | Solution |
|---|---|---|---|
| 400 | Invalid Format | Invalid request body format | Modify request body according to error message hints |
| 401 | Authentication Fails | Wrong API key | Check your API key; create one if needed |
| 402 | Insufficient Balance | Run out of balance | Check balance and top up |
| 422 | Invalid Parameters | Request contains invalid parameters | Modify parameters according to error message hints |
| 429 | Rate Limit Reached | Sending requests too quickly | Pace requests reasonably; temporarily switch to alternative providers |
| 500 | Server Error | Server encounters an issue | Retry after a brief wait; contact support if issue persists |
| 503 | Server Overloaded | Server overloaded due to high traffic | Retry after a brief wait |

### Retry Strategy

**Recommended approach: Exponential backoff with jitter**

```python
import time
import random
from openai import OpenAI

client = OpenAI(api_key="<key>", base_url="https://api.deepseek.com")

def retry_with_backoff(func, max_retries=5, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            if "429" in str(e) or "500" in str(e) or "503" in str(e):
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                print(f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}")
                time.sleep(delay)
            else:
                raise  # Non-retryable error

response = retry_with_backoff(lambda: client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "Hello"}]
))
```

### Common HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad Request — check request format |
| 401 | Unauthorized — check API key |
| 402 | Payment Required — insufficient balance |
| 422 | Unprocessable Entity — invalid parameters |
| 429 | Too Many Requests — rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## 12. Token Usage

### What is a Token?

Tokens are the basic units used by models to represent natural language text and are the units used for billing. Typically:
- A Chinese word, an English word, a number, or a symbol counts as approximately one token
- **1 English character** ≈ 0.3 token
- **1 Chinese character** ≈ 0.6 token

> Note: Conversion ratios vary by model. The actual number of tokens is based on the model's return, visible in the `usage` field of responses.

### Offline Tokenizer

Download the offline tokenizer for estimating token usage:
[deepseek_tokenizer.zip](https://cdn.deepseek.com/api-docs/deepseek_v3_tokenizer.zip)

### Viewing Usage in Responses

Every response includes a `usage` object:
```json
"usage": {
  "prompt_tokens": 45,
  "completion_tokens": 120,
  "total_tokens": 165,
  "prompt_cache_hit_tokens": 30,
  "prompt_cache_miss_tokens": 15
}
```

---

## 13. SDK Examples

### 13.1 Non-streaming (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are an expert Python developer."},
        {"role": "user", "content": "Write a binary search function in Python."}
    ],
    temperature=0.3,
    max_tokens=2000
)

print(response.choices[0].message.content)
print(f"Usage: {response.usage}")
```

### 13.2 Streaming (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

stream = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    stream=True,
    stream_options={"include_usage": True}
)

full_response = ""
for chunk in stream:
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
        full_response += content
        print(content, end="", flush=True)
    if chunk.usage:
        print(f"\n\n[Usage: {chunk.usage}]")
```

### 13.3 Streaming with Reasoning (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

stream = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "user", "content": "Solve: If x + 2y = 10 and 3x - y = 5, find x and y."}
    ],
    stream=True,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print("=== Reasoning ===")
for chunk in stream:
    if chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
    elif chunk.choices[0].delta.content:
        if not hasattr(stream, '_reasoning_done'):
            print("\n=== Answer ===")
            stream._reasoning_done = True
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 13.4 Tool Calling (Python)

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search the database for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def run_conversation():
    messages = [
        {"role": "user", "content": "Search the database for 'active users'"}
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        # Execute the function call
        for tool_call in message.tool_calls:
            if tool_call.function.name == "search_database":
                args = json.loads(tool_call.function.arguments)
                # Simulate function execution
                result = f"Found 42 active users matching '{args['query']}'"

                # Add results back to messages
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        # Get final response
        final_response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            tools=tools
        )
        return final_response.choices[0].message.content

    return message.content
```

### 13.5 Structured Output / JSON Extraction (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {
            "role": "system",
            "content": "You are a data extraction assistant. Output valid JSON."
        },
        {
            "role": "user",
            "content": """
            Extract the following information as JSON from this email:
            From: jane@example.com
            Subject: Meeting Request
            Body: Hi, can we schedule a meeting on Friday at 2pm? Please bring the Q3 report.
            
            Return: {
                "sender_email": "...",
                "subject": "...",
                "requested_meeting": true,
                "date": "...",
                "time": "...",
                "mentioned_documents": ["..."]
            }
            """
        }
    ],
    response_format={"type": "json_object"},
    max_tokens=500
)

import json
data = json.loads(response.choices[0].message.content)
print(data)
```

### 13.6 Reasoning Mode with Error Handling (TypeScript)

```typescript
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DEEPSEEK_API_KEY!,
    baseURL: "https://api.deepseek.com",
});

async function thinkAndRespond(prompt: string, maxRetries = 3): Promise<string> {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await client.chat.completions.create({
                model: "deepseek-v4-pro",
                messages: [{ role: "user", content: prompt }],
                reasoning_effort: "high",
                extra_body: { thinking: { type: "enabled" } },
                max_tokens: 4000,
            });

            const message = response.choices[0].message;
            return message.content ?? "";
        } catch (error: any) {
            if (error.status === 429) {
                const delay = Math.pow(2, attempt) * 1000;
                console.warn(`Rate limited. Retrying in ${delay}ms...`);
                await new Promise(r => setTimeout(r, delay));
                continue;
            }
            if (error.status === 402) {
                throw new Error("Insufficient balance. Please top up.");
            }
            throw error;
        }
    }
    throw new Error("Max retries exceeded");
}

// Usage
thinkAndRespond("What is the difference between TCP and UDP?")
    .then(console.log)
    .catch(console.error);
```

### 13.7 Streaming with Timeout (Node.js)

```typescript
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DEEPSEEK_API_KEY!,
    baseURL: "https://api.deepseek.com",
    timeout: 30000,  // 30 second timeout
    maxRetries: 3,
});

async function streamResponse(prompt: string): Promise<string> {
    const stream = await client.chat.completions.create({
        model: "deepseek-v4-flash",
        messages: [{ role: "user", content: prompt }],
        stream: true,
    });

    let full = "";
    for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content || "";
        full += content;
        process.stdout.write(content);
    }
    return full;
}
```

### 13.8 Multi-turn Conversation (Python)

```python
from openai import OpenAI

client = OpenAI(api_key="<key>", base_url="https://api.deepseek.com")

messages = [
    {"role": "system", "content": "You are a helpful travel assistant."}
]

def chat(user_input: str) -> str:
    global messages
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages
    )

    assistant_msg = response.choices[0].message
    messages.append({
        "role": "assistant",
        "content": assistant_msg.content
    })
    return assistant_msg.content

# Multi-turn conversation
print(chat("What are the best places to visit in Japan?"))
print(chat("How much would a 10-day trip cost?"))
print(chat("What about accommodations in Tokyo?"))
```

---

## 14. Best Practices

### Production Deployment

1. **Use environment variables** for API keys — never hardcode them
2. **Implement retry logic** with exponential backoff for 429, 500, and 503 errors
3. **Set timeouts** appropriate to your use case (30s for real-time, 60-120s for complex reasoning)
4. **Monitor token usage** and set budget alerts
5. **Use the Flash model** for simple tasks and the Pro model only when needed
6. **Cache responses** for idempotent requests to reduce cost and latency

### Prompt Engineering

1. **System prompts**: Be specific and detailed about the assistant's role and behavior
2. **Few-shot examples**: Include 2-3 examples for complex formatting tasks
3. **JSON output**: Always include the word "json" in the prompt and provide the schema
4. **Chain-of-thought**: For complex reasoning, use thinking mode rather than asking for step-by-step in the prompt
5. **Be explicit**: State constraints and output format requirements clearly

### Token Optimization

1. **Use caching**: Design prompts with a stable system prompt prefix to maximize cache hits
2. **Trim conversation history**: For long conversations, summarize older turns instead of including them verbatim
3. **Set max_tokens**: Always set a reasonable `max_tokens` to prevent unexpectedly long responses
4. **Use Flash for drafts**: Generate first drafts with Flash, then refine with Pro
5. **Minimize system prompt length**: Remove unnecessary instructions and examples

### Latency Optimization

| Technique | Model | Expected Improvement |
|---|---|---|
| Use `deepseek-v4-flash` | Flash | 3-5x faster than Pro |
| Disable thinking mode | Both | 2-4x lower TTFT |
| Lower `max_tokens` | Both | Directly proportional |
| Use streaming | Both | Lower perceived latency |
| Enable caching | Both | Lower TTFT on cache hit |

### Cost Optimization

1. **Cache hits are ~50x cheaper**: Design stable system prompts to maximize cache hits
2. **Use Flash for simple tasks**: Reserve Pro for complex reasoning
3. **Short system prompts**: Minimize input tokens
4. **Batch similar requests**: Group requests sharing a common prefix for cache benefits
5. **Monitor usage**: Track `prompt_cache_hit_tokens` vs `prompt_cache_miss_tokens`
6. **Set budget alerts** on the DeepSeek Platform

### Security

1. **Rotate API keys** regularly
2. **Use separate keys** for different environments or applications
3. **Validate and sanitize** model outputs before using them in your application
4. **Use user_id** for content safety isolation in multi-tenant applications
5. **Never expose API keys** in client-side code, logs, or version control

### Logging & Monitoring

1. **Log request IDs** (`id` in response) for debugging
2. **Track token usage** per user, per session, and per day
3. **Monitor error rates** by error code (especially 429, 500, 503)
4. **Alert on balance depletion** using the `/user/balance` endpoint
5. **Log response quality** metrics for continuous improvement

---

## 15. Production Examples

### 15.1 Chatbot (Full Implementation)

```python
import os
import json
from openai import OpenAI
from typing import List, Dict

class DeepSeekChatbot:
    def __init__(self, model: str = "deepseek-v4-flash"):
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )
        self.model = model
        self.system_prompt = "You are a helpful, friendly assistant."

    def chat(self, messages: List[Dict], stream: bool = False):
        full_messages = [
            {"role": "system", "content": self.system_prompt}
        ] + messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            stream=stream,
            max_tokens=2000
        )

        if stream:
            return self._handle_stream(response)
        return response.choices[0].message.content

    def _handle_stream(self, stream):
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

# Usage
bot = DeepSeekChatbot(model="deepseek-v4-flash")
for token in bot.chat(
    [{"role": "user", "content": "Tell me a joke about programming"}],
    stream=True
):
    print(token, end="", flush=True)
```

### 15.2 Coding Assistant

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

def review_code(code: str, language: str = "python"):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": f"You are an expert {language} code reviewer."},
            {"role": "user", "content": f"Review this {language} code and suggest improvements:\n\n```{language}\n{code}\n```"}
        ],
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
        max_tokens=4000
    )
    return response.choices[0].message.content

def generate_code(description: str, language: str = "python"):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": f"You are an expert {language} developer. Write clean, well-documented code."},
            {"role": "user", "content": description}
        ],
        max_tokens=4000
    )
    return response.choices[0].message.content

# Usage
code_snippet = """
def calc(a,b):
    return a*b+2
"""
print(review_code(code_snippet))
print(generate_code("Write a function that merges two sorted lists"))
```

### 15.3 Agent with Tool Calling

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# Define tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time for a timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"}
                },
                "required": ["timezone"]
            }
        }
    }
]

def execute_function(name: str, args: dict) -> str:
    if name == "get_weather":
        return json.dumps({"temperature": 22, "condition": "sunny", "location": args["location"]})
    elif name == "get_time":
        return json.dumps({"time": "14:30", "timezone": args.get("timezone", "UTC")})
    return json.dumps({"error": "Unknown function"})

def agent_loop(user_input: str, max_turns: int = 5):
    messages = [{"role": "user", "content": user_input}]

    for turn in range(max_turns):
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = execute_function(tool_call.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return messages[-1].content

# Usage
print(agent_loop("What's the weather in Tokyo and what time is it in London?"))
```

### 15.4 RAG Pipeline

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

class SimpleRAG:
    def __init__(self, documents: list):
        self.documents = documents

    def retrieve(self, query: str, top_k: int = 3) -> str:
        # Simple keyword-based retrieval for demonstration
        # In production, use embeddings + vector search
        query_terms = set(query.lower().split())
        scored = []
        for doc in self.documents:
            doc_terms = set(doc.lower().split())
            score = len(query_terms & doc_terms)
            scored.append((score, doc))
        scored.sort(reverse=True)
        return "\n\n".join(doc for _, doc in scored[:top_k])

    def query(self, question: str) -> str:
        context = self.retrieve(question)
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer questions based on the provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer based only on the context provided."}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content

# Usage
documents = [
    "DeepSeek API supports OpenAI and Anthropic compatible endpoints.",
    "Context caching reduces costs by 50x for repeated prefixes.",
    "Thinking mode enables chain-of-thought reasoning before answering."
]
rag = SimpleRAG(documents)
print(rag.query("How does context caching work?"))
```

### 15.5 Streaming UI (FastAPI + SSE)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

@app.post("/chat")
async def chat(prompt: str):
    async def generate():
        stream = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 15.6 JSON Data Extraction Pipeline

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

def extract_entities(text: str) -> dict:
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "Extract entities from text as JSON."},
            {"role": "user", "content": f"Extract: persons (name, role), organizations, dates, and locations from:\n\n{text}\n\nReturn valid JSON."}
        ],
        response_format={"type": "json_object"},
        max_tokens=2000
    )
    return json.loads(response.choices[0].message.content)

# Batch processing
texts = [
    "John Smith was hired as CEO of TechCorp on January 15, 2024 in San Francisco.",
    "Microsoft announced a partnership with OpenAI in Seattle on November 1, 2023."
]

for text in texts:
    entities = extract_entities(text)
    print(json.dumps(entities, indent=2))
```

---

## 16. Changelog

### 2026-04-24 — DeepSeek-V4 Release

**DeepSeek-V4 Preview is officially live and open-sourced.**

- **deepseek-v4-pro**: 1.6T total / 49B active parameters. Performance rivaling top closed-source models.
- **deepseek-v4-flash**: 284B total / 13B active parameters. Fast, efficient, and economical.
- Context length: **1M tokens** (default for all models)
- Maximum output: **384K tokens**
- Novel attention mechanisms: Token-wise compression + DSA (DeepSeek Sparse Attention)
- Enhanced agentic capabilities, rich world knowledge, world-class reasoning

**Deprecation notice**: The legacy model names `deepseek-chat` and `deepseek-reasoner` will be discontinued on **2026-07-24 15:59 UTC**. During the transition, these names map to the non-thinking and thinking modes of `deepseek-v4-flash`, respectively.

### 2025-12-01 — DeepSeek-V3.2 Release

- Both `deepseek-chat` and `deepseek-reasoner` upgraded to DeepSeek-V3.2
- `deepseek-chat` = V3.2 non-thinking mode
- `deepseek-reasoner` = V3.2 thinking mode
- First model to integrate thinking directly into tool-use
- Introduced massive agent training data synthesis (1,800+ environments, 85k+ instructions)
- V3.2-Speciale: Temporary endpoint at `base_url="https://api.deepseek.com/v3.2_speciale_expires_on_20251215"`. API-only, no tool calls, available until Dec 15, 2025.

### 2025-09-29 — DeepSeek-V3.2-Exp Release

- Both `deepseek-chat` and `deepseek-reasoner` upgraded to V3.2-Exp
- Debuted DeepSeek Sparse Attention (DSA)
- API prices cut by 50%+
- V3.1-Terminus remained available for comparison testing until Oct 15, 2025

### 2025-09-22 — DeepSeek-V3.1-Terminus Release

- Both models upgraded to V3.1-Terminus
- Fixes: Reduced Chinese-English mixing, improved agent capabilities (Code Agent, Search Agent)

### 2025-08-21 — DeepSeek-V3.1 Release

- Both models upgraded to DeepSeek-V3.1
- Hybrid reasoning architecture: Single model supports both thinking and non-thinking modes
- Improved reasoning efficiency (faster than R1-0528)
- Enhanced agent capabilities
- Benchmarks: SWE-bench Verified 66.0, SWE-bench Multilingual 54.5, Terminal-bench 31.3

### 2025-05-28 — deepseek-reasoner Upgraded to R1-0528

- Enhanced reasoning: AIME 2025: 70.0 → 87.5, GPQA: 71.5 → 81.0, LCB_v6: 63.5 → 73.3, Aider: 57.0 → 71.6
- Optimized front-end development
- Reduced hallucinations
- JSON Output and Function Calling support for deepseek-reasoner

### 2025-03-24 — deepseek-chat Upgraded to V3-0324

- MMLU-Pro: 75.9 → 81.2, GPQA: 59.1 → 68.4, AIME: 39.6 → 59.4, LiveCodeBench: 39.2 → 49.2
- Optimized front-end web development

### Earlier Releases

| Date | Event |
|---|---|
| 2025-01-20 | DeepSeek-R1 Release |
| 2025-01-15 | DeepSeek App Launch |
| 2024-12-26 | Model update |
| 2024-12-10 | Model update |
| 2024-11-20 | Model update |
| 2024-09-05 | Model update |
| 2024-08-02 | Model update |
| 2024-07-25 | Model update |

### Deprecation Timeline

| Item | Deprecation Date |
|---|---|
| `deepseek-chat` model name | 2026-07-24 15:59 UTC |
| `deepseek-reasoner` model name | 2026-07-24 15:59 UTC |
| V3.2-Speciale endpoint | 2025-12-15 15:59 UTC (expired) |
| V3.1-Terminus comparison endpoint | 2025-10-15 15:59 UTC (expired) |

**Migration path**: Replace `deepseek-chat` with `deepseek-v4-flash` (for non-thinking mode) and `deepseek-reasoner` with `deepseek-v4-flash` with thinking enabled.

---

## 17. Hidden Details & Edge Cases

### Undocumented Caveats

1. **Empty JSON responses**: When using JSON Output, the API may occasionally return empty content. DeepSeek is actively optimizing this. Workaround: modify the prompt to be more specific.

2. **Silent parameter ignoring**: Parameters like `temperature`, `top_p`, `presence_penalty`, and `frequency_penalty` have no effect in thinking mode but do not trigger errors. This is by design for compatibility.

3. **reasoning_content behavior**: 
   - When the model did NOT perform a tool call between two user messages, `reasoning_content` from the intermediate assistant can be dropped
   - When the model DID perform a tool call, `reasoning_content` MUST be included in subsequent turns
   - If sent in a context where it's not needed, the API silently ignores it

4. **Anthropic model fallback**: Any model name that doesn't match the known Claude patterns maps to `deepseek-v4-flash`, not the Pro model.

5. **Beta features require base_url change**: Chat Prefix Completion, FIM Completion, and strict mode all require `base_url="https://api.deepseek.com/beta"`.

### Compatibility Quirks

6. **OpenAI SDK `extra_body` requirement**: The `thinking` parameter must be sent via `extra_body` in the OpenAI SDK because it's a DeepSeek-specific parameter not in the OpenAI spec.

7. **Anthropic `x-api-key`**: The Anthropic SDK uses `x-api-key` header for auth. DeepSeek fully supports this.

8. **Anthropic `anthropic-version` and `anthropic-beta` headers**: These are ignored by DeepSeek. Set them if your SDK requires them, but they have no effect.

9. **Model name unsupported in Anthropic format**: Unsupported Anthropic model names are silently mapped to flash, not rejected. This means typos won't fail but may silently underperform.

### Edge Cases

10. **Empty user_id**: An empty string `user_id` is treated as a special, separate user_id for isolation purposes.

11. **Concurrent requests from same user_id**: For accounts with expanded quotas, each `user_id` has its own concurrency limit (500 for pro, 2500 for flash).

12. **Cache miss vs cache hit**: Cache hits require an EXACT match of an entire cache prefix unit. Partial overlaps do NOT trigger cache hits.

13. **Cache persistence timing**: Cache prefixes are persisted at request boundaries, on common prefix detection, and at fixed token intervals. A first request to a new system prompt will always be a cache miss.

14. **Context window implications**: With 1M context length and 384K max output, a single request could theoretically generate very large responses. Always set `max_tokens` to avoid surprises.

15. **Deprecated model names still work (for now)**: `deepseek-chat` and `deepseek-reasoner` are still functional but map to `deepseek-v4-flash`. They will be fully removed on 2026-07-24.

16. **The `stop` parameter exclusion**: The returned text will NOT contain the stop sequence, but token counts may still include it depending on implementation. Always verify.

---

> **Contact**: api-service@deepseek.com
>
> **Terms of Service**: https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html
>
> **Platform**: https://platform.deepseek.com
>
> **GitHub Integrations**: https://github.com/deepseek-ai/awesome-deepseek-integration
>
> **FAQ**: https://static.deepseek.com/faq/index.html?lang=en#/category/4
>
> **License**: MIT
