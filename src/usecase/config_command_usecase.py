from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Type
from src.domain.config.config import Config, ConfigSource
from src.domain.config.config_repository import ConfigRepository
from src.domain.parameter_locations.parameter import ParameterGroup
from src.domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository, ParameterLocations
from src.domain.rule.rule_repository import RuleRepository
from src.utils.logger import get_custom_logger
import os
import pprint


logger = get_custom_logger(__name__)


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

        logger.info(f"Starting create_config(config_sample_file={config_sample_file}, parameter_sheet_file={parameter_sheet_file}, rule_file={rule_file}, output_path={output_path}, exception_sheets={exception_sheets})...")

        rule_repo_inst                  = self.rule_repo(rule_file=rule_file)
        rule_object                     = rule_repo_inst.read()
        converter_rules                 = rule_object.converter_rules
        common_parameter                = rule_object.common_parameter

        logger.info(f"Getting rule from ({parameter_sheet_file}) has been completed")
    
        parameter_locations_repo_inst = self.parameter_locations_repo(parameter_sheet_file=parameter_sheet_file)

        logger.info(f"Instantiating parameter_locations_repo(parameter_sheet_file={parameter_sheet_file}) has been completed")

        config_repo_inst = self.config_repo(config_sample_file=config_sample_file)

        logger.info(f"Instantiating config_repo(config_sample_file={config_sample_file}) has been completed")

        for device_name in self.get_sheets(parameter_locations_repo_inst.get_sheets(), exception_sheets):

            output_file: str = os.path.join(output_path, f"{device_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

            config_sources: List[ConfigSource] = []

            for converter_rule in converter_rules.values():

                parameter_group_list: List[ParameterGroup] = []

                parameter_locations_list: List[ParameterLocations] = converter_rule.data.convert_to_parameter_locations_list()

                for parameter_locations in parameter_locations_list:
                
                    parameter_group = parameter_locations_repo_inst.read(sheet_name=device_name, parameter_locations=parameter_locations)

                    logger.info(f"Getting parameter_group({parameter_group}) has been completed successfully")
                
                    if parameter_group.is_all_required_params_available():
            
                        parameter_group_list.append(parameter_group)

                        logger.info(f"parameter_group({parameter_group}) has been validated")

                config_source = converter_rule.make_config_source(
                    parameter_group_list=parameter_group_list,
                    common_parameter=common_parameter
                )

                config_sources.append(config_source)

            config_repo_inst.write(
                config=Config(config_sources=config_sources),
                output_config_file=output_file
            )

            logger.info(f"Writing {device_name} config in {output_file} has been completed successfully")

        logger.info(f"Creating config from {parameter_sheet_file} has been completed successfully")

    @staticmethod
    def get_sheets(available_sheets: List[str], exception_sheets: List[str]) -> List[str]:
        return [sheet for sheet in available_sheets if sheet not in exception_sheets]








