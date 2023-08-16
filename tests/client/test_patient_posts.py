import os
import zipfile

import httpx
import pytest

from ..data import a_patient


def test_anonymize_patient(client_with_data):
    result = client_with_data.post_patients_id_anonymize(a_patient.IDENTIFIER)

    assert isinstance(result, dict)
    assert 'ID' in result.keys()
    assert 'Path' in result.keys()
    assert 'PatientID' in result.keys()
    assert result['ID'] in client_with_data.get_patients()
    assert 'Anonymized' in client_with_data.get_patients_id(result['ID'])['MainDicomTags']['PatientName']


def test_anonymize_patient_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.post_patients_id_anonymize(a_patient.IDENTIFIER)


def test_archiving_patient(client_with_data):
    result = client_with_data.post_patients_id_archive(a_patient.IDENTIFIER)

    assert isinstance(result, bytes)
    with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
        file_handler.write(result)

    a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
    assert a_zip_file.testzip() is None
    os.remove(a_patient.ZIP_FILE_PATH)


def test_archiving_patient_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.post_patients_id_archive(a_patient.IDENTIFIER)
