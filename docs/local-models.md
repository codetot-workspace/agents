# Local AI Models Audit

> Hardware: MacBook Pro M1 Max 32GB (2021)
> Runtime: Ollama
> Last updated: 2026-03-31

## Hardware Budget

- **Total RAM:** 32GB unified memory
- **Available for models:** ~24GB (OS needs ~8GB)
- **GPU:** M1 Max (32-core GPU, 400GB/s memory bandwidth)
- **Metal acceleration:** Yes (all Ollama models use it automatically)

## Installed Models

### Fast Autocomplete — Qwen 2.5 Coder 7B
```
ollama pull qwen2.5-coder:7b
```
- **Size:** 4.7GB RAM
- **Context:** 32K tokens
- **Speed:** ~30-40 tok/s
- **Use:** Inline autocomplete, simple code generation, FIM (fill-in-middle)
- **Pair with:** Continue.dev, Tabby, or any editor with Ollama support

### Daily Driver — Qwen 2.5 Coder 14B
```
ollama pull qwen2.5-coder:14b
```
- **Size:** 9.0GB RAM
- **Context:** 32K tokens
- **Speed:** ~18-25 tok/s
- **Use:** General coding assistance, code review, explanations
- **Pair with:** Aider, OpenCode, Cline

### Agentic Coding — Devstral 24B
```
ollama pull devstral
```
- **Size:** 14GB RAM
- **Context:** 128K tokens
- **Speed:** ~12-18 tok/s
- **Use:** Multi-file edits, codebase exploration, agentic workflows
- **Pair with:** Codex CLI, OpenCode, Goose
- **Note:** #1 open-source on SWE-bench. Built by Mistral + All Hands AI specifically for coding agents.

### Best Quality — Qwen 2.5 Coder 32B
```
ollama pull qwen2.5-coder:32b
```
- **Size:** 20GB RAM
- **Context:** 32K tokens
- **Speed:** ~8-12 tok/s
- **Use:** Complex refactors, hard bugs, architecture decisions
- **Pair with:** Aider (best results)
- **Note:** Matches GPT-4o on coding benchmarks. Tight on 32GB — close other apps when using.

## Usage with Agents

### Aider + Ollama
```bash
aider --model ollama_chat/qwen2.5-coder:14b
# Or for best quality:
aider --model ollama_chat/qwen2.5-coder:32b
```

### OpenCode + Ollama
Configure in `opencode.json`:
```json
{
  "provider": "ollama",
  "model": "qwen2.5-coder:14b"
}
```

### Codex CLI + Ollama
```bash
codex --provider ollama --model qwen2.5-coder:14b
```

### Goose + Ollama
Configure provider in `~/.config/goose/config.yaml`:
```yaml
provider: ollama
model: qwen2.5-coder:14b
```

## Memory Management

Only ONE large model fits comfortably at a time:

| Combo | RAM Used | Feasible? |
|-------|----------|-----------|
| 7B alone | ~5GB | Easy |
| 14B alone | ~9GB | Easy |
| 14B + 7B | ~14GB | Fine |
| Devstral alone | ~14GB | Fine |
| 32B alone | ~20GB | Tight but works |
| 32B + 7B | ~25GB | At limit, may swap |
| 32B + 14B | ~29GB | Will swap, avoid |

Ollama auto-unloads idle models after 5 minutes. To manually unload:
```bash
ollama stop qwen2.5-coder:32b
```

## Models to Skip (Already Installed, Outdated)

- `yi:latest` — general purpose, not code-focused, superseded
- `deepseek-coder:6.7b` — old generation, Qwen 2.5 Coder 7B is strictly better

You can remove them to save disk:
```bash
ollama rm yi:latest
ollama rm deepseek-coder:6.7b
```

## Future Upgrades to Watch

| Model | Why | When |
|-------|-----|------|
| Qwen 3 Coder 30B | Newer arch, 256K context, agentic-trained | Available now, 19GB |
| Qwen 3.5 35B MoE | Newest gen, fast MoE, 256K | Available, 24GB (tight) |
| DeepSeek Coder V3 | If released for Ollama | TBD |
