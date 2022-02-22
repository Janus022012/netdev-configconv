import sys
import os
import yaml

sys.path.append(os.path.abspath("../../domain/rule"))
from .rule import Rule
from .rule_repository import RuleRepository


class RuleYamlImpl(RuleRepository):
    def __init__(self, rule_file: str):
        super(RuleYamlImpl, self).__init__(rule_file)

    def read(self) -> Rule:
        with open(self.rule_file, "r", encoding="UTF-8") as f:
            raw_rule = yaml.safe_load(f)
        return Rule(**raw_rule)
