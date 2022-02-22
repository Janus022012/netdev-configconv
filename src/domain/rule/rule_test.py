from typing import Dict
import pytest

from .rule import ParameterColumnLocation, ParameterLocationSource, CommandCondition, Options, ConverterRule, CommonParameter, Rule


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {"name": "Example", "column_number": "A"},
                ParameterColumnLocation(name="Example", column_number="A"),
                None
        ),
        # empty name
        (
                {"name": "", "column_number": "A"},
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # empty column_number
        (
                {"name": "Example", "column_number": ""},
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # invalid syntax column_number
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
                        ParameterColumnLocation(
                            name="Example", column_number="A"
                        )
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
                    "row_from": 0,
                    "row_to": 1,
                },
                None,
                ValueError("the 'row_from' property of the ParameterSaveLocationSource must not be empty and must be greater than 1")
        ),
        # 6.empty row_to
        (
                {
                    "parameter_column_locations": [{"name": "Example", "column_number": "A"}],
                    "row_from": 1,
                    "row_to": 0,
                },
                None,
                ValueError('ensure this value is greater than or equal to 1 (type=value_error.number.not_ge; limit_value=1)')
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
        # correct
        (
                {
                    "condition": "Example",
                    "action": "Delete",
                    "command": ["Command"],
                 },
                CommandCondition(
                    condition="Example",
                    action="Delete",
                    command=["Command"],
                ),
                None
        ),
        # empty condition
        (
            {
                "condition": "",
                "action": "Delete",
                "command": ["Command"],
            },
            None,
            ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # invalid syntax action
        (
                {
                    "condition": "Example",
                    "action": "Multiply",
                    "command": ["Command"],
                },
                None,
                ValueError("unexpected value; permitted: 'Delete', 'Add' (type=value_error.const; given=Multiply; permitted=('Delete', 'Add'))")
        ),
        # empty command
        (
                {
                    "condition": "Example",
                    "action": "Multiply",
                    "command": [],
                },
                None,
                ValueError("ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)")
        ),
    ]
)
def test_command_condition(test_input: Dict[str, str], test_result: CommandCondition, test_exception_result: Exception):
    if test_result:
        assert CommandCondition(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = CommandCondition(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0.correct
        (
                {
                    "indent_level": 1,
                    "filling_each_command": True
                 },
                Options(
                    indent_level=1,
                    filling_each_command=True
                ),
                None
        ),
        # 1.correct
        (
                {
                    "filling_each_command": True
                },
                Options(
                    indent_level=0,
                    filling_each_command=True
                ),
                None
        ),
        # 2.correct
        (
                {
                    "indent_level": 1,
                },
                Options(
                    indent_level=1,
                    filling_each_command=False
                ),
                None
        ),
        # 3.invalid filling_each_command
        (
                {
                    "indent_level": "g",
                    "filling_each_command": True
                },
                None,
                ValueError("value is not a valid integer (type=type_error.integer)")
        ),
        # 4.invalid filling_each_command
        (
                {
                    "indent_level": 1,
                    "filling_each_command": "TRUEK"
                },
                None,
                ValueError("value could not be parsed to a boolean (type=type_error.bool)")
        ),
    ]
)
def test_options(test_input: Dict[str, str], test_result: Options, test_exception_result: Exception):
    if test_result:
        assert Options(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Options(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
            None, None, None
        )
    ]
)
def test_converter_rule(test_input: Dict[str, str], test_result: ConverterRule, test_exception_result: Exception):
    if test_result:
        assert ConverterRule(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ConverterRule(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
            None, None, None
        )
    ]
)
def test_common_parameter(test_input: Dict[str, str], test_result: CommonParameter, test_exception_result: Exception):
    if test_result:
        assert CommonParameter(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = CommonParameter(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
            None, None, None
        )
    ]
)
def test_rule(test_input: Dict[str, str], test_result: Rule, test_exception_result: Exception):
    if test_result:
        assert Rule(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Rule(**test_input)
        assert str(test_exception_result) in str(e.value)