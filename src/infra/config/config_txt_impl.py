from src.domain.config.config import Config
from src.domain.config.config_repository import ConfigRepository

from typing import List


class ConfigTxtImpl(ConfigRepository):

    def __init__(self, config_sample_file: str) -> None:

        super(ConfigTxtImpl, self).__init__(config_sample_file)

    def write(self, config: Config, output_config_file: str) -> None:

        with open(self.config_sample_file, "r", encoding="utf-8") as cs:

            config_sample: List[str] = cs.readlines()

        with open(output_config_file, "w", encoding="utf-8") as c:

            for config_row, config_line in enumerate(config_sample):

                stripped_config_line: str = config_line.strip()

                if self._inspect_marker(stripped_config_line):

                    if stripped_config_line in config.get_markers():

                        for commands_group in config.get_commands_group(stripped_config_line):

                            for command in commands_group:

                                c.write(f"{command}\n")

                    else:

                        print(config_row)

                else:

                    c.write(config_line)
