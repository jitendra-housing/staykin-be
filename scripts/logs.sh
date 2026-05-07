#!/usr/bin/env bash
set -euo pipefail

# Run from project root regardless of where this script is invoked from.
cd "$(dirname "$0")/.."

# Tail compose logs. Defaults to the api service. Pass another service name
# (e.g. db) as the first arg to follow that one instead, or "all" for both.
#
#   ./scripts/logs.sh           # follow api
#   ./scripts/logs.sh db        # follow db
#   ./scripts/logs.sh all       # follow everything
service="${1:-api}"

if [[ "${service}" == "all" ]]; then
  exec docker compose logs -f --tail=100
fi

exec docker compose logs -f --tail=100 "${service}"
