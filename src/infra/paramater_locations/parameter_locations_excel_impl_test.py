from typing import List, Dict, Any
import pytest
import os

from .parameter_locations_excel_impl import ParameterLocationsExcelImpl
from src.domain.parameter_locations.parameter_locations import ParameterLocations, ParameterLocation
from src.domain.parameter_locations.parameter import Parameter


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "file_name": os.path.abspath("../../../test/data/test_parameter_sheet.xlsx"),
                    "sheet_name": "test_device",
                    "parameter_locations":
                        ParameterLocations(
                            locations=[
                                ParameterLocation(name="parameter1", cell_number="C2"),
                                ParameterLocation(name="parameter2", cell_number="C3"),
                                ParameterLocation(name="parameter3", cell_number="C4")
                            ]
                        )
                 },
                [
                    Parameter(name="parameter1", value="value1"),
                    Parameter(name="parameter2", value="value2"),
                    Parameter(name="parameter3", value="value3"),
                ],
                None
        ),
        # unexisted file name
        (
                {
                    "file_name": os.path.abspath("../../../test/data/test_parameter_sheet2.xlsx"),
                    "sheet_name": "test_device",
                    "parameter_locations": ""
                 },
                None,
                ValueError(r"The 'parameter_sheet_file' property(value: C:\Users\81802\PycharmProjects\github\network-device-converter\test\data\test_parameter_sheet2.xlsx)" +
                           r" of the ParameterLocationRepository doesn't exist in your directories")
        ),
        # unexisted sheet name
        (
                {
                    "file_name": os.path.abspath("../../../test/data/test_parameter_sheet.xlsx"),
                    "sheet_name": "test_device2",
                    "parameter_locations": ""
                 },
                None,
                ValueError(r"the sheet name 'test_device2' doesn't exist in " +
                           r"C:\Users\81802\PycharmProjects\github\network-device-converter\test\data\test_parameter_sheet.xlsx")
        ),
    ]
)
def test_read(test_input: Dict[str, Any], test_result: List[Parameter], test_exception_result: Exception):
    if test_result:
        assert ParameterLocationsExcelImpl(test_input["file_name"]).read(test_input["sheet_name"], test_input["parameter_locations"]) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterLocationsExcelImpl(test_input["file_name"]).read(test_input["sheet_name"], test_input["parameter_locations"])
        assert str(test_exception_result) in str(e.value)
