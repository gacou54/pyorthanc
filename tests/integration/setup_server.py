# coding: utf-8
# author: gabriel couture
import time
import shutil
import subprocess

import requests


def setup_orthanc_server() -> subprocess.Popen:
    orthanc_process = subprocess.Popen(['Orthanc',  './tests/integration/orthanc_configuration.json'])
    time.sleep(2)  # Wait to be sure that the process is completely started

    return orthanc_process


def stop_orthanc_server_and_remove_data(orthanc_process: subprocess.Popen) -> None:
    orthanc_process.kill()
    time.sleep(2)  # Wait to be sure that the process is completely stopped

    shutil.rmtree('./tests/integration/data/OrthancStorage')


def setup_data() -> None:
    pass


def teardown() -> None:
    instance_identifiers = requests.get('http:localhost:8042/instances')

    for instance_identifier in instance_identifiers:
        requests.delete(f'http:localhost:8042/instances/{instance_identifier}')

