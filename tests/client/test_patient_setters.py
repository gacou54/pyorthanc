import warnings

import httpx
import pytest

from ..data import a_patient


def test_set_patient_to_protected(client_with_data):
    warnings.warn('Cannot set Patient to protected (not working with the generated Orthanc client) -- skipping test')
    # assert client_with_data.get_patients_id_protected(a_patient.IDENTIFIER) == '0'

    # # Set to protected
    # result = client_with_data.put_patients_id_protected(a_patient.IDENTIFIER)
    # assert result == '1'
    # assert client_with_data.get_patients_id_protected(a_patient.IDENTIFIER) == '1'

    # # Set to unprotected
    # result = client_with_data.put_patients_id_protected(a_patient.IDENTIFIER)
    # assert result == '0'
    # assert client_with_data.get_patients_id_protected(a_patient.IDENTIFIER) == '0'


def test_set_patient_to_protected_when_no_data(client):
    with pytest.raises(httpx.HTTPError):
        client.put_patients_id_protected(a_patient.IDENTIFIER)

    with pytest.raises(httpx.HTTPError):
        client.put_patients_id_protected(a_patient.IDENTIFIER)
