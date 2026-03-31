#!/bin/bash
# Install free AI coding agents locally
# Usage: bash install/install.sh

set -e

echo "=== Installing Free AI Coding Agents ==="
echo ""

# 1. Gemini CLI (free 1000 req/day)
echo "[1/5] Gemini CLI..."
if command -v gemini &> /dev/null; then
  echo "  ✓ Already installed: $(gemini --version 2>/dev/null || echo 'installed')"
else
  npm install -g @google/gemini-cli
  echo "  ✓ Installed. Run: gemini"
fi

# 2. OpenCode
echo "[2/5] OpenCode..."
if command -v opencode &> /dev/null; then
  echo "  ✓ Already installed"
else
  npm install -g opencode-ai@latest
  echo "  ✓ Installed. Run: opencode"
fi

# 3. Aider
echo "[3/5] Aider..."
if command -v aider &> /dev/null; then
  echo "  ✓ Already installed: $(aider --version 2>/dev/null || echo 'installed')"
else
  pipx install aider-chat 2>/dev/null || pip install aider-chat
  echo "  ✓ Installed. Run: aider"
fi

# 4. Codex CLI
echo "[4/5] Codex CLI..."
if command -v codex &> /dev/null; then
  echo "  ✓ Already installed"
else
  npm install -g @openai/codex
  echo "  ✓ Installed. Run: codex"
fi

# 5. Goose
echo "[5/5] Goose..."
if command -v goose &> /dev/null; then
  echo "  ✓ Already installed"
else
  if command -v brew &> /dev/null; then
    brew install block-goose-cli
  else
    echo "  ⚠ Install manually: https://github.com/block/goose"
  fi
  echo "  ✓ Installed. Run: goose"
fi

echo ""
echo "=== Done! ==="
echo ""
echo "Quick start:"
echo "  gemini          # Free, no API key (Google account)"
echo "  opencode        # Best TUI, BYOK"
echo "  aider           # Git-native, BYOK"
echo "  codex           # Free with ChatGPT Plus"
echo "  goose           # MCP-native, BYOK"
