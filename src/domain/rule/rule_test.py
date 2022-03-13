from turtle import filling
from typing import Dict, Any
import pytest
from src.domain.config.config import ConfigSource

from .rule import Action, ParameterLocationSource, CommandCondition, Options, ConverterRule, CommonParameter, Rule, IsEmptyCondition, IsContainedCondition
from src.domain.parameter_locations.parameter import Parameter, ParameterGroup
from src.domain.parameter_locations.parameter_locations import ParameterColumnLocation


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0.correct(all empty)
        (
                {
                    "isEmptyCondition": {
                        "type": "isEmpty",
                        "target_parameters": ["test1", "test2"]
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test1", value=""),
                            Parameter(name="test2", value=""),
                        ]
                    ),
                },
                True,
                None
        ),
        # 1.correct(partially empty)
        (
                {
                    "isEmptyCondition": {
                        "type": "isEmpty",
                        "target_parameters": ["test1", "test2"]
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test2", value=""),
                        ]
                    ),
                },
                True,
                None
        ),
        # 2.correct(all not empty)
        (
                {
                    "isEmptyCondition": {
                        "type": "isEmpty",
                        "target_parameters": ["test1", "test2"]
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test1", value="〇"),
                            Parameter(name="test2", value="〇"),
                        ]
                    ),
                },
                False,
                None
        ),
        # 3.correct(partially not empty)
        (
                {
                    "isEmptyCondition": {
                        "type": "isEmpty",
                        "target_parameters": ["test1", "test2"]
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test2", value="〇"),
                        ]
                    ),
                },
                False,
                None
        ),
    ]
)
def test_is_empty_condition(test_input: Dict[str, Any], test_result: bool, test_exception_result: Exception):
    if not test_exception_result:
        assert IsEmptyCondition(**test_input["isEmptyCondition"]).evaluate(test_input["parameters"]) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = IsEmptyCondition(**test_input["isEmptyCondition"]).evaluate(test_input["parameters"])
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0.all contained
        (
                {
                    "isContainedCondition": {
                        "type": "isContained",
                        "target_parameters": ["test1", "test2"],
                        "target_string": "〇"
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test1", value="〇"),
                            Parameter(name="test2", value="〇×"),
                        ]
                    )
                },
                True,
                None
        ),
        # 1. partially contained
        (
                {
                    "isContainedCondition": {
                        "type": "isContained",
                        "target_parameters": ["test1", "test2"],
                        "target_string": "〇"
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test1", value="〇"),
                            Parameter(name="test2", value="×"),
                        ]
                    )
                },
                False,
                None
        ),
        # 2. all not contained
        (
                {
                    "isContainedCondition": {
                        "type": "isContained",
                        "target_parameters": ["test1", "test2"],
                        "target_string": "〇"
                    },
                    "parameters": ParameterGroup(
                        parameters=[
                            Parameter(name="test1", value="〇"),
                            Parameter(name="test2", value="×"),
                        ]
                    )
                },
                False,
                None
        ),
    ]
)
def test_is_contained_condition(test_input: Dict[str, Any], test_result: bool, test_exception_result: Exception):
    if not test_exception_result:
        assert IsContainedCondition(**test_input["isContainedCondition"]).evaluate(test_input["parameters"]) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = IsContainedCondition(**test_input["isContainedCondition"]).evaluate(test_input["parameters"])
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "condition": {
                        "type": "isEmpty",
                        "target_parameters": ["Example"]
                    },
                    "action": "Delete",
                    "commands": ["Command"],
                 },
                CommandCondition(
                    condition=IsEmptyCondition(
                        type="isEmpty",
                        target_parameters=["Example"]
                    ),
                    action="Delete",
                    commands=["Command"],
                ),
                None
        ),
        # 1. empty condition
        (
            {
                "condition": {
                    "type": "",
                    "target_parameters": ["Example"]
                },
                "action": "Delete",
                "commands": ["Command"],
            },
            None,
            ValueError("No match for discriminator 'type' and value ''")
        ),
        # 2. invalid syntax action
        (
                {
                    "condition": {
                        "type": "isEmpty",
                        "target_parameters": ["Example"]
                    },
                    "action": "Multiply",
                    "commands": ["Command"],
                },
                None,
                ValueError("unexpected value; permitted: 'Delete', 'Add' (type=value_error.const; given=Multiply; permitted=('Delete', 'Add'))")
        ),
        # 3. empty commands
        (
                {
                    "condition": {
                        "type": "isEmpty",
                        "target_parameters": ["Example"]
                    },
                    "action": "Delete",
                    "commands": [],
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
        # 0. correct(isEmpty)
        (
                {
                    "command_condition": {
                        "condition": {
                            "type": 'isEmpty',
                            "target_parameters": ["Example"]
                        },
                        "action": "Delete",
                        "commands": ["Command1"],
                    },
                    "conditional_commands": ["    Command1"],
                    "applicable_commands": ["    Command1", "     Command2"],
                    "parameters": ParameterGroup(
                        parameters=[Parameter(name="Example", value="")]
                    ),
                },
                ["     Command2"],
                None
        ),
        # 1. incorrect(isEmpty)
        (
                {
                    "command_condition": {
                        "condition": {
                            "type": 'isEmpty',
                            "target_parameters": ["Example"]
                        },
                        "action": "Delete",
                        "commands": ["Command1"],
                    },
                    "conditional_commands": ["    Command1"],
                    "applicable_commands": ["    Command1", "     Command2"],
                    "parameters": ParameterGroup(
                        parameters=[Parameter(name="Example", value="〇")]
                    ),
                },
                ["    Command1", "     Command2"],
                None
        ),
        # 2. correct(isContained)
        (
                {
                    "command_condition": {
                        "condition": {
                            "type": 'isContained',
                            "target_parameters": ["Example"],
                            "target_string": "〇"
                        },
                        "action": "Delete",
                        "commands": ["Command1"],
                    },
                    "conditional_commands": ["    Command1"],
                    "applicable_commands": ["    Command1", "     Command2"],
                    "parameters": ParameterGroup(
                        parameters=[Parameter(name="Example", value="〇")]
                    ),
                },
                ["     Command2"],
                None
        ),
        # 3. incorrect(isContained)
        (
                {
                    "command_condition": {
                        "condition": {
                            "type": 'isContained',
                            "target_parameters": ["Example"],
                            "target_string": "〇"
                        },
                        "action": "Delete",
                        "commands": ["Command1"],
                    },
                    "conditional_commands": ["    Command1"],
                    "applicable_commands": ["    Command1", "     Command2"],
                    "parameters": ParameterGroup(
                        parameters=[Parameter(name="Example", value="")]
                    ),
                },
                ["    Command1", "     Command2"],
                None
        ),
    ]
)
def test_apply_command_condition(test_input: Dict[str, Any], test_result: ParameterLocationSource, test_exception_result: Exception):
    if test_result:
        assert CommandCondition(**test_input["command_condition"]).apply_command_condition(
            test_input["parameters"],
            test_input["conditional_commands"],
            test_input["applicable_commands"]
        ) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = CommandCondition(**test_input["command_condition"]).apply_command_condition(
                test_input["parameters"],
                test_input["conditional_commands"],
                test_input["applicable_commands"]
            )
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "command_condition": {
                        "condition": {
                            "type": 'isEmpty',
                            "target_parameters": ["Example"]
                        },
                        "action": "Delete",
                        "commands": ["Command1"],
                    },
                    "conditional_commands": ["    Command1"],
                    "applicable_commands": ["    Command1", "     Command2"],
                },
                ["     Command2"],
                None
        ),
    ]
)
def test_delete_do(test_input: Dict[str, Any], test_result: ParameterLocationSource, test_exception_result: Exception):
    if test_result:
        assert Action.build("Delete").do(
            test_input["command_condition"],
            test_input["conditional_commands"],
            test_input["applicable_commands"]
        ) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Action.build("Delete").do(
                test_input["command_condition"],
                test_input["conditional_commands"],
                test_input["applicable_commands"]
            )
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
                {
                    "command_condition": {
                        "condition": {
                            "type": 'isEmpty',
                            "target_parameters": ["Example"]
                        },
                        "action": "Add",
                        "commands": ["Command1"],
                    },
                    "conditional_commands": ["    Command2"],
                    "applicable_commands":  ["    Command1"],
                },
                ["    Command1", "    Command2"],
                None
        ),
    ]
)
def test_add_do(test_input: Dict[str, Any], test_result: ParameterLocationSource, test_exception_result: Exception):
    if test_result:
        assert Action.build("Add").do(
            test_input["command_condition"],
            test_input["conditional_commands"],
            test_input["applicable_commands"]
        ) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Action.build("Add").do(
                test_input["command_condition"],
                test_input["conditional_commands"],
                test_input["applicable_commands"]
            )
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0.correct
        (
                {
                    "indent_level": 1,
                    "filling_each_command": True,
                    "filling_each_commands_group": True
                 },
                Options(
                    indent_level=1,
                    filling_each_command=True,
                    filling_each_commands_group=True
                ),
                None
        ),
        # 1.correct
        (
                {
                    "filling_each_command": True,
                    "filling_each_commands_group": True
                },
                Options(
                    indent_level=0,
                    filling_each_command=True,
                    filling_each_commands_group=True
                ),
                None
        ),
        # 2.correct
        (
                {},
                Options(
                    indent_level=0,
                    filling_each_command=False,
                    filling_each_commands_group=False
                ),
                None
        ),
        # 3.empty indent_level
        (
                {
                    "indent_level": "g"
                },
                None,
                ValueError("value is not a valid integer (type=type_error.integer)")
        ),
        # 4.invalid filling_each_command
        (
                {
                    "filling_each_commands": "TRUEK"
                },
                None,
                ValueError("value could not be parsed to a boolean (type=type_error.bool)")
        ),
        # 5.invalid filling_each_commands_group
        (
                {
                    "filling_each_commands_group": "TRUEK"
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
        # 0.correct
        (
                {
                    "options": {
                        "indent_level": 4,
                        "filling_each_commands": True,
                        "filling_each_commands_group": True
                    },
                    "commands_group": [
                        ["command1", "command2"]
                    ],
                    "filling": "!"
                },
                [
                    ["    command1", "!", "    command2", "!"]
                ],
                None
        ),
    ]
)
def test_options_assign_options(test_input: Dict[str, str], test_result: Options, test_exception_result: Exception):
    if test_result:
        assert Options(**test_input["options"]).assign_options(test_input["commands_group"], test_input["filling"]) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Options(**test_input["options"]).assign_options(test_input["commands_group"], test_input["filling"])
        assert str(test_exception_result) in str(e.value)



