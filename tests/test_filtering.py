import pytest

from pyorthanc import AsyncOrthanc, Instance, Orthanc, Patient, Series, Study, filtering
from pyorthanc.util import make_datetime_from_dicom_date
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


@pytest.mark.parametrize('patient_filter, study_filter, series_filter, instance_filter, expected_nbr_of_patient, expected_nbr_of_series', [
    (None, None, None, None, 1, 3),
    (lambda p: p.name == 'MR-R', None, None, None, 1, 3),
    (lambda p: p.name == 'NOT_EXISTING_PATIENT', None, None, None, 0, 0),
    (None, lambda s: s.date == make_datetime_from_dicom_date('20100223'), None, None, 1, 3),
    (None, lambda s: s.date == make_datetime_from_dicom_date('19990101'), None, None, 0, 0),  # Fake date.
    (None, None, lambda s: s.modality == 'RTDOSE', None, 1, 1),
    (None, None, lambda s: s.modality == 'NOT_EXISTING_MODALITY', None, 0, 0),
    (None, None, None, lambda i: i.creation_date == make_datetime_from_dicom_date('20100301', '170155'), 1, 3),
    (None, None, None, lambda i: i.creation_date == make_datetime_from_dicom_date('19990101'), 0, 0),  # Fake date.
])
def test_find(client, patient_filter, study_filter, series_filter, instance_filter, expected_nbr_of_patient, expected_nbr_of_series):
    patients = filtering.find(
        orthanc=client,
        patient_filter=patient_filter,
        study_filter=study_filter,
        series_filter=series_filter,
        instance_filter=instance_filter
    )

    assert type(patients) == list
    assert len(patients) == expected_nbr_of_patient
    if expected_nbr_of_patient != 0:
        patient = patients[0]
        assert type(patient) == Patient
        assert patient.patient_id == a_patient.ID

        assert len(patient.studies) != 0
        study = patients[0].studies[0]
        assert type(study) == Study
        assert study.uid == a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
        assert len(study.series) == expected_nbr_of_series

        assert len(study.series) != 0
        series = patients[0].studies[0].series[0]
        assert type(series) == Series
        assert series.uid == a_series.INFORMATION['MainDicomTags']['SeriesInstanceUID']

        assert len(series.instances) != 0
        instance = series.instances[0]
        assert type(instance) == Instance
        assert instance.uid == an_instance.INFORMATION['MainDicomTags']['SOPInstanceUID']
