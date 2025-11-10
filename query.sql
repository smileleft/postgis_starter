# check PostGIS loading
SELECT name, ST_Area(geom) AS area, ST_Perimeter(geom) AS perimeter FROM seoul_districts LIMIT 5;

# check position
SELECT name
FROM seoul_districts
WHERE ST_Contains(geom, ST_SetSRID(ST_Point(126.9780, 37.5665), 4326));

# check the Center of border
SELECT ST_AsText(ST_Centroid(geom)) FROM seoul_districts WHERE name='강남구';

# Top 5 largest districts
SELECT name, ST_Area(geom::geography)/1000000 AS area_km2
FROM seoul_districts
ORDER BY area_km2 DESC LIMIT 5;
