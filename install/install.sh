#!/bin/bash
# Install free AI coding agents locally
# Usage: bash install/install.sh

set -e

echo "=== Installing Free AI Coding Agents ==="
echo ""

# 1. OpenCode
echo "[1/3] OpenCode..."
if command -v opencode &> /dev/null; then
  echo "  ✓ Already installed"
else
  npm install -g opencode-ai@latest
  echo "  ✓ Installed. Run: opencode"
fi

# 2. Aider
echo "[2/3] Aider..."
if command -v aider &> /dev/null; then
  echo "  ✓ Already installed: $(aider --version 2>/dev/null || echo 'installed')"
else
  pipx install aider-chat 2>/dev/null || pip install aider-chat
  echo "  ✓ Installed. Run: aider"
fi

# 3. Goose
echo "[3/3] Goose..."
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
echo "  opencode        # Best TUI, BYOK"
echo "  aider           # Git-native, BYOK"
echo "  goose           # MCP-native, BYOK"
