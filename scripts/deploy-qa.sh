#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f env/.env.qa ]; then
  echo "Missing env/.env.qa. Copy env/.env.qa.example to env/.env.qa and update server IP and passwords."
  exit 1
fi

git pull --ff-only
docker compose --env-file env/.env.qa -f docker-compose.qa.yml up -d --build
docker compose --env-file env/.env.qa -f docker-compose.qa.yml ps
