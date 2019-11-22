import subprocess

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

FLAKE8_COMMAND = ['./venv/bin/flake8', '--ignore=E501', 'pyorthanc', 'tests']
MYPY_COMMAND = ['./venv/bin/mypy', '--config-file=./mypy.ini', 'pyorthanc']
TESTS_COMMAND = ['./venv/bin/python', '-m', 'unittest', 'discover', '-s', 'tests']


def _run_command(command: str) -> None:
    try:
        subprocess.check_call(command)

    except subprocess.CalledProcessError as error:
        print('Command failed with exit code', error.returncode)
        exit(error.returncode)


class Tests(TestCommand):
    description = 'run tests'
    user_options = []

    def run_tests(self):
        _run_command(TESTS_COMMAND)


class LintTests(TestCommand):
    description = 'run linters'
    user_options = []

    def run_tests(self):
        _run_command(FLAKE8_COMMAND)
        _run_command(MYPY_COMMAND)


class AllTests(TestCommand):
    description = 'run tests and linters'
    user_options = []

    def run_tests(self):
        _run_command(TESTS_COMMAND)
        _run_command(FLAKE8_COMMAND)
        _run_command(MYPY_COMMAND)


with open('./README.md', 'r') as file_handler:
    long_description = file_handler.read()


setup(
    name='pyorthanc',
    version='0.2.8',
    packages=find_packages(),
    url='https://gitlab.physmed.chudequebec.ca/gacou54/pyorthanc',
    license='MIT',
    author='Gabriel Couture',
    author_email='gacou54@gmail.com',
    description='Orthanc REST API python wrapper with additional utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['urllib3'],
    cmdclass={
        'lint': LintTests,
        'acceptance': Tests,
        'test': AllTests
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
