# from .domain.config.config_repository import ConfigRepository
# from .domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository
# from .domain.rule.rule_repository import RuleRepository
from src.usecase.config_command_usecase import AbstractConfigCommandUsecase, ConfigCommandUsecase
from src.usecase.params_command_usecase import AbstractParamsCommandUsecase, ParamsCommandUsecase
from src.presentation.cli_presentation import CliPresentation
from src.infra.config.config_txt_impl import ConfigTxtImpl
from src.infra.paramater_locations.parameter_locations_excel_impl import ParameterLocationsExcelImpl
from src.infra.rule.rule_yaml_impl import RuleYamlImpl
from src.utils.custom_error import CustomError


def run_cli(config_command_usecase: AbstractConfigCommandUsecase, params_command_usecase: AbstractParamsCommandUsecase) -> None:
    args = CliPresentation().run()

    if args["command"] == "create_config":
        config_command_usecase.create_config(**{key: value for key, value in args.items() if key != "command"})
    else:
        raise NotImplementedError("Not Implement")


def main() -> None:

    # try:
    config_repo = ConfigTxtImpl
    parameter_locations_repo = ParameterLocationsExcelImpl
    rule_repo = RuleYamlImpl
    config_command_usecase: AbstractConfigCommandUsecase = ConfigCommandUsecase(config_repo, parameter_locations_repo, rule_repo)
    params_command_usecase: AbstractParamsCommandUsecase = ParamsCommandUsecase(config_repo, parameter_locations_repo, rule_repo)

    run_cli(config_command_usecase, params_command_usecase)
    # except CustomError as e:
    #     print(e.get_ja_message())

    # except Exception as e:
    #     print(f"実行中に以下のエラーが発生しました。\n{e}")


if __name__ == '__main__':
    main()