from typing import Dict
import pytest

from .config import Config, ConfigSource


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct1
        (
                {"marker": "%%example%%", "commands": ["example command"]},
                ConfigSource(marker="%%example%%", commands=["example command"]),
                None
        ),
        # correct2
        (
                {"marker": "%%example%%", "commands": ["example command1", "example command2"]},
                ConfigSource(marker="%%example%%", commands=["example command1", "example command2"]),
                None
        ),
        # wrong format marker
        (
                {"marker": "%%example%", "commands": ["example command"]},
                None,
                ValueError('string does not match regex "%{2}\\w+%{2}" (type=value_error.str.regex; pattern=%{2}\\w+%{2})')
        ),
        # too short marker
        (
                {"marker": "%%%%", "commands": ["example command"]},
                None,
                ValueError(
                    'ensure this value has at least 5 characters (type=value_error.any_str.min_length; limit_value=5)')
        ),
        # no commands
        (
                {"marker": "%%example%%", "commands": []},
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
                            {"marker": "%%example%%", "commands": ["example command"]},
                            {"marker": "%%example%%", "commands": ["example command1", "example command2"]}
                        ]
                },
                Config(config_sources=[
                    ConfigSource(marker="%%example%%", commands=["example command"]),
                    ConfigSource(marker="%%example%%", commands=["example command1", "example command2"])
                ]),
                None
        ),
        # wrong format marker
        (
                {
                    "config_sources":
                        [
                            {"marker": "fffffff%%", "commands": ["example command"]},
                            {"marker": "%%example%%", "commands": ["example command1", "example command2"]}
                        ]
                },
                None,
                ValueError('string does not match regex "%{2}\\w+%{2}" (type=value_error.str.regex; pattern=%{2}\\w+%{2})')
        ),
        # too short marker
        (
                {
                    "config_sources":
                        [
                            {"marker": "%%%%", "commands": ["example command"]},
                            {"marker": "%%example%%", "commands": ["example command1", "example command2"]}
                        ]
                },
                None,
                ValueError('ensure this value has at least 5 characters (type=value_error.any_str.min_length; limit_value=5)')
        ),
        # no commands
        (
                {
                    "config_sources":
                        [
                            {"marker": "%%%%", "commands": []},
                            {"marker": "%%example%%", "commands": ["example command1", "example command2"]}
                        ]
                },
                None,
                ValueError('ensure this value has at least 1 items (type=value_error.list.min_items; limit_value=1)')
        ),
    ]
)
def test_config(test_input: Dict[str, str], test_result: Config, test_exception_result: Exception):
    if test_result:
        assert Config(**test_input) == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = Config(**test_input)
        assert str(test_exception_result) in str(e.value)

