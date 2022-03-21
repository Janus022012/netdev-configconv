from typing import List, Literal, Dict
from pydantic import BaseModel, Field
from src.utils.logger import get_custom_logger
from src.domain.parameter_locations.parameter import Parameter, ParameterGroup

import abc
import re

logger = get_custom_logger(__name__)


class CustomValidator:
    @abc.abstractmethod
    def is_valid(self, parameter: Parameter) -> bool:
        raise NotImplementedError("The 'validate' method of the Validator must be implemented")


class RegexValidator(CustomValidator, BaseModel):
    validator_type: Literal['RegexValidator']
    parameter_name: str = Field(..., min_length=1)
    pattern: str = Field(..., min_length=1)

    def is_valid(self, parameter_group: ParameterGroup) -> bool:
        parameter =  parameter_group.get(self.parameter_name)
        if parameter:
            return True if re.search(self.pattern, parameter.value) else False
        else:
            return False

class NumberRangeValidator(CustomValidator, BaseModel):
    validator_type: Literal['regexValidator']
    parameter_name: str = Field(..., min_length=1)
    min: int = Field(...)
    max: int = Field(...)

    def is_valid(self, parameter_group: ParameterGroup) -> bool:
        parameter =  int(parameter_group.get(self.parameter_name))
        if min <= parameter <= max:
            return True
        else:
            return False