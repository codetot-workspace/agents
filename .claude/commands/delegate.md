Delegate a task to another AI agent. Pick the best agent for the job based on these rules:

## Agent Selection

| Agent | Best For | Command |
|-------|----------|---------|
| **Aider** | Git-aware edits, multi-file refactors | `aider --message "PROMPT" --yes-always --no-auto-commits` |
| **Goose** | Complex workflows, MCP tasks | `echo "PROMPT" \| goose run` |
| **Ollama** | Quick local inference, no API cost | `ollama run qwen2.5-coder:14b "PROMPT"` |

## Instructions

1. Read the user's task from $ARGUMENTS
2. Decide which agent fits best (prefer free agents: Ollama > Aider > Goose)
3. Run the agent via Bash in headless mode
4. Capture and analyze the output
5. Report back: what the sub-agent did, whether it succeeded, and any issues
