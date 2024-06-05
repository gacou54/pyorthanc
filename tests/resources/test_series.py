import io
from datetime import datetime
from zipfile import ZipFile

import httpx
import pytest

from pyorthanc import Patient, Series, Study, errors
from tests.conftest import LABEL_SERIES
from tests.data import a_patient, a_series, a_study


def test_attributes(series: Series):
    assert series.get_main_information().keys() == a_series.INFORMATION.keys()
    assert series.main_dicom_tags == a_series.INFORMATION['MainDicomTags']

    assert series.identifier == a_series.IDENTIFIER
    assert series.uid == a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    assert series.modality == a_series.MODALITY
    assert series.manufacturer == a_series.MANUFACTURER
    assert series.study_identifier == a_series.PARENT_STUDY
    assert series.instances != []
    assert series.station_name == a_series.INFORMATION['MainDicomTags']['StationName']
    assert series.image_orientation_patient == [1, 0, 0, 0, 1, 0]

    shared_tags = series.shared_tags
    assert isinstance(shared_tags, dict)
    assert 'PatientName' in shared_tags  # simply checking for common shared tags
    assert 'PixelSpacing' in shared_tags

    assert series.labels == [LABEL_SERIES]
    assert not series.is_stable
    assert isinstance(series.last_update, datetime)
    assert str(series) == f'Series({a_series.IDENTIFIER})'

    assert isinstance(series.parent_study, Study)
    assert series.parent_study.date == a_study.DATE
    assert isinstance(series.parent_patient, Patient)
    assert series.parent_patient.name == a_patient.NAME

    for absent_attribute in ['performed_procedure_step_description', 'sequence_name',
                             'protocol_name', 'description', 'body_part_examined', 'cardiac_number_of_images',
                             'images_in_acquisition', 'number_of_temporal_positions', 'number_of_slices',
                             'number_of_time_slices', 'series_type', 'operators_name',
                             'acquisition_device_processing_description', 'contrast_bolus_agent']:
        with pytest.raises(errors.TagDoesNotExistError):
            getattr(series, absent_attribute)


def test_zip(series):
    result = series.get_zip()

    assert isinstance(result, bytes)
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_download(series: Series, tmp_dir: str):
    buffer = io.BytesIO()
    series.download(buffer)
    buffer.seek(0)
    assert ZipFile(buffer).testzip() is None  # Verify that zip files are valid (if it is, returns None)

    series.download(f'{tmp_dir}/file.zip')
    assert ZipFile(f'{tmp_dir}/file.zip').testzip() is None


def test_anonymize(series: Series):
    anonymized_series = series.anonymize(remove=['Modality'])
    assert anonymized_series.uid != a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    with pytest.raises(errors.TagDoesNotExistError):
        anonymized_series.modality

    anonymized_series = series.anonymize(replace={'Modality': 'RandomModality'})
    assert series.modality == a_series.MODALITY
    assert anonymized_series.modality == 'RandomModality'

    anonymized_series = series.anonymize(keep=['StationName'])
    assert series.get_main_information()['MainDicomTags']['StationName'] == \
           a_series.INFORMATION['MainDicomTags']['StationName']
    assert anonymized_series.get_main_information()['MainDicomTags']['StationName'] == \
           a_series.INFORMATION['MainDicomTags']['StationName']


def test_anonymize_as_job(series: Series):
    job = series.anonymize_as_job(remove=['Modality'])
    job.wait_until_completion()
    anonymized_series = Series(job.content['ID'], series.client)
    assert anonymized_series.uid != a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    with pytest.raises(errors.TagDoesNotExistError):
        anonymized_series.modality

    job = series.anonymize_as_job(replace={'Modality': 'RandomModality'})
    job.wait_until_completion()
    anonymized_series = Series(job.content['ID'], series.client)
    assert series.modality == a_series.MODALITY
    assert anonymized_series.modality == 'RandomModality'

    job = series.anonymize_as_job(keep=['StationName'])
    job.wait_until_completion()
    anonymized_series = Series(job.content['ID'], series.client)
    assert series.get_main_information()['MainDicomTags']['StationName'] == \
           a_series.INFORMATION['MainDicomTags']['StationName']
    assert anonymized_series.get_main_information()['MainDicomTags']['StationName'] == \
           a_series.INFORMATION['MainDicomTags']['StationName']


def test_modify_remove(series: Series):
    assert series.manufacturer == a_series.MANUFACTURER

    modified_series = series.modify(remove=['Manufacturer'])
    assert series.uid == a_series.UID
    assert modified_series.uid != a_series.UID
    with pytest.raises(errors.TagDoesNotExistError):
        modified_series.manufacturer

    # Modify itself
    modified_series = series.modify(
        remove=['Manufacturer'],
        keep=['SeriesInstanceUID'],
        force=True
    )
    assert modified_series.id_ == series.id_  # Ensure that it is the same object (since SeriesInstanceUID has not changed)
    assert modified_series.uid == a_series.UID
    assert Study(modified_series.study_identifier, series.client).uid == Study(series.study_identifier, series.client).uid

    with pytest.raises(httpx.HTTPError):
        series.modify(remove=['SeriesInstanceUID'])

    with pytest.raises(httpx.HTTPError):
        series.modify(remove=['SeriesInstanceUID'], force=True)


