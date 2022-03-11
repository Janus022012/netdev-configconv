import os
import pytest

from .rule_yaml_impl import RuleYamlImpl
from src.domain.rule.rule import Rule


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                os.path.abspath("../../../test/data/test_rule.yml"),
                Rule(
                    **{
                        'common_parameter': {'filling': '?'},
                        'converter_rules': {
                            'HostName': {
                                'description': 'ホスト名',
                                'marker': '%%HostName%%',
                                'data': {
                                    'parameter_column_locations': [{'name': 'HostName', 'column_number': 'D'}],
                                    'row_to': 9, 'row_from': 9
                                },
                                'commands': ['hostname {HostName}'],
                                'conditions': [
                                    {
                                        'condition': {
                                            "type": "isEmpty",
                                            "target_parameters": ["HostName"]
                                        },
                                        'action': 'Add',
                                        'commands': ['hostname {HostName}']
                                    }
                                ],
                                'options': {
                                    'indent_level': 4,
                                    'filling_each_commands': True,
                                    'filling_each_command_groups': True
                                }
                            }
                        }
                    }
                ),
                None
        ),
        # unexisted filename
        (
                os.path.abspath("../../../test/data/test_rule2.yml"),
                None,
                ValueError(
                    r"The 'rule_file' property(C:\Users\81802\PycharmProjects\github\network-device-converter\test\data\test_rule2.yml)" +
                    r" of the RuleRepository must exist in directories."
                )
        ),
    ]
)
def test_read(test_input: str, test_result: Rule, test_exception_result: Exception):
    if test_result:
        assert RuleYamlImpl(test_input).read() == test_result
    else:
        with pytest.raises(Exception) as e:
            _ = RuleYamlImpl(test_input).read()
        assert str(test_exception_result) in str(e.value)
