# postgis_starter
starter project for postGIS

## collect gis data for Seoul City
```
wget https://raw.githubusercontent.com/southkorea/seoul-maps/master/json/seoul_municipalities_geo_simple.json
```

## convert GeoJSON -> PostGIS
```
sudo apt install gdal-bin
ogr2ogr -f "PostgreSQL" PG:"dbname=gisdb user=gisuser password=secret host=localhost" \
  -nln seoul_districts \
  -nlt MULTIPOLYGON \
  -lco GEOMETRY_NAME=geom \
  -lco FID=id \
  seoul_municipalities_geo_simple.json
```

## check data (in query.sql)

## install FastAPI backend
```
pip install fastapi uvicorn asyncpg geoalchemy2 sqlalchemy
```

