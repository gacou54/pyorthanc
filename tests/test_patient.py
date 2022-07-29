import io
from zipfile import ZipFile

import pytest

from pyorthanc import Orthanc, Patient
from .data import a_patient
from .setup_server import ORTHANC_1, clear_data, setup_data, stop_server_and_remove_data


@pytest.fixture
def patient():
    setup_data(ORTHANC_1)

    client = Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)
    yield Patient(client=client, patient_id=client.get_patients()[0])

    clear_data(ORTHANC_1)


def test_attributes(patient):
    patient.build_studies()

    assert patient.get_main_information().keys() == a_patient.INFORMATION.keys()

    assert patient.identifier == a_patient.IDENTIFIER
    assert patient.patient_id == a_patient.ID
    assert patient.name == a_patient.NAME
    assert patient.sex == a_patient.SEX

    assert [s.identifier for s in patient.studies] == a_patient.INFORMATION['Studies']


def test_zip(patient):
    result = patient.get_zip()

    assert type(result) == bytes
    zip = ZipFile(io.BytesIO(result))
    assert zip.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_patient_module(patient):
    result = patient.get_patient_module()
    assert result == a_patient.MODULE

    result = patient.get_patient_module(simplify=True)
    assert result == a_patient.MODULE_IN_SIMPLIFIED_VERSION

    result = patient.get_patient_module(short=True)
    assert result == a_patient.MODULE_IN_SHORTER_VERSION


def test_protection(patient):
    assert patient.is_protected() is False

    patient.set_to_protected()
    assert patient.is_protected() is True

    patient.set_to_unprotected()
    assert patient.is_protected() is False


def test_anonymize(patient):
    patient.build_studies()

    anonymize_patient = patient.anonymize(remove=['PatientName'])
    anonymize_patient.build_studies()
    assert anonymize_patient.patient_id != a_patient.ID
    with pytest.raises(KeyError):
        anonymize_patient.name

    anonymize_patient = patient.anonymize(replace={'PatientName': 'NewName'})
    anonymize_patient.build_studies()
    assert patient.name == a_patient.NAME
    assert anonymize_patient.name == 'NewName'

    anonymize_patient = patient.anonymize(keep=['PatientName'])
    anonymize_patient.build_studies()
    assert patient.name == a_patient.NAME
    assert anonymize_patient.name == a_patient.NAME
