#!/usr/bin/env bash
set -euo pipefail

# Run from project root regardless of where this script is invoked from.
cd "$(dirname "$0")/.."

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "==> Pulling latest on branch: ${BRANCH}"
git pull --ff-only origin "${BRANCH}"

echo "==> Stopping running containers"
docker compose down

echo "==> Building and starting containers"
docker compose up -d --build

echo "==> Status"
docker compose ps

echo "==> Done. Tail logs with: docker compose logs -f api"
