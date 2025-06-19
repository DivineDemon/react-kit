set -euo pipefail

echo "🔧 Running oxlint format + lint for JS/TS…"
pnpm --filter frontend exec oxlint . --fix
pnpm --filter frontend exec oxlint .

echo "🐍 Running Ruff for Python…"
if [[ -x backend/.venv/bin/ruff ]]; then
  backend/.venv/bin/ruff check --fix backend
#  backend/.venv/bin/ruff check backend
else
  echo "⚠️ Ruff not found at backend/.venv/bin/ruff."
  echo "   → Did you forget to create & activate your venv?"
  echo "     Try: python -m venv backend/.venv && source backend/.venv/bin/activate && pip install ruff"
  exit 1
fi
