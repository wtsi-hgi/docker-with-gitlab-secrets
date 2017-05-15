import unittest

from dockerwithgitlabsecrets.entrypoint import CliConfiguration, parse_cli_arguments, CONFIG_PARAMETER, \
    PROJECT_PARAMETER, ENV_FILE_PARAMETER, is_interactive
from dockerwithgitlabsecrets.tests._common import EXAMPLE_PROJECT, EXAMPLE_LOCATION, EXAMPLE_LOCATION_2, \
    EXAMPLE_DOCKER_ARGS

_CONFIG_PARAMETER_FLAG = f"--{CONFIG_PARAMETER}"
_PROJECT_PARAMETER_FLAG = f"--{PROJECT_PARAMETER}"
_ENV_FILE_PARAMETER_FLAG = f"--{ENV_FILE_PARAMETER}"


class TestParseCliArguments(unittest.TestCase):
    """
    Tests for `parse_cli_arguments`.
    """
    def test_parse_only_config_location_argument(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION]
        expected = CliConfiguration(config_location=EXAMPLE_LOCATION)
        self.assertEquals(expected, parse_cli_arguments(arguments))

    def test_parse_only_project_argument(self):
        arguments = [_PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT]
        expected = CliConfiguration(project=EXAMPLE_PROJECT)
        self.assertEquals(expected, parse_cli_arguments(arguments))

    def test_parse_program_arguments_with_docker_arguments(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION, _PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT] \
                    + EXAMPLE_DOCKER_ARGS
        expected = CliConfiguration(project=EXAMPLE_PROJECT, config_location=EXAMPLE_LOCATION,
                                    docker_args=EXAMPLE_DOCKER_ARGS, interactive=True)
        self.assertEquals(expected, parse_cli_arguments(arguments))

    def test_parse_program_arguments_with_env_docker_argument(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION, _PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT,
                     _ENV_FILE_PARAMETER_FLAG, EXAMPLE_LOCATION_2] + EXAMPLE_DOCKER_ARGS
        expected = CliConfiguration(project=EXAMPLE_PROJECT, config_location=EXAMPLE_LOCATION,
                                    env_file=EXAMPLE_LOCATION_2, docker_args=EXAMPLE_DOCKER_ARGS, interactive=True)
        configuration = parse_cli_arguments(arguments)
        self.assertEquals(expected, configuration)
        self.assertNotIn(ENV_FILE_PARAMETER, configuration.docker_args)


class TestIsInteractive(unittest.TestCase):
    """
    Tests for `parse_cli_arguments`.
    """
    def test_without_flag(self):
        self.assertFalse(is_interactive(["run", "--rm", "ubuntu", "command"]))

    def test_with_interactive_flag(self):
        self.assertTrue(is_interactive(["run", "-t", "ubuntu"]))

    def test_with_interactive_flag_and_stdin_attach(self):
        self.assertTrue(is_interactive(["run", "-it", "ubuntu"]))

    def test_with_interactive_flag_and_stdin_attach_reversed(self):
        self.assertTrue(is_interactive(["run", "-ti", "ubuntu"]))




# class TestRun(unittest.TestCase):
#     """
#     Tests for `run_wrapped`.
#     """
#     _gitlab_service: DockerisedServiceWithUsers
#     _gitlab_controller: DockerisedServiceController
#     project_variables_manager: ProjectVariablesManager
#     project_name: str
#
#     @classmethod
#     def setUpClass(cls):
#         cls._gitlab_controller = GitLab8_16_6_ce_0ServiceController()
#         cls._gitlab_service = cls._gitlab_controller.start_service()
#         gitlab_location = f"http://{cls._gitlab_service.host}:{cls._gitlab_service.ports[_GITLAB_PORT]}"
#
#         gitlab = Gitlab(url=gitlab_location, email=cls._gitlab_service.root_user.username,
#                         password=cls._gitlab_service.root_user.password)
#         gitlab.auth()
#
#         cls._gitlab_token = gitlab.private_token
#         cls.project_name = f"{cls._gitlab_service.root_user.username}/{EXAMPLE_PROJECT}"
#         gitlab.projects.create({"name": EXAMPLE_PROJECT})
#
#         cls.project_variables_manager = ProjectVariablesManager(
#             GitLabConfig(gitlab_location, cls._gitlab_token), cls.project_name)
#         cls.project_variables_manager.set(_PROJECT_VARIABLES)
#
#     @classmethod
#     def tearDownClass(cls):
#         cls._gitlab_controller.stop_service(cls._gitlab_service)
#
#     def setUp(self):
#         self.project_variables_manager = TestWrapper.project_variables_manager
#         self.project_name = TestWrapper.project_name


# TODO: Tests for run
    # def test_help(self):
    #     return_code, stdout, stderr = run_wrapped(["--help"], _PROJECT_VARIABLES)
    #     self.assertEquals(0, return_code)
    #     self.assertIn(CONFIG_PARAMETER, stdout.strip())



if __name__ == '__main__':
    unittest.main()
