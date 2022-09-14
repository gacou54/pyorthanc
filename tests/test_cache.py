import pytest

from pyorthanc import Orthanc, Cache

from tests.setup_server import ORTHANC_1, add_data, clear_data

# remove this
ORTHANC_1.url = 'http://localhost:8042'

@pytest.fixture
def client():
    yield Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def cache(client):
    return Cache(client, db_path='cache.db')


def test_changes(cache):
    cache.get_changes()
