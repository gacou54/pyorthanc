import httpx
import pytest

from ..data import a_patient


def test_delete_patient(client_with_data):
    result = client_with_data.delete_patients_id(a_patient.IDENTIFIER)

    assert result == {'RemainingAncestor': None}
    with pytest.raises(httpx.HTTPError):
        client_with_data.get_patients_id(a_patient.IDENTIFIER)


def test_delete_patient_with_no_patient(client):
    with pytest.raises(httpx.HTTPError):
        client.delete_patients_id(a_patient.IDENTIFIER)
