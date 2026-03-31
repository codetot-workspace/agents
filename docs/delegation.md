# Multi-Agent Delegation Guide

> How Claude Code assigns tasks to sub-agents from other AI providers

## 3 Approaches (Simple to Advanced)

### Approach 1: Bash Headless Mode (works now, zero setup)

Claude calls other agents via shell commands. Every major CLI agent supports non-interactive mode:

```bash
# Gemini CLI (free, 1000 req/day)
gemini -p "review this code for security issues: $(cat src/auth.ts)"

# Codex CLI (free with ChatGPT Plus)
codex exec "implement a rate limiter in src/ratelimit.ts" --full-auto --json

# Aider (BYOK, git-aware)
aider --message "refactor the auth module to use JWT" --yes-always --no-auto-commits src/auth.ts

# Goose (BYOK, MCP-native)
echo "write tests for the API routes" | goose run

# Ollama (fully local, zero cost)
ollama run qwen2.5-coder:14b "explain what this function does: $(cat src/utils.ts)"
```

**Pros:** Works immediately, no config needed.
**Cons:** Text-only interface, no structured tool calling.

### Approach 2: MCP Servers (structured tool integration)

Register other agents as MCP servers so Claude can call them as tools:

```bash
# Codex as MCP server (exposes codex tools to Claude)
claude mcp add codex -s project -- codex mcp-server

# Ollama via mcp-local-llm (exposes summarize, draft, classify tools)
git clone https://github.com/aplaceforallmystuff/mcp-local-llm.git
cd mcp-local-llm && npm install && npm run build
claude mcp add local-llm -s project -- node /path/to/mcp-local-llm/dist/index.js

# OllamaClaude (code-focused: generate, review, test tools)
git clone https://github.com/Jadael/OllamaClaude.git
cd OllamaClaude && npm install
claude mcp add ollama-code -s project -- node /path/to/OllamaClaude/index.js
```

**Pros:** Structured tools, Claude sees them natively, type-safe.
**Cons:** Requires setup per server.

### Approach 3: Custom Slash Commands (team workflows)

Create `.claude/commands/` files that define delegation patterns:

- `/project:delegate <task>` — Auto-pick best agent and delegate
- `/project:review-with <agent> <file>` — Get a review from another AI
- `/project:consensus <question>` — Ask multiple agents, find consensus

See `.claude/commands/` in this repo for implementations.

## Agent Headless Reference

| Agent | Headless Command | Output Format |
|-------|-----------------|---------------|
| Gemini CLI | `gemini -p "prompt"` | text (stdout) |
| Codex CLI | `codex exec "prompt" --json` | JSONL events |
| Codex Review | `codex review file --json` | JSONL events |
| Aider | `aider -m "prompt" --yes-always` | text + file edits |
| Goose | `echo "prompt" \| goose run` | text (stdout) |
| Ollama | `ollama run model "prompt"` | text (stdout) |
| OpenCode | `opencode run "prompt" --format json` | JSON |

## Task Routing Strategy

Route tasks to the cheapest capable agent:

```
Is it a simple question/summary?
  → Ollama local (free, fast)

Is it a code review or second opinion?
  → Gemini CLI (free, 1000/day)

Does it need multi-file git-aware edits?
  → Aider (best git integration)

Does it need full agentic execution?
  → Codex CLI or Goose

Is it complex reasoning or architecture?
  → Claude (keep in main context)
```

## CLAUDE.md Integration

Add this to any project's CLAUDE.md to enable delegation:

```markdown
## Sub-Agent Delegation

When a task is mechanical or benefits from a second opinion, delegate to a sub-agent:

- Simple summaries/transforms: `ollama run qwen2.5-coder:14b "TASK"`
- Code reviews: `gemini -p "review: $(cat FILE)"`
- File edits with git: `aider -m "TASK" --yes-always FILE`
- Full auto execution: `codex exec "TASK" --full-auto`

Always review sub-agent output before accepting. Report what the sub-agent did and flag any issues.
```

## Auth Setup Required

| Agent | Auth |
|-------|------|
| Gemini CLI | Run `gemini` once interactively to login with Google account |
| Codex CLI | Set `OPENAI_API_KEY` or login with `codex auth` |
| Aider | Set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or use `--model ollama_chat/MODEL` |
| Goose | Configure in `~/.config/goose/config.yaml` |
| Ollama | No auth needed (local) |
