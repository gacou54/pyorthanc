import io
from datetime import datetime
from zipfile import ZipFile

import httpx
import pytest

from pyorthanc import Patient, errors
from tests.conftest import LABEL_PATIENT
from tests.data import a_patient


def test_attributes(patient):
    assert patient.get_main_information().keys() == a_patient.INFORMATION.keys()
    assert patient.main_dicom_tags == a_patient.INFORMATION['MainDicomTags']

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

    shared_tags = patient.shared_tags
    assert isinstance(shared_tags, dict)
    assert 'PatientName' in shared_tags  # simply checking for common shared tags
    assert 'PatientBirthDate' in shared_tags

    assert [s.identifier for s in patient.studies] == a_patient.INFORMATION['Studies']


def test_zip(patient):
    result = patient.get_zip()

    assert isinstance(result, bytes)
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_download(patient: Patient, tmp_dir: str):
    buffer = io.BytesIO()
    patient.download(buffer)
    buffer.seek(0)
    assert ZipFile(buffer).testzip() is None  # Verify that zip files are valid (if it is, returns None)

    patient.download(f'{tmp_dir}/file.zip')
    assert ZipFile(f'{tmp_dir}/file.zip').testzip() is None


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


def test_anonymize_as_job(patient: Patient):
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


def test_modify_remove(patient):
    assert patient.name == a_patient.NAME

    patient.modify(remove=['PatientName'])
    assert patient.patient_id == a_patient.ID
    with pytest.raises(errors.TagDoesNotExistError):
        patient.name

    with pytest.raises(httpx.HTTPError):
        patient.modify(remove=['PatientID'])

    with pytest.raises(httpx.HTTPError):
        patient.modify(remove=['PatientID'], force=True)


def test_modify_replace(patient):
    assert patient.name == a_patient.NAME

    patient.modify(replace={'PatientName': 'NewName'})

    assert patient.patient_id == a_patient.ID
    assert patient.name == 'NewName'

    with pytest.raises(errors.ModificationError):
        patient.modify(replace={'PatientID': 'new-id'})

    modified_patient = patient.modify(replace={'PatientID': 'new-id'}, force=True)
    assert modified_patient.patient_id == 'new-id'


def test_modify_as_job_remove(patient):
    job = patient.modify_as_job(remove=['PatientName'])
    assert patient.name == a_patient.NAME

    job.wait_until_completion()
    assert patient.patient_id == a_patient.ID
    with pytest.raises(errors.TagDoesNotExistError):
        patient.name

    with pytest.raises(httpx.HTTPError):
        patient.modify_as_job(remove=['PatientID'])

    job = patient.modify_as_job(remove=['PatientID'], force=True)
    job.wait_until_completion()
    assert 'ID' not in job.content  # Has no effect because PatientID can't be removed


def test_modify_as_job_replace(patient: Patient):
    job = patient.modify_as_job(replace={'PatientName': 'NewName'})
    assert patient.name == a_patient.NAME

    job.wait_until_completion()
    assert patient.patient_id == a_patient.ID
    assert patient.name == 'NewName'

    with pytest.raises(errors.ModificationError):
        patient.modify_as_job(replace={'PatientID': 'new-id'})

    job = patient.modify_as_job(replace={'PatientID': 'new-id'}, force=True)
    job.wait_until_completion()
    modified_patient = Patient(job.content['ID'], patient.client)
    assert modified_patient.patient_id == 'new-id'


@pytest.mark.parametrize('label', ['a_label'])
def test_label(patient, label):
    patient.add_label(label)
    assert label in patient.labels

    patient.remove_label(label)
    assert label not in patient.labels
