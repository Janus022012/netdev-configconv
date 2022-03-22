from src.utils.custom_error import CustomError


class CLIPresentationError(CustomError):
    pass

class CommandNotExistError(CLIPresentationError):
    ja_message = "コマンド {command}は存在しません。{available_commands}から選択してください。"


class RequiredFileNotExistError(CLIPresentationError):
    ja_message = "{file_type}: {file_path}が存在しません。"