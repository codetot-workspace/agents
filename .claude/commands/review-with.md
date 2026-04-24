---
description: "Get a code review from another AI provider. Usage: /project:review-with <agent> <file-or-description>"
argument-hint: <agent> <file-or-description>
---

Get a code review from another AI provider. Parse $ARGUMENTS to extract the agent name and target file.

**IMPORTANT: Always use Bash timeout. Never use interactive `ollama run` — use REST API instead.**

## Run the review

- If agent is "deepseek": 
  ```bash
  opencode run -m deepseek/deepseek-chat "Review this code for bugs, security issues, and improvements: $(cat TARGET_FILE)"
  ```
  Use Bash tool with `timeout: 120000`.

- If agent is "ollama" or "local":
  ```bash
  curl -s --max-time 120 http://localhost:11434/api/generate \
    -d "{\"model\":\"qwen2.5-coder:14b\",\"prompt\":\"Review this code for bugs, security issues, and improvements:\\n\\n$(cat TARGET_FILE)\",\"stream\":false}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
  ```

- If agent is "goose":
  ```bash
  goose run -t "Review this code for bugs, security issues, and improvements: $(cat TARGET_FILE)" --no-session
  ```
  Use Bash tool with `timeout: 180000`.

- If agent is "gemini":
  ```bash
  gemini -p "Review this code for bugs, security issues, and improvements: $(cat TARGET_FILE)"
  ```
  Use Bash tool with `timeout: 120000`.

## Then

Capture the output, then provide your own analysis comparing your review with the sub-agent's review. Highlight any disagreements.
