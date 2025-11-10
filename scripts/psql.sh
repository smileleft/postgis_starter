#!/usr/bin/env bash
set -euo pipefail


docker compose exec -e PGPASSWORD=${POSTGRES_PASSWORD:-secret} db psql -U ${POSTGRES_USER:-gisuser} -d ${POSTGRES_DB:-gisdb}
