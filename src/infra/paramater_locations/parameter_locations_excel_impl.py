from typing import List
from src.utils.logger import get_custom_logger

from .parameter_locations_excel_impl_exceptions import SheetNotExistError
from src.domain.parameter_locations.parameter import ParameterGroup, Parameter
from src.domain.parameter_locations.parameter_locations import ParameterLocations
from src.domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository

import openpyxl


logger = get_custom_logger(__name__)


class ParameterLocationsExcelImpl(ParameterLocationsRepository):
    """ParameterLocationsExcelImpl
    
    本クラスは、ParameterLocationsを用いてParameterをExcelから取得する具象クラスである

    Attributes:
        parameter_sheet_file (str): パラメータシートが存在するファイルパス
        
    """

    def __init__(self, parameter_sheet_file: str):
        super().__init__(parameter_sheet_file)
        self.workbook = openpyxl.load_workbook(self.parameter_sheet_file)


    def get_sheets(self) -> List[str]:
        """get_sheets

        パラメータシートからシート配列を取得する関数

        Returns:
            List[str]: 取得されたシート配列

        """
        logger.debug(f"Getting sheets in the ParameterLocationsExcelImpl...")

        result: List[str] = self.workbook.sheetnames

        logger.debug(f"Getting sheets({result}) in the ParameterLocationsExcelImpl has been completed")

        return result


    def read(self, sheet_name: str, parameter_locations: ParameterLocations) -> ParameterGroup:
        """read

        パラメータシートからSheetNameとParameterLocationsを指定して、Excelファイルからパラメータを取得する関数

        Args:
            sheet_name (str): シート名
            parameter_locations  (:obj:`ParameterLocations`): パラメータが存在する位置を記述したもの

        Returns:
            ParameterGroup: 取得したパラメータ群
            
        """
        parameters: List[Parameter] = []

        logger.debug(f"Getting parameter_group from ({self.parameter_sheet_file}) in the ParameterLocationsExcelImpl...")

        if not self._validate_sheet_name(sheet_name):

            raise SheetNotExistError({"sheet_name": sheet_name, "parameter_sheet_file": self.parameter_sheet_file})

        for location in parameter_locations.locations:

            logger.debug(f"Getting parameter({location.name}) at {self.workbook[sheet_name][location.cell_number].value} in the ParameterLocationsExcelImpl...")

            parameters.append(
                Parameter(
                    name=location.name,
                    value=self.workbook[sheet_name][location.cell_number].value,
                    required=location.required
                )
            )

            logger.debug(f"Getting parameter({location.name}) at {self.workbook[sheet_name][location.cell_number].value} in the ParameterLocationsExcelImpl has been completed")

        logger.debug(f"Getting parameter_group from ({self.parameter_sheet_file}) in the ParameterLocationsExcelImpl has been completed")

        return ParameterGroup(parameters=parameters)

    def _validate_sheet_name(self, sheet_name) -> bool:
        sheets: List[str] = self.get_sheets()
        
        logger.debug(f"Checking the existence of sheet_name({sheet_name}) in ({sheets})...")

        result: bool = any([True if sheet_name == sheet else False for sheet in sheets])

        logger.debug(f"Checking the existence of sheet_name({sheet_name}) in ({sheets}) is {result}")

        return result

