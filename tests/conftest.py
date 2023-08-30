import pytest

from pyorthanc import AsyncOrthanc, Instance, Modality, Orthanc, Patient, Series, Study
from .data import a_patient, a_series, a_study, an_instance
from .setup_server import ORTHANC_1, ORTHANC_2, add_modality, clear_data, setup_data

LABEL_PATIENT = 'my_label_patient'
LABEL_STUDY = 'my_label_study'
LABEL_SERIES = 'my_label_series'
LABEL_INSTANCE = 'my_label_instance'


@pytest.fixture
def client():
    yield Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def client_with_data(client):
    setup_data(ORTHANC_1)

    return client


@pytest.fixture
def client_with_data_and_labels(client_with_data):
    client_with_data.put_patients_id_labels_label(a_patient.IDENTIFIER, LABEL_PATIENT)
    client_with_data.put_studies_id_labels_label(a_study.IDENTIFIER, LABEL_STUDY)
    client_with_data.put_series_id_labels_label(a_series.IDENTIFIER, LABEL_SERIES)
    client_with_data.put_instances_id_labels_label(an_instance.IDENTIFIER, LABEL_INSTANCE)

    return client_with_data


@pytest.fixture
def second_client():
    yield Orthanc(ORTHANC_2.url, ORTHANC_2.username, ORTHANC_2.password)

    clear_data(ORTHANC_2)


@pytest.fixture
def second_client_with_data(second_client):
    setup_data(ORTHANC_2)

    return second_client


@pytest.fixture
def async_client() -> AsyncOrthanc:
    yield AsyncOrthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)

    clear_data(ORTHANC_1)


@pytest.fixture
def async_client_with_data(async_client):
    setup_data(ORTHANC_1)

    return async_client


@pytest.fixture
def modality(client, second_client):
    if ORTHANC_2.AeT not in client.get_modalities():
        add_modality(ORTHANC_1, ORTHANC_2.AeT, 'orthanc2', 4242)
        add_modality(ORTHANC_2, ORTHANC_1.AeT, 'orthanc1', 4242)

    return Modality(client, ORTHANC_2.AeT)


@pytest.fixture
def patient(client_with_data_and_labels):
    return Patient(client=client_with_data_and_labels, id_=a_patient.IDENTIFIER)


@pytest.fixture
def study(client_with_data_and_labels):
    return Study(client=client_with_data_and_labels, id_=a_study.IDENTIFIER)


@pytest.fixture
def series(client_with_data_and_labels):
    return Series(client=client_with_data_and_labels, id_=a_series.IDENTIFIER)


@pytest.fixture
def instance(client_with_data_and_labels):
    return Instance(client=client_with_data_and_labels, id_=an_instance.IDENTIFIER)
