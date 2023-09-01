import io
from datetime import datetime
from zipfile import ZipFile

import pytest

from pyorthanc import Series, errors
from .conftest import LABEL_SERIES
from .data import a_series


def test_attributes(series):
    assert series.get_main_information().keys() == a_series.INFORMATION.keys()

    assert series.identifier == a_series.IDENTIFIER
    assert series.uid == a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    assert series.modality == a_series.MODALITY
    assert series.manufacturer == a_series.MANUFACTURER
    assert series.study_identifier == a_series.PARENT_STUDY
    assert series.instances != []
    assert series.station_name == a_series.INFORMATION['MainDicomTags']['StationName']
    assert series.image_orientation_patient == [1, 0, 0, 0, 1, 0]

    assert series.labels == [LABEL_SERIES]
    assert not series.is_stable
    assert isinstance(series.last_update, datetime)
    assert str(series) == f'Series({a_series.IDENTIFIER})'

    for absent_attribute in ['performed_procedure_step_description', 'sequence_name',
                             'protocol_name', 'description', 'body_part_examined', 'cardiac_number_of_images',
                             'images_in_acquisition', 'number_of_temporal_positions', 'number_of_slices',
                             'number_of_time_slices', 'series_type', 'operators_name',
                             'acquisition_device_processing_description', 'contrast_bolus_agent']:
        with pytest.raises(errors.TagDoesNotExistError):
            getattr(series, absent_attribute)


def test_zip(series):
    result = series.get_zip()

    assert type(result) == bytes
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_anonymize(series):
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


def test_anonymize_as_job(series):
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

def test_remote_empty_instances(series):
    series.lock = True

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
