from abc import ABC, abstractmethod
from datetime import datetime
from logging import config
from typing import List, Type

from src.domain.config.config import Config, ConfigSource
from src.domain.config.config_repository import ConfigRepository
from src.domain.parameter_locations.parameter import ParameterGroup
from src.domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository, ParameterLocations
from src.domain.rule.rule_repository import RuleRepository

import logging
import os


config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AbstractConfigCommandUsecase(ABC):
    def __init__(self, config_repo: Type[ConfigRepository], parameter_locations_repo: Type[ParameterLocationsRepository], rule_repo: Type[RuleRepository]) -> None:
        self.config_repo               = config_repo
        self.parameter_locations_repo  = parameter_locations_repo
        self.rule_repo                 = rule_repo

    @abstractmethod
    def create_config(self, config_sample_file: str, parameter_sheet_file: str, rule_file: str, output_path: str, exception_sheets: list) -> None:
        raise NotImplementedError("The 'create_config' method of AbstractConfigCommandUsecase must be implemented")


class ConfigCommandUsecase(AbstractConfigCommandUsecase):
    def __init__(self,  config_repo: Type[ConfigRepository], parameter_locations_repo: Type[ParameterLocationsRepository], rule_repo: Type[RuleRepository]) -> None:
        super().__init__(config_repo, parameter_locations_repo, rule_repo)
        
    def create_config(self, config_sample_file: str, parameter_sheet_file: str, rule_file: str, output_path: str, exception_sheets: list) -> None:
        # Ruleエンティティの取得
        rule_repo_inst                  = self.rule_repo(rule_file=rule_file)
        rule_object                     = rule_repo_inst.read()
        converter_rules                 = rule_object.converter_rules
        common_parameter                = rule_object.common_parameter

        # ParameterLocationsRepositoryのインスタンス化
        parameter_locations_repo_inst = self.parameter_locations_repo(parameter_sheet_file)

        # ConfigRepositoryのインスタンス化
        config_repo_inst = self.config_repo(config_sample_file=config_sample_file)

        for device_name in self.get_sheets(parameter_locations_repo_inst.get_sheets(), exception_sheets):

            config_sources: List[ConfigSource] = []

            for converter_rule in converter_rules.values():

                parameter_group_list: List[ParameterGroup] = []

                parameter_locations_list: List[ParameterLocations] = converter_rule.data.convert_to_parameter_locations_list()

                for parameter_locations in parameter_locations_list:
                
                    parameter_group = parameter_locations_repo_inst.read(sheet_name=device_name, parameter_locations=parameter_locations)
                
                    if parameter_group.is_all_required_params_available():
            
                        parameter_group_list.append(parameter_group)

                config_sources.append(
                    converter_rule.make_config_source(
                            parameter_group_list=parameter_group_list,
                            common_parameter=common_parameter
                    )
                )

            config_repo_inst.write(
                config=Config(config_sources=config_sources),
                output_config_file=os.path.join(output_path, f"{device_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")
            )

    @staticmethod
    def get_sheets(available_sheets: List[str], exception_sheets: List[str]) -> List[str]:
        return [sheet for sheet in available_sheets if sheet not in exception_sheets]








