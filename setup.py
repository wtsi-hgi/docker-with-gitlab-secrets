from setuptools import setup, find_packages

try:
    from pypandoc import convert
    def read_markdown(file: str) -> str:
        return convert(file, "rst")
except ImportError:
    def read_markdown(file: str) -> str:
        return open(file, "r").read()

setup(
    name="docker-with-gitlab-secrets",
    version="1.0.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=open("requirements.txt", "r").readlines(),
    url="https://github.com/wtsi-hgi/docker-with-gitlab-secrets",
    license="MIT",
    description="",     # TODO
    long_description=read_markdown("README.md"),
    entry_points={
        "console_scripts": [
            "docker-with-gitlab-secrets=dockerwithgitlabsecrets.entrypoint:main",
        ]
    }
)
