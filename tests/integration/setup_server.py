# coding: utf-8
# author: gabriel couture
import os
import time
import shutil
import subprocess

import requests

ORTHANC_URL = 'http://localhost:8042'


def setup_orthanc_server() -> subprocess.Popen:
    orthanc_process = subprocess.Popen(['Orthanc', './tests/integration/orthanc_configuration.json'])
    time.sleep(2)  # Wait to be sure that the process is completely started

    return orthanc_process


def stop_orthanc_server_and_remove_data_directory(orthanc_process: subprocess.Popen) -> None:
    orthanc_process.kill()
    time.sleep(2)  # Wait to be sure that the process is completely stopped

    shutil.rmtree('./tests/integration/data/OrthancStorage')


def setup_data() -> None:
    headers = {'content-type': 'application/dicom'}

    list_of_dicom_file_paths = [
        f'./tests/integration/data/dicom_files/{i}'
        for i in os.listdir('./tests/integration/data/dicom_files/')
    ]

    for file_path in list_of_dicom_file_paths:
        with open(file_path, 'rb') as file_handler:
            data = file_handler.read()

        requests.post(
            f'{ORTHANC_URL}/instances',
            data=data,
            headers=headers
        )


def clear_data() -> None:
    instance_identifiers = requests.get(f'{ORTHANC_URL}/instances')

    for instance_identifier in instance_identifiers:
        requests.delete(f'{ORTHANC_URL}/instances/{instance_identifier}')
