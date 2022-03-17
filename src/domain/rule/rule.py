from typing import List, Literal, Dict, Union
from pydantic import BaseModel, Field, validator
from src.utils.logger import get_custom_logger
from src.domain.config.config import ConfigSource
from src.domain.parameter_locations.parameter_locations import ParameterLocationSource
from src.domain.parameter_locations.parameter import ParameterGroup
from .condition import IsEmptyCondition, IsContainedCondition
from .action import Action
from .validator import RegexValidator, NumberRangeValidator
import copy


logger = get_custom_logger(__name__)


class CommandCondition(BaseModel):
    condition: Union[IsEmptyCondition, IsContainedCondition] = Field(..., discriminator='type')
    action: Literal["Delete", "Add"]
    commands: List[str] = Field(..., min_items=1)

    class Config:
        allow_mutation = False

    def apply_command_condition(self, parameter_group: ParameterGroup, conditional_commands: List[str], applicable_commands: List[str]) -> List[str]:
        if self.condition.evaluate(parameter_group):
            return Action.build(self.action).do(conditional_commands, applicable_commands)
        return applicable_commands
    
    
class ParamsValidation(BaseModel):
    validator: Union[RegexValidator, NumberRangeValidator] = Field(..., discriminator='validator_type')
    level: Literal["Error", "Warning", "Info"] = "Info"


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
