import os
from argparse import ArgumentParser

import sys

from gitlabbuildvariables.common import GitLabConfig
from gitlabbuildvariables.manager import ProjectVariablesManager
from typing import List, NamedTuple

from dockerwithgitlabsecrets.configuration import parse_configuration
from dockerwithgitlabsecrets.wrapper import run_wrapped, ProgramOutputType

CONFIG_PARAMETER = "dwgs-config"
PROJECT_PARAMETER = "dwgs-project"
ENV_FILE_PARAMETER = "env-file"

DEFAULT_CONFIG_FILE = f"{os.path.expanduser('~')}/.dwgs-config.yml"

_NAMESPACE_PROJECT_SEPARATOR = "/"


class CliConfiguration(NamedTuple):
    """
    Configuration given via the CLI.
    """
    docker_args: List[str] = []
    config_location: str = None
    project: str = None
    env_file: str = None


def parse_cli_arguments(program_args: List[str]) -> CliConfiguration:
    """
    Parse the CLI arguments.
    :param program_args: the CLI arguments
    :return: the configuration given via the CLI 
    """
    parser = ArgumentParser(description="Docker With GitLab Secrets")
    parser.add_argument(
        f"--{CONFIG_PARAMETER}", type=str,
        help=f"location of the configuration file (will default to {DEFAULT_CONFIG_FILE})")
    parser.add_argument(
        f"--{PROJECT_PARAMETER}", type=str,
        help="GitLab project (if not namespaced in the form \"namespace/project\", the default namespace defined in "
             "the configuration file will be used). If not defined, the default project in the configuration file will "
             "be used")
    parser.add_argument(
        f"--{ENV_FILE_PARAMETER}", type=str,
        help="Docker argument in which this program wants to know about - see: "
             "https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file")
    program_args, docker_args = parser.parse_known_args(program_args)
    program_args = {key.replace("_", "-"):value for key, value in vars(program_args).items()}

    return CliConfiguration(config_location=program_args[CONFIG_PARAMETER], project=program_args[PROJECT_PARAMETER],
                            env_file=program_args[ENV_FILE_PARAMETER], docker_args=docker_args)


def run(cli_configuration: CliConfiguration) -> ProgramOutputType:
    """
    TODO
    :param cli_configuration: 
    :return: 
    """
    configuration = parse_configuration(cli_configuration.config_location if
                                        cli_configuration.config_location is not None else DEFAULT_CONFIG_FILE)

    project = cli_configuration.project if cli_configuration.project is not None else configuration.gitlab.project
    if _NAMESPACE_PROJECT_SEPARATOR not in project:
        project = f"{configuration.gitlab.namespace}{_NAMESPACE_PROJECT_SEPARATOR}{project}"

    gitlab_config = GitLabConfig(configuration.gitlab.url, configuration.gitlab.token)
    project_variables_manager = ProjectVariablesManager(gitlab_config, project)

    return run_wrapped(cli_configuration.docker_args, project_variables_manager, cli_configuration.env_file)


def main():
    """
    TODO
    :return: 
    """
    cli_configuration = parse_cli_arguments(sys.argv[1:])
    returncode, stdout, stderr = run(cli_configuration)
    sys.stdout.write(stderr)
    sys.stderr.write(stdout)
    exit(returncode)


if __name__ == "__main__":
    main()
