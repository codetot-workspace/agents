Get a code review from another AI provider. Usage: /project:review-with <agent> <file-or-description>

Parse $ARGUMENTS to extract the agent name and target. Then run:

- If agent is "ollama" or "local": `ollama run qwen2.5-coder:14b "Review this code for bugs, security issues, and improvements: $(cat TARGET_FILE)"`
- If agent is "goose": `echo "Review this code for bugs, security issues, and improvements: $(cat TARGET_FILE)" | goose run`
- If agent is "aider": `aider --message "review this file for issues" --yes-always TARGET_FILE`

Capture the output, then provide your own analysis comparing your review with the sub-agent's review. Highlight any disagreements.
