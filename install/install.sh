#!/bin/bash
# Install free AI coding agents locally
# Usage: bash install/install.sh

set -e

echo "=== Installing Free AI Coding Agents ==="
echo ""

# 0. 9router (provider routing proxy)
echo "[0/4] 9router..."
if command -v 9router &> /dev/null; then
  echo "  ✓ Already installed"
else
  npm install -g 9router
  echo "  ✓ Installed. Run: 9router (dashboard at http://localhost:20128)"
fi

# 1. OpenCode
echo "[1/4] OpenCode..."
if command -v opencode &> /dev/null; then
  echo "  ✓ Already installed"
else
  npm install -g opencode-ai@latest
  echo "  ✓ Installed. Run: opencode"
fi

# 2. Aider
echo "[2/4] Aider..."
if command -v aider &> /dev/null; then
  echo "  ✓ Already installed: $(aider --version 2>/dev/null || echo 'installed')"
else
  pipx install aider-chat 2>/dev/null || pip install aider-chat
  echo "  ✓ Installed. Run: aider"
fi

# 3. Goose
echo "[3/4] Goose..."
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
echo "  9router          # Start routing proxy (http://localhost:20128)"
echo "  opencode         # Best TUI, BYOK"
echo "  aider            # Git-native, BYOK"
echo "  goose            # MCP-native, BYOK"
echo ""
echo "To route all agents through 9router:"
echo "  1. Run: 9router"
echo "  2. Copy API key from dashboard"
echo "  3. Point agent base URLs to http://localhost:20128/v1"
