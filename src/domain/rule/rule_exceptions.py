from src.utils.custom_error import CustomError


class RuleError(CustomError):
    pass


class RuleFileNotExistError(RuleError):
    ja_message = "ルールファイル({rule_file})が存在しません。"


class ActionNotImplementedError(RuleError):
    ja_message = "アクション名({action})は存在しません。"

