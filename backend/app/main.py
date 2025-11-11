from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


from .db import get_session
from .schemas import Feature, FeatureCollection
from . import queries


app = FastAPI(title="PostGIS Seoul Demo")


# CORS (adjust for your domains)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/health")
async def health():
  return {"status": "ok"}


@app.get("/districts", response_model=FeatureCollection)
async def list_districts(session: AsyncSession = Depends(get_session)):
  res = await session.execute(text(queries.LIST_DISTRICTS))
  rows = res.fetchall()
  feats = [
    Feature(geometry=row.geometry, properties={"name": row.name})
    for row in rows
  ]
  return FeatureCollection(features=feats)


@app.get("/districts/{name}", response_model=Feature)
async def get_district(name: str, session: AsyncSession = Depends(get_session)):
  res = await session.execute(text(queries.GET_DISTRICT_BY_NAME), {"name": name})
  row = res.fetchone()
  if not row:
    return Feature(geometry=None, properties={"name": name})
  return Feature(geometry=row.geometry, properties={"name": row.name})


@app.get("/contains")
async def contains(
  lng: float = Query(..., description="Longitude (EPSG:4326)"),
  lat: float = Query(..., description="Latitude (EPSG:4326)"),
  session: AsyncSession = Depends(get_session),
):
  res = await session.execute(text(queries.CONTAINS_POINT), {"lng": lng, "lat": lat})
  row = res.fetchone()
  return {"lng": lng, "lat": lat, "district": row.name if row else None}


@app.get("/nearest")
async def nearest(
  lng: float = Query(...),
  lat: float = Query(...),
  session: AsyncSession = Depends(get_session),
):
  res = await session.execute(text(queries.NEAREST_DISTRICT), {"lng": lng, "lat": lat})
  row = res.fetchone()
  if not row:
    return {"district": None}
  return {"district": row.name, "distance_m": row.meters}


# server static page
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
