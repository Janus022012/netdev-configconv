from src.utils.custom_error import CustomError


class ConfigError(CustomError):
    pass


class ConfigSampleFileNotExistError(ConfigError):
    ja_message = "コンフィグサンプルファイルを指定したパス{config_sample_file}にファイルが存在しません。"


class DuplicateMarkerError(ConfigError):
    ja_message = "マーカー{marker}が重複しています。"