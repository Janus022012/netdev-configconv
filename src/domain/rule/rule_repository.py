from abc import ABC, abstractmethod
from src.domain.rule.rule_exceptions import RuleFileNotExistError
from src.utils.logger import get_custom_logger
from .rule import Rule
import os


logger = get_custom_logger(__name__)


class RuleRepository(ABC):
    """RuleRepository
    
    本クラスは、パラメータシートからパラメータを取り出すルールが記載されたファイルを読み込む抽象クラスである。

    Attributes:
        rule_file (str): パラメータシートからパラメータを取り出すルールが書かれたファイル
        
    """

    def __init__(self, rule_file: str) -> None:

        logger.debug(f"Intializing RuleRepository(rule_file={rule_file})...")

        self.rule_file : str = rule_file

    @property
    def rule_file(self) -> str:

        logger.debug(f"Getting rule_file({self._rule_file}) in the RuleRepository...")

        return self._rule_file

    @rule_file.setter
    def rule_file(self, value) -> None:

        logger.debug(f"Setting rule_file({value}) in the RuleRepository...")

        if not os.path.exists(value):
            raise RuleFileNotExistError({"rule_file": value})
        
        else:
            logger.debug(f"Setting rule_file({value}) has been completed")
            self._rule_file = value

    @abstractmethod
    def read(self) -> Rule:
        raise NotImplementedError("the 'read' method of the RuleRepository must be implemented")
