from typing import List
from pydantic import BaseModel, Field


class ParameterLocation(BaseModel):
    name: str = Field(..., min_length=1)
    cell_number: str = Field(..., min_length=2,regex=r"^[A-Z]+\d+")

    class Config:
        allow_mutation = False


class ParameterLocations(BaseModel):
    locations: List[ParameterLocation]

    class Config:
        allow_mutation = False