def test_modify_replace(series: Series):
    assert series.manufacturer == a_series.MANUFACTURER

    modified_series = series.modify(replace={'Manufacturer': 'new-manufacturer'})
    assert modified_series.uid != a_series.UID
    assert modified_series.manufacturer == 'new-manufacturer'

    # Modify itself
    modified_series = series.modify(replace={'Manufacturer': 'new-manufacturer'}, keep=['SeriesInstanceUID'], force=True)
    assert modified_series.id_ == series.id_
    assert modified_series.uid == series.uid
    assert Study(modified_series.study_identifier, series.client).uid == Study(series.study_identifier, series.client).uid
    assert modified_series.manufacturer == 'new-manufacturer'
    assert series.manufacturer == 'new-manufacturer'

    with pytest.raises(errors.ModificationError):
        series.modify(replace={'SeriesInstanceUID': '1.2.840.113745.101000.999999999999'})

    modified_series = series.modify(
        replace={
            'StudyInstanceUID': '1.2.840.113745.101000.888888888888',
            'SeriesInstanceUID': '1.2.840.113745.101000.999999999999'
        },
        force=True
    )
    assert Study(modified_series.study_identifier, series.client).uid == '1.2.840.113745.101000.888888888888'
    assert modified_series.uid == '1.2.840.113745.101000.999999999999'
    assert modified_series.id_ != series.id_


def test_modify_as_job_remove(series: Series):
    # Create new modified series
    job = series.modify_as_job(remove=['Manufacturer'])
    job.wait_until_completion()
    modified_series = Series(job.content['ID'], series.client)
    assert series.uid == a_series.UID
    assert modified_series.uid != a_series.UID
    with pytest.raises(errors.TagDoesNotExistError):
        modified_series.manufacturer

    # Modify itself
    job = series.modify_as_job(
        remove=['Manufacturer'],
        keep=['SeriesInstanceUID'],
        force=True
    )
    job.wait_until_completion()
    modified_series = Series(job.content['ID'], series.client)
    assert modified_series.id_ == series.id_   # Ensure that it is the same object (since SeriesInstanceUID has not changed)
    assert modified_series.uid == a_series.UID
    assert series.uid == a_series.UID
    assert Study(modified_series.study_identifier, series.client).uid == Study(series.study_identifier, series.client).uid
    with pytest.raises(errors.TagDoesNotExistError):
        series.manufacturer

    with pytest.raises(httpx.HTTPError):
        series.modify_as_job(remove=['SeriesInstanceUID'])

    job = series.modify_as_job(remove=['SeriesInstanceUID'], force=True)
    job.wait_until_completion()
    assert 'ID' not in job.content  # Has no effect because SeriesInstanceUID can't be removed


def test_modify_as_job_replace(series: Series):
    job = series.modify_as_job(replace={'Manufacturer': 'new-manufacturer'})
    job.wait_until_completion()
    modified_series = Series(job.content['ID'], series.client)
    assert modified_series.uid != a_series.UID
    assert modified_series.manufacturer == 'new-manufacturer'

    # Modify itself
    job = series.modify_as_job(replace={'Manufacturer': 'new-manufacturer'}, keep=['SeriesInstanceUID'], force=True)
    job.wait_until_completion()
    modified_series = Series(job.content['ID'], series.client)
    assert modified_series.id_ == series.id_
    assert modified_series.uid == series.uid
    assert Study(modified_series.study_identifier, series.client).uid == Study(series.study_identifier, series.client).uid
    assert modified_series.manufacturer == 'new-manufacturer'
    assert series.manufacturer == 'new-manufacturer'

    with pytest.raises(errors.ModificationError):
        series.modify_as_job(replace={'SeriesInstanceUID': '1.2.840.113745.101000.999999999999'})

    job = series.modify_as_job(replace={'SeriesInstanceUID': '1.2.840.113745.101000.999999999999'}, force=True)
    job.wait_until_completion()
    modified_series = Series(job.content['ID'], series.client)
    assert modified_series.uid == '1.2.840.113745.101000.999999999999'


def test_remote_empty_instances(series):
    series._lock_children = True

    # Putting an empty instance
    series._child_resources = [None]

    series.remove_empty_instances()
    assert series.instances == []


@pytest.mark.parametrize('label', ['a_label'])
def test_label(series, label):
    series.add_label(label)
    assert label in series.labels

    series.remove_label(label)
    assert label not in series.labels
