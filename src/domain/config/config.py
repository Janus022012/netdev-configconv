from pydantic import BaseModel, Field, validator
from typing import List
from logging import config
from .config_exception import DuplicateMarkerError

import logging
import os

config.fileConfig(os.path.abspath("logger.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ConfigSource(BaseModel):
    """ConfigSource
    
    ConfigSourceは、Configの元となるcommands_groupとcommands_groupの挿入位置であるmarkerを保持するデータクラスである

    Attributes:
        marker str: コンフィグの挿入位置を一意にする文字列
        commands_group List[List[str]]: 一定のパラメータを有するコマンド群

    """

    marker: str = Field(..., min_length=5, regex=r"%{2}\w+%{2}")
    commands_group: List[List[str]] = Field(..., min_items=1)

    class Config:
        allow_mutation = False


class Config(BaseModel):
    """Config
    
    Configは、コンフィグを作成する元となるconfig_sourcesを属性に持つデータクラスである。

    Attributes:
        config_sources  List[ConfigSource]: コンフィグ作成の元になるConfigSource群

    """
    
    config_sources: List[ConfigSource]


    @validator("config_sources")
    def _validate_no_duplicate_marker(cls, value: List[ConfigSource]):

        logger.debug(f"Validating duplicated markers of the ConfigSources({value}) in the Config...")

        for i in value:
            dup_num = 0
            for j in value:
                if i.marker == j.marker:
                    dup_num += 1
            
            if dup_num >= 2:
                raise DuplicateMarkerError(message_items={"marker": i.marker})

        logger.debug(f"Validating duplicated markers of the ConfigSources({value}) has been finished successfully")

        return value


    def get_markers(self) -> List[str]:
        """get_markers

        config_source配列からmarkerの配列を取得するための関数

        Returns:
            List[str]: markerの配列

        Note:
            markerは、%%MARKER%%の書式に従っている。

        """

        result: List[str] = [config_source.marker for config_source in self.config_sources]

        logger.debug(f"Getting markers({result}) of the ConfigSources has been finished successfully")

        return result

    def get_commands_group(self, marker: str) -> List[List[str]]:
        """get_commands_group

        ConfigSourceの配列からmarker文字列をキーとして、CommandsGroup配列を取得する関数

        Args:
            marker (str): marker文字列

        Returns:
            List[List[str]]: コンフィグに書き込むコマンドを記述した配列

        Note:
            該当するmarkerが存在しなかった場合、空文字が出力される。

        """

        logger.debug(f"Getting commands_group of the ConfigSources by a marker({marker})...")

        result = []

        for config_source in self.config_sources:

            if marker == config_source.marker:

                result = config_source.commands_group

        logger.debug(f"Getting commands_group({result}) of the ConfigSources by a marker({marker}) has been finished successfully")

        return result
