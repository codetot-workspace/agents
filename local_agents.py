"""
AI Sub-Agents — Local (Ollama) + Cloud (DeepSeek, OpenCode, Goose, Gemini)
==========================================================================
Call local or cloud models as sub-agents for delegation from Claude Code.

Local models (Ollama, uses RAM):
  - gemma4            : General reasoning, review (~10 GB)
  - qwen2.5-coder:14b : Daily driver codegen (~9 GB)
  - qwen2.5-coder:7b  : Quick code tasks (~5 GB)

Cloud agents (zero RAM):
  - deepseek          : DeepSeek V4 Flash / R1 via API (cheap, reliable)
  - opencode          : opencode run "PROMPT" (Qwen3 Coder 30B via OpenRouter, free)
  - goose             : goose run -t "PROMPT" (Qwen3 Coder via OpenRouter, free)
  - gemini            : gemini -p "PROMPT" (Gemini 2.5 Pro, 1M context, free)

Requirements:
  pip install openai
"""

import os
import subprocess
from openai import OpenAI

# ---------------------------------------------------------------------------
# 1. Ollama client (local, OpenAI-compatible)
# ---------------------------------------------------------------------------

ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def ask(model: str, prompt: str, system: str = "") -> str:
    """Send a single prompt to a local Ollama model and return the response."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = ollama_client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# 2. DeepSeek client (cloud, cheap)
# ---------------------------------------------------------------------------

deepseek_client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
)


def deepseek_agent(prompt: str, model: str = "deepseek-chat", system: str = "") -> str:
    """Call DeepSeek API. Models: 'deepseek-chat' (V4 Flash), 'deepseek-reasoner' (R1)."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = deepseek_client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def deepseek_code(prompt: str) -> str:
    """Generate code using DeepSeek V4 Flash."""
    return deepseek_agent(
        prompt=prompt,
        system="You are an expert software engineer. Write clean, production-ready code.",
    )


def deepseek_reason(prompt: str) -> str:
    """Solve hard problems using DeepSeek R1 reasoner."""
    return deepseek_agent(prompt=prompt, model="deepseek-reasoner")


# ---------------------------------------------------------------------------
# 3. Specialized local agents
# ---------------------------------------------------------------------------

def code_agent(prompt: str) -> str:
    """Generate code using qwen2.5-coder:14b."""
    return ask(
        model="qwen2.5-coder:14b",
        prompt=prompt,
        system="You are an expert software engineer. Write clean, production-ready code.",
    )


def review_agent(code: str) -> str:
    """Review code using gemma4."""
    return ask(
        model="gemma4",
        prompt=f"Review the following code for bugs, security issues, and improvements:\n\n```\n{code}\n```",
        system="You are a senior code reviewer. Be concise and actionable.",
    )


def quick_agent(prompt: str) -> str:
    """Fast responses using qwen2.5-coder:7b."""
    return ask(model="qwen2.5-coder:7b", prompt=prompt)


# ---------------------------------------------------------------------------
# 4. Multi-agent pipeline: generate -> review -> refine
# ---------------------------------------------------------------------------

def code_and_review(prompt: str) -> dict:
    """Generate code, review it, then refine based on feedback."""
    code = code_agent(prompt)
    review = review_agent(code)
    refined = code_agent(f"Original code:\n{code}\n\nReview feedback:\n{review}\n\nRefine the code based on the feedback.")
    return {"code": code, "review": review, "refined": refined}


# ---------------------------------------------------------------------------
# 5. Cloud agents (subprocess — zero RAM, needs network)
#    IMPORTANT: Always use timeout to prevent hanging.
# ---------------------------------------------------------------------------

def opencode_agent(prompt: str, model: str = "", timeout: int = 120) -> str:
    """Run a prompt via OpenCode. Set model='deepseek/deepseek-chat' for DeepSeek."""
    cmd = ["opencode", "run"]
    if model:
        cmd.extend(["-m", model])
    cmd.append(prompt)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def goose_agent(prompt: str, timeout: int = 180) -> str:
    """Run a prompt via Goose (Qwen3 Coder, free via OpenRouter)."""
    result = subprocess.run(
        ["goose", "run", "-t", prompt, "--no-session"],
        capture_output=True, text=True, timeout=timeout,
    )
    return result.stdout.strip()


def gemini_agent(prompt: str, timeout: int = 120) -> str:
    """Run a prompt via Gemini CLI (Gemini 2.5 Pro, free tier)."""
    result = subprocess.run(
        ["gemini", "-p", prompt],
        capture_output=True, text=True, timeout=timeout,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # DeepSeek (cloud, cheap)
    print("=== DeepSeek V4 Flash ===")
    print(deepseek_agent("What model are you? Reply in one sentence."))

    # Local model
    print("\n=== Gemma 4 (local) ===")
    print(ask("gemma4", "What are you? Reply in one sentence."))

    # Code generation + review pipeline
    print("\n=== Code + Review Pipeline ===")
    result = code_and_review("Write a Python function to validate an email address")
    print("--- Generated Code ---")
    print(result["code"])
    print("--- Review ---")
    print(result["review"])
    print("--- Refined Code ---")
    print(result["refined"])
