import io
from datetime import datetime
from zipfile import ZipFile

import httpx
import pytest

from pyorthanc import Patient, Study, errors, util
from tests.conftest import LABEL_STUDY
from tests.data import a_patient, a_study


def test_attributes(study: Study):
    assert study.get_main_information().keys() == a_study.INFORMATION.keys()
    assert study.main_dicom_tags == a_study.INFORMATION['MainDicomTags']

    assert study.identifier == a_study.IDENTIFIER
    assert study.study_id == a_study.ID
    assert study.uid == a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
    assert study.referring_physician_name == a_study.REFERRING_PHYSICIAN_NAME
    assert study.date == a_study.DATE
    assert study.patient_identifier == a_study.PARENT_PATIENT_IDENTIFIER
    assert study.patient_information.keys() == a_study.PATIENT_MAIN_INFORMATION.keys()
    assert study.labels == [LABEL_STUDY]
    assert not study.is_stable
    assert isinstance(study.last_update, datetime)
    assert study.series != []
    assert str(study) == f'Study({a_study.IDENTIFIER})'

    assert isinstance(study.parent_patient, Patient)
    assert study.parent_patient.name == a_patient.NAME

    shared_tags = study.shared_tags
    assert isinstance(shared_tags, dict)
    assert 'PatientName' in shared_tags  # simply checking for common shared tags
    assert 'StudyDate' in shared_tags

    for absent_attribute in ['description', 'institution_name', 'requested_procedure_description', 'requesting_physician']:
        with pytest.raises(errors.TagDoesNotExistError):
            getattr(study, absent_attribute)


def test_remove_empty_series(study: Study):
    study.lock = True

    for series in study.series:
        series._child_resources = []

    study.remove_empty_series()
    assert study.series == []


def test_zip(study):
    result = study.get_zip()

    assert isinstance(result, bytes)
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_download(study: Study, tmp_dir: str):
    buffer = io.BytesIO()
    study.download(buffer)
    buffer.seek(0)
    assert ZipFile(buffer).testzip() is None  # Verify that zip files are valid (if it is, returns None)

    study.download(f'{tmp_dir}/file.zip')
    assert ZipFile(f'{tmp_dir}/file.zip').testzip() is None


def test_anonymize(study):
    anonymized_study = study.anonymize(remove=['StudyDate'])
    assert anonymized_study.uid != a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
    with pytest.raises(errors.TagDoesNotExistError):
        anonymized_study.date

    anonymized_study = study.anonymize(replace={'StudyDate': '20220101'})
    assert study.date == a_study.DATE
    assert anonymized_study.date == util.make_datetime_from_dicom_date('20220101')

    anonymized_study = study.anonymize(keep=['StudyDate'])
    assert study.date == a_study.DATE
    assert anonymized_study.date == a_study.DATE


def test_anonymize_as_job(study: Study):
    job = study.anonymize_as_job(remove=['StudyDate'])
    job.wait_until_completion()
    anonymize_study = Study(job.content['ID'], study.client)
    with pytest.raises(errors.TagDoesNotExistError):
        anonymize_study.date

    job = study.anonymize_as_job(replace={'StudyDate': '20220101'})
    job.wait_until_completion()
    anonymize_study = Study(job.content['ID'], study.client)
    assert study.date == a_study.DATE
    assert anonymize_study.date == util.make_datetime_from_dicom_date('20220101')

    job = study.anonymize_as_job(keep=['StudyDate'])
    job.wait_until_completion()
    anonymize_study = Study(job.content['ID'], study.client)
    assert study.date == a_study.DATE
    assert anonymize_study.date == a_study.DATE


def test_modify_remove(study: Study):
    assert study.referring_physician_name == a_study.INFORMATION['MainDicomTags']['ReferringPhysicianName']

    modified_study = study.modify(remove=['ReferringPhysicianName'])
    assert study.uid == a_study.UID
    assert modified_study.uid != a_study.UID
    with pytest.raises(errors.TagDoesNotExistError):
        modified_study.referring_physician_name

    # Modify itself
    modified_study = study.modify(
        remove=['ReferringPhysicianName'],
        keep=['StudyInstanceUID'],
        force=True
    )
    assert modified_study.id_ == study.id_  # Ensure that it is the same object (since StudyInstanceUID has not changed)
    assert modified_study.uid == a_study.UID
    assert modified_study.series[0].uid == study.series[0].uid

    with pytest.raises(httpx.HTTPError):
        study.modify(remove=['StudyInstanceUID'])

    with pytest.raises(httpx.HTTPError):
        study.modify(remove=['StudyInstanceUID'], force=True)


