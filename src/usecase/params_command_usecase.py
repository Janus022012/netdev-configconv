from abc import ABC, abstractmethod

import os
import sys

sys.path.append(os.path.abspath("../domain"))
from .config.config_repository import ConfigRepository
from .parameter_locations.parameter_locations_repository import ParameterLocationsRepository
from .rule.rule_repository import RuleRepository


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