from http import HTTPStatus

import pytest

import pyorthanc
from pyorthanc.errors import NotInInternalEnvironmentError
from tests.setup_server import ORTHANC_1, setup_data


def test_internal_client_while_being_external():
    with pytest.raises(NotInInternalEnvironmentError):
        pyorthanc.get_internal_client()


def test_route_with_internal_client(client):
    setup_data(ORTHANC_1)

    response = client.get(f'{ORTHANC_1.url}/test-internal-client')

    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert 'modalities' in result
    assert 'RTDOSE' in result['modalities']
    assert 'RTPLAN' in result['modalities']
    assert 'RTSTRUCT' in result['modalities']
