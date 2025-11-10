LIST_DISTRICTS = """
SELECT
COALESCE(name, name_1, 'unknown') AS name,
ST_AsGeoJSON(geom) AS geometry
FROM seoul_districts
ORDER BY name;
"""


GET_DISTRICT_BY_NAME = """
SELECT
COALESCE(name, name_1, 'unknown') AS name,
ST_AsGeoJSON(geom) AS geometry
FROM seoul_districts
WHERE COALESCE(name, name_1) = :name
LIMIT 1;
"""


CONTAINS_POINT = """
SELECT COALESCE(name, name_1, 'unknown') AS name
FROM seoul_districts
WHERE ST_Contains(geom, ST_SetSRID(ST_Point(:lng, :lat), 4326));
"""


NEAREST_DISTRICT = """
SELECT COALESCE(name, name_1, 'unknown') AS name,
ST_DistanceSphere(geom, ST_SetSRID(ST_Point(:lng, :lat), 4326)) AS meters
FROM seoul_districts
ORDER BY geom <-> ST_SetSRID(ST_Point(:lng, :lat), 4326)
LIMIT 1;
"""
