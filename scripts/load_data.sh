#!/usr/bin/env bash
set -euo pipefail


: "${POSTGRES_DB:?}"
: "${POSTGRES_USER:?}"
: "${POSTGRES_PASSWORD:?}"
: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"


FILE="/data/seoul_municipalities.geojson"


echo "Loading $FILE into PostGIS…"


# use ogr2ogr inside the gdal container; connect to the db service by name
CMD="ogr2ogr -f PostgreSQL \"
PG:host=${POSTGRES_HOST} port=${POSTGRES_PORT} dbname=${POSTGRES_DB} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD}\" \
-nln seoul_districts \
-nlt MULTIPOLYGON \
-lco GEOMETRY_NAME=geom \
-lco FID=id \
-dialect SQLite \
-sql 'SELECT *, CAST(NULL AS INTEGER) AS id FROM \"seoul_municipalities.geojson\"' \
-a_srs EPSG:4326 \
-overwrite ${FILE}"


docker compose exec gdal sh -lc "$CMD"


echo "Creating spatial index…"
docker compose exec -e PGPASSWORD=${POSTGRES_PASSWORD} db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c \
"CREATE INDEX IF NOT EXISTS idx_seoul_districts_geom ON seoul_districts USING GIST(geom); ANALYZE seoul_districts;"


echo "Done."