@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "filling": "!"
                },
                CommonParameter(filling="!"),
                None
        ),
        #  filling
        (
                {
                    "filling": ""
                },
                None,
                ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
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
        # 0. correct
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 5,
                        "row_to": 10,
                    },
                    "commands": [
                        "command1",
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            ConverterRule(
                description="example",
                marker="%%example_marker%%",
                data=ParameterLocationSource(
                    parameter_column_locations=[
                        ParameterColumnLocation(name="Example", column_number="A")
                    ],
                    row_from=5,
                    row_to=10
                ),
                commands=["command1"],
                conditions=[CommandCondition(
                    condition=IsEmptyCondition(
                        type="isEmpty",
                        target_parameters=["Example"]
                    ),
                    action="Delete",
                    commands=["Command1"],
                )],
                options=Options(
                    indent_level=1,
                    filling_each_command=True,
                    filling_each_commands_group=True
                )
            ), 
            None
        ),
        # 1.invalid marker
        (
            {
                    "description": "example",
                    "marker": "%%%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 5,
                        "row_to": 10,
                    },
                    "commands": [
                        "command1",
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None, 
            ValueError("ensure this value has at least 5 characters (type=value_error.any_str.min_length; limit_value=5)")
        ),
        # 2. invalid parameter_column_locations.name
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "", "column_number": "A"}
                        ],
                        "row_from": 5,
                        "row_to": 10,
                    },
                    "commands": [
                        "command1",
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)")
        ),
        # 3. invalid parameter_column_locations.column_number
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "あ"}
                        ],
                        "row_from": 5,
                        "row_to": 10,
                    },
                    "commands": [
                        "command1",
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError('string does not match regex "[A-Z]+" (type=value_error.str.regex; pattern=[A-Z]+)')
        ),
        # 4. invalid parameter_column_locations.row_from
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 0,
                        "row_to": 10,
                    },
                    "commands": [
                        "command1",
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("'row_from' property of the ParameterSaveLocationSource must not be empty and must be greater than 1 (type=value_error)")
        ),
        # 5. invalid parameter_column_locations.row_to
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 1,
                        "row_to": 0,
                    },
                    "commands": [
                        "command1",
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("ensure this value is greater than or equal to 1 (type=value_error.number.not_ge; limit_value=1)")
        ),
        # 6, invalid commands
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 1,
                        "row_to": 5,
                    },
                    "commands": [],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)")
        ),
        # 7, invalid condition type
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 1,
                        "row_to": 5,
                    },
                    "commands": [
                        "command1"
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'Assume',
                                "target_parameters": ["Example"]
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("No match for discriminator 'type' and value 'Assume' (allowed values: 'isEmpty', 'isContained') (type=value_error.discriminated_union.invalid_discriminator; discriminator_key=type; discriminator_value=Assume; allowed_values='isEmpty', 'isContained')")
        ),
        # 8, invalid condition target_parameters
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 1,
                        "row_to": 5,
                    },
                    "commands": [
                        "command1"
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": []
                            },
                            "action": "Delete",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)")
        ),
        # 9. invalid condition action
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 1,
                        "row_to": 5,
                    },
                    "commands": [
                        "command1"
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example1"]
                            },
                            "action": "Assume",
                            "commands": ["Command1"],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("'Delete', 'Add' (type=value_error.const; given=Assume; permitted=('Delete', 'Add'))")
        ),
        # 10. invalid condition commands
        (
            {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 1,
                        "row_to": 5,
                    },
                    "commands": [
                        "command1"
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example1"]
                            },
                            "action": "Delete",
                            "commands": [],
                        },
                    ],
                    "options": {
                        "indent_level": 1,
                        "filling_each_command": True,
                        "filling_each_commands_group": True
                    },
            },
            None,
            ValueError("ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)")
        ),
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
        # 0. correct
        (
            {
                "converter_rule":  {
                    "description": "example",
                    "marker": "%%example_marker%%",
                    "data": {
                        "parameter_column_locations": [
                            {"name": "Example", "column_number": "A"}
                        ],
                        "row_from": 5,
                        "row_to": 10,
                    },
                    "commands": [
                        "command1",
                        "command2"
                    ],
                    "conditions": [
                        {           
                            "condition": {
                                "type": 'isEmpty',
                                "target_parameters": ["Example1"]
                            },
                            "action": "Delete",
                            "commands": ["command1"],
                        },
                        {           
                            "condition": {
                                "type": 'isContained',
                                "target_parameters": ["Example2"],
                                "target_string": "example"
                            },
                            "action": "Add",
                            "commands": ["command3"],
                        },
                    ],
                    "options": {
                        "indent_level": 4,
                        "filling_each_commands": True,
                        "filling_each_commands_group": True
                    },
                },
                "parameter_group_list": [ParameterGroup(parameters=[
                    Parameter(name="Example1", value=""),
                    Parameter(name="Example2", value="example")
                ])],
                "common_parameter": CommonParameter(filling="!")
            },
            ConfigSource(
                marker="%%example_marker%%",
                commands_group=[["    command2", "!", "    command3", "!"]]
            ),
            None, 
        ),
    ]
)
def test_converter_rule_make_config_source(test_input: Dict[str, str], test_result: ConverterRule, test_exception_result: Exception):
    if test_result:
        assert ConverterRule(**test_input["converter_rule"]).make_config_source(test_input["parameter_group_list"], test_input["common_parameter"]) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ConverterRule(**test_input["converter_rule"]).make_config_source(test_input["parameter_group_list"], test_input["common_parameter"])
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # 0. correct
        (
            {
                    "common_parameter": {
                        "filling": "!"
                    },
                    "converter_rules": {
                        "example_marker": {
                            "description": "example",
                            "marker": "%%example_marker%%",
                            "data": {
                                "parameter_column_locations": [
                                    {"name": "Example", "column_number": "A"}
                                ],
                                "row_from": 5,
                                "row_to": 10,
                            },
                            "commands": [
                                "command1",
                            ],
                            "conditions": [
                                {           
                                    "condition": {
                                        "type": 'isEmpty',
                                        "target_parameters": ["Example"]
                                    },
                                    "action": "Delete",
                                    "commands": ["Command1"],
                                },
                            ],
                            "options": {
                                "indent_level": 1,
                                "filling_each_command": True,
                                "filling_each_commands_group": True
                            },
                        },
                    }
            },
            Rule(
                common_parameter=CommonParameter(filling="!"),
                converter_rules={
                    "example_marker": 
                        ConverterRule(
                        description="example",
                        marker="%%example_marker%%",
                        data=ParameterLocationSource(
                            parameter_column_locations=[
                                ParameterColumnLocation(name="Example", column_number="A")
                            ],
                            row_from=5,
                            row_to=10
                        ),
                        commands=["command1"],
                        conditions=[CommandCondition(
                            condition=IsEmptyCondition(
                                type="isEmpty",
                                target_parameters=["Example"]
                            ),
                            action="Delete",
                            commands=["Command1"],
                        )],
                        options=Options(
                            indent_level=1,
                            filling_each_command=True,
                            filling_each_commands_group=True
                        )
                    )
                }
            ), 
            None
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