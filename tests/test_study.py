import pytest

from pyorthanc import Orthanc, Study
from .data import a_study
from .setup_server import start_server, stop_server_and_remove_data, setup_data, ORTHANC_1


@pytest.fixture
def study():
    start_server(ORTHANC_1)
    setup_data(ORTHANC_1)

    client = Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)
    yield Study(client=client, study_id=client.get_studies()[0])

    stop_server_and_remove_data(ORTHANC_1)


def test_attributes(study):
    study.build_series()

    assert study.get_main_information().keys() == a_study.INFORMATION.keys()

    assert study.identifier == a_study.IDENTIFIER
    assert study.study_id == a_study.ID
    assert study.uid == a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
    assert study.referring_physician_name == a_study.REFERRING_PHYSICIAN_NAME
    assert study.date == a_study.DATE
    assert study.patient_identifier == a_study.PARENT_PATIENT_IDENTIFIER
    assert study.patient_information.keys() == a_study.PATIENT_MAIN_INFORMATION.keys()
    assert [s.identifier for s in study.series] == a_study.SERIES


def test_remote_empty_series(study):
    study.build_series()

    for series in study.series:
        series._instances = []

    study.remove_empty_series()
    assert study.series == []