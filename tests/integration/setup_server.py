# coding: utf-8
# author: gabriel couture
import os
import time
import shutil
import subprocess

import requests

ORTHANC_URL = 'http://localhost:9999'


def setup_orthanc_server() -> subprocess.Popen:
    """Start an Orthanc server

    Returns
    -------
    subprocess.Popen
        Subprocess of the test Orthanc server instance.
    """
    orthanc_process = subprocess.Popen(['Orthanc', './tests/integration/orthanc_configuration.json'])
    time.sleep(2)  # Wait to be sure that the process is completely started

    return orthanc_process


def stop_orthanc_server_and_remove_data_directory(orthanc_process: subprocess.Popen) -> None:
    """Stop the test orthanc server and remove its data directory

    Parameters
    ----------
    orthanc_process
        Orthanc subprocess.Popen process.
    """
    orthanc_process.kill()
    time.sleep(2)  # Wait to be sure that the process is completely stopped

    shutil.rmtree('./tests/integration/data/OrthancStorage')


def setup_data() -> None:
    """Load test dicom files to the test Orthanc server instance
    """
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
    """Remove all patient data in the test Orthanc instance with API calls
    """
    patient_identifiers = requests.get(f'{ORTHANC_URL}/patients').json()

    for patient_identifier in patient_identifiers:
        requests.delete(f'{ORTHANC_URL}/patients/{patient_identifier}')
