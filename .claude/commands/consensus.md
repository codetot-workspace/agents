---
description: "Run a task across multiple AI agents and find consensus. Usage: /project:consensus <task>"
argument-hint: <task description>
---

Run $ARGUMENTS across multiple AI agents and find consensus.

**IMPORTANT: Always use Bash timeout. Never use interactive `ollama run` — use REST API instead.**

## Step 1: Run on 2-3 agents in parallel via Bash

Pick 2-3 from this list (use different model families for diversity):

**DeepSeek (cloud, cheap, reliable):**
```bash
opencode run -m deepseek/deepseek-chat "TASK"
```
Use Bash tool with `timeout: 120000`.

**Ollama local (free):**
```bash
curl -s --max-time 120 http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:14b","prompt":"TASK","stream":false}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
```

**Gemini CLI (free tier, large context):**
```bash
gemini -p "TASK"
```
Use Bash tool with `timeout: 120000`.

**Your own analysis (Claude):** Always include this as one of the opinions.

## Step 2: Compare all responses

## Step 3: Report
- What all agents agreed on (high confidence)
- Where they disagreed (needs human review)
- Your recommended answer with reasoning
