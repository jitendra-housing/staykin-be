#!/usr/bin/env bash
set -euo pipefail

# Run from project root regardless of where this script is invoked from.
cd "$(dirname "$0")/.."

# Wipes the Postgres volume entirely (all data lost), then starts the stack
# back up. Migration runs automatically on api startup, which re-seeds
# localities. Use this when you want a clean slate without touching code.

echo "==> WARNING: this will DELETE ALL DATA in the staykin Postgres volume."
read -r -p "Proceed? Type 'yes' to confirm: " confirm
if [[ "${confirm}" != "yes" ]]; then
  echo "Aborted."
  exit 1
fi

echo "==> Stopping containers and removing volume"
docker compose down -v

echo "==> Starting containers (migration runs on api startup)"
docker compose up -d

echo "==> Status"
docker compose ps

echo "==> Done. Tail logs with: docker compose logs -f api"
