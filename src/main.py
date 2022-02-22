# from .domain.config.config_repository import ConfigRepository
# from .domain.parameter_locations.parameter_locations_repository import ParameterLocationsRepository
# from .domain.rule.rule_repository import RuleRepository
from .usecase.config_command_usecase import AbstractConfigCommandUsecase, ConfigCommandUsecase
from .usecase.params_command_usecase import AbstractParamsCommandUsecase, ParamsCommandUsecase
from .presentation.cli_presentation import CliPresentation
from .infra.config.config_txt_impl import ConfigTxtImpl
from .infra.paramater_locations.parameter_locations_excel_impl import ParameterLocationsExcelImpl
from .infra.rule.rule_yaml_impl import RuleYamlImpl


def run_cli_app(config_command_usecase: AbstractConfigCommandUsecase, params_command_usecase: AbstractParamsCommandUsecase) -> None:
    args = CliPresentation().run()

    if args["command"] == "create_config":
        config_command_usecase.create_config(**args)
    else:
        raise NotImplementedError("Not Implement")


def main() -> None:
    try:
        config_repo = ConfigTxtImpl
        parameter_locations_repo = ParameterLocationsExcelImpl
        rule_repo = RuleYamlImpl
        config_command_usecase: AbstractConfigCommandUsecase = ConfigCommandUsecase(config_repo, parameter_locations_repo, rule_repo)
        params_command_usecase: AbstractParamsCommandUsecase = ParamsCommandUsecase(config_repo, parameter_locations_repo, rule_repo)

        run_cli_app(config_command_usecase, params_command_usecase)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()