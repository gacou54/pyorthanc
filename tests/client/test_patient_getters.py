import os
import warnings
import zipfile
from typing import Dict

import httpx
import pytest

from ..data import a_patient

KEYS_TO_EXCLUDE = {'LastUpdate', 'FileUuid', 'FileSize', 'DiskSize', 'UncompressedSize', 'DiskSizeMB',
                   'UncompressedSizeMB'}  # Removing keys that are never the same


@pytest.mark.parametrize('client_fixture, expected_number_of_patients', [
    ('client', 0),
    ('client_with_data', 1)
])
def test_get_patients(client_fixture, expected_number_of_patients, request):
    result = request.getfixturevalue(client_fixture).get_patients()

    assert isinstance(result, list)
    assert len(result) == expected_number_of_patients


def test_get_patient(client_with_data):
    result = client_with_data.get_patients_id(a_patient.IDENTIFIER)

    assert isinstance(result, dict)
    result = {key: value for key, value in result.items() if key not in KEYS_TO_EXCLUDE}
    expected = {key: value for key, value in a_patient.INFORMATION.items() if key not in KEYS_TO_EXCLUDE}
    assert result == expected


def test_get_patient_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_patients_id(a_patient.IDENTIFIER)


def test_get_patient_zip(client_with_data):
    result = client_with_data.get_patients_id_archive(a_patient.IDENTIFIER)

    assert isinstance(result, bytes)
    with open(a_patient.ZIP_FILE_PATH, 'wb') as file_handler:
        file_handler.write(result)

    a_zip_file = zipfile.ZipFile(a_patient.ZIP_FILE_PATH)
    assert a_zip_file.testzip() is None
    os.remove(a_patient.ZIP_FILE_PATH)


def test_get_patient_instances(client_with_data):
    result = client_with_data.get_patients_id_instances(a_patient.IDENTIFIER)

    assert isinstance(result, list)
    for i in [{key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE} for i in result]:
        assert i in [{key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE} for i in
                     a_patient.INSTANCES]


@pytest.mark.parametrize('params, expected_tags', [
    (None, a_patient.INSTANCE_TAGS),
    ({'simplify': True}, a_patient.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION),
    ({'short': True}, a_patient.INSTANCE_TAGS_IN_SHORTER_VERSION),
])
def test_get_study_instances_tags(client_with_data, params, expected_tags):
    result = client_with_data.get_patients_id_instances_tags(a_patient.IDENTIFIER, params=params)

    if params == {'short': True}:
        assert result == expected_tags
    else:
        for instance_identifier, instance in result.items():
            for expected_key in expected_tags[instance_identifier]:
                assert expected_key in instance


@pytest.mark.parametrize('params, expected_module', [
    (None, a_patient.MODULE),
    ({'simplify': True}, a_patient.MODULE_IN_SIMPLIFIED_VERSION),
    ({'short': True}, a_patient.MODULE_IN_SHORTER_VERSION),
])
def test_get_patient_module(client_with_data, params, expected_module):
    result = client_with_data.get_patients_id_module(a_patient.IDENTIFIER, params=params)

    assert result == expected_module


def test_get_patient_module_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_patients_id_module(a_patient.IDENTIFIER)


def test_get_if_patient_protected(client_with_data):
    # TODO: Test cases where 1) patient is protected and 2) patient is unprotected
    warnings.warn('Cannot set Patient to unprotected (not working with the generated Orthanc client) -- skipping test')


def test_get_patient_series(client_with_data):
    result = client_with_data.get_patients_id_series(a_patient.IDENTIFIER)

    assert isinstance(result, list)
    for i in [{key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE} for i in result]:
        assert i in [{key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE} for i in a_patient.SERIES]


def test_get_patient_series_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_patients_id_series(a_patient.IDENTIFIER)


@pytest.mark.parametrize('params, expected_shared_tags', [
    (None, a_patient.SHARED_TAGS),
    ({'simplify': True}, a_patient.SHARED_TAGS_IN_SIMPLIFIED_VERSION),
    ({'short': True}, a_patient.SHARED_TAGS_IN_SHORTER_VERSION),
])
def test_get_patient_shared_tags(client_with_data, params, expected_shared_tags):
    result = client_with_data.get_patients_id_shared_tags(a_patient.IDENTIFIER, params=params)

    assert result == expected_shared_tags


def test_get_patient_share_tags_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_patients_id_shared_tags(a_patient.IDENTIFIER)


def test_get_patient_statistics(client_with_data):
    result = client_with_data.get_patients_id_statistics(a_patient.IDENTIFIER)

    assert isinstance(result, dict)
    result = {key: value for key, value in result.items() if key not in KEYS_TO_EXCLUDE}
    expected = {key: value for key, value in a_patient.STATISTICS.items() if key not in KEYS_TO_EXCLUDE}
    assert result == expected


def test_get_patient_statistics_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_patients_id_statistics(a_patient.IDENTIFIER)


def test_get_patient_studies(client_with_data):
    result = client_with_data.get_patients_id_studies(a_patient.IDENTIFIER)

    assert isinstance(result, list)
    for i in [_sort_dictionary_element({key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE}) for i in
              result]:
        assert i in [_sort_dictionary_element({key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE})
                     for i in a_patient.STUDIES]


def _sort_dictionary_element(dictionary: Dict) -> Dict:
    for key, value in dictionary.items():
        if type(value) == list:
            dictionary[key] = value.sort()

        elif type(value) == dict:
            dictionary[key] = _sort_dictionary_element(value)

    return dictionary
