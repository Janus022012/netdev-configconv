from typing import List, Literal, Dict, Union
from pydantic import BaseModel, Field, validator
from src.utils.logger import get_custom_logger
from src.domain.config.config import ConfigSource
from src.domain.parameter_locations.parameter_locations import ParameterLocationSource
from src.domain.parameter_locations.parameter import Parameter, ParameterGroup

import abc
import copy
import re
import logging
import os


logger = get_custom_logger(__name__)


class Condition:
    @abc.abstractmethod
    def evaluate(self, parameters: List[Parameter]) -> bool:
        raise NotImplementedError("The 'evaluate' method must be implemented")


class IsEmptyCondition(Condition, BaseModel):
    type: Literal['isEmpty']
    target_parameters: List[str] = Field(..., min_items=1)

    def evaluate(self, parameter_group: ParameterGroup) -> bool:
        for target_parameter in self.target_parameters:
            if target_parameter in parameter_group:
                if parameter_group.get(target_parameter).value:
                    return False
        return True


class IsContainedCondition(Condition, BaseModel):
    type: Literal['isContained']
    target_parameters: List[str] = Field(..., min_items=1)
    target_string: str = Field(..., min_length=1)

    def evaluate(self, parameter_group: ParameterGroup) -> bool:
        for target_parameter in self.target_parameters:
            if target_parameter in parameter_group:
                if not re.search(self.target_string, parameter_group.get(target_parameter).value):
                    return False
            else:
                return False
        return True


class CommandCondition(BaseModel):
    condition: Union[IsEmptyCondition, IsContainedCondition] = Field(..., discriminator='type')
    action: Literal["Delete", "Add"]
    commands: List[str] = Field(..., min_items=1)

    class Config:
        allow_mutation = False

    def apply_command_condition(self, parameter_group: ParameterGroup, conditional_commands: List[str], applicable_commands: List[str]) -> List[str]:
        if self.condition.evaluate(parameter_group):
            return Action.build(self.action).do(self, conditional_commands, applicable_commands)
        return applicable_commands


class Action:
    action_type = "Action"

    @abc.abstractmethod
    def do(self, command_condition: CommandCondition, conditional_command: List[str], applicable_commands: List[str]) -> List[str]:
        pass

    @classmethod
    def build(cls, action: str):
        if cls.action_type == "Action":
            for subclass_name, subclass in {c.action_type: c for c in cls.__subclasses__()}.items():
                if subclass_name == action:
                    return subclass()
            raise ValueError(f"The action name of '{action}' have not implemented yet")
        else:
            raise ValueError(f"The 'build' command cannot call except 'Action' class")


class Delete(Action):
    action_type = "Delete"

    def do(self, command_condition: CommandCondition, conditional_command: List[str], applicable_commands: List[str]) -> List[str]:
        result: List[str] = []

        for ac in applicable_commands:
            flag = True
            for cc in conditional_command:
                if re.search(ac, cc):
                    flag = False
            if flag:
                result.append(ac)
        return result


class Add(Action):
    action_type = "Add"

    def do(self, command_condition: CommandCondition, conditional_command: List[str], applicable_commands: List[str]) -> List[str]:
        return copy.copy(applicable_commands) + copy.copy(conditional_command)


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
    
    
class ParamsValidation(BaseModel):
    validator: Union[RegexValidator, NumberRangeValidator] = Field(..., discriminator='validator_type')
    # TODO Validationの仕組みをどうするか。
    #       ・やりたい事
    #           レベルに応じて、処理の中断具合を変えたい(アプリケーションの停止、デバイス単位の停止など)
    # level: Literal["Error", "Warning", "Info"] = "Info"


    def apply_validation(self, parameter_group: ParameterGroup) -> bool:
        return self.validator.is_valid(parameter_group=parameter_group)

class Options(BaseModel):
    indent_level: int = Field(0, ge=0)
    filling_each_commands: bool = Field(False)
    filling_each_commands_group: bool = Field(False)

    class Config:
        allow_mutation = False

    def assign_options(self, commands_group: List[List[str]], filling: str) -> List[List[str]]:
        result: List[List[str]] = copy.deepcopy(commands_group)

        if self.indent_level:
            result: List[List[str]] = self._apply_indent_level(
                indent_level=self.indent_level,
                filling=filling,
                commands_group=result
            )

        if self.filling_each_commands:
            result: List[List[str]] = self._apply_filling_each_commands(
                filling=filling,
                commands_group=result
            )
        

        if self.filling_each_commands_group:
            result: List[List[str]] = self._apply_filling_each_commands_group(
                filling=filling,
                commands_group=result
            )

        return result

    @staticmethod
    def _apply_indent_level(indent_level: int, filling: str, commands_group: List[List[str]]) -> List[List[str]]:
        result: List[List[str]] = []

        for commands in commands_group:
            commands_result = []
            for command in commands:
                if command != filling:
                    commands_result.append(" " * indent_level + command)
            result.append(commands_result)

        return result

    @staticmethod
    def _apply_filling_each_commands(filling: str, commands_group: List[List[str]]) -> List[List[str]]:
        result: List[List[str]] = []

        for commands in commands_group:
            commands_result = []
            for i, command in enumerate(commands):
                commands_result.append(command)
                if len(commands) != (i+1):
                    commands_result.append(filling)
            result.append(commands_result)

        return result

    @staticmethod
    def _apply_filling_each_commands_group(filling: str, commands_group: List[List[str]]) -> List[List[str]]:
        result: List[List[str]] = []

        for commands in commands_group:
            commands_result = []
            for i, command in enumerate(commands):
                commands_result.append(command)
                if len(commands) == (i+1):
                    commands_result.append(filling)
            result.append(commands_result)
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
    validations: List[ParamsValidation] = Field(..., min_items=0)
    conditions: List[CommandCondition] = Field(..., min_items=0)
    options: Options

    class Config:
        allow_mutation = False

    def make_config_source(self, parameter_group_list: List[ParameterGroup], common_parameter: CommonParameter) -> ConfigSource:
        commands_group: List[List[str]] = []

        for parameter_group in parameter_group_list:
            if self._apply_validation_all_parameters(self.validations, parameter_group):

                commands: List[str] = self._get_params_inserted_commands(commands=self.commands,parameter_group=parameter_group)

                for command_condition in self.conditions:

                    commands = command_condition.apply_command_condition(
                        parameter_group=parameter_group,
                        conditional_commands=self._get_params_inserted_commands(commands=command_condition.commands, parameter_group=parameter_group),
                        applicable_commands=commands,
                    )

            commands_group.append(commands)

        # optionの適用
        result: List[List[str]] = self.options.assign_options(commands_group, common_parameter.filling)

        return ConfigSource(marker=self.marker, commands_group=result)

    @staticmethod
    def _get_params_inserted_commands(commands: List[str], parameter_group: ParameterGroup) -> List[str]:
        return [command.format_map(parameter_group.to_dict()) for command in commands]

    @staticmethod
    def _apply_validation_all_parameters(validations: List[ParamsValidation], parameter_group: ParameterGroup) -> bool:
        # TODO Validationの仕組みをどうするか。
        #       ・やりたい事
        #           レベルに応じて、処理の中断具合を変えたい(アプリケーションの停止、デバイス単位の停止など)
        # ここで、戻り値をEnum ValidationLevelにして、それぞれ処理を変更出来れば可能？
        # 現状は、Validation違反があれば、そのParameterGroupのみSkipという形にする。
        # return all([validation.apply_validation(parameter_group=parameter_group) for validation in validations])
        return True


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
