import pytest

from pyorthanc import Instance, Labels, Patient, Series, Study
from .data import a_patient, a_series, a_study, an_instance

LABEL_PATIENT = 'my_label_patient'
LABEL_STUDY = 'my_label_study'
LABEL_SERIES = 'my_label_series'
LABEL_INSTANCE = 'my_label_instance'


@pytest.fixture
def labels(client_with_data):
    client_with_data.put_patients_id_labels_label(a_patient.IDENTIFIER, LABEL_PATIENT)
    client_with_data.put_studies_id_labels_label(a_study.IDENTIFIER, LABEL_STUDY)
    client_with_data.put_series_id_labels_label(a_series.IDENTIFIER, LABEL_SERIES)
    client_with_data.put_instances_id_labels_label(an_instance.IDENTIFIER, LABEL_INSTANCE)

    return Labels(client_with_data)


@pytest.mark.parametrize('expected', [
    [LABEL_PATIENT, LABEL_STUDY, LABEL_SERIES, LABEL_INSTANCE]
])
def test_labels(labels, expected):
    assert labels == expected
    assert sorted([label for label in labels]) == sorted(expected)
    assert len(labels) == len(expected)
    assert LABEL_PATIENT in labels


@pytest.mark.parametrize('label, expected_identifiers', [
    ('bad_label', []),
    (LABEL_PATIENT, [a_patient.IDENTIFIER])
])
def test_find_patients(labels, label, expected_identifiers):
    result = labels.find_patients(label)

    assert result == [Patient(id_, labels.client) for id_ in expected_identifiers]


@pytest.mark.parametrize('label, expected_identifiers', [
    ('bad_label', []),
    (LABEL_STUDY, [a_study.IDENTIFIER])
])
def test_find_studies(labels, label, expected_identifiers):
    result = labels.find_studies(label)

    assert result == [Study(id_, labels.client) for id_ in expected_identifiers]


@pytest.mark.parametrize('label, expected_identifiers', [
    ('bad_label', []),
    (LABEL_SERIES, [a_series.IDENTIFIER])
])
def test_find_series(labels, label, expected_identifiers):
    result = labels.find_series(label)

    assert result == [Series(id_, labels.client) for id_ in expected_identifiers]


@pytest.mark.parametrize('label, expected_identifiers', [
    ('bad_label', []),
    (LABEL_INSTANCE, [an_instance.IDENTIFIER])
])
def test_find_instances(labels, label, expected_identifiers):
    result = labels.find_instances(label)

    assert result == [Instance(id_, labels.client) for id_ in expected_identifiers]
