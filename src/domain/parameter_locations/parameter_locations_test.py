from typing import Dict

import pytest

from .parameter import Parameter
from .parameter_locations import ParameterLocations, ParameterLocation


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {"name": "Example", "value": "Example"},
                Parameter(name="Example", value="Example"),
                None
        ),
        # empty name
        (
                {"name": "", "value": "Example"},
                None,
                ValueError('ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)')
        ),
        # empty value
        (
                {"name": "Example", "value": ""},
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
def test_parameter_save_location(test_input: Dict[str, str], test_result: ParameterLocation, test_exception_result: Exception):
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