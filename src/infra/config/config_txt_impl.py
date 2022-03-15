from typing import List
from logging import config
from src.domain.config.config import Config
from src.domain.config.config_repository import ConfigRepository

import logging
import os


config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ConfigTxtImpl(ConfigRepository):
    """ConfigTxtImpl
    
    本クラスは、ConfigSampleFileとConfigを用いてtxt(log)形式のコンフィグを出力するための具象クラスである

    Attributes:
        config_sample_file str: ConfigSampleFileが存在するファイルパス

    """

    def __init__(self, config_sample_file: str) -> None:

        logger.debug(f"Intializing ConfigTxtImpl(config_sample_file={config_sample_file})...")

        super(ConfigTxtImpl, self).__init__(config_sample_file)


    def write(self, config: Config, output_config_file: str) -> None:
        """write
    
        ConfigSampleFileとConfigインスタンスからConfigファイルをTxt(Log)形式で出力する関数

        Attributes:
            config_sample_file str: ConfigSampleFileが存在するファイルパス

        """

        logger.debug(f"Reading a config_sample_file({self.config_sample_file})...")

        with open(self.config_sample_file, "r", encoding="utf-8") as cs:
            config_sample: List[str] = cs.readlines()

        logger.debug(f"Reading a config_sample_file({self.config_sample_file}) has been finished successfully")

        logger.debug(f"Writing a config_file({output_config_file})...")

        with open(output_config_file, "w", encoding="utf-8") as c:

            for config_row, config_line in enumerate(config_sample):
                stripped_config_line: str = config_line.strip()

                if self._inspect_marker(stripped_config_line):

                    logger.debug(f"Inspected a marker({stripped_config_line}) in the ConfigTxtImpl")

                    if stripped_config_line in config.get_markers():
                        for commands_group in config.get_commands_group(stripped_config_line):
                            for command in commands_group:

                                logger.debug(f"writing {command} at the marker({stripped_config_line}) in the config_sample_file({self.config_sample_file}) in the ConfigTxtImpl")

                                c.write(f"{command}\n")

                    else:
                        logger.warning(f"Inspected a marker({stripped_config_line}) at line({config_row}) in the ConfigTxtImpl, but any config_source doesn't exist")

                else:
                    c.write(config_line)
