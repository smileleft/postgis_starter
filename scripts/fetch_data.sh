#!/usr/bin/env bash
set -euo pipefail
mkdir -p data


# Seoul municipal boundaries (simplified)
URL="https://raw.githubusercontent.com/southkorea/seoul-maps/master/json/seoul_municipalities_geo_simple.json"
OUT="data/seoul_municipalities.geojson"


if command -v curl >/dev/null 2>&1; then
  curl -L "$URL" -o "$OUT"
elif command -v wget >/dev/null 2>&1; then
  wget "$URL" -O "$OUT"
else
  echo "Please install curl or wget." >&2
  exit 1
fi


echo "Downloaded → $OUT"
