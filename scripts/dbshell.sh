#!/usr/bin/env bash
set -euo pipefail

# Run from project root regardless of where this script is invoked from.
cd "$(dirname "$0")/.."

# Drop into psql inside the running db container. Picks up POSTGRES_USER /
# POSTGRES_DB from the container's environment so this works even if you
# change credentials in .env later.
exec docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
