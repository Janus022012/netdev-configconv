from typing import List
from logging import config

from src.domain.parameter_locations.parameter import ParameterGroup, Parameter
from src.domain.parameter_locations.parameter_locations import ParameterLocations
from src.domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository

import logging
import openpyxl
import os


config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ParameterLocationsExcelImpl(ParameterLocationsRepository):

    def __init__(self, parameter_sheet_file: str):
        super(ParameterLocationsExcelImpl, self).__init__(parameter_sheet_file)
        self.workbook = openpyxl.load_workbook(self.parameter_sheet_file)

    def get_sheets(self) -> List[str]:
        return self.workbook.sheetnames

    def read(self, sheet_name: str, parameter_locations: ParameterLocations) -> ParameterGroup:

        parameters: List[Parameter] = []

        if not self._validate_sheet_name(sheet_name):

            raise ValueError(f"the sheet name '{sheet_name}' doesn't exist in {self.parameter_sheet_file}")

        for location in parameter_locations.locations:

            parameters.append(
                Parameter(
                    name=location.name,
                    value=self.workbook[sheet_name][location.cell_number].value,
                    required=location.required
                )
            )

        return ParameterGroup(parameters=parameters)

    def _validate_sheet_name(self, sheet_name) -> bool:

        return any([True if sheet_name == sheet else False for sheet in self.get_sheets()])

