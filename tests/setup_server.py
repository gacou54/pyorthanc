import os
import dataclasses
import time
import shutil
import subprocess

import httpx


@dataclasses.dataclass
class OrthancServer:
    url: str
    AeT: str
    config_path: str
    storage_path: str
    test_data_path: str
    username: str
    password: str

    process: subprocess.Popen = None


ORTHANC_1 = OrthancServer(
    url='http://localhost:8042',
    AeT='ORTHANC1',
    storage_path='./tests/data/config/OrthancStorage-1',
    config_path='./tests/data/config/config-1.json',
    test_data_path='./tests/data/orthanc_1_test_data',
    username='orthanc1',
    password='orthanc1',
)

ORTHANC_2 = OrthancServer(
    url='http://localhost:8043',
    AeT='ORTHANC2',
    storage_path='./tests/data/config/OrthancStorage-2',
    config_path='./tests/data/config/config-2.json',
    test_data_path='./tests/data/orthanc_2_test_data',
    username='orthanc2',
    password='orthanc2',
)


def start_orthanc_server(orthanc: OrthancServer) -> OrthancServer:
    """Start an Orthanc server."""
    orthanc.process = subprocess.Popen(['Orthanc', orthanc.config_path], stderr=subprocess.DEVNULL)

    ready = False
    while not ready:
        try:
            httpx.get(f'{orthanc.url}/patients').json()
            ready = True
        except httpx.HTTPError:
            time.sleep(0.1)  # Time to ensure that the server has started

    return orthanc


def stop_orthanc_server_and_remove_data_directory(orthanc: OrthancServer) -> None:
    """Stop the test orthanc server and remove its data directory."""
    orthanc.process.kill()
    orthanc.process.wait()

    try:
        shutil.rmtree(orthanc.storage_path)
    except FileNotFoundError:
        pass


def setup_data(orthanc: OrthancServer) -> None:
    """Load test dicom files to the test Orthanc server instance."""
    headers = {'content-type': 'application/dicom'}

    dicom_file_paths = [f'{orthanc.test_data_path}/{i}' for i in os.listdir(orthanc.test_data_path)]

    for file_path in dicom_file_paths:
        with open(file_path, 'rb') as file:
            httpx.post(
                f'{orthanc.url}/instances',
                content=file.read(),
                headers=headers
            )


def clear_data(orthanc: OrthancServer) -> None:
    """Remove all patient data in the test Orthanc instance with API calls."""
    patient_identifiers = httpx.get(f'{orthanc.url}/patients').json()

    for patient_identifier in patient_identifiers:
        httpx.delete(f'{orthanc.url}/patients/{patient_identifier}')

    query_identifiers = httpx.get(f'{orthanc.url}/queries').json()

    for query_identifier in query_identifiers:
        httpx.delete(f'{orthanc.url}/queries/{query_identifier}')
