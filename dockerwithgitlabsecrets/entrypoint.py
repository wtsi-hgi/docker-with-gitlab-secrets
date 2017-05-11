from typing import List, NamedTuple

CONFIG_PARAMETER = "dwgs-config"
PROJECT_PARAMETER = "dwgs-project"
ENV_FILE_PARAMETER = "env-file"


class CliConfiguration(NamedTuple):
    """
    Configuration given via the CLI.
    """
    config_location: str = None
    project: str = None
    env_file: str = None


def parse_cli_arguments(arguments: List[str]) -> CliConfiguration:
    """
    Parse the CLI arguments.
    :param arguments: the CLI arguments
    :return: the configuration given via the CLI 
    """
