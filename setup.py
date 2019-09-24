import subprocess

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

FLAKE8_COMMAND = ['./venv/bin/flake8', '--ignore=E501', 'pyorthanc', 'tests']
MYPY_COMMAND = ['./venv/bin/mypy', 'pyorthanc']
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
        _run_command(FLAKE8_COMMAND)
        _run_command(MYPY_COMMAND)


class AllTests(TestCommand):
    description = 'run unit tests, integration tests and linters'
    user_options = []

    def run_tests(self):
        _run_command(UNIT_TESTS_COMMAND)
        _run_command(INTEGRATION_TESTS_COMMAND)
        _run_command(FLAKE8_COMMAND)
        _run_command(MYPY_COMMAND)


with open('./README.md', 'r') as file_hanlder:
    long_description = file_hanlder.read()


setup(
    name='pyorthanc',
    version='0.2.4',
    packages=find_packages(),
    url='https://gitlab.physmed.chudequebec.ca/gacou54/pyorthanc',
    license='MIT',
    author='Gabriel Couture',
    author_email='gacou54@gmail.com',
    description='Orthanc REST API python wrapper with additional utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    cmdclass={
        'lint': LintTests,
        'unit': UnitTests,
        'integration': IntegrationTests,
        'test': AllTests
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7'
    ]
)
