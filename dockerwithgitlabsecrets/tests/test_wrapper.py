from tempfile import NamedTemporaryFile
import unittest

from dockerwithgitlabsecrets.tests._common import EXAMPLE_VALUE, EXAMPLE_PARAMETER
from dockerwithgitlabsecrets.wrapper import run_wrapped, SAFE_LINE_BREAK

_PROJECT_VARIABLES = {
    "EXAMPLE": "value",
    "HELLO": "hello\nworld"
}


class TestWrapper(unittest.TestCase):
    """
    Tests for `run_wrapped`.
    """
    def test_help_with_docker_command(self):
        return_code, stdout, stderr = run_wrapped(["ps", "--help"], _PROJECT_VARIABLES)
        self.assertEquals(0, return_code)
        self.assertIn("Usage:\tdocker ps", stdout.strip())

    def test_with_non_supported_action(self):
        return_code, stdout, stderr = run_wrapped(["version"], _PROJECT_VARIABLES)
        self.assertEquals(0, return_code)
        self.assertIn("Version", stdout.strip())

    def test_has_standard_variable(self):
        return_code, stdout, stderr = run_wrapped(
            ["run", "-e", f"{EXAMPLE_PARAMETER}={EXAMPLE_VALUE}", "--rm", "alpine", "printenv", EXAMPLE_PARAMETER],
            _PROJECT_VARIABLES)
        self.assertEquals(0, return_code)
        self.assertEquals(EXAMPLE_VALUE, stdout.strip())

    def test_run_has_secret_variable(self):
        key, value = list(_PROJECT_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["--debug", "run", "--rm", "alpine", "printenv", key],
                                                  _PROJECT_VARIABLES)
        self.assertEquals(0, return_code)
        self.assertEquals(value, stdout.strip())

    def test_run_has_multiline_secret_variable(self):
        key, value = list(_PROJECT_VARIABLES.items())[1]
        return_code, stdout, stderr = run_wrapped(["run", "--rm", "alpine", "printenv", key],
                                                  _PROJECT_VARIABLES)
        self.assertEquals(0, return_code)
        self.assertEquals(value.replace("\n", SAFE_LINE_BREAK), stdout.strip())

    def test_run_cli_variable_has_higher_precedence(self):
        other_value = "other-value"
        key, value = list(_PROJECT_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["run", "-e", f"{key}={other_value}", "--rm", "alpine", "printenv",
                                                   key], _PROJECT_VARIABLES)
        self.assertEquals(0, return_code)
        self.assertEquals(other_value, stdout.strip())

    def test_run_with_env_file(self):
        key, value = list(_PROJECT_VARIABLES.items())[0]
        with NamedTemporaryFile("w") as env_file:
            env_file.write("other=value")
            env_file.flush()
            return_code, stdout, stderr = run_wrapped(
                ["run", "--env-file", f"{env_file.name}", "--rm", "alpine", "printenv", key], {key: value})
            self.assertEquals(0, return_code)
            self.assertEquals(value, stdout.strip())

    def test_run_with_env_file_that_overrides(self):
        key, value = list(_PROJECT_VARIABLES.items())[0]
        example_override = "override"

        with NamedTemporaryFile("w") as env_file:
            env_file.write(f"{key}={example_override}")
            env_file.flush()
            return_code, stdout, stderr = run_wrapped(
                ["run", "--env-file", f"{env_file.name}", "--rm", "alpine", "printenv", key], _PROJECT_VARIABLES)
            self.assertEquals(0, return_code)
            self.assertEquals(example_override, stdout.strip())


if __name__ == "__main__":
    unittest.main()
