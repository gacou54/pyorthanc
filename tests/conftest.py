import pytest

from pyorthanc import Orthanc, AsyncOrthanc, RemoteModality

from .setup_server import ORTHANC_1, setup_data, clear_data, ORTHANC_2, add_modality


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


@pytest.fixture
def modality(client, second_client):
    if ORTHANC_2.AeT not in client.get_modalities():
        add_modality(ORTHANC_1, ORTHANC_2.AeT, 'orthanc2', 4242)
        add_modality(ORTHANC_2, ORTHANC_1.AeT, 'orthanc1', 4242)

    return RemoteModality(client, ORTHANC_2.AeT)

