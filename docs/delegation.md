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

| Agent | Headless Command | Writes files? | Idle RAM | Cost |
|-------|-----------------|---------------|----------|------|
| OpenCode+DeepSeek | `opencode run -m deepseek/deepseek-chat "TASK"` | Yes (native) | 15 MB | $0.27/$1.10 per 1M |
| OpenCode | `opencode run "$(cat task.md)"` | Yes (native) | 15 MB | Free (OpenRouter) |
| Goose | `goose run -i task.md` | Yes (write_file) | 0 MB | Free (OpenRouter) |
| Ollama 7b | REST API (see below) | No — text only | ~5 GB | Free |
| Ollama 32b | REST API (see below) | No — text only | ~20 GB | Free |

> ⚠️ **Never use `ollama run model "$(cat task)"` for background tasks.**
> The shell process stays alive indefinitely, keeping the model loaded in RAM.
> A 32b model uses ~20 GB of unified memory. Killed on 2026-04-15 after 3h23m = 5.5 GB wasted.

### Confirmed working commands (tested 2026-04-24)

```bash
# DeepSeek — PREFERRED for reliable work (cheap, no rate limits, ~30s)
opencode run -m deepseek/deepseek-chat "$(cat task.md)"
opencode run -m deepseek/deepseek-reasoner "$(cat task.md)"  # hard reasoning

# OpenCode via OpenRouter — for free tier tasks (may rate-limit)
opencode run "$(cat task.md)"

# Goose — for agentic multi-step workflows (cloud, ~45s, no RAM cost)
GOOSE_MODEL="qwen/qwen3-coder-30b-a3b-instruct" goose run -i task.md

# Ollama 7b via REST API — for quick local tasks (5 GB RAM, free)
curl -s http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"PROMPT","stream":false}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"

# Ollama 32b via REST API — for complex local tasks (20 GB RAM, free)
# Unload immediately after: ollama stop qwen2.5-coder:32b
curl -s http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:32b","prompt":"PROMPT","stream":false}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
```

### ⚠️ Ollama RAM Management (M1 Max 32GB)

```bash
# Check what's loaded
ollama ps

# Unload a model immediately after use
ollama stop qwen2.5-coder:32b   # frees ~20 GB
ollama stop gemma4               # frees ~6 GB

# Only one large model (14B+) at a time — Ollama auto-unloads after 5min idle
# but background shell processes prevent auto-unload
```

**RAM budget per model:**

| Model | RAM (RSS) | Notes |
|-------|-----------|-------|
| qwen2.5-coder:7b | ~5 GB | Daily driver for simple tasks |
| gemma4 | ~6 GB | Reviews, text analysis |
| qwen2.5-coder:32b | ~20 GB | Reserve for complex codegen, unload after |
| Ollama daemon (no model) | 60 MB | Always-on, fine |

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

Route tasks cheapest-first, RAM-aware:

```
Single file codegen (reliable, quality matters)?
  → DeepSeek via OpenCode (cloud, 0 RAM, ~30s, cheap)
  → opencode run -m deepseek/deepseek-chat "TASK"

Hard reasoning / complex algorithms?
  → DeepSeek R1 via OpenCode (cloud, 0 RAM, ~45s)
  → opencode run -m deepseek/deepseek-reasoner "TASK"

Single file codegen (free tier OK)?
  → OpenCode (cloud, 0 RAM, ~30s, free)

Multi-file agentic workflow (SSH, multiple edits)?
  → Goose (cloud, 0 RAM, ~45s)

Quick question / text analysis / review?
  → Ollama 7b via REST API (5 GB RAM, free, fast)

Complex algorithm / large file (> 300 lines)?
  → Ollama 32b via REST API (20 GB RAM, free, slow)
  → Run ollama stop <model> immediately after

Architecture / multi-file reasoning / debugging?
  → Claude (keep in main context)
```

**Cost comparison (2026-04-24 prices):**

| Agent | Per 1M tokens (in/out) | Per typical task (~5K tokens) |
|-------|------------------------|-------------------------------|
| Ollama (any model) | Free | Free |
| OpenCode / Goose (qwen3-coder-30b) | $0.07 | $0.0004 |
| DeepSeek V4 Flash | $0.27 / $1.10 | ~$0.003 |
| DeepSeek R1 | $0.55 / $2.19 | ~$0.007 |
| Claude Sonnet | ~$3.00 / $15.00 | ~$0.045 |

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
| 2026-04-15 | runcloud-go | `internal/collect/ssh.go` | OpenCode | qwen3-coder-30b (OpenRouter) | Passed — needed 1 nil-check fix |
| 2026-04-15 | runcloud-go | `internal/portal/webhook.go` | Goose | qwen3-coder-30b (OpenRouter) | All tests pass |
| 2026-04-15 | runcloud-go | `internal/portal/client.go` | Goose | qwen3-coder-30b (OpenRouter) | Tests pass, 1 unused import fix |
| 2026-04-15 | runcloud-go | `internal/tui/dashboard.go` | OpenCode | qwen3-coder-30b (OpenRouter) | Built OK, needed 5 logic fixes (counts, age, events) |
| 2026-04-15 | runcloud-go | `cmd/sites.go` | Goose | qwen3-coder-30b (OpenRouter) | Perfect — zero fixes needed |
| 2026-04-15 | runcloud-go | `internal/web/static/index.html` (dashboard v2) | OpenCode | qwen3-coder-30b (OpenRouter) | 1256 lines, built OK, needed metric layout fix |

## Failures & Lessons (2026-04-15)

| Agent | Failure | Root Cause | Fix |
|-------|---------|------------|-----|
| `ollama run qwen2.5-coder:32b "$(cat task)"` | Zombie processes, 5.5 GB RAM wasted for 3h23m | Shell process keeps model loaded; TTY spinner swamps output | Use REST API: `curl localhost:11434/api/generate` |
| Goose `qwen3.6-plus:free` | Model deprecated | OpenRouter removed the free model | Updated `~/.zshrc` to `qwen3-coder:free` then paid model |
| Goose `qwen3-coder:free` | Rate limited | Free tier quota too low for large tasks | Use paid `qwen3-coder-30b-a3b-instruct` ($0.07/1M) |
| OpenCode `--print` flag | Flag doesn't exist | Wrong CLI syntax assumption | Correct: `opencode run "$(cat task.md)"` |
| OpenCode `server.go` | Invented DB methods (`GetAllServers`, `GetWebAppByID`) | LLM hallucinated non-existent API | Always verify generated code compiles before trusting |
| OpenCode `internal/web/static/index.html` | Metric cells stacked vertically | `flex-direction:column` on `<td>` elements | Rewrote CSS to horizontal `metric-cell` layout |

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
| OpenCode+DeepSeek | `DEEPSEEK_API_KEY` in `~/.zshrc` — provider auto-configured in `~/.config/opencode/opencode.json` |
| Goose | Configure in `~/.config/goose/config.yaml` or set OpenAI-compatible env vars pointing to 9router |
| Ollama | No auth needed (local) |
| 9router | `npm install -g 9router && 9router` — copy API key from dashboard |
