# Agents Workspace

A curated workspace for evaluating, installing, and orchestrating free/open-source AI coding agents.

## Purpose

This repo tracks which AI coding agents are available for free, how to install them, and how they compare — so we can hire the right "AI teammates" without cost.

## Project Structure

```
/
├── CLAUDE.md          # This file — project instructions for Claude Code
├── .claude/commands/  # Custom slash commands for delegation
│   ├── delegate.md    # /project:delegate — auto-pick agent
│   ├── review-with.md # /project:review-with — cross-agent review
│   └── consensus.md   # /project:consensus — multi-agent agreement
├── docs/
│   ├── audit.md       # Full audit of free AI coding agents
│   ├── local-models.md # Local Ollama models audit
│   └── delegation.md  # Multi-agent delegation guide
├── install/           # Installation scripts and configs
│   └── install.sh     # One-shot installer for selected agents
└── configs/           # Per-agent configuration templates
```

## Installed Agents

The following CLI agents are installed locally:

| Agent | Command | Status |
|-------|---------|--------|
| Claude Code | `claude` | Active (primary) |
| OpenCode | `opencode` | OpenRouter free (Qwen3 Coder) |
| Goose | `goose` | OpenRouter free (Qwen3 Coder) |

## Provider Routing: 9router

**GitHub:** https://github.com/decolua/9router

Smart routing proxy that auto-fallbacks across free → cheap → subscription AI providers. Replaces direct OpenRouter usage with automatic failover.

```bash
# Install & start
npm install -g 9router
9router    # Dashboard at http://localhost:20128

# Point any agent to 9router
# Endpoint: http://localhost:20128/v1
# API Key: copy from dashboard
```

Free providers (no signup): iFlow AI, Qwen Code, Kiro AI (Claude models), Gemini CLI.
Cheap providers: GLM-4.7 ($0.6/1M), MiniMax M2.1 ($0.2/1M), Kimi K2 ($9/mo).

9router-specific config in `configs/9router-opencode.json`.

## Local Models (Ollama on M1 Max 32GB)

| Model | Command | Size | Speed | Use Case |
|-------|---------|------|-------|----------|
| Qwen 2.5 Coder 7B | `ollama run qwen2.5-coder:7b` | 4.7GB | ~35 tok/s | Fast autocomplete |
| Qwen 2.5 Coder 14B | `ollama run qwen2.5-coder:14b` | 9GB | ~20 tok/s | Daily driver |
| Devstral 24B | `ollama run devstral` | 14GB | ~15 tok/s | Agentic coding |
| Qwen 2.5 Coder 32B | `ollama run qwen2.5-coder:32b` | 20GB | ~10 tok/s | Best quality |

Run only ONE large model at a time (14B+ uses significant RAM). See `docs/local-models.md` for full details.

## Cloud Models (OpenRouter Free Tier / 9router)

Agents can use OpenRouter directly via `OPENROUTER_API_KEY` in `.env`, or route through 9router for automatic free/cheap fallback.

| Model | ID | Context | Best For |
|-------|-----|---------|----------|
| Qwen3 Coder 480B | `qwen/qwen3-coder:free` | 262K | **Default** — agentic coding |
| Qwen 3.6 Plus | `qwen/qwen3.6-plus:free` | 1M | Massive context tasks |
| Nemotron 3 Super 120B | `nvidia/nemotron-3-super-120b-a12b:free` | 262K | Multi-agent workflows |
| GPT-OSS 120B | `openai/gpt-oss-120b:free` | 131K | Reasoning + agentic |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct:free` | 65K | Solid all-rounder |

Configs in `configs/` — installed to `~/.config/opencode/opencode.json` and Goose via env vars in `~/.zshrc`.

## Conventions

- All agent evaluation notes go in `docs/`
- Installation scripts go in `install/`
- Agent-specific configs go in `configs/`
- Use this repo to compare agents on real tasks and track findings

## Key Commands

```bash
# Start 9router (smart provider routing)
9router

# Run agents via OpenRouter (default)
opencode
goose

# Run OpenCode via 9router (auto-fallback across free providers)
opencode --config configs/9router-opencode.json
```

## Sub-Agent Delegation

When working in any project, Claude should delegate mechanical tasks to sub-agents to save cost and get second opinions. Route by capability:

```
Simple summary/transform → ollama run qwen2.5-coder:14b "TASK"
Code review/second opinion → ollama run gemma4 "review FILE"
Full agentic execution → goose run -i task-file.md
Complex reasoning → Claude (keep in main context)
```

Custom commands available:
- `/project:delegate <task>` — Auto-pick best agent and run
- `/project:review-with <agent> <file>` — Cross-agent code review
- `/project:consensus <question>` — Multi-agent consensus

See `docs/delegation.md` for full guide.

## Agent Selection Criteria

1. **Truly free** — no API cost or generous free tier
2. **CLI-first** — terminal-native, not browser-only
3. **Open source** — MIT/Apache 2.0 preferred
4. **Active development** — skip dead/paused projects
5. **Practical** — can do real coding tasks, not just demos
