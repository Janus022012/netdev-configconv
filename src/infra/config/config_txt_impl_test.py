from typing import Dict, Any
import pytest
import os

from .config_txt_impl import ConfigTxtImpl
from src.domain.config.config import Config, ConfigSource


@pytest.mark.parametrize(
    "test_input,test_result,test_exception_result", [
        # correct
        (
                {
                    "config_sample_file": os.path.abspath("../../../test/data/config_sample.log"),
                    "config": Config(
                        config_sources=[
                            ConfigSource(marker="%%parameter1%%", command_groups=["ddddddddddddddddd\n", "!\n"]),
                            ConfigSource(marker="%%parameter2%%", command_groups=["eeeeeeeeeeeeeeeee\n", "!\n"])
                        ]
                    ),
                    "output_config_file": os.path.abspath("../../../test/data/test_device.log")
                },
                "show running-config\n!\naaaaaaaaaaaaaaaaa\n!\nbbbbbbbbbbbbbbbbb\n!\nccccccccccccccccc\n!\nddddddddddddddddd\n!\neeeeeeeeeeeeeeeee\n!\nend",
                None
        ),
        # unexisted config_sample
        (
                {
                    "config_sample_file": os.path.abspath("../../../test/data/config_sample2.log"),
                    "config": "",
                    "output_config_file": os.path.abspath("../../../test/data/test_device.log")
                },
                None,
                ValueError(r"of the ConfigRepository doesn't exist in your directories")
        ),
    ]
)
def test_read(test_input: Dict[str, Any], test_result: str, test_exception_result: Exception):
    if test_result:
        ConfigTxtImpl(test_input["config_sample_file"]).write(test_input["config"], test_input["output_config_file"])
        assert open(test_input["output_config_file"], "r").read() == test_result
    else:
        with pytest.raises(Exception) as e:
            ConfigTxtImpl(test_input["config_sample_file"]).write(test_input["config"], test_input["output_config_file"])
        assert str(test_exception_result) in str(e.value)
