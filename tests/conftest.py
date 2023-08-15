import pytest

from pyorthanc import Orthanc, AsyncOrthanc

from .setup_server import ORTHANC_1, setup_data, clear_data, ORTHANC_2


@pytest.fixture
def client():
    yield Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def client_with_data(client):
    setup_data(ORTHANC_1)

    return client


@pytest.fixture
def second_client():
    yield Orthanc(ORTHANC_2.url, ORTHANC_2.username, ORTHANC_2.password)

    clear_data(ORTHANC_2)


@pytest.fixture
def second_client_with_data(second_client):
    setup_data(ORTHANC_2)

    return second_client


@pytest.fixture
def async_client() -> AsyncOrthanc:
    yield AsyncOrthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def async_client_with_data(async_client):
    setup_data(ORTHANC_1)

    return async_client
