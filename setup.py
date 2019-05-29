from setuptools import setup, find_packages

setup(
    name='pyorthanc',
    version='',
    packages=find_packages(),
    url='https://github.com/gacou54/pyorthanc',
    license='MIT',
    author='Gabriel Couture',
    author_email='gacou54@gmail.com',
    description='Orthanc REST API python wrapper with additional utilities',
    install_requires=['requests'],
    test_suite='tests'
)
