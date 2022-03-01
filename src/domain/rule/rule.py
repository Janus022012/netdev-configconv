from typing import List, Literal, Dict, Union
from pydantic import BaseModel, Field, validator

from src.domain.parameter_locations.parameter_locations import ParameterLocation, ParameterLocations
from src.domain.parameter_locations.parameter import Parameter
import abc
import copy
import re


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


class Condition:
    @abc.abstractmethod
    def evaluate(self, parameters: List[Parameter]) -> bool:
        pass


class IsEmptyCondition(Condition, BaseModel):
    type: Literal['isEmpty']
    target_parameters: List[str] = Field(..., min_items=1)

    def evaluate(self, parameters: List[Parameter]) -> bool:
        for parameter in parameters:
            if parameter.name in self.target_parameters:
                if not parameter.value:
                    return True
        return False


class IsContainedCondition(Condition, BaseModel):
    type: Literal['isContained']
    target_parameters: List[str] = Field(..., min_items=1)
    target_string: str = Field(..., min_length=1)

    def evaluate(self, parameters: List[Parameter]) -> bool:
        for parameter in parameters:
            if parameter.name in self.target_parameters:
                if re.search(self.target_string, parameter.value):
                    return True
        return False


class CommandCondition(BaseModel):
    condition: Union[IsEmptyCondition, IsContainedCondition] = Field(..., discriminator='type')
    action: Literal["Delete", "Add"]
    commands: List[str] = Field(..., min_items=1)

    class Config:
        allow_mutation = False

    def apply_command_condition(self, commands: List[str], parameters: List[Parameter]) -> List[str]:
        copied_commands = copy.copy(commands)
        copied_parameters = copy.copy(parameters)

        if self.condition.evaluate(copied_parameters):
            return Action.build(self.action).do(self, copied_commands)
        return copied_commands


class Action:
    def __str__(self):
        return "Action"

    @abc.abstractmethod
    def do(self, command_condition: CommandCondition, inserted_commands: List[str]) -> List[str]:
        pass

    @classmethod
    def build(cls, action: str):
        if str(cls()) == "Action":
            for subclass_name, subclass in {str(c()): c for c in cls.__subclasses__()}.items():
                if subclass_name == action:
                    return subclass()
            raise ValueError(f"The action name of '{action}' have not implemented yet")
        else:
            raise ValueError(f"The 'build' command cannot call except 'Action' class")


class Delete(Action):
    def __str__(self):
        return "Delete"

    def do(self, command_condition: CommandCondition, inserted_commands: List[str]) -> List[str]:
        result: List[str] = []
        copied_inserted_commands = copy.copy(inserted_commands)

        for copied_inserted_command in copied_inserted_commands:
            if not any([re.search(target_command, copied_inserted_command) for target_command in command_condition.commands]):
                result.append(copied_inserted_command)
        return result


class Add(Action):
    def __str__(self):
        return "Add"

    def do(self, command_condition: CommandCondition, inserted_commands: List[str]) -> List[str]:
        return copy.copy(inserted_commands) + copy.copy(command_condition.commands)


class Options(BaseModel):
    indent_level: int = Field(0, ge=0)
    filling_each_commands: bool = Field(False)
    filling_each_command_groups: bool = Field(False)

    class Config:
        allow_mutation = False

    def assign_options(self, commands: List[str], filling: str) -> List[str]:
        result: List[str] = []
        copied_commands = copy.copy(commands)

        if self.filling_each_commands:
            for i, command in enumerate(copied_commands):
                if i+1 % 2:
                    if i != len(copied_commands):
                        result.append(filling)
                result.append(command)

        if self.filling_each_commands:
            result.insert(0, filling)
            result.insert(len(copied_commands), filling)

        if self.indent_level:
            result = [""*self.indent_level + command for command in result if command != filling]

        return result


class CommonParameter(BaseModel):
    filling: str = Field("!", min_length=1)

    class Config:
        allow_mutation = False


class ConverterRule(BaseModel):
    description: str = Field("")
    marker: str = Field(..., min_length=5, regex=r"%{2}\w+%{2}")
    data: ParameterLocationSource
    commands: List[str] = Field(..., min_items=1)
    conditions: List[CommandCondition] = Field(..., min_items=0)
    options: Options

    class Config:
        allow_mutation = False

    def parse_commands(self, parameters: List[Parameter], common_parameter: CommonParameter) -> str:
        copied_parameter = copy.copy(parameters)
        result = self._get_inserted_commands(self.commands, copied_parameter)

        # conditionの適用
        for command_condition in self.conditions:
            result = command_condition.apply_command_condition(result, parameters)

        # optionの適用
        result = self.options.assign_options(result, common_parameter.filling)

        return "\n".join(result)

    @staticmethod
    def _get_inserted_commands(commands: List[str], parameters: List[Parameter]) -> List[str]:
        return [command.format(**{parameter.name: parameter.value for parameter in parameters}) for command in commands]


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
