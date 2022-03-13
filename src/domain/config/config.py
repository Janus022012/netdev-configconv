from pydantic import BaseModel, Field, validator
from typing import List


class ConfigSource(BaseModel):
    marker: str = Field(..., min_length=5, regex=r"%{2}\w+%{2}")
    commands_group: List[List[str]] = Field(..., min_items=1)

    class Config:
        allow_mutation = False


class Config(BaseModel):
    config_sources: List[ConfigSource]

    @validator("config_sources")
    def _validate_no_duplicate_marker(cls, value: List[ConfigSource]):
        if len(set([i.marker for i in value])) != len(value):
            raise ValueError("Each element of the markers in 'config_sources' of the Config must be unique")
        return value

    def get_markers(self) -> List[str]:
        return [config_source.marker for config_source in self.config_sources]

    def get_commands_group(self, marker: str) -> List[List[str]]:
        for config_source in self.config_sources:
            if marker == config_source.marker:
                return config_source.commands_group
        return []
