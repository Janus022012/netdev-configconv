from pydantic import BaseModel, Field, validator
from typing import List, Dict
from logging import config

import logging
import os

config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Parameter(BaseModel):
    name: str = Field(..., min_length=1)
    value: str = None
    required: bool = False

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

    def is_all_required_params_available(self) -> bool:
        for parameter in self.parameters:
            if parameter.required == True and parameter.value == False:
                return False
        return True

    def to_dict(self) -> Dict[str, str]:
        return {parameter.name: parameter.value for parameter in self.parameters}

    class Config:
        allow_mutation = False
