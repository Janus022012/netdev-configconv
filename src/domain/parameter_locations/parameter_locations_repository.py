from abc import ABC, abstractmethod
from typing import List
from src.utils.logger import get_custom_logger
from .parameter_locations import ParameterLocations
from .parameter_locations_exceptions import ParameterSheetNotExistError
from .parameter import ParameterGroup

import os

logger = get_custom_logger(__name__)


class ParameterLocationsRepository(ABC):
    """ParameterLocationsRepository
    
    本クラスは、ParameterLocationsを用いてParameterを取得する抽象クラスである

    Attributes:
        parameter_sheet_file (str): パラメータシートが存在するファイルパス

    """
    def __init__(self, parameter_sheet_file: str):

        logger.debug(f"Intializing ParameterLocationsRepository(parameter_sheet_file={parameter_sheet_file})...")

        self.instance = None
        self.parameter_sheet_file = parameter_sheet_file


    @property
    def parameter_sheet_file(self) -> str:

        logger.debug(f"Getting parameter_sheet_file({self._parameter_sheet_file}) in the ParameterLocationsRepository...")

        return self._parameter_sheet_file


    @parameter_sheet_file.setter
    def parameter_sheet_file(self, value):

        logger.debug(f"Setting parameter_sheet_file({value}) in the ParameterLocationsRepository...")

        if not os.path.exists(value):

            raise ParameterSheetNotExistError(message_items={"parameter_sheet_file": value})

        else:

            logger.debug(f"Setting parameter_sheet_file({value}) has been completed")

            self._parameter_sheet_file = value


    @abstractmethod
    def get_sheets(self) -> List[str]:
        """get_sheets

        パラメータシートからシート配列を取得する関数

        Returns:
            List[str]: 取得されたシート配列

        """
        raise NotImplementedError("The 'get_sheets' method of the ParameterLocationsRepository must be implemented")


    @abstractmethod
    def read(self, sheet_name: str, parameter_locations: ParameterLocations) -> ParameterGroup:
        """read

        パラメータシートからSheetNameとParameterLocationsを指定して、パラメータを取得する関数

        Args:
            sheet_name (str): シート名
            parameter_locations  (:obj:`ParameterLocations`): パラメータが存在する位置を記述したもの

        Returns:
            ParameterGroup: 取得したパラメータ群
            
        """
        raise NotImplementedError("The 'read' method of the ParameterLocationsRepository must be implemented")
