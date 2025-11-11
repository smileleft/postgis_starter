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

## Run backend
```
uvicorn main:app --reload
```

## start App in a nutshell
```
make up
make fetch
make load

# check
make health

# open browser
http://localhost:8000
```

## useful command
```
# db connect
make db-psql

# make space index
make reindex

# tail log
make logs

# tail api log only
make api-logs

# clean data 
make clean
```

