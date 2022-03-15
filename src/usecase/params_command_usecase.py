from abc import ABC, abstractmethod
from logging import config

from src.domain.config.config_repository import ConfigRepository
from src.domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository
from src.domain.rule.rule_repository import RuleRepository

import logging
import os

config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AbstractParamsCommandUsecase(ABC):
    def __init__(self, config_repo: ConfigRepository, parameter_locations_repo: ParameterLocationsRepository, rule_repo: RuleRepository) -> None:
        self.config_repo: ConfigRepository                       = config_repo
        self.parameter_locations: ParameterLocationsRepository  = parameter_locations_repo
        self.rule_repo: RuleRepository                           = rule_repo

    @abstractmethod
    def create_parameter_sheet_file(self, config_sample_file: str, parameter_sheet_file: str, rule_file: str, exception_sheets: list) -> None:
        raise NotImplementedError("The 'create_parameter_sheet_file' method of AbstractParamsCommandUsecase must be implemented")


class ParamsCommandUsecase(AbstractParamsCommandUsecase):
    def __init__(self, config_repo: ConfigRepository, parameter_locations_repo: ParameterLocationsRepository, rule_repo: RuleRepository) -> None:
        super().__init__(config_repo, parameter_locations_repo, rule_repo)
        
    def create_parameter_sheet_file(self, config_sample_file: str, parameter_sheet_file: str, rule_file: str, exception_sheets: list) -> None:
        pass