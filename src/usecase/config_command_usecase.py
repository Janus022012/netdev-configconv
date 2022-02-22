from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

import os
import sys

sys.path.append(os.path.abspath("../domain"))
from .config.config import Config, ConfigSource
from .config.config_repository import ConfigRepository
from .parameter_locations.parameter_locations_repository import ParameterLocationsRepository
from .rule.rule_repository import RuleRepository


class AbstractConfigCommandUsecase(ABC):
    def __init__(self, config_repo: ConfigRepository, parameter_locations_repo: ParameterLocationsRepository, rule_repo: RuleRepository) -> None:
        self.config_repo: ConfigRepository                              = config_repo
        self.parameter_locations_repo: ParameterLocationsRepository     = parameter_locations_repo
        self.rule_repo: RuleRepository                                  = rule_repo

    @abstractmethod
    def create_config(self, config_sample_file: str, parameter_sheet_file: str, rule_file: str, output_path: str, exception_sheets: list) -> None:
        raise NotImplementedError("The 'create_config' method of AbstractConfigCommandUsecase must be implemented")


class ConfigCommandUsecase(AbstractConfigCommandUsecase):
    def __init__(self, config_repo: ConfigRepository, parameter_locations_repo: ParameterLocationsRepository, rule_repo: RuleRepository) -> None:
        super().__init__(config_repo, parameter_locations_repo, rule_repo)
        
    def create_config(self, config_sample_file: str, parameter_sheet_file: str, rule_file: str, output_path: str, exception_sheets: list) -> None:
        rule_inst: RuleRepository                               = self.rule_repo(rule_file)
        parameter_locations_inst: ParameterLocationsRepository  = self.parameter_locations_repo(parameter_sheet_file)

        # シートの取得
        for device_name in [sheet for sheet in parameter_locations_inst.get_sheets() if sheet not in exception_sheets]:
            config_sources: List[ConfigSource] = []

            for converter_rule in rule_inst.read().converter_rules:
                commands_group = []

                # command
                for parameter_locations in converter_rule.data.convert_to_parameter_locations_list():
                    commands_group.append(
                        converter_rule.parse_commands(
                            parameters=parameter_locations_inst.read(device_name, parameter_locations)
                        )
                    )

                # commands_group
                config_sources.append(
                    rule_inst.read().common_parameter.assign_common_parameter(
                        marker=converter_rule.marker,
                        commands_group=commands_group
                    )
                )

            # save config
            self.config_repo(
                config_sample_file=config_sample_file,
                config=Config(config_sources),
                output_config_file=os.path.join(output_path, f"{device_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")
            ).write()









