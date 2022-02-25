from src.domain.config.config import Config
from src.domain.config.config_repository import ConfigRepository


class ConfigTxtImpl(ConfigRepository):
    def __init__(self, config_sample_file: str) -> None:
        super(ConfigTxtImpl, self).__init__(config_sample_file)

    def write(self, config: Config, output_config_file: str) -> None:
        with open(self.config_sample_file, "r", encoding="utf-8") as cs:
            config_sample = cs.readlines()

        with open(output_config_file, "w", encoding="utf-8") as c:
            for config_row, config_line in enumerate(config_sample):
                if self._inspect_marker(config_line.strip()):
                    if config_line.strip() in config.get_markers():
                        c.writelines(config.get_commands_group(config_line.strip()))
                else:
                    c.write(config_line)
