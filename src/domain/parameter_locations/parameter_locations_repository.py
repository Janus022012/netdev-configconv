from abc import ABC, abstractmethod
from typing import List

import os

from .parameter_locations import ParameterLocations
from .parameter import Parameter


class ParameterLocationsRepository(ABC):
    def __init__(self, parameter_sheet_file: str):
        self.instance = None
        self.parameter_sheet_file = parameter_sheet_file

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(ParameterLocationsRepository, cls).__new__(cls)
        return cls.instance

    @property
    def parameter_sheet_file(self) -> str:
        return self._parameter_sheet_file

    @parameter_sheet_file.setter
    def parameter_sheet_file(self, value):
        if not os.path.exists(value):
            raise ValueError(f"The 'parameter_sheet_file' property(value: {value}) of the ParameterLocationRepository doesn't exist in your directories")
        else:
            self._parameter_sheet_file = value

    @abstractmethod
    def get_sheets(self) -> List[str]:
        raise NotImplementedError("The 'get_sheets' method of the ParameterLocationsRepository must be implemented")

    @abstractmethod
    def read(self, sheet_name: str, parameter_locations: ParameterLocations) -> List[Parameter]:
        raise NotImplementedError("The 'read' method of the ParameterLocationsRepository must be implemented")
