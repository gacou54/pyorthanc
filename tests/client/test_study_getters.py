import os
import zipfile

import httpx
import pytest

from ..data import a_study

KEYS_TO_EXCLUDE = {'LastUpdate', 'FileUuid', 'FileSize'}  # Removing keys that are never the same


@pytest.mark.parametrize('client_fixture, expected_number_of_studies', [
    ('client', 0),
    ('client_with_data', 1)
])
def test_get_studies(client_fixture, expected_number_of_studies, request):
    result = request.getfixturevalue(client_fixture).get_studies()

    assert isinstance(result, list)
    assert len(result) == expected_number_of_studies


def test_get_study(client_with_data):
    result = client_with_data.get_studies_id(a_study.IDENTIFIER)

    assert isinstance(result, dict)
    assert {key: value.sort() if type(value) == list else value for key, value in result.items() if
            key not in KEYS_TO_EXCLUDE} == \
           {key: value.sort() if type(value) == list else value for key, value in a_study.INFORMATION.items() if
            key not in KEYS_TO_EXCLUDE}


def test_get_study_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_studies_id(a_study.IDENTIFIER)


def test_get_study_zip(client_with_data):
    result = client_with_data.get_studies_id_archive(a_study.IDENTIFIER)

    assert isinstance(result, bytes)
    with open(a_study.ZIP_FILE_PATH, 'wb') as file_handler:
        file_handler.write(result)

    zip_file = zipfile.ZipFile(a_study.ZIP_FILE_PATH)
    assert zip_file.testzip() is None
    os.remove(a_study.ZIP_FILE_PATH)


def test_get_study_zip_with_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_studies_id_archive(a_study.IDENTIFIER)


def test_get_study_instances(client_with_data):
    result = client_with_data.get_studies_id_instances(a_study.IDENTIFIER)

    assert isinstance(result, list)
    for i in [{key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE} for i in result]:
        assert i in [{key: value for key, value in i.items() if key not in KEYS_TO_EXCLUDE} for i in a_study.INSTANCES]


def test_get_study_instances_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_studies_id_instances(a_study.IDENTIFIER)


@pytest.mark.parametrize('params, expected_tags', [
    (None, a_study.INSTANCE_TAGS),
    ({'simplify': True}, a_study.INSTANCE_TAGS_IN_SIMPLIFIED_VERSION),
    ({'short': True}, a_study.INSTANCE_TAGS_IN_SHORTER_VERSION),
])
def test_get_study_instances_tags(client_with_data, params, expected_tags):
    result = client_with_data.get_studies_id_instances_tags(a_study.IDENTIFIER, params=params)

    if params == {'short': True}:
        assert result == expected_tags

    else:
        for instance_identifier, instance in result.items():
            for expected_key in expected_tags[instance_identifier]:
                assert expected_key in instance


def test_get_study_instances_tags_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.get_studies_id_instances_tags(a_study.IDENTIFIER)
