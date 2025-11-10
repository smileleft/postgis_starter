from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from sqlalchemy import select, text

DATABASE_URL = "postgresql+asyncpg://gisuser:secret@localhost:5432/gisdb"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
app = FastAPI()

@app.get("/districts")
async def get_districts():
    async with SessionLocal() as session:
        result = await session.execute(text("SELECT name, ST_AsGeoJSON(geom) as geometry FROM seoul_districts"))
        rows = result.fetchall()
        return [{"name": r[0], "geometry": r[1]} for r in rows]
