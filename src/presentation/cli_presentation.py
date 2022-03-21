import argparse
import os
from typing import Dict

from .abstract_presentation import AbstractPresentation
from src.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


class CliPresentation(AbstractPresentation):
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
        args = vars(self._parse_arguments())

        if "command" in args:
            if args["command"] not in self.available_commands:
                raise ValueError("コマンドは{}から選択してください。".format(self.available_commands))
        else:
            raise ValueError("引数にコマンドが存在しません。")

        for file_path in [args["config_sample_file"], args["parameter_sheet_file"], args["rule_file"], args["output_path"]]:
            if not os.path.exists(file_path):
                raise FileNotFoundError("入力として指定されたパス({})が存在しません。".format(file_path))

        return args