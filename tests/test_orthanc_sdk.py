from http import HTTPStatus

from .setup_server import ORTHANC_1


def test_new_route(client):
    response = client.get(f'{ORTHANC_1.url}/test')

    assert response.status_code == HTTPStatus.OK
    assert response.text == 'ok'
