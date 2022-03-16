from src.utils.custom_error import CustomError

class ParameterLocationsError(CustomError):
    pass


class ParameterSheetNotExistError(ParameterLocationsError):
    ja_message = "指定されたパラメータシート({parameter_sheet_file})が存在しません。"


class RowFromNotExistError(ParameterLocationsError):
    ja_message = "row_fromプロパティが存在しません。"


class RowFromBiggerThanRowToExistError(ParameterLocationsError):
    ja_message = "row_fromプロパティ({row_from})がrow_toプロパティ({row_to})よりも大きく定義されている箇所があります。"