#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8100}"

check_endpoint() {
  local path="$1"
  local url="${BASE_URL}${path}"
  echo "Checking ${url}"
  curl --fail --silent --show-error "$url" >/tmp/canteen_smoke_response.json
  cat /tmp/canteen_smoke_response.json
  echo
}

check_endpoint "/health"
check_endpoint "/health/db"
check_endpoint "/api/v1/system/info"
check_endpoint "/metrics"

echo "Smoke test completed."
