from pydantic import BaseModel, Field


class Parameter(BaseModel):
    name: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)

    class Config:
        allow_mutation = False
