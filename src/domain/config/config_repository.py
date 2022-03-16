from abc import ABC, abstractmethod
from logging import config
from src.domain.config.config import Config
from .config_exception import ConfigSampleFileNotExistError
import logging
import re
import os

config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ConfigRepository(ABC):
    """ConfigRepository
    
    本クラスは、ConfigSampleFileとConfigを用いてコンフィグを出力するための抽象クラスである

    Attributes:
        config_sample_file str: ConfigSampleFileが存在するファイルパス
        
    """

    def __init__(self, config_sample_file: str) -> None:

        logger.debug(f"Intializing ConfigRepository(config_sample_file={config_sample_file})...")

        self.config_sample_file: str    = config_sample_file


    @property
    def config_sample_file(self) -> str:

        logger.debug(f"Getting config_sample_value({self._config_sample_file}) in the ConfigRepository...")

        return self._config_sample_file


    @config_sample_file.setter
    def config_sample_file(self, value: str) -> None:

        logger.debug(f"Setting config_sample_value({value}) in the ConfigRepository...")

        if not os.path.exists(value):
        
            raise ConfigSampleFileNotExistError(message_items={"config_sample_file": value})
        
        else:
            
            logger.debug(f"Setting config_sample_value({value}) has been completed")
            
            self._config_sample_file = value


    @abstractmethod
    def write(self, config: Config, output_config_file: str) -> None:
        """write

        ConfigSampleFileとConfigインスタンスからConfigファイルを出力する関数

        Args:
            config (:obj:`Config`): コンフィグに記載すべき内容を含んだオブジェクト
            output_config_file (str): 出力先のディレクトリ

        """
        raise NotImplementedError("The 'write_config' method of the ConfigRepository must be implemented.")

    @staticmethod
    def _inspect_marker(line: str) -> bool:
        
        logger.debug(f"Inspecting a maker in the line({line})...")

        result = True if re.search(r"%{2}\w+%{2}", line) else False

        logger.debug(f"Inspecting a marker in the line({line}) is {result}")

        return result
