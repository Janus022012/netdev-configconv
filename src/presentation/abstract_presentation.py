from abc import ABC, abstractmethod
from typing import Dict


class AbstractPresentation(ABC):
    """AbstractPresentation
    
    AbstractPresentationは、ユーザーから実行に必要な引数を取得するための抽象クラスである。

    Attributes:
        available_commands (List[str]): 利用可能なコマンドの配列

    """

    def __init__(self):
        self.available_commands = ["create_config", "create_params"]

    @staticmethod
    @abstractmethod
    def _parse_arguments() -> Dict[str, str]:
        pass

    @abstractmethod
    def run(self) -> Dict[str, str]:
        """run

        run関数は、ユーザーから実行に必要な引数を取得するための関数である。

        Returns:
            Dict[str, str]: 取得した引数の引数名とデータの仮想配列
        
        """
        pass






