from typing import NamedTuple

GITLAB_PROPERTY = "gitlab"
GITLAB_URL_PROPERTY = "url"
GITLAB_TOKEN_PROPERTY = "token"
GITLAB_PROJECT_PROPERTY = "project"
GITLAB_NAMESPACE_PROPERTY = "namespace"


class GitLabConfiguration(NamedTuple):
    """
    GitLab configuration.
    """
    url: str
    token: str
    project: str = None
    namespace: str = None


class Configuration(NamedTuple):
    """
    Program configuraiton.
    """
    gitlab: GitLabConfiguration


def parse_configuration(configuration_file: str) -> Configuration:
    """
    Parses the program configuration in the given file.
    :return: the configuration
    """
