#!/bin/bash
set -e

echo "🚀 Barry Content Agent — Setup"
echo "================================"

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker required. Install from docker.com"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose required."; exit 1; }

# Check .env exists
if [ ! -f .env ]; then
    echo "❌ .env file missing. Copy .env.example to .env and fill in secrets."
    echo "   cp .env.example .env"
    exit 1
fi

# Validate required vars
source .env
required_vars=("MIXPOST_APP_URL" "MIXPOST_DB_PASSWORD" "MYSQL_ROOT_PASSWORD" "N8N_USER" "N8N_PASSWORD" "ANTHROPIC_API_KEY" "APIFY_API_TOKEN" "UPLOAD_POST_API_KEY")
missing=()
for var in "${required_vars[@]}"; do
    [ -z "${!var}" ] && missing+=("$var")
done
if [ ${#missing[@]} -ne 0 ]; then
    echo "❌ Missing required vars in .env:"
    printf '   - %s\n' "${missing[@]}"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create networks
docker network create barry-net 2>/dev/null || true

# Deploy core services
echo ""
echo "📦 Deploying core services (Mixpost + n8n)..."
docker-compose up -d mixpost mixpost-db redis n8n

# Wait for services
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Health checks
echo ""
echo "🏥 Health checks..."
if curl -sf http://localhost:8080 >/dev/null; then
    echo "   ✅ Mixpost: http://localhost:8080"
else
    echo "   ⚠️  Mixpost not yet ready (may take a minute)"
fi

if curl -sf http://localhost:5678/healthz >/dev/null; then
    echo "   ✅ n8n: http://localhost:5678"
else
    echo "   ⚠️  n8n not yet ready (may take a minute)"
fi

# Import workflows
echo ""
echo "📋 Importing n8n workflows..."
for f in workflows/*.json; do
    name=$(basename "$f" .json)
    echo "   Importing: $name"
    # n8n CLI import (requires auth)
    docker exec barry-n8n n8n import:workflow --input="/home/node/.n8n/workflows/$(basename "$f")" 2>/dev/null || \
        echo "   ⚠️  Import $name failed — import manually via n8n UI"
done

echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Open n8n: http://localhost:5678"
echo "  2. Login: $N8N_USER / (your password)"
echo "  3. Import workflows from /workflows folder (if not auto-imported)"
echo "  4. Open Mixpost: http://localhost:8080"
echo "  5. Complete Mixpost setup wizard"
echo "  6. Connect social accounts in Mixpost"
echo "  7. Test: publish a test post"
echo ""
echo "Docs: docs/SETUP.md"
echo "Runbook: docs/RUNBOOK.md"
