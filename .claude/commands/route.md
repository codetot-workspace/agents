---
description: Route a task to the cheapest capable agent (local-first)
argument-hint: <task description>
---

Route the task from $ARGUMENTS to the cheapest agent that can handle it. **Local models first, DeepSeek for reliability, Claude only as last resort.**

## Step 1: Classify complexity

Read $ARGUMENTS and classify:

- **L1 (trivial)**: One-shot question, format conversion, commit message, simple code gen → Local model or DeepSeek
- **L2 (moderate)**: Code review, single-file refactor, bug in isolated code, text analysis → DeepSeek or local model
- **L3 (complex)**: Multi-file changes, architectural reasoning, debugging with context → Claude subagent

## Step 2: Check local agent availability

```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:11434/v1/models  # Ollama
```
Use Bash tool with `timeout: 5000`.

## Step 3: Execute

**IMPORTANT: Always set Bash timeout. Never let agent calls hang.**

**For L1 tasks — cheapest available:**
```bash
# Prefer Ollama REST API (free, local — NEVER use `ollama run` interactively)
curl -s --max-time 60 http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"TASK","stream":false}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"

# Fallback: DeepSeek (cheap, reliable)
opencode run -m deepseek/deepseek-chat "TASK"
```

**For L2 tasks — best quality at low cost:**
```bash
# Code tasks → DeepSeek (reliable, cheap)
opencode run -m deepseek/deepseek-chat "TASK"

# Hard reasoning → DeepSeek R1
opencode run -m deepseek/deepseek-reasoner "TASK"

# Text/review tasks → gemma4 via REST API
curl -s --max-time 120 http://localhost:11434/api/generate \
  -d '{"model":"gemma4","prompt":"TASK","stream":false}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
```

**For code review specifically — run multi-agent consensus:**
Run on 2 models in parallel, compare outputs, report agreements and disagreements.

## Step 4: Validate output

- If output is valid and complete → use it, report which agent handled it
- If output is partial → fix only the gaps yourself, credit the agent
- If output is garbage → escalate to next tier, note the failure
- If agent hangs/times out → kill it and try next option

## Step 5: Report

Format: `[AGENT_NAME] handled: TASK_SUMMARY — Quality: PASS/PARTIAL/FAIL`
