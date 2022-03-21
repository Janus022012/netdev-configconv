from typing import List
from src.domain.rule.rule_exceptions import ActionNotImplementedError
from src.utils.logger import get_custom_logger
import abc
import copy
import re


logger = get_custom_logger(__name__)

class Action:
    """Action
    
    Actionは、Conditionに適用されたコマンドに対しての処理を表現するデータクラスである。

    Attributes:
        action_type (str): アクション名を記述する文字列

    """

    action_type = "Action"

    @abc.abstractmethod
    def do(self, conditional_commands: List[str], applicable_commands: List[str]) -> List[str]:
        """do
    
       do関数は、Conditionに適用されたコマンドに対しての処理を実施する関数である。

        Args:
            conditional_commands List[str]: Conditionが適用された時に関連するコマンド群
            applicable_commands List[str]: Condition関係なく適用されるコマンド群

        Returns:
            List[str]: Actionを適用された後のコマンド群

        """
        pass

    @classmethod
    def build(cls, action: str):
        """build
    
       build関数は、action名からクラスを取得するクラスメソッドである。

        Args:
            action (str): 取得したアクション名

        Returns:
            (Obj'Action'): Actionクラスのサブクラス

        """
        logger.debug(f"Building an action({action})...")

        for subclass_name, subclass in {c.action_type: c for c in cls.__subclasses__()}.items():
            if subclass_name == action:
                logger.debug(f"Building an action({action}) has been completed successfully")
                return subclass()
            
        raise ActionNotImplementedError({"rule_file": action})


class Delete(Action):
    """Delete
    
    Deleteは、Actionのサブクラスでコマンドの削除を表現するデータクラスである。

    Attributes:
        action_type (str): アクション名を記述する文字列

    """

    action_type = "Delete"

    def do(self, conditional_commands: List[str], applicable_commands: List[str]) -> List[str]:
        result: List[str] = []

        logger.debug(f"Apply conditional commands({conditional_commands}) a delete action against applicable commands({applicable_commands})...")

        for ac in applicable_commands:
            flag = True
            for cc in conditional_commands:
                if re.search(ac, cc):
                    logger.debug(f"Apply an conditional command({cc}) a delete action against an applicable command({ac})...")
                    flag = False
            if flag:
                result.append(ac)

        logger.debug(f"The Result of applying an delete action is {result}")
        logger.debug(f"Apply conditional commands a delete action against applicable commands has been completed successfully")
        return result


class Add(Action):
    """Add
    
    Addは、Actionのサブクラスでコマンドの追加を表現するデータクラスである。

    Attributes:
        action_type (str): アクション名を記述する文字列

    """
    action_type = "Add"

    def do(self, conditional_commands: List[str], applicable_commands: List[str]) -> List[str]:
        logger.debug(f"Apply conditional commands({conditional_commands}) a add action against applicable commands({applicable_commands})...")

        result: List[str] = copy.copy(applicable_commands) + copy.copy(conditional_commands)

        logger.debug(f"The Result of applying an add action is {result}")

        return result
