from typing import List
from pydantic import BaseModel, Field, validator
from src.utils.logger import get_custom_logger
from .parameter_locations_exceptions import RowFromNotExistError, RowFromBiggerThanRowToExistError


logger = get_custom_logger(__name__)


class ParameterLocation(BaseModel):
    """ParameterLocation
    
    ParameterLocationは、Parameterの位置を記述したデータクラスである。

    Attributes:
        name (str): パラメータ名
        cell_number (str): パラメータの位置
        required (bool): パラメータが必須かどうか、本パラメータが存在しないパラメータグループはコマンド化されない。

    """

    name: str = Field(..., min_length=1)
    cell_number: str = Field(..., min_length=2, regex=r"^[A-Z]+\d+")
    required: bool = False

    class Config:
        allow_mutation = False


class ParameterLocations(BaseModel):
    """ParameterLocation
    
    ParameterLocationsは、ParameterGroupの位置を記述したデータクラスである。

    Attributes:
        locations (List[ParameterLocation]): ParameterGroupの位置を記述した配列

    """

    locations: List[ParameterLocation]

    class Config:
        allow_mutation = False


class ParameterColumnLocation(BaseModel):
    """ParameterColumnLocation
    
    ParameterColumnLocationは、パラメータのカラムの位置を記述したデータクラスである。

    Attributes:
        name (str): パラメータ名
        cell_number (str): パラメータのカラム位置
        required (bool): パラメータが必須かどうか、本パラメータが存在しないパラメータグループはコマンド化されない。

    """

    name: str = Field(..., min_length=1)
    column_number: str = Field(..., min_length=1, regex=r"[A-Z]+")
    required: bool = False


class ParameterLocationSource(BaseModel):
    """ParameterLocationSource
    
    ParameterLocationSourceは、パラメータの位置を記述したデータクラスである。

    Attributes:
        parameter_column_locations (List[ParameterColumnLocation]): ParameterGroupのカラム位置を記述したもの
        row_from (int): 行の始端
        row_to (int): 行の終端

    """

    parameter_column_locations: List[ParameterColumnLocation] = Field(..., min_items=1)
    row_from: int = Field(..., ge=1)
    row_to: int = Field(..., ge=1)

    class Config:
        allow_mutation = False


    @validator("row_to")
    def _validate_row_to(cls, value, values) -> int:
        
        logger.debug(f"Validating row_to({value}) in the ParameterLocationSource...")

        if "row_from" not in values.keys():

            raise RowFromNotExistError()

        if value < values["row_from"]:

            raise RowFromBiggerThanRowToExistError(message_items={"row_from": values["row_from"], "row_to": value})
        
        logger.debug(f"row_to({value}) in the ParameterLocationSource has been finished successfully")

        return value


    def convert_to_parameter_locations_list(self) -> List[ParameterLocations]:
        """convert_to_parameter_locations_list

        ParameterLocationSourceをParameterLocationsの配列に変換する関数

        Returns:
            List[ParameterLocations]: ParameterGroup配列の位置を記述した配列

        """

        return [
            ParameterLocations(
                locations=[
                    ParameterLocation(
                        name=i.name,
                        cell_number=f"{i.column_number}{j}",
                        required=i.required
                    ) for i in self.parameter_column_locations
                ]
            ) for j in range(self.row_from, self.row_to+1)
        ]