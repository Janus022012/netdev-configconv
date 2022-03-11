from pydantic import BaseModel, Field, validator
from typing import List, Dict


class Parameter(BaseModel):
    name: str = Field(..., min_length=1)
    value: str = Field(...)

    class Config:
        allow_mutation = False


class ParameterGroup(BaseModel):
    parameters: List[Parameter] = Field(..., min_items=1)

    @validator("parameters")
    def _validate_no_duplicate_name(cls, value: List[Parameter]):
        if len(set([i.name for i in value])) != len(value):
            raise ValueError("Each element of the name in 'parameters' of the ParameterGroup must be unique")
        return value

    def __contains__(self, name: str) -> bool:
        return any([parameter.name == name for parameter in self.parameters])

    def get(self, name: str) -> Parameter:
        for parameter in self.parameters:
            if parameter.name == name:
                return parameter

    def to_dict(self) -> Dict[str, str]:
        return {parameter.name: parameter.value for parameter in self.parameters}

    class Config:
        allow_mutation = False
