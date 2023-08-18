import io
from zipfile import ZipFile

import pytest

from .conftest import LABEL_SERIES
from .data import a_series


def test_attributes(series):
    series.build_instances()

    assert series.get_main_information().keys() == a_series.INFORMATION.keys()

    assert series.identifier == a_series.IDENTIFIER
    assert series.uid == a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    assert series.modality == a_series.MODALITY
    assert series.manufacturer == a_series.MANUFACTURER
    assert series.study_identifier == a_series.PARENT_STUDY
    assert series.labels == [LABEL_SERIES]
    assert series.instances != []


def test_zip(series):
    result = series.get_zip()

    assert type(result) == bytes
    zipfile = ZipFile(io.BytesIO(result))
    assert zipfile.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_anonymize(series):
    series.build_instances()

    anonymized_series = series.anonymize(remove=['Modality'])
    anonymized_series.build_instances()
    assert anonymized_series.uid != a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    with pytest.raises(KeyError):
        anonymized_series.modality

    anonymized_series = series.anonymize(replace={'Modality': 'RandomModality'})
    anonymized_series.build_instances()
    assert series.modality in a_series.MODALITY
    assert anonymized_series.modality == 'RandomModality'

    anonymized_series = series.anonymize(keep=['StationName'])
    anonymized_series.build_instances()
    assert series.get_main_information()['MainDicomTags']['StationName'] == \
           a_series.INFORMATION['MainDicomTags']['StationName']
    assert anonymized_series.get_main_information()['MainDicomTags']['StationName'] == \
           a_series.INFORMATION['MainDicomTags']['StationName']


def test_remote_empty_instances(series):
    series.build_instances()

    # Putting an empty instance
    series._instances = [None]

    series.remove_empty_instances()
    assert series.instances == []


@pytest.mark.parametrize('label', ['a_label'])
def test_label(series, label):
    series.add_to_label(label)

    assert label in series.labels
