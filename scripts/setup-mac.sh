#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing system dependencies via Homebrew..."
if ! command -v brew &>/dev/null; then
    echo "Error: Homebrew is not installed. Install it from https://brew.sh" >&2
    exit 1
fi

brew install uv node sqlite

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
