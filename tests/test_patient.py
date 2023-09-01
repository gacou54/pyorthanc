import io
from datetime import datetime
from zipfile import ZipFile

import pytest

from pyorthanc import Patient, errors
from .conftest import LABEL_PATIENT
from .data import a_patient


def test_attributes(patient):
    assert patient.get_main_information().keys() == a_patient.INFORMATION.keys()

    assert patient.identifier == a_patient.IDENTIFIER
    assert patient.patient_id == a_patient.ID
    assert patient.name == a_patient.NAME
    assert patient.sex == a_patient.SEX
    assert patient.birth_date == datetime(year=1941, month=9, day=1)
    assert patient.other_patient_ids == ['other-id-1', 'other-id-2']

    assert patient.labels == [LABEL_PATIENT]
    assert not patient.is_stable
    assert isinstance(patient.last_update, datetime)
    assert str(patient) == f'Patient({a_patient.IDENTIFIER})'

    assert [s.identifier for s in patient.studies] == a_patient.INFORMATION['Studies']


def test_zip(patient):
    result = patient.get_zip()

    assert type(result) == bytes
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_patient_module(patient):
    result = patient.get_patient_module()
    assert result == a_patient.MODULE

    result = patient.get_patient_module(simplify=True)
    assert result == a_patient.MODULE_IN_SIMPLIFIED_VERSION

    result = patient.get_patient_module(short=True)
    assert result == a_patient.MODULE_IN_SHORTER_VERSION


def test_protection(patient):
    assert not patient.protected

    patient.protected = True
    assert patient.protected

    patient.protected = False
    assert not patient.protected


def test_anonymize(patient):
    anonymize_patient = patient.anonymize(remove=['PatientName'])
    assert anonymize_patient.patient_id != a_patient.ID
    with pytest.raises(errors.TagDoesNotExistError):
        anonymize_patient.name

    anonymize_patient = patient.anonymize(replace={'PatientName': 'NewName'})
    assert patient.name == a_patient.NAME
    assert anonymize_patient.name == 'NewName'

    anonymize_patient = patient.anonymize(keep=['PatientName'])
    assert patient.name == a_patient.NAME
    assert anonymize_patient.name == a_patient.NAME


def test_anonymize_as_job(patient):
    job = patient.anonymize_as_job(remove=['PatientName'])
    job.wait_until_completion()
    anonymize_patient = Patient(job.content['ID'], patient.client)
    assert anonymize_patient.patient_id != a_patient.ID
    with pytest.raises(errors.TagDoesNotExistError):
        anonymize_patient.name

    job = patient.anonymize_as_job(replace={'PatientName': 'NewName'})
    job.wait_until_completion()
    anonymize_patient = Patient(job.content['ID'], patient.client)
    assert patient.name == a_patient.NAME
    assert anonymize_patient.name == 'NewName'

    job = patient.anonymize_as_job(keep=['PatientName'])
    job.wait_until_completion()
    anonymize_patient = Patient(job.content['ID'], patient.client)
    assert patient.name == a_patient.NAME
    assert anonymize_patient.name == a_patient.NAME



@pytest.mark.parametrize('label', ['a_label'])
def test_label(patient, label):
    patient.add_label(label)
    assert label in patient.labels

    patient.remove_label(label)
    assert label not in patient.labels
