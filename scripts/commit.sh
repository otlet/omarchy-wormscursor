#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run pytest -q

if command -v pre-commit >/dev/null 2>&1; then
  pre-commit run --all-files
else
  uvx pre-commit run --all-files
fi

git commit "$@"
