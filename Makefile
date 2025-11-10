SHELL := /bin/bash


.PHONY: up down logs api-logs db-psql fetch load reindex curl health clean


up:
docker compose up -d --build


logs:
docker compose logs -f --tail=200


api-logs:
docker compose logs -f api


down:
docker compose down


# open psql inside db
db-psql:
docker compose exec -e PGPASSWORD=$$POSTGRES_PASSWORD db psql -U $$POSTGRES_USER -d $$POSTGRES_DB


# 1) download Seoul GeoJSON
fetch:
./scripts/fetch_data.sh


# 2) load into PostGIS using ogr2ogr inside gdal container
load:
./scripts/load_data.sh


# Build spatial index (if not created by ogr2ogr)
reindex:
docker compose exec -e PGPASSWORD=$$POSTGRES_PASSWORD db psql -U $$POSTGRES_USER -d $$POSTGRES_DB -c \
"CREATE INDEX IF NOT EXISTS idx_seoul_districts_geom ON seoul_districts USING GIST(geom); ANALYZE seoul_districts;"


curl:
curl -s http://localhost:8000/districts | head -c 400 | jq


health:
curl -s http://localhost:8000/health | jq


clean:
rm -rf pgdata data/*.json data/*.geojson
