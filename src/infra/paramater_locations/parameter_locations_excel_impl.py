import openpyxl
from typing import List

from src.domain.parameter_locations.parameter import Parameter
from src.domain.parameter_locations.parameter_locations import ParameterLocations
from src.domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository


class ParameterLocationsExcelImpl(ParameterLocationsRepository):
    def __init__(self, parameter_sheet_file: str):
        super(ParameterLocationsExcelImpl, self).__init__(parameter_sheet_file)
        self.workbook = openpyxl.load_workbook(self.parameter_sheet_file)

    def get_sheets(self) -> List[str]:
        return self.workbook.sheetnames

    def read(self, sheet_name: str, parameter_locations: ParameterLocations) -> List[Parameter]:
        result: List[Parameter] = []

        if not self._validate_sheet_name(sheet_name):
            raise ValueError(f"the sheet name '{sheet_name}' doesn't exist in {self.parameter_sheet_file}")

        for location in parameter_locations.locations:
            result.append(Parameter(name=location.name, value=self.workbook[sheet_name][location.cell_number].value))

        return result

    def _validate_sheet_name(self, sheet_name) -> bool:
        return any([True if sheet_name == sheet else False for sheet in self.get_sheets()])

