from typing import Dict, Any

import pytest

from .parameter import Parameter, ParameterGroup
from .parameter_locations import ParameterLocations, ParameterLocation, ParameterColumnLocation, ParameterLocationSource


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {"name": "Example", "value": "Example"},
                Parameter(name="Example", value="Example"),
                None
        ),
        # 1. correct(empty value)
        (
                {"name": "Example", "value": ""},
                Parameter(name="Example", value=""),
                None
        ),
        # 2. empty name
        (
                {"name": "", "value": "Example"},
                None,
                ValueError('ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)')
        ),
    ]
)
def test_parameter(test_input: Dict[str, str], test_result: Parameter, test_exception_result: Exception):
    if test_result:
        assert Parameter(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Parameter(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "parameters": [
                        {"name": "Example1", "value": "Example1"},
                        {"name": "Example2", "value": "Example2"}
                    ]
                },
                ParameterGroup(
                    parameters=[
                        Parameter(name="Example1", value="Example1"),
                        Parameter(name="Example2", value="Example2")
                    ]
                ),
                None
        ),
        # 1. correct(empty value)
        (
                {
                    "parameters": [
                        {"name": "Example1", "value": ""},
                        {"name": "Example2", "value": "Example2"}
                    ]
                },
                ParameterGroup(
                    parameters=[
                        Parameter(name="Example1", value=""),
                        Parameter(name="Example2", value="Example2")
                    ]
                ),
                None
        ),
        # 2. empty name
        (
                {
                    "parameters": [
                        {"name": "Example1", "value": "Example1"},
                        {"name": "", "value": "Example2"}
                    ]
                },
                None,
                ValueError('ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)')
        ),
    ]
)
def test_parameter_group(test_input: Dict[str, str], test_result: Parameter, test_exception_result: Exception):
    if test_result:
        assert ParameterGroup(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterGroup(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "parameter_group": {
                        "parameters": [
                                {"name": "Example1", "value": "Example1"},
                                {"name": "Example2", "value": "Example2"}
                        ]
                    },
                    "name": "Example1",
                },
                True,
                None
        ),
        # 1. correct
        (
                {
                    "parameter_group": {
                        "parameters": [
                                {"name": "Example1", "value": "Example1"},
                                {"name": "Example2", "value": "Example2"}
                        ]
                    },
                    "name": "Examplex",
                },
                False,
                None
        ),
    ]
)
def test_parameter_group_contain(test_input: Dict[str, Any], test_result: bool, test_exception_result: Exception):
    if not test_exception_result:
        assert (test_input["name"] in ParameterGroup(**test_input["parameter_group"])) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = test_input["name"] in ParameterGroup(**test_input["parameter_group"])
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "parameter_group": {
                        "parameters": [
                                {"name": "Example1", "value": "Example1"},
                                {"name": "Example2", "value": "Example2"}
                        ]
                    },
                    "name": "Example1",
                },
                Parameter(name="Example1", value="Example1"),
                None
        ),
        # 1. correct
        (
                {
                    "parameter_group": {
                        "parameters": [
                                {"name": "Example1", "value": "Example1"},
                                {"name": "Example2", "value": "Example2"}
                        ]
                    },
                    "name": "Examplex",
                },
                None,
                None
        ),
    ]
)
def test_parameter_get(test_input: Dict[str, Any], test_result: bool, test_exception_result: Exception):
    if not test_exception_result:
        assert (ParameterGroup(**test_input["parameter_group"]).get(test_input["name"])) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterGroup(**test_input["parameter_group"]).get(test_input["name"])
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "parameters": [
                            {"name": "Example1", "value": "Example1"},
                            {"name": "Example2", "value": "Example2"}
                    ]
                },
                {"Example1": "Example1", "Example2": "Example2"},
                None
        ),
    ]
)
def test_parameter_tp_dict(test_input: Dict[str, Any], test_result: bool, test_exception_result: Exception):
    if not test_exception_result:
        assert (ParameterGroup(**test_input).to_dict()) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterGroup(**test_input).to_dict()
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {"name": "Example", "column_number": "A"},
                ParameterColumnLocation(name="Example", column_number="A"),
                None
        ),
        # 1. empty name
        (
                {"name": "", "column_number": "A"},
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # 2. empty column_number
        (
                {"name": "Example", "column_number": ""},
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # 3. invalid syntax column_number
        (
                {"name": "Example", "column_number": "1"},
                None,
                ValueError('string does not match regex "[A-Z]+" (type=value_error.str.regex; pattern=[A-Z]+)')
        )
    ]
)
def test_parameter_column_location(test_input: Dict[str, str], test_result: ParameterColumnLocation, test_exception_result: Exception):
    if test_result:
        assert ParameterColumnLocation(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterColumnLocation(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0.correct
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "A"}],
                    "row_from": 1,
                    "row_to": 1,
                },
                ParameterLocationSource(
                    parameter_column_locations=[
                        ParameterColumnLocation(name="Example", column_number="A")
                    ],
                    row_from=1,
                    row_to=1
                ),
                None
        ),
        # 1.empty name
        (
                {
                    "parameter_column_locations": [{"name": "", "column_number": "A"}],
                    "row_from": 1,
                    "row_to": 1,
                },
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # 2.empty column_number
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": ""}],
                    "row_from": 1,
                    "row_to": 1,
                },
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # 3.invalid syntax column_number
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "1"}],
                    "row_from": 1,
                    "row_to": 1,
                },
                None,
                ValueError('string does not match regex "[A-Z]+" (type=value_error.str.regex; pattern=[A-Z]+)')
        ),
        # 4.empty parameter_column_locations
        (
                {
                    "parameter_column_locations": [],
                    "row_from": 1,
                    "row_to": 1,
                },
                None,
                ValueError('ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)')
        ),
        # 5.empty row_from
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "A"}],
                    "row_to": 1,
                },
                None,
                ValueError("row_from\n  field required (type=value_error.missing)")
        ),
        # 6.empty row_to
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "A"}],
                    "row_from": 1,
                },
                None,
                ValueError('1 validation error for ParameterLocationSource\nrow_to\n  field required (type=value_error.missing)')
        ),
        # 7.invalid row_to
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "A"}],
                    "row_from": 10,
                    "row_to": 5,
                },
                None,
                ValueError("the 'row_to' property of the ParameterSaveLocationSource must be greater than the 'row_from' property (type=value_error)")
        ),
    ]
)
def test_parameter_location_source(test_input: Dict[str, str], test_result: ParameterLocationSource, test_exception_result: Exception):
    if test_result:
        assert ParameterLocationSource(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterLocationSource(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0.correct
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "A"}],
                    "row_from": 1,
                    "row_to": 3,
                },
                [
                    ParameterLocations(locations=[ParameterLocation(name="Example", cell_number="A1")]),
                    ParameterLocations(locations=[ParameterLocation(name="Example", cell_number="A2")]),
                    ParameterLocations(locations=[ParameterLocation(name="Example", cell_number="A3")]),
                ],
                None
        ),
    ]
)
def test_convert_to_parameter_locations_list(test_input: Dict[str, str], test_result: ParameterLocationSource, test_exception_result: Exception):
    if test_result:
        assert ParameterLocationSource(**test_input).convert_to_parameter_locations_list() == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterLocationSource(**test_input).convert_to_parameter_locations_list()
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {"name": "Example", "cell_number": "A10"},
                ParameterLocation(name="Example", cell_number="A10"),
                None
        ),
        # empty name
        (
                {"name": "", "cell_number": "A10"},
                None,
                ValueError('ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)')
        ),
        # empty cell_number
        (
                {"name": "Example", "cell_number": ""},
                None,
                ValueError('ensure this value has at least 2 characters (type=value_error.any_str.min_length; limit_value=2)')
        ),
        # wrong syntax cell_number
        (
                {"name": "Example", "cell_number": "100"},
                None,
                ValueError('string does not match regex "^[A-Z]+\\d+" (type=value_error.str.regex; pattern=^[A-Z]+\\d+)')
        ),
    ]
)
def test_parameter_location(test_input: Dict[str, str], test_result: ParameterLocation, test_exception_result: Exception):
    if test_result:
        assert ParameterLocation(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterLocation(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "locations": [
                        {"name": "Example1", "cell_number": "A10"},
                        {"name": "Example2", "cell_number": "A11"},
                    ]
                },
                ParameterLocations(locations=[
                    ParameterLocation(name="Example1", cell_number="A10"),
                    ParameterLocation(name="Example2", cell_number="A11")
                ]),
                None
        ),
        # empty name
        (
                {
                    "locations": [
                        {"name": "", "cell_number": "A10"},
                        {"name": "Example2", "cell_number": "A11"},
                    ]
                },
                None,
                ValueError('ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)')
        ),
        # empty cell_number
        (
                {
                    "locations": [
                        {"name": "Example1", "cell_number": ""},
                        {"name": "Example2", "cell_number": "A11"},
                    ]
                },
                None,
                ValueError('ensure this value has at least 2 characters (type=value_error.any_str.min_length; limit_value=2)')
        ),
        # wrong syntax cell_number
        (
                {
                    "locations": [
                        {"name": "Example1", "cell_number": "100"},
                        {"name": "Example2", "cell_number": "A11"},
                    ]
                },
                None,
                ValueError('string does not match regex "^[A-Z]+\\d+" (type=value_error.str.regex; pattern=^[A-Z]+\\d+)')
        ),
    ]
)
def test_parameter_locations(test_input: Dict[str, str], test_result: ParameterLocations, test_exception_result: Exception):
    if test_result:
        assert ParameterLocations(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ParameterLocations(**test_input)
        assert str(test_exception_result) in str(e.value)