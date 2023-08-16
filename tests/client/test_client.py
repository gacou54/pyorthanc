from http import HTTPStatus

import httpx
import pytest

from pyorthanc import Orthanc
from ..setup_server import ORTHANC_1


@pytest.fixture
def client_that_return_raw_response() -> Orthanc:
    return Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password, return_raw_response=True)


def test_client_as_context_manager():
    with Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password) as client:
        result = client.get_system()

    assert isinstance(result, dict)
    assert 'ApiVersion' in result
    assert 'DicomAet' in result
    assert 'DicomPort' in result


def test_client_when_return_raw_response(client_that_return_raw_response):
    result = client_that_return_raw_response.get_system()

    assert isinstance(result, httpx.Response)
    assert result.status_code == HTTPStatus.OK
    assert 'ApiVersion' in result.json()
    assert 'DicomAet' in result.json()
    assert 'DicomPort' in result.json()
