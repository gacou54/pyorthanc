import pytest

from pyorthanc import find_patients
from .data import a_patient


@pytest.mark.parametrize('query, expected', [
    (None, [a_patient.IDENTIFIER]),
    ({}, [a_patient.IDENTIFIER]),
    ({'PatientID': '*'}, [a_patient.IDENTIFIER]),
    ({'PatientID': 'NOT_EXISTING_PATIENT'}, []),
])
def test_find_patients(client_with_data, query, expected):
    result = find_patients(client_with_data, query)

    assert result == expected


def test_find_studies(client_with_data):
    raise NotImplementedError


def test_find_series(client_with_data):
    raise NotImplementedError


def test_find_instances(client_with_data):
    raise NotImplementedError


def test_query_orthanc(client_with_data):
    raise NotImplementedError
