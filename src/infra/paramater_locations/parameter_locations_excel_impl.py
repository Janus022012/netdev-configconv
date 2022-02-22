import sys
import os
import openpyxl
from typing import List

sys.path.append(os.path.abspath("../../domain/parameter_locations"))
from .parameter import Parameter
from .parameter_locations import ParameterLocations
from .parameter_locations_repository import ParameterLocationsRepository


class ParameterLocationsExcelImpl(ParameterLocationsRepository):
    def __init__(self, parameter_sheet_file: str):
        super(ParameterLocationsExcelImpl, self).__init__(parameter_sheet_file)
        self.workbook = openpyxl.load_workbook(self.parameter_sheet_file)

    def get_sheets(self) -> List[str]:
        raise self.workbook.sheetnames

    def read(self, sheet_name: str, parameter_locations: ParameterLocations) -> List[Parameter]:
        result: List[Parameter] = []

        if not self.validate_sheet_name(sheet_name):
            raise ValueError(f"the sheet name '{sheet_name}' doesn't exist in f{self.parameter_sheet_file}")

        for location in parameter_locations.locations:
            result.append(Parameter(name=location.name, value=self.workbook[sheet_name][location.cell_number]))

        return result

    def validate_sheet_name(self, sheet_name):
        return any([True if sheet_name == sheet else False for sheet in self.workbook.sheetnames])

