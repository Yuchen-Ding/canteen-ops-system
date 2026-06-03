#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f env/.env.local ]; then
  cp env/.env.local.example env/.env.local
fi

docker compose --env-file env/.env.local -f docker-compose.local.yml up -d --build
