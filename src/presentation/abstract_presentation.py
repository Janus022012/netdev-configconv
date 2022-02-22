from abc import ABC, abstractmethod
from typing import Dict


class AbstractPresentation(ABC):
    def __init__(self):
        self.available_commands = ["create_config", "create_params"]

    @staticmethod
    @abstractmethod
    def _parse_arguments() -> Dict[str, str]:
        pass

    @abstractmethod
    def run(self) -> Dict[str, str]:
        pass






