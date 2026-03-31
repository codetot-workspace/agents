Run a task across multiple AI agents and find consensus. Usage: /project:consensus <task>

1. Take the task from $ARGUMENTS
2. Run it on 2-3 agents in parallel via Bash:
   - `ollama run qwen2.5-coder:14b "TASK"` (local, free)
   - `gemini -p "TASK"` (free tier)
   - Your own analysis (Claude)
3. Compare all responses
4. Report:
   - What all agents agreed on (high confidence)
   - Where they disagreed (needs human review)
   - Your recommended answer with reasoning
