import os
import dataclasses
import subprocess

import httpx


@dataclasses.dataclass
class OrthancServer:
    url: str
    AeT: str
    config_path: str
    storage_path: str
    test_data_path: str
    username: str = 'orthanc'
    password: str = 'orthanc'

    process: subprocess.Popen = None


ORTHANC_1 = OrthancServer(
    url=f'http://orthanc1:8042',
    AeT='ORTHANC',
    storage_path='./tests/data/config/OrthancStorage-1',
    config_path='./tests/data/config/config-1.json',
    test_data_path='./tests/data/orthanc_1_test_data',
)

ORTHANC_2 = OrthancServer(
    url=f'http://orthanc2:8042',
    AeT='ORTHANC',
    storage_path='./tests/data/config/OrthancStorage-2',
    config_path='./tests/data/config/config-2.json',
    test_data_path='./tests/data/orthanc_2_test_data',
)


def setup_data(orthanc: OrthancServer) -> None:
    """Load test dicom files to the test Orthanc server instance."""
    headers = {'content-type': 'application/dicom'}

    dicom_file_paths = [f'{orthanc.test_data_path}/{i}' for i in os.listdir(orthanc.test_data_path)]

    for file_path in dicom_file_paths:
        with open(file_path, 'rb') as file:
            httpx.post(
                f'{orthanc.url}/instances',
                content=file.read(),
                headers=headers,
                auth=httpx.BasicAuth(orthanc.username, orthanc.password)
            )


def clear_data(orthanc: OrthancServer) -> None:
    """Remove all patient data in the test Orthanc instance with API calls."""
    patient_identifiers = httpx.get(
        url=f'{orthanc.url}/patients',
        auth=httpx.BasicAuth(orthanc.username, orthanc.password)
    ).json()

    for patient_identifier in patient_identifiers:
        httpx.delete(
            url=f'{orthanc.url}/patients/{patient_identifier}',
            auth=httpx.BasicAuth(orthanc.username, orthanc.password)
        )

    query_identifiers = httpx.get(
        url=f'{orthanc.url}/queries',
        auth=httpx.BasicAuth(orthanc.username, orthanc.password)
    ).json()

    for query_identifier in query_identifiers:
        httpx.delete(
            url=f'{orthanc.url}/queries/{query_identifier}',
            auth=httpx.BasicAuth(orthanc.username, orthanc.password)
        )


def add_modality(orthanc: OrthancServer, modality: str, host: str, port: int):
    httpx.put(
        f'{orthanc.url}/modalities/{modality}',
        json={
            'AET': modality.upper(),
            'AllowEcho': True,
            'AllowFind': True,
            'AllowFindWorklist': True,
            'AllowGet': True,
            'AllowMove': True,
            'AllowStorageCommitment': True,
            'AllowStore': True,
            'AllowTranscoding': True,
            'Host': host,
            'Manufacturer': 'Generic',
            'Port': port,
            'UseDicomTls': False
        },
        auth=httpx.BasicAuth(orthanc.username, orthanc.password)
    )
