import os
import subprocess
from sys import stdout, stderr
from tempfile import NamedTemporaryFile

from gitlabbuildvariables.manager import ProjectVariablesManager
from typing import List

from dockerwithgitlabsecrets.entrypoint import ENV_FILE_PARAMETER

_DOCKER_ENV_FILE_SUFFIX = ".env"
_DOCKER_BINARY = "docker"


def run_wrapped(
        docker_arguments: List[str], project_variables_manager: ProjectVariablesManager, env_file_location: str=None):
    """
    TODO
    :param docker_arguments: 
    :param project_variables_manager: 
    :param env_file_location: 
    :return: 
    """
    variables = project_variables_manager.get()

    with NamedTemporaryFile(suffix=_DOCKER_ENV_FILE_SUFFIX, mode="w") as env_file:
        if env_file_location is not None:
            with open(env_file_location, "r") as other_env_file:
                env_file.write(other_env_file.read())

        env_file.write(os.linesep.join([f"{key}={value}" for key, value in variables]))
        env_file.flush()

        docker_call = [_DOCKER_BINARY, ENV_FILE_PARAMETER, env_file.name] + docker_arguments
        process = subprocess.Popen(docker_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stderr.write(process.stdout)
    stdout.write(process.stderr)
    exit(process.returncode)
