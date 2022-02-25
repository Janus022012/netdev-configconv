from typing import List, Literal, Dict
from pydantic import BaseModel, Field, validator

from src.domain.parameter_locations.parameter_locations import ParameterLocation, ParameterLocations
from src.domain.parameter_locations.parameter import Parameter


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
            ) for j in range(self.row_from, self.row_to)
        ]


class CommandCondition(BaseModel):
    condition: str = Field(..., min_length=1)
    action: Literal["Delete", "Add"]
    command: List[str] = Field(..., min_items=1)

    class Config:
        allow_mutation = False

    def assign_command_condition_to_commands(self, commands: List[str]) -> List[str]:
        pass


class Options(BaseModel):
    indent_level: int = Field(0)
    filling_each_commands: bool = Field(False)
    filling_each_command_groups: bool = Field(False)

    class Config:
        allow_mutation = False

    def assign_options_to_commands(self, commands: List[str]) -> List[str]:
        pass


class ConverterRule(BaseModel):
    description: str = Field("")
    marker: str = Field(..., min_length=5, regex=r"%{2}\w+%{2}")
    data: ParameterLocationSource
    commands: List[str] = Field(..., min_items=1)
    conditions: List[CommandCondition] = Field(..., min_items=0)
    options: Options

    class Config:
        allow_mutation = False

    def parse_commands(self) -> List[str]:
        pass

    @staticmethod
    def get_raw_commands(commands: List[str], parameters: List[Parameter]) -> List[str]:
        params_dict: Dict[str, str] = {parameter.name: parameter.value for parameter in parameters}
        return [command.format(**params_dict) for command in commands]


class CommonParameter(BaseModel):
    filling: str = Field("!", min_length=1)

    class Config:
        allow_mutation = False

    def assign_common_parameter_to_commands_group(self, commands_group: List[List[str]]):
        pass


class Rule(BaseModel):
    common_parameter: CommonParameter
    converter_rules: Dict[str, ConverterRule]

    class Config:
        allow_mutation = False

    @validator("converter_rules")
    def _validate_no_duplicate_marker(cls, value: Dict[str, ConverterRule]):
        if len(set([i.marker for i in value.values()])) != len(value):
            raise ValueError("Each element of the markers in 'converter_rules' of the Rule must be unique")
        return value
