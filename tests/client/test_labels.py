import httpx
import pytest

from ..data import a_patient, a_study, a_series, an_instance

LABEL = 'my_label'
BAD_LABEL = 'my label'


def test_patients_labels(client_with_data):
    result = client_with_data.get_patients_id_labels(a_patient.IDENTIFIER)
    assert result == []

    # Assign label
    result = client_with_data.put_patients_id_labels_label(a_patient.IDENTIFIER, LABEL)
    assert result == ''

    # Get patient's labels
    result = client_with_data.get_patients_id_labels(a_patient.IDENTIFIER)
    assert result == [LABEL]

    # Test if patient as label
    result = client_with_data.get_patients_id_labels_label(a_patient.IDENTIFIER, LABEL)
    assert result is ''

    # Delete label
    result = client_with_data.delete_patients_id_labels_label(a_patient.IDENTIFIER, LABEL)
    assert result is ''

    result = client_with_data.get_patients_id_labels(a_patient.IDENTIFIER)
    assert result == []


def test_studies_labels(client_with_data):
    result = client_with_data.get_studies_id_labels(a_study.IDENTIFIER)
    assert result == []

    # Assign label
    result = client_with_data.put_studies_id_labels_label(a_study.IDENTIFIER, LABEL)
    assert result == ''

    # Get study's labels
    result = client_with_data.get_studies_id_labels(a_study.IDENTIFIER)
    assert result == [LABEL]

    # Test if study as label
    result = client_with_data.get_studies_id_labels_label(a_study.IDENTIFIER, LABEL)
    assert result is ''

    # Delete label
    result = client_with_data.delete_studies_id_labels_label(a_study.IDENTIFIER, LABEL)
    assert result is ''

    result = client_with_data.get_studies_id_labels(a_study.IDENTIFIER)
    assert result == []


def test_series_labels(client_with_data):
    result = client_with_data.get_series_id_labels(a_series.IDENTIFIER)
    assert result == []

    # Assign label
    result = client_with_data.put_series_id_labels_label(a_series.IDENTIFIER, LABEL)
    assert result == ''

    # Get series's labels
    result = client_with_data.get_series_id_labels(a_series.IDENTIFIER)
    assert result == [LABEL]

    # Test if series as label
    result = client_with_data.get_series_id_labels_label(a_series.IDENTIFIER, LABEL)
    assert result is ''

    # Delete label
    result = client_with_data.delete_series_id_labels_label(a_series.IDENTIFIER, LABEL)
    assert result is ''

    result = client_with_data.get_series_id_labels(a_series.IDENTIFIER)
    assert result == []


def test_instances_labels(client_with_data):
    result = client_with_data.get_instances_id_labels(an_instance.IDENTIFIER)
    assert result == []

    # Assign label
    result = client_with_data.put_instances_id_labels_label(an_instance.IDENTIFIER, LABEL)
    assert result == ''

    # Get instance's labels
    result = client_with_data.get_instances_id_labels(an_instance.IDENTIFIER)
    assert result == [LABEL]

    # Test if instance as label
    result = client_with_data.get_instances_id_labels_label(an_instance.IDENTIFIER, LABEL)
    assert result is ''

    # Delete label
    result = client_with_data.delete_instances_id_labels_label(an_instance.IDENTIFIER, LABEL)
    assert result is ''

    result = client_with_data.get_instances_id_labels(an_instance.IDENTIFIER)
    assert result == []


def test_tools_labels(client_with_data):
    result = client_with_data.get_tools_labels()
    assert result == []

    # Assign label
    client_with_data.put_instances_id_labels_label(an_instance.IDENTIFIER, LABEL)

    result = client_with_data.get_tools_labels()
    assert result == [LABEL]


def test_bad_label(client_with_data):
    with pytest.raises(httpx.HTTPError):
        client_with_data.put_patients_id_labels_label(a_patient.IDENTIFIER, BAD_LABEL)

