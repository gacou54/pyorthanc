import pytest

from pyorthanc import AsyncOrthanc, Instance, Orthanc, Patient, Series, Study, filtering
from tests.data import a_patient, a_series, a_study, an_instance
from tests.setup_server import ORTHANC_1, clear_data, setup_data


@pytest.fixture
def client():
    setup_data(ORTHANC_1)

    yield Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def async_client():
    setup_data(ORTHANC_1)

    yield AsyncOrthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.mark.parametrize('async_mode, series_filter, expected_nbr_of_series', [
    (False, None, 3),
    (False, lambda s: s.modality == 'RTDOSE', 1),
    (True, None, 3),
    (True, lambda s: s.modality == 'RTDOSE', 1),
]
                         )
def test_find(client, async_mode, series_filter, expected_nbr_of_series):
    patients = filtering.find(
        orthanc_url=client.url,
        auth=(ORTHANC_1.username, ORTHANC_1.password),
        async_mode=async_mode,
        series_filter=series_filter
    )

    assert type(patients) == list
    assert type(patients[0]) == Patient
    assert patients[0].patient_id == a_patient.ID

    assert type(patients[0].studies[0]) == Study
    assert patients[0].studies[0].uid == a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
    assert len(patients[0].studies[0].series) == expected_nbr_of_series

    assert type(patients[0].studies[0].series[0]) == Series
    assert patients[0].studies[0].series[0].uid == a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']

    assert type(patients[0].studies[0].series[0].instances[0]) == Instance
    assert patients[0].studies[0].series[0].instances[0].uid == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']
