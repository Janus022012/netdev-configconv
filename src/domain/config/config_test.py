from typing import Dict
import pytest

from .config import Config, ConfigSource


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct1
        (
                {
                    "marker": "%%example%%",
                    "command_groups": [
                        ["example command"],
                    ]
                },
                ConfigSource(
                    marker="%%example%%",
                    command_groups=[
                        ["example command"],
                    ]
                ),
                None
        ),
        # correct2
        (
                {
                    "marker": "%%example%%",
                    "command_groups": [
                        ["example command1"],
                        ["example command2"]
                    ]
                },
                ConfigSource(
                    marker="%%example%%",
                    command_groups=[
                        ["example command1"],
                        ["example command2"]
                    ]
                ),
                None
        ),
        # wrong format marker
        (
                {
                    "marker": "%%example%",
                    "command_groups": [
                        ["example command"],
                    ]
                },
                None,
                ValueError(
                    'string does not match regex "%{2}\\w+%{2}" (type=value_error.str.regex; pattern=%{2}\\w+%{2})')
        ),
        # too short marker
        (
                {
                    "marker": "%%%%",
                    "command_groups": [
                        ["example command"],
                    ]
                },
                None,
                ValueError(
                    'ensure this value has at least 5 characters (type=value_error.any_str.min_length; limit_value=5)')
        ),
        # no command_groups
        (
                {
                    "marker": "%%example%%",
                    "command_groups": []
                },
                None,
                ValueError('ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)')
        ),
    ]
)
def test_config_source(test_input: Dict[str, str], test_result: ConfigSource, test_exception_result: Exception):
    if test_result:
        assert ConfigSource(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = ConfigSource(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%example1%%",
                                "command_groups": [
                                    ["example command"],
                                ]
                            },
                            {
                                "marker": "%%example2%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                Config(config_sources=[
                    ConfigSource(
                        marker="%%example1%%",
                        command_groups=[
                            ["example command"]
                        ]),
                    ConfigSource(
                        marker="%%example2%%",
                        command_groups=[
                            ["example command1"],
                            ["example command2"]
                        ]
                    )
                ]),
                None
        ),
        # wrong format marker
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "fffffff%%",
                                "command_groups": [
                                    ["example command"]
                                ]
                            },
                            {
                                "marker": "%%example%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                None,
                ValueError(
                    'string does not match regex "%{2}\\w+%{2}" (type=value_error.str.regex; pattern=%{2}\\w+%{2})')
        ),
        # too short marker
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%%%",
                                "command_groups": [
                                    ["example command"]
                                ]
                            },
                            {
                                "marker": "%%example%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                None,
                ValueError(
                    'ensure this value has at least 5 characters (type=value_error.any_str.min_length; limit_value=5)')
        ),
        # no command_groups
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%%%",
                                "command_groups": []
                            },
                            {
                                "marker": "%%example%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                None,
                ValueError('ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)')
        ),
        # duplicate marker
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%example%%",
                                "command_groups": [
                                    ["example command1"]
                                ]
                            },
                            {
                                "marker": "%%example%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                None,
                ValueError("Each element of the markers in 'config_sources' of the Config must be unique (type=value_error)")
        )
    ]
)
def test_config(test_input: Dict[str, str], test_result: Config, test_exception_result: Exception):
    if test_result:
        assert Config(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Config(**test_input)
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%example1%%",
                                "command_groups": [
                                    ["example command"],
                                ]
                            },
                            {
                                "marker": "%%example2%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                ["%%example1%%", "%%example2%%"],
                None
        ),
    ]
)
def test_config_get_markers(test_input: Dict[str, str], test_result: Config, test_exception_result: Exception):
    if test_result:
        assert Config(**test_input).get_markers() == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Config(**test_input).get_markers()
        assert str(test_exception_result) in str(e.value)


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%example1%%",
                                "command_groups": [
                                    ["example command"],
                                ]
                            },
                            {
                                "marker": "%%example2%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                [
                    ["example command"],
                ],
                None
        ),
        # 1. correct
        (
                {
                    "config_sources":
                        [
                            {
                                "marker": "%%example3%%",
                                "command_groups": [
                                    ["example command"],
                                ]
                            },
                            {
                                "marker": "%%example2%%",
                                "command_groups": [
                                    ["example command1"],
                                    ["example command2"]
                                ]
                            }
                        ]
                },
                [],
                None
        ),
    ]
)
def test_config_get_commands_group(test_input: Dict[str, str], test_result: Config, test_exception_result: Exception):
    if not test_exception_result:
        assert Config(**test_input).get_commands_group("%%example1%%") == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Config(**test_input).get_commands_group("%%example1%%")
        assert str(test_exception_result) in str(e.value)