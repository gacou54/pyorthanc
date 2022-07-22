import pytest

from pyorthanc import Orthanc, Series
from .data import a_series
from .setup_server import ORTHANC_1, start_server, stop_server_and_remove_data, setup_data


@pytest.fixture
def series():
    start_server(ORTHANC_1)
    setup_data(ORTHANC_1)

    client = Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)
    yield Series(client=client, series_id=client.get_series()[0])

    stop_server_and_remove_data(ORTHANC_1)


def test_attributes(series):
    series.build_instances()

    assert series.get_main_information().keys() == a_series.INFORMATION.keys()

    assert series.identifier == a_series.IDENTIFIER
    assert series.uid == a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    assert series.modality == a_series.MODALITY
    assert series.manufacturer == a_series.MANUFACTURER
    assert series.study_identifier == a_series.PARENT_STUDY
    assert series.series_number == a_series.INFORMATION['MainDicomTags']['SeriesNumber']
    assert [i.id_ for i in series.instances] == a_series.INSTANCES


def test_anonymize(series):
    series.build_instances()

    anonymized_series = series.anonymize(remove=['Modality'])
    anonymized_series.build_instances()
    assert anonymized_series.uid != a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']
    with pytest.raises(KeyError):
        anonymized_series.modality

    anonymized_series = series.anonymize(replace={'Modality': 'RandomModality'})
    anonymized_series.build_instances()
    assert series.modality == a_series.MODALITY
    assert anonymized_series.modality == 'RandomModality'

    anonymized_series = series.anonymize(keep=['StationName'])
    anonymized_series.build_instances()
    assert series.get_main_information()['MainDicomTags']['StationName'] == a_series.INFORMATION['MainDicomTags']['StationName']
    assert anonymized_series.get_main_information()['MainDicomTags']['StationName'] == a_series.INFORMATION['MainDicomTags']['StationName']
