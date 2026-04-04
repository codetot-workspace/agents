# Multi-Agent Delegation Guide

> How Claude Code assigns tasks to sub-agents from other AI providers

## 3 Approaches (Simple to Advanced)

### Approach 1: Bash Headless Mode (works now, zero setup)

Claude calls other agents via shell commands. Every major CLI agent supports non-interactive mode:

```bash
# Aider (BYOK, git-aware)
aider --message "refactor the auth module to use JWT" --yes-always --no-auto-commits src/auth.ts

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

| Agent | Headless Command | Output Format |
|-------|-----------------|---------------|
| Aider | `aider -m "prompt" --yes-always` | text + file edits |
| Goose | `goose run -i file.md` or `goose run -t "prompt"` | text (stdout) |
| Ollama | `ollama run model "prompt"` | text (stdout) |
| OpenCode | `opencode run "prompt" --format json` | JSON |

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
  → Aider or Ollama local

Does it need multi-file git-aware edits?
  → Aider (best git integration)

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
- Code reviews: `aider --message "review FILE" --yes-always FILE`
- File edits with git: `aider -m "TASK" --yes-always FILE`
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

| Date | Project | Task File | Agent | Result |
|------|---------|-----------|-------|--------|
| 2026-04-04 | khoipro | `content/mariadb-task.md` | Goose (qwen3.6-plus:free) | Draft post ID 388 created, all E-E-A-T/SEO checks passed |

## Auth Setup Required

| Agent | Auth |
|-------|------|
| Aider | Set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or use `--model ollama_chat/MODEL` |
| Goose | Configure in `~/.config/goose/config.yaml` |
| Ollama | No auth needed (local) |