def test_modify_replace(study):
    assert study.referring_physician_name == a_study.INFORMATION['MainDicomTags']['ReferringPhysicianName']

    modified_study = study.modify(replace={'ReferringPhysicianName': 'last^first'})
    assert modified_study.uid != a_study.UID
    assert modified_study.referring_physician_name == 'last^first'

    # Modify itself
    modified_study = study.modify(replace={'ReferringPhysicianName': 'last^first'}, keep=['StudyInstanceUID'], force=True)
    assert modified_study.id_ == study.id_
    assert modified_study.uid == study.uid
    assert modified_study.referring_physician_name == 'last^first'
    assert study.referring_physician_name == 'last^first'

    with pytest.raises(errors.ModificationError):
        study.modify(replace={'StudyInstanceUID': '1.2.840.113745.101000.999999999999'})

    modified_study = study.modify(replace={'StudyInstanceUID': '1.2.840.113745.101000.999999999999'}, force=True)
    assert modified_study.uid == '1.2.840.113745.101000.999999999999'
    assert modified_study.id_ != study.id_


def test_modify_as_job_remove(study: Study):
    # Create new modified study
    job = study.modify_as_job(remove=['ReferringPhysicianName'])
    job.wait_until_completion()
    modified_study = Study(job.content['ID'], study.client)
    assert study.uid == a_study.UID
    assert modified_study.uid != a_study.UID
    with pytest.raises(errors.TagDoesNotExistError):
        modified_study.referring_physician_name

    # Modify itself
    job = study.modify_as_job(
        remove=['ReferringPhysicianName'],
        keep=['StudyInstanceUID'],
        force=True
    )
    assert study.referring_physician_name == a_study.INFORMATION['MainDicomTags']['ReferringPhysicianName']
    job.wait_until_completion()
    modified_study = Study(job.content['ID'], study.client)
    assert modified_study.id_ == study.id_   # Ensure that it is the same object (since StudyInstanceUID has not changed)
    assert study.uid == a_study.UID
    assert modified_study.uid == a_study.UID
    with pytest.raises(errors.TagDoesNotExistError):
        study.referring_physician_name

    with pytest.raises(httpx.HTTPError):
        study.modify_as_job(remove=['StudyInstanceUID'])

    job = study.modify_as_job(remove=['StudyInstanceUID'], force=True)
    job.wait_until_completion()
    assert 'ID' not in job.content  # Has no effect because StudyInstanceUID can't be removed


def test_modify_as_job_replace(study: Study):
    job = study.modify_as_job(replace={'ReferringPhysicianName': 'last^first'})
    job.wait_until_completion()
    modified_study = Study(job.content['ID'], study.client)
    assert modified_study.uid != a_study.UID
    assert modified_study.referring_physician_name == 'last^first'

    # Modify itself
    job = study.modify_as_job(replace={'ReferringPhysicianName': 'last^first'}, keep=['StudyInstanceUID'], force=True)
    job.wait_until_completion()
    modified_study = Study(job.content['ID'], study.client)
    assert modified_study.id_ == study.id_
    assert modified_study.uid == study.uid
    assert modified_study.referring_physician_name == 'last^first'
    assert study.referring_physician_name == 'last^first'

    with pytest.raises(errors.ModificationError):
        study.modify_as_job(replace={'StudyInstanceUID': '1.2.840.113745.101000.999999999999'})

    job = study.modify_as_job(replace={'StudyInstanceUID': '1.2.840.113745.101000.999999999999'}, force=True)
    job.wait_until_completion()
    modified_study = Study(job.content['ID'], study.client)
    assert modified_study.uid == '1.2.840.113745.101000.999999999999'


@pytest.mark.parametrize('label', ['a_label'])
def test_label(study, label):
    study.add_label(label)
    assert label in study.labels

    study.remove_label(label)
    assert label not in study.labels
