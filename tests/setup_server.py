# coding: utf-8
# author: gabriel couture
import os
import time
import shutil
import subprocess

import requests

ORTHANC_URL = 'http://localhost:9999'
SECOND_ORTHANC_URL = 'http://localhost:9997'


def setup_orthanc_server() -> subprocess.Popen:
    """Start an Orthanc server

    Returns
    -------
    subprocess.Popen
        Subprocess of the test Orthanc server instance.
    """
    orthanc_process = subprocess.Popen(['Orthanc', './tests/orthanc_configuration.json'])
    time.sleep(1)  # Wait to be sure that the process is completely started

    return orthanc_process


def setup_second_orthanc_server() -> subprocess.Popen:
    """Start an second Orthanc server

    Returns
    -------
    subprocess.Popen
        Subprocess of the test Orthanc server instance.
    """
    second_orthanc_process = subprocess.Popen(['Orthanc', './tests/orthanc_second_configuration.json'])
    time.sleep(1)  # Wait to be sure that the process is completely started

    return second_orthanc_process


def stop_orthanc_server_and_remove_data_directory(orthanc_process: subprocess.Popen) -> None:
    """Stop the test orthanc server and remove its data directory

    Parameters
    ----------
    orthanc_process
        Orthanc subprocess.Popen process.
    """
    orthanc_process.kill()
    orthanc_process.wait()

    try:
        shutil.rmtree('./tests/data/FirstOrthancStorage')
    except FileNotFoundError:
        pass


def stop_second_orthanc_server_and_remove_data_directory(second_orthanc_process: subprocess.Popen) -> None:
    """Stop the test orthanc server and remove its data directory

    Parameters
    ----------
    second_orthanc_process
        Orthanc subprocess.Popen process.
    """
    second_orthanc_process.kill()
    second_orthanc_process.wait()

    try:
        shutil.rmtree('./tests/data/SecondOrthancStorage')
    except FileNotFoundError:
        pass


def setup_data() -> None:
    """Load test dicom files to the test Orthanc server instance
    """
    headers = {'content-type': 'application/dicom'}

    list_of_dicom_file_paths = [
        f'./tests/data/dicom_files/{i}'
        for i in os.listdir('./tests/data/dicom_files/')
    ]

    for file_path in list_of_dicom_file_paths:
        with open(file_path, 'rb') as file_handler:
            data = file_handler.read()

        requests.post(
            f'{ORTHANC_URL}/instances',
            data=data,
            headers=headers
        )


def setup_data_for_second_orthanc() -> None:
    headers = {'content-type': 'application/dicom'}

    list_of_dicom_file_paths = [
        f'./tests/data/second_dicom_files/RTSTRUCT.dcm'
    ]

    for file_path in list_of_dicom_file_paths:
        with open(file_path, 'rb') as file_handler:
            data = file_handler.read()

        requests.post(
            f'{SECOND_ORTHANC_URL}/instances',
            data=data,
            headers=headers
        )


def clear_data() -> None:
    """Remove all patient data in the test Orthanc instance with API calls
    """
    patient_identifiers = requests.get(f'{ORTHANC_URL}/patients').json()

    for patient_identifier in patient_identifiers:
        requests.delete(f'{ORTHANC_URL}/patients/{patient_identifier}')

    query_identifiers = requests.get(f'{ORTHANC_URL}/queries').json()

    for query_identifier in query_identifiers:
        requests.delete(f'{ORTHANC_URL}/queries/{query_identifier}')


def clear_data_of_second_orthanc() -> None:
    """Remove all patient data in the test Orthanc instance with API calls
    """
    patient_identifiers = requests.get(f'{SECOND_ORTHANC_URL}/patients').json()

    for patient_identifier in patient_identifiers:
        requests.delete(f'{SECOND_ORTHANC_URL}/patients/{patient_identifier}')

    query_identifiers = requests.get(f'{ORTHANC_URL}/queries').json()

    for query_identifier in query_identifiers:
        requests.delete(f'{ORTHANC_URL}/queries/{query_identifier}')
