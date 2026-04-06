#!/usr/bin/env bash
set -euo pipefail

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
fi

echo "==> Installing system dependencies via apt-get..."
if ! command -v apt-get &>/dev/null; then
    echo "Error: apt-get not found. This script is for Debian/Ubuntu-based systems." >&2
    exit 1
fi

$SUDO apt-get update
$SUDO apt-get install -y \
    build-essential \
    libsqlite3-dev \
    libpcre3-dev \
    nodejs \
    npm

echo "==> Installing uv..."
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/0.7.2/install.sh | sh
    source $HOME/.local/bin/env
fi

echo "==> Installing Python and project dependencies via uv..."
uv sync --frozen

echo "==> Setting up database..."
if [ ! -f database/books.sqlite ]; then
    cp database/books-sample.sqlite database/books.sqlite
    echo "    Copied books-sample.sqlite -> books.sqlite"
else
    echo "    database/books.sqlite already exists, skipping"
fi

echo "==> Installing frontend dependencies..."
cd static
npm ci
npx gulp
cd ..

echo ""
echo "Setup complete! To run the app:"
echo "  uv run python controller.py"
echo "  # then visit http://localhost:5000"
