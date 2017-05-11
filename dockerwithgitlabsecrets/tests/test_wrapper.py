import unittest

from gitlab import Gitlab
from gitlabbuildvariables.common import GitLabConfig
from gitlabbuildvariables.manager import ProjectVariablesManager
from useintest.models import DockerisedServiceWithUsers
from useintest.predefined.gitlab import GitLab8_16_6_ce_0ServiceController
from useintest.services.controllers import DockerisedServiceController

from dockerwithgitlabsecrets.tests._common import EXAMPLE_PROJECT
from dockerwithgitlabsecrets.wrapper import run_wrapped


_GITLAB_PORT = 80
_PROJECT_VARIABLES = {
    "EXAMPLE": "value",
    "HELLO": "world"
}


class TestWrapper(unittest.TestCase):
    """
    Tests for `run_wrapped`.
    """
    _gitlab_service: DockerisedServiceWithUsers
    _gitlab_controller: DockerisedServiceController
    _project_variables_manager: ProjectVariablesManager
    _project_name: str

    @classmethod
    def setUpClass(cls):
        cls._gitlab_controller = GitLab8_16_6_ce_0ServiceController()
        cls._gitlab_service = cls._gitlab_controller.start_service()
        gitlab_location = f"http://{cls._gitlab_service.host}:{cls._gitlab_service.ports[_GITLAB_PORT]}"

        gitlab = Gitlab(url=gitlab_location, email=cls._gitlab_service.root_user.username,
                        password=cls._gitlab_service.root_user.password)
        gitlab.auth()

        cls._gitlab_token = gitlab.private_token
        cls._project_name = f"{cls._gitlab_service.root_user.username}/{EXAMPLE_PROJECT}"
        gitlab.projects.create({"name": EXAMPLE_PROJECT})

        cls.project_variables_manager = ProjectVariablesManager(
            GitLabConfig(gitlab_location, cls._gitlab_token), cls._project_name)
        cls.project_variables_manager.set(_PROJECT_VARIABLES)

    @classmethod
    def tearDownClass(cls):
        cls._gitlab_controller.stop_service(cls._gitlab_service)

    def setUp(self):
        self.project_variables_manager = TestWrapper._project_variables_manager
        self.project_name = TestWrapper._project_name

    def test_with_docker_version(self):
        return_code, stdout, stderr = run_wrapped(["docker", "--version"], self.project_variables_manager)
        self.assertEquals(0, return_code)

    # TODO: Other tests


if __name__ == "__main__":
    unittest.main()
