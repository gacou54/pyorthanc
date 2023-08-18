import pytest

from pyorthanc import Labels, Patient, Study, Series, Instance
from .conftest import LABEL_PATIENT, LABEL_STUDY, LABEL_SERIES, LABEL_INSTANCE
from .data import a_patient, a_study, a_series, an_instance


@pytest.fixture
def labels(client_with_data_and_labels):
    return Labels(client_with_data_and_labels)


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
