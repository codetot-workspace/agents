# Free AI Coding Agents Audit

> Last updated: 2026-03-31

## Tier 1: CLI-First Coding Agents (Claude Code Alternatives)

### 1. OpenCode
- **GitHub:** https://github.com/anomalyco/opencode
- **Stars:** ~133k
- **What:** Terminal-native AI coding agent with polished TUI (Go/Bubble Tea). Reads/writes files, runs commands, edits code.
- **Install:** `npm i -g opencode-ai@latest` or `brew install opencode`
- **API key:** BYOK — 75+ providers (OpenAI, Anthropic, Gemini, Ollama, OpenRouter, etc.)
- **License:** MIT
- **Verdict:** Top-tier. Best TUI experience. Use with Ollama for zero-cost local usage.

### 2. Aider
- **GitHub:** https://github.com/Aider-AI/aider
- **Stars:** ~42k
- **What:** AI pair programming. Git-native with auto-commits.
- **Install:** `pipx install aider-chat`
- **API key:** BYOK (Claude, GPT-4o, DeepSeek, Ollama local models)
- **License:** Apache 2.0
- **Verdict:** Best git integration. Mature and reliable.

### 4. Goose (by Block)
- **GitHub:** https://github.com/block/goose
- **Stars:** ~34k
- **What:** Extensible AI agent. MCP-native. Desktop app + CLI.
- **Install:** `brew install block-goose-cli`
- **API key:** BYOK (any LLM)
- **License:** Apache 2.0
- **Verdict:** Most extensible via MCP. Good for orchestration.

### 5. RA.Aid
- **GitHub:** https://github.com/ai-christianson/RA.Aid
- **Stars:** ~2.2k
- **What:** Autonomous agent built on LangGraph. Research/plan/implement pipeline.
- **Install:** `pip install ra-aid`
- **API key:** BYOK (Gemini, OpenAI, Anthropic)
- **License:** Apache 2.0
- **Verdict:** Interesting research-first approach. Smaller community.

---

## Tier 2: Full Platforms (Run Locally)

### 7. OpenHands (formerly OpenDevin)
- **GitHub:** https://github.com/OpenHands/OpenHands
- **Stars:** ~69k
- **What:** AI development platform. Agents write code, run terminal, browse web.
- **Install:** Docker or `pip install openhands`
- **API key:** BYOK
- **License:** MIT
- **Verdict:** Most capable platform. Heavy (Docker required).

### 8. SWE-agent
- **GitHub:** https://github.com/SWE-agent/SWE-agent
- **Stars:** ~19k
- **What:** Takes GitHub issues and fixes them autonomously.
- **Install:** From source (Python)
- **API key:** BYOK
- **License:** MIT
- **Verdict:** Best for automated issue fixing. Research-grade.

### 9. bolt.diy (Open Source bolt.new)
- **GitHub:** https://github.com/stackblitz-labs/bolt.diy
- **Stars:** ~18k
- **What:** Prompt, run, edit, deploy full-stack web apps using any LLM.
- **Install:** Clone + Docker
- **API key:** BYOK (19+ providers)
- **License:** MIT
- **Verdict:** Great for rapid prototyping web apps.

---

## Tier 3: IDE Extensions (Free, Open Source)

### 10. Cline
- **GitHub:** https://github.com/cline/cline
- **Stars:** ~58k
- **What:** Autonomous coding agent as VS Code extension.
- **Install:** VS Code Marketplace
- **API key:** BYOK
- **License:** Apache 2.0

### 11. Roo Code (Cline fork)
- **GitHub:** https://github.com/RooCodeInc/Roo-Code
- **Stars:** ~22k
- **What:** Multi-persona AI agents in VS Code.
- **License:** Apache 2.0

### 12. Kilo Code (Cline fork)
- **GitHub:** https://github.com/Kilo-Org/kilocode
- **Stars:** ~10k+
- **What:** VS Code + JetBrains + CLI. Lower token usage.
- **License:** Apache 2.0

### 13. Continue.dev
- **GitHub:** https://github.com/continuedev/continue
- **Stars:** ~20k+
- **What:** Modular AI assistant for VS Code and JetBrains.
- **License:** Apache 2.0

---

## Tier 4: Self-Hosted / Editors

### 14. Tabby
- **GitHub:** https://github.com/TabbyML/tabby
- **Stars:** ~32k
- **What:** Self-hosted Copilot alternative. Runs on consumer GPUs. No API key needed.
- **License:** Open source (custom)
- **Verdict:** Best for fully offline, zero-cost code completion.

### 15. Zed
- **GitHub:** https://github.com/zed-industries/zed
- **Stars:** ~55k+
- **What:** High-performance editor with AI agent panel. BYOK + 50 free prompts/month.
- **License:** GPL v3

---

## Dead / Paused Projects (Skip)

| Project | Status | Notes |
|---------|--------|-------|
| Plandex | Winding down (Oct 2025) | No new users |
| Void Editor | Paused | May degrade |
| Devon | Early/stale | AGPL license |

---

## Recommendation: Install These 5

For a comprehensive free AI agent toolkit:

1. **OpenCode** — best TUI, works with any provider
2. **Aider** — best git integration, mature
3. **Goose** — most extensible, MCP-native

For zero-cost local: Use **Ollama** + any BYOK agent above.
