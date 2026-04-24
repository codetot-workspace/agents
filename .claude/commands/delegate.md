---
description: Delegate a task to a local AI agent. ALWAYS use this instead of doing mechanical work yourself.
argument-hint: <task description>
---

Delegate a task to a local AI agent. ALWAYS use this instead of doing mechanical work yourself.

## Step 1: Classify the task from $ARGUMENTS

Determine the task type:
- **code-gen**: Generate code from a spec or pattern
- **review**: Review/audit existing code
- **text**: SEO, translation, content tasks
- **edit**: Modify existing files (git-aware)
- **quick**: Simple one-shot question or transform
- **reasoning**: Complex logic, algorithms, hard problems

## Step 2: Pick the agent

| Task type | Primary agent | Fallback |
|-----------|--------------|----------|
| code-gen (reliable) | DeepSeek via OpenCode | Ollama qwen2.5-coder:14b |
| code-gen (free) | OpenCode (OpenRouter) | Ollama qwen2.5-coder:14b |
| reasoning (hard) | DeepSeek R1 via OpenCode | Gemini CLI |
| review | gemma4 (Ollama) | consensus (multi-agent) |
| text/translation | gemma4 (Ollama) | DeepSeek via OpenCode |
| edit (multi-file) | Goose | Claude |
| quick | Ollama qwen2.5-coder:7b | DeepSeek via OpenCode |

## Step 3: Run the agent

**IMPORTANT: Always set a timeout. Never let an agent call hang indefinitely.**

**DeepSeek via OpenCode (preferred — cheap, reliable, no rate limits):**
```bash
opencode run -m deepseek/deepseek-chat "TASK"
# For hard reasoning:
opencode run -m deepseek/deepseek-reasoner "TASK"
```
Use Bash tool with `timeout: 120000` (2 min).

**OpenCode via OpenRouter (free, may rate-limit):**
```bash
opencode run "TASK"
```
Use Bash tool with `timeout: 60000` (1 min).

**Ollama via REST API (local, no hanging — NEVER use `ollama run` interactively):**
```bash
curl -s --max-time 120 http://localhost:11434/api/generate \
  -d '{"model":"MODEL","prompt":"TASK","stream":false}' \
  | jq -r '.response'
```

**Goose (agentic execution):**
```bash
goose run -t "TASK" --no-session
```
Use Bash tool with `timeout: 180000` (3 min).

## Step 4: Evaluate the output

1. Did the agent produce valid, usable output? → Apply it
2. Was it partial or had errors? → Fix the specific issues yourself (don't redo the whole task)
3. Was it garbage? → Try the fallback agent from the table above
4. Still failing? → Do it yourself, but report: "Local agent couldn't handle: [reason]"

## Step 5: Report back

Tell the user:
- Which agent handled it
- Whether the output was used as-is or needed fixes
- Any quality notes for future routing decisions
