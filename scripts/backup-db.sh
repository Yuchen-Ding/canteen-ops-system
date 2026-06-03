#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-qa}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${ROOT_DIR}/backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
CONTAINER_NAME="canteen_postgres_${ENVIRONMENT}"

mkdir -p "$BACKUP_DIR"

if [ "$ENVIRONMENT" = "local" ]; then
  ENV_FILE="${ROOT_DIR}/env/.env.local"
elif [ "$ENVIRONMENT" = "qa" ]; then
  ENV_FILE="${ROOT_DIR}/env/.env.qa"
else
  echo "Only local and qa backups are supported by this script."
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing ${ENV_FILE}."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

docker exec "$CONTAINER_NAME" pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "${BACKUP_DIR}/canteen_${ENVIRONMENT}_${TIMESTAMP}.sql"
echo "Backup written to ${BACKUP_DIR}/canteen_${ENVIRONMENT}_${TIMESTAMP}.sql"
