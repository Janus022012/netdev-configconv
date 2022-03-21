from typing import List, Literal
from pydantic import BaseModel, Field
from src.utils.logger import get_custom_logger
from src.domain.parameter_locations.parameter import Parameter, ParameterGroup

import abc
import re


logger = get_custom_logger(__name__)


class Condition:
    """Condition
    
    Conditionは、Parameterの入力内容によってParameterGroupに対してCommandの追加・削除等の操作を行うか決定するインターフェースである。

    """

    @abc.abstractmethod
    def evaluate(self, parameter_group: List[Parameter]) -> bool:
        """evaluate
    
        evaluate関数は、ParameterGroupがConditionの内容を満たしているか判断する関数である。

        Attributes:
            parameter_group (List[Parameter]): パラメータグループ

        Returns:
            bool: Parameterが条件を満たしているかを真偽値で返す。

        """
        raise NotImplementedError("The 'evaluate' method must be implemented")


class IsEmptyCondition(Condition, BaseModel):
    """IsEmptyCondition
    
    IsEmptyConditionは、Parameterが空の場合にParameterGroupに対してActionを行うデータクラスである。

    Attributes:
        type (Literal['isEmpty']):  Conditionのタイプを表すタイプ
        target_parameter (List[str]): 空かどうか判断するパラメータ名の配列

    """

    type: Literal['isEmpty']
    target_parameters: List[str] = Field(..., min_items=1)

    def evaluate(self, parameter_group: ParameterGroup) -> bool:

        logger.debug(f"Evaluating whether a parameter_group({parameter_group}) is empty...")

        for target_parameter in self.target_parameters:

            if target_parameter in parameter_group:

                if parameter_group.get(target_parameter).value:

                    logger.debug(f"The parameter({target_parameter}) is empty")

                    logger.debug(f"Evaluating whether a parameter_group is empty has been completed successfully")

                    return False

        logger.debug(f"All parameters({self.target_parameters}) is not Empty")

        logger.debug(f"Evaluating whether a parameter_grouphas been completed successfully")

        return True


class IsContainedCondition(Condition, BaseModel):
    """IsContainedCondition
    
    IsContainedConditionは、Parameterに特定の文字列を含んでいる場合にParameterGroupに対してActionを行うデータクラスである。

    Attributes:
        type (Literal['isContained']):  Conditionのタイプを表すタイプ
        target_parameter (List[str]): 空かどうか判断するパラメータ名の配列
        target_string str: 対象となる文字列

    """
    type: Literal['isContained']
    target_parameters: List[str] = Field(..., min_items=1)
    target_string: str = Field(..., min_length=1)

    def evaluate(self, parameter_group: ParameterGroup) -> bool:

        for target_parameter in self.target_parameters:

            if target_parameter in parameter_group:

                if not re.search(self.target_string, parameter_group.get(target_parameter).value):

                    logger.debug(f"A parameter({target_parameter}) doesn't contain target_string({self.target_string})")

                    logger.debug(f"Evaluating whether a parameter_group contained target_string({self.target_string}) has been completed successfully")

                    return False

            else:

                logger.debug(f"A parameter({target_parameter}) doesn't exist")

                logger.debug(f"Evaluating whether a parameter_group contained target_string({self.target_string}) has been completed successfully")

                return False

        logger.debug(f"All parameters({self.target_parameters}) contain target_string({self.target_string})")

        logger.debug(f"Evaluating whether a parameter_group contained target_string({self.target_string}) has been completed successfully")

        return True