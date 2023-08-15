import httpx
import pytest


@pytest.fixture
def instance_bytes():
    with open('tests/data/orthanc_1_test_data/RTSTRUCT.dcm', 'rb') as fh:
        return fh.read()


@pytest.fixture
def bad_instance_bytes():
    with open('tests/__init__.py', 'rb') as fh:
        return fh.read()


def test_post_instance(client, instance_bytes):
    result = client.post_instances(instance_bytes)

    assert 'ID' in result
    assert 'ParentPatient' in result
    assert 'ParentStudy' in result
    assert 'ParentSeries' in result
    assert len(client.get_instances()) == 1


def test_post_instance_with_bad_data(client, bad_instance_bytes):
    with pytest.raises(httpx.HTTPError):
        client.post_instances(bad_instance_bytes)
