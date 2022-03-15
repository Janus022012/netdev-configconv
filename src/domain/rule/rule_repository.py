from abc import ABC, abstractmethod
from logging import config
from .rule import Rule
import logging
import os


config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class RuleRepository(ABC):
    def __init__(self, rule_file: str) -> None:
        self.rule_file = rule_file

    @property
    def rule_file(self) -> str:
        return self._rule_file

    @rule_file.setter
    def rule_file(self, value) -> None:
        if not os.path.exists(value):
            raise ValueError(f"The 'rule_file' property({value}) of the RuleRepository must exist in directories.")
        else:
            self._rule_file = value

    @abstractmethod
    def read(self) -> Rule:
        raise NotImplementedError("the 'read' method of the RuleRepository must be implemented")
