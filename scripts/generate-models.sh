set -e

OPENAPI_URL="${OPENAPI_URL:-http://localhost:8000/openapi.json}"
OUTPUT_FILE="shared/models.ts"

echo "🛠  Generating TypeScript models from $OPENAPI_URL → $OUTPUT_FILE"

pnpm exec openapi-typescript "$OPENAPI_URL" --output "$OUTPUT_FILE"

echo "✅ Models generated."
