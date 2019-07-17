import subprocess

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

LINTER_COMMAND = ['pycodestyle', '--ignore=E501', 'pyorthanc', 'tests']
UNIT_TESTS_COMMAND = ['./venv/bin/python', '-m', 'unittest', 'discover', '-s', './tests/unit/']
INTEGRATION_TESTS_COMMAND = ['./venv/bin/python', '-m', 'unittest', 'discover', '-s', './tests/integration']


def _run_command(command: str) -> None:
    try:
        subprocess.check_call(command)

    except subprocess.CalledProcessError as error:
        print('Command failed with exit code', error.returncode)
        exit(error.returncode)


class UnitTests(TestCommand):
    description = 'run unit tests'
    user_options = []

    def run_tests(self):
        _run_command(UNIT_TESTS_COMMAND)


class IntegrationTests(TestCommand):
    description = 'run integration tests'
    user_options = []

    def run_tests(self):
        _run_command(INTEGRATION_TESTS_COMMAND)


class LintTests(TestCommand):
    description = 'run linters'
    user_options = []

    def run_tests(self):
        _run_command(LINTER_COMMAND)


class AllTests(TestCommand):
    description = 'run unit tests, integration tests and linters'
    user_options = []

    def run_tests(self):
        _run_command(UNIT_TESTS_COMMAND)
        _run_command(INTEGRATION_TESTS_COMMAND)
        _run_command(LINTER_COMMAND)


setup(
    name='pyorthanc',
    version='0.2.1',
    packages=find_packages(),
    url='https://gitlab.physmed.chudequebec.ca/gacou54/pyorthanc',
    license='MIT',
    author='Gabriel Couture',
    author_email='gacou54@gmail.com',
    description='Orthanc REST API python wrapper with additional utilities',
    install_requires=['requests'],
    cmdclass={
        'lint': LintTests,
        'test': UnitTests,
        'integration': IntegrationTests,
        'alltests': AllTests
    },
)
