# Multi-Agent Delegation Guide

> How Claude Code assigns tasks to sub-agents from other AI providers

## 3 Approaches (Simple to Advanced)

### Approach 1: Bash Headless Mode (works now, zero setup)

Claude calls other agents via shell commands. Every major CLI agent supports non-interactive mode:

```bash
# Goose (BYOK, MCP-native)
goose run -i task-file.md
goose run -t "write tests for the API routes"

# Ollama (fully local, zero cost)
ollama run qwen2.5-coder:14b "explain what this function does: $(cat src/utils.ts)"
```

**Pros:** Works immediately, no config needed.
**Cons:** Text-only interface, no structured tool calling.

### Approach 2: MCP Servers (structured tool integration)

Register other agents as MCP servers so Claude can call them as tools:

```bash
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

| Agent | Headless Command | Output Format | Writes files? |
|-------|-----------------|---------------|---------------|
| Goose | `goose run -i file.md` | text (stdout) + tool calls | Yes (write_file tool) |
| Ollama | `curl localhost:11434/api/generate -d '{"model":"...","prompt":"..."}'` | JSON stream | No — text only |
| OpenCode | `OPENAI_API_KEY=$OPENROUTER_API_KEY opencode run -m openrouter/MODEL "$(cat task.md)"` | text (stdout) | Yes (native) |

> **Ollama note:** Never use `ollama run model "$(cat task)"` for large tasks — the TTY spinner
> escape codes swamp the output. Always use the REST API or `local_agents.py` instead.

### Confirmed working commands (tested 2026-04-15)

```bash
# Goose via OpenRouter (writes files, agentic)
GOOSE_MODEL="qwen/qwen3-coder-30b-a3b-instruct" goose run -i task.md

# OpenCode via OpenRouter (writes files, faster)
OPENAI_API_KEY=$OPENROUTER_API_KEY opencode run \
  -m openrouter/qwen/qwen3-coder-30b-a3b-instruct \
  "$(cat task.md)"

# Ollama via REST API (text only, local/free)
curl -s http://localhost:11434/api/generate \
  -d "{\"model\":\"qwen2.5-coder:32b\",\"prompt\":\"$(cat task.md)\",\"stream\":false}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"

# Ollama via local_agents.py (best for programmatic use)
python3 /Users/khoipro/Workspaces/Agents/local_agents.py
```

### Goose `run` Key Flags

| Flag | Description |
|------|-------------|
| `-i, --instructions <FILE>` | Read task from a Markdown file |
| `-t, --text <TEXT>` | Inline task text |
| `-s, --interactive` | Stay interactive after task completes |
| `-q, --quiet` | Only print model response |
| `-n, --name <NAME>` | Name the session (for `--resume`) |
| `-r, --resume` | Resume a previous named session |
| `--max-turns <N>` | Limit agent iterations |
| `--no-session` | Run without persisting session |
| `--provider <PROVIDER>` | Override provider (anthropic, openai, ollama) |
| `--model <MODEL>` | Override model for this run |
| `--system <TEXT>` | Additional system instructions |

## Task Routing Strategy

Route tasks to the cheapest capable agent:

```
Is it a simple question/summary?
  → Ollama local (free, fast)

Is it a code review or second opinion?
  → Ollama local (gemma4 or qwen2.5-coder)

Does it need full agentic execution (SSH, WP-CLI, multi-step)?
  → Goose (goose run -i task-file.md)

Is it complex reasoning or architecture?
  → Claude (keep in main context)
```

## CLAUDE.md Integration

Add this to any project's CLAUDE.md to enable delegation:

```markdown
## Sub-Agent Delegation

When a task is mechanical or benefits from a second opinion, delegate to a sub-agent:

- Simple summaries/transforms: `ollama run qwen2.5-coder:14b "TASK"`
- Code reviews: `ollama run gemma4 "review FILE"`
- Full auto execution: `goose run -i task-file.md` or `goose run -t "TASK"`

Always review sub-agent output before accepting. Report what the sub-agent did and flag any issues.
```

## Writing Task Files for Goose

Goose reads Markdown instruction files via `goose run -i <file>`. Structure them for reliable autonomous execution:

### Template

```markdown
# Task: [Short Description]

> Run: `goose run -i path/to/this-file.md`

## Instructions
What to do, which docs to follow, where credentials are.

## Source Material
Point to real files — never let the agent fabricate technical details.

## E-E-A-T Requirements (for blog posts)
- Experience: Real incident/production context
- Expertise: Explain WHY, not just HOW
- Authority: Link to credentials (GitHub, WordPress.org badges)
- Trust: Safety warnings, rollback steps

## SEO Rules (for blog posts)
- [ ] Focus keyword in title, slug, first paragraph, H2, meta desc
- [ ] Title under 60 chars, meta desc under 155 chars
- [ ] Internal + external links
- [ ] Images with alt text

## Steps
Numbered steps or bash commands the agent should run.

## Pre-Publish Confirmation (REQUIRED)
Checklist the agent must pass before executing any publishing commands.
All items must be [x]. Any [FAIL] blocks publishing.

## Deliverable
What to report back.
```

### Conventions

1. **Credentials via `.env`** — never hardcode SSH keys or passwords in task files.
2. **Draft only** — agents create posts as `draft`, never `publish` directly.
3. **Source material first** — point to real content files, never let agents guess.
4. **Pre-publish gate** — require a self-review checklist before any write operation.
5. **E-E-A-T + SEO mandatory** — all blog content tasks must include both sections.

## Validated Runs

| Date | Project | Task | Agent | Model | Result |
|------|---------|------|-------|-------|--------|
| 2026-04-04 | khoipro | Blog post draft | Goose | qwen3.6-plus:free | Post ID 388 created, all E-E-A-T/SEO passed |
| 2026-04-15 | runcloud-go | `internal/collect/collect.go` | OpenCode | qwen3-coder-30b (OpenRouter) | Files written, all tests pass in ~30s |
| 2026-04-15 | runcloud-go | `internal/collect/collect.go` | Goose | qwen3-coder-30b (OpenRouter) | Identical output, wrote same files in ~45s |

## Provider Routing with 9router

Instead of configuring each agent with OpenRouter directly, you can run [9router](https://github.com/decolua/9router) as a local proxy that auto-fallbacks across free → cheap → subscription providers:

```bash
# Start 9router
9router   # Dashboard at http://localhost:20128

# Point any agent to 9router instead of OpenRouter
# Endpoint: http://localhost:20128/v1
# API Key: from 9router dashboard
```

Benefits for delegation:
- Agents never stall on quota exhaustion — auto-fallback to next free provider
- Single dashboard to monitor token usage across all agents
- Multi-account round-robin for higher throughput

See `configs/9router-aider.conf.yml` and `configs/9router-opencode.json` for ready-to-use configs.

## Auth Setup Required

| Agent | Auth |
|-------|------|
| Goose | Configure in `~/.config/goose/config.yaml` or set OpenAI-compatible env vars pointing to 9router |
| Ollama | No auth needed (local) |
| 9router | `npm install -g 9router && 9router` — copy API key from dashboard |
