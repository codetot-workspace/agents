Delegate a task to a local AI agent. ALWAYS use this instead of doing mechanical work yourself.

## Step 1: Classify the task from $ARGUMENTS

Determine the task type:
- **code-gen**: Generate code from a spec or pattern
- **review**: Review/audit existing code
- **text**: SEO, translation, content tasks
- **edit**: Modify existing files (git-aware)
- **quick**: Simple one-shot question or transform

## Step 2: Pick the agent

| Task type | Primary agent | Fallback |
|-----------|--------------|----------|
| code-gen (simple) | Jan 4B via API | qwen2.5-coder:7b |
| code-gen (complex) | qwen2.5-coder:32b | goose |
| review | gemma4 | consensus (multi-agent) |
| text/translation | gemma4 | Jan 4B |
| edit (multi-file) | goose | Claude |
| quick | qwen2.5-coder:7b | Jan 4B |

## Step 3: Run the agent

**Jan (API — best for structured output):**
```bash
curl -s http://localhost:6767/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"janhq/Jan-v3-4b-base-instruct-Q4_K_XL","messages":[{"role":"system","content":"SYSTEM_PROMPT"},{"role":"user","content":"TASK"}],"temperature":0.3}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
```

**Ollama (CLI — best for quick tasks):**
```bash
ollama run MODEL "TASK"
```

**Goose (agentic execution):**
```bash
echo "TASK" | goose run
# or with a task file:
goose run -i task-file.md
```

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
