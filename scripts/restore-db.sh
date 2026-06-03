#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-qa}"
BACKUP_FILE="${2:-}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTAINER_NAME="canteen_postgres_${ENVIRONMENT}"

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: scripts/restore-db.sh <local|qa> <backup_sql_file>"
  exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Backup file not found: ${BACKUP_FILE}"
  exit 1
fi

if [ "$ENVIRONMENT" = "local" ]; then
  ENV_FILE="${ROOT_DIR}/env/.env.local"
elif [ "$ENVIRONMENT" = "qa" ]; then
  ENV_FILE="${ROOT_DIR}/env/.env.qa"
else
  echo "Only local and qa restores are supported by this script."
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing ${ENV_FILE}."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

docker exec -i "$CONTAINER_NAME" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < "$BACKUP_FILE"
echo "Restore completed from ${BACKUP_FILE}"
