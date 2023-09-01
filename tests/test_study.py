import io
from datetime import datetime
from zipfile import ZipFile

import pytest

from pyorthanc import Study, errors, util
from .conftest import LABEL_STUDY
from .data import a_study


def test_attributes(study):
    assert study.get_main_information().keys() == a_study.INFORMATION.keys()

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

    for absent_attribute in ['description', 'institution_name', 'requested_procedure_description', 'requesting_physician']:
        with pytest.raises(errors.TagDoesNotExistError):
            getattr(study, absent_attribute)


def test_remove_empty_series(study):
    study.lock = True

    for series in study.series:
        series._child_resources = []

    study.remove_empty_series()
    assert study.series == []


def test_zip(study):
    result = study.get_zip()

    assert type(result) == bytes
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


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


def test_anonymize_as_job(study):
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

@pytest.mark.parametrize('label', ['a_label'])
def test_label(study, label):
    study.add_label(label)
    assert label in study.labels

    study.remove_label(label)
    assert label not in study.labels
