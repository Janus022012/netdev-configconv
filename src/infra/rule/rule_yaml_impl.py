from logging import config

from src.domain.rule.rule import Rule
from src.domain.rule.rule_repository import RuleRepository

import logging
import os
import yaml


config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class RuleYamlImpl(RuleRepository):
    def __init__(self, rule_file: str) -> None:
        super(RuleYamlImpl, self).__init__(rule_file)

    def read(self) -> Rule:
        with open(self.rule_file, "r", encoding="UTF-8") as f:
            raw_rule = yaml.safe_load(f)
        return Rule(**raw_rule)
