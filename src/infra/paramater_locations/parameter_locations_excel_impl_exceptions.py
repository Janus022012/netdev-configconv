from src.utils.custom_error import CustomError


class ParameterLocationsExcelImplError(CustomError):
    pass


class SheetNotExistError(ParameterLocationsExcelImplError):
    ja_message = "シート({sheet_name})は、パラメータシート({parameter_sheet_file})内に存在しません。"