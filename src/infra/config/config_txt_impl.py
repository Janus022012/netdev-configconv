import sys
import os
import re

sys.path.append(os.path.abspath("../../domain/config"))
from .config import Config
from .config_repository import ConfigRepository


class ConfigTxtImpl(ConfigRepository):
    def __init__(self, config_sample_file: str, config: Config, output_config_file: str) -> None:
        super(ConfigTxtImpl, self).__init__(config_sample_file, config, output_config_file)

    def read(self) -> None:
        with open(self.config_sample_file, "r", encoding="utf-8") as cs:
            config_sample = cs.readlines()

        with open(self.output_config_file, "w", encoding="utf-8") as c:
            for config_row, config_line in enumerate(config_sample):
                stripped_config_line = config_line.strip()
                if self.inspect_marker(stripped_config_line):
                    if stripped_config_line in self.config.get_markers():
                        c.write(self.config.get_command(stripped_config_line))
                    else:
                        # loggerに変更
                        print(config_row, config_line)
                else:
                    c.write(config_line)
