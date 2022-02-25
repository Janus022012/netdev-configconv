from abc import ABC, abstractmethod

from src.domain.config.config import Config

import re
import os


class ConfigRepository(ABC):
    def __init__(self, config_sample_file: str) -> None:
        self.config_sample_file: str    = config_sample_file

    @property
    def config_sample_file(self) -> str:
        return self._config_sample_file

    @config_sample_file.setter
    def config_sample_file(self, value: str) -> None:
        if not os.path.exists(value):
            raise ValueError(f"The 'config_sample_file' property(value: {value}) of the ConfigRepository doesn't exist in your directories")
        else:
            self._config_sample_file = value

    @abstractmethod
    def write(self, config: Config, output_config_file: str) -> None:
        raise NotImplementedError("The 'write_config' method of the ConfigRepository must be implemented.")

    @staticmethod
    def _inspect_marker(line: str) -> bool:
        return True if re.search(r"%{2}\w+%{2}", line) else False
