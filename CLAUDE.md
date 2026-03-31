# Agents Workspace

A curated workspace for evaluating, installing, and orchestrating free/open-source AI coding agents.

## Purpose

This repo tracks which AI coding agents are available for free, how to install them, and how they compare — so we can hire the right "AI teammates" without cost.

## Project Structure

```
/
├── CLAUDE.md          # This file — project instructions for Claude Code
├── docs/
│   └── audit.md       # Full audit of free AI coding agents
├── install/           # Installation scripts and configs
│   └── install.sh     # One-shot installer for selected agents
└── configs/           # Per-agent configuration templates
```

## Installed Agents

The following CLI agents are installed locally:

| Agent | Command | Status |
|-------|---------|--------|
| Claude Code | `claude` | Active (primary) |
| Gemini CLI | `gemini` | Free 1000 req/day |
| OpenCode | `opencode` | BYOK |
| Aider | `aider` | BYOK |
| Codex CLI | `codex` | ChatGPT Plus |
| Goose | `goose` | BYOK |

## Conventions

- All agent evaluation notes go in `docs/`
- Installation scripts go in `install/`
- Agent-specific configs go in `configs/`
- Use this repo to compare agents on real tasks and track findings

## Key Commands

```bash
# Run Gemini CLI (free, no API key needed — just Google account)
gemini

# Run OpenCode
opencode

# Run Aider with Claude
aider --model claude-3.5-sonnet

# Run Codex
codex

# Run Goose
goose
```

## Agent Selection Criteria

1. **Truly free** — no API cost or generous free tier
2. **CLI-first** — terminal-native, not browser-only
3. **Open source** — MIT/Apache 2.0 preferred
4. **Active development** — skip dead/paused projects
5. **Practical** — can do real coding tasks, not just demos
