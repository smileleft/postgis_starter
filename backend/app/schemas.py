from pydantic import BaseModel


class Feature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict


class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: list[Feature]
