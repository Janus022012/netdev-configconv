from typing import List
from pydantic import BaseModel, Field, validator


class ParameterLocation(BaseModel):
    name: str = Field(..., min_length=1)
    cell_number: str = Field(..., min_length=2,regex=r"^[A-Z]+\d+")

    class Config:
        allow_mutation = False


class ParameterLocations(BaseModel):
    locations: List[ParameterLocation]

    class Config:
        allow_mutation = False


class ParameterColumnLocation(BaseModel):
    name: str = Field(..., min_length=1)
    column_number: str = Field(..., min_length=1, regex=r"[A-Z]+")


class ParameterLocationSource(BaseModel):
    parameter_column_locations: List[ParameterColumnLocation] = Field(..., min_items=1)
    row_from: int = Field(..., ge=1)
    row_to: int = Field(..., ge=1)

    class Config:
        allow_mutation = False

    @validator("row_to")
    def _validate_row_to(cls, value, values) -> int:
        if "row_from" not in values.keys():
            raise ValueError("the 'row_from' property of the ParameterSaveLocationSource must not be empty and must be greater than 1")
        if value < values["row_from"]:
            raise ValueError("the 'row_to' property of the ParameterSaveLocationSource must be greater than the 'row_from' property")
        return value

    def convert_to_parameter_locations_list(self) -> List[ParameterLocations]:
        return [
            ParameterLocations(
                locations=[
                    ParameterLocation(
                        name=i.name,
                        cell_number=f"{i.column_number}{j}"
                    ) for i in self.parameter_column_locations
                ]
            ) for j in range(self.row_from, self.row_to+1)
        ]