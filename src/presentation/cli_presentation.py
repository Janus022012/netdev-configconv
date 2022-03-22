import argparse
import os
from typing import Dict

from .abstract_presentation import AbstractPresentation
from .presentation_exception import CommandNotExistError, RequiredFileNotExistError
from src.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


class CliPresentation(AbstractPresentation):
    """CliPresentation
    
    CliPresentationは、コマンドから実行に必要な引数を取得するクラスである。

    Attributes:
        available_commands (List[str]): 利用可能なコマンドの配列

    """

    def __init__(self):
        super().__init__()

    def _parse_arguments(self):
        exceptional_sheets_lambda = lambda x:list(map(str, x.split(',')))

        parser = argparse.ArgumentParser("netdevpy", description="本プログラムはエクセルからコンフィグファイルを作成するためのプログラムです。")
        subparsers = parser.add_subparsers(help='help for subcommand')
        run_parser = subparsers.add_parser('create_config', help="エクセルファイルからコンフィグファイルを作成する際に使用します。")
        run_parser.set_defaults(command="create_config")
        run_parser.add_argument("-cs", "--config_sample_file", required=True, help="コンフィグの元となるコンフィグサンプルのパスを指定して下さい。")
        run_parser.add_argument("-ps", "--parameter_sheet_file",  required=True, help="パラメータシートが存在するディレクトリまたはファイルを指定して下さい。")
        run_parser.add_argument("-rf", "--rule_file",  required=True, help="コンフィグの変換をするモデル名を指定して下さい。")
        run_parser.add_argument("-op", "--output_path", required=True, help="作成ファイルの出力先を指定してください。")
        run_parser.add_argument("-es", "--exception_sheets",  type=exceptional_sheets_lambda, help="パラメーターシートがエクセルの場合、コンフィグ作成時に参照しないエクセルのシートを指定して下さい。")
        args = parser.parse_args()

        return args

    def run(self) -> Dict[str, str]:
        """run

        run関数は、CLIコマンドから実行に必要な情報を取得するために関数である。

        Returns:
            Dict[str, str]: 取得した引数の引数名とデータの仮想配列
        
        """
        logger.debug("Getting args from cli commands...")

        args = vars(self._parse_arguments())

        if "command" in args:
            if args["command"] not in self.available_commands:
                raise CommandNotExistError({"command": args["command"], "available_commands": self.available_commands})

        for file_type in ["config_sample_file", "parameter_sheet_file", "rule_file", "output_path"]:
            if not os.path.exists(args[file_type]):
                raise RequiredFileNotExistError({"file_type": file_type, "file_path": args[file_type]})

        logger.debug(f"The result of getting args from cli commands is {args}")
        logger.debug("Getting args from cli commands has been completed successfully")

        return args