import pytest

from pyorthanc import find_instances, find_patients, find_series, find_studies, query_orthanc
from .conftest import LABEL_INSTANCE, LABEL_PATIENT, LABEL_SERIES, LABEL_STUDY
from .data import a_patient, a_series, a_study, an_instance


@pytest.mark.parametrize('query, labels, expected', [
    (None, None, [a_patient.IDENTIFIER]),
    ({}, [], [a_patient.IDENTIFIER]),
    ({}, LABEL_PATIENT, [a_patient.IDENTIFIER]),
    ({}, [LABEL_PATIENT], [a_patient.IDENTIFIER]),
    ({'PatientID': '*'}, [LABEL_PATIENT], [a_patient.IDENTIFIER]),
    ({'PatientID': '*'}, ['NOT_EXISTING_LABEL'], []),
    ({'PatientID': 'NOT_EXISTING_PATIENT'}, None, []),
])
def test_find_patients(client_with_data_and_labels, query, labels, expected):
    result = find_patients(
        client=client_with_data_and_labels,
        query=query,
        labels=labels
    )

    assert [patient.id_ for patient in result] == expected


@pytest.mark.parametrize('query, labels, expected', [
    (None, None, [a_study.IDENTIFIER]),
    ({}, [], [a_study.IDENTIFIER]),
    ({}, LABEL_STUDY, [a_study.IDENTIFIER]),
    ({}, [LABEL_STUDY], [a_study.IDENTIFIER]),
    ({'ReferringPhysicianName': '*'}, [LABEL_STUDY], [a_study.IDENTIFIER]),
    ({'ReferringPhysicianName': '*'}, ['NOT_EXISTING_LABEL'], []),
    ({'ReferringPhysicianName': 'BAD_NAME'}, None, []),
])
def test_find_studies(client_with_data_and_labels, query, labels, expected):
    result = find_studies(
        client=client_with_data_and_labels,
        query=query,
        labels=labels
    )

    assert [study.id_ for study in result] == expected


@pytest.mark.parametrize('query, labels, expected', [
    (None, None, ['60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b', 'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06', 'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96']),
    ({}, [], ['60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b', 'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06', 'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96']),
    ({}, LABEL_SERIES, [a_series.IDENTIFIER]),
    ({}, [LABEL_SERIES], [a_series.IDENTIFIER]),
    ({'Modality': 'RTDose'}, [LABEL_SERIES], [a_series.IDENTIFIER]),
    ({'Modality': 'RTDose'}, ['NOT_EXISTING_LABEL'], []),
    ({'Modality': 'NOT_EXISTING_MODALITY'}, None, []),
])
def test_find_series(client_with_data_and_labels, query, labels, expected):
    result = find_series(
        client=client_with_data_and_labels,
        query=query,
        labels=labels
    )

    assert [series.id_ for series in result] == expected


@pytest.mark.parametrize('query, labels, expected', [
    (None, None, ['22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9', 'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599', '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220']),
    ({}, [], ['22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9', 'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599', '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220']),
    ({}, LABEL_INSTANCE, [an_instance.IDENTIFIER]),
    ({}, [LABEL_INSTANCE], [an_instance.IDENTIFIER]),
    ({'InstanceCreationDate': an_instance.CREATION_DATE}, [LABEL_INSTANCE], [an_instance.IDENTIFIER]),
    ({'InstanceCreationDate': an_instance.CREATION_DATE}, ['NOT_EXISTING_LABEL'], []),
    ({'InstanceCreationDate': '99990320'}, None, []),  # Not existing date
])
def test_find_instance(client_with_data_and_labels, query, labels, expected):
    result = find_instances(
        client=client_with_data_and_labels,
        query=query,
        labels=labels
    )

    assert [instance.id_ for instance in result] == expected


@pytest.mark.parametrize('level, query, labels, labels_constraint, expected', [
    # On level
    ('Patient', None, None, 'All', [a_patient.IDENTIFIER]),
    ('Study', None, None, 'All', [a_study.IDENTIFIER]),
    ('Series', None, None, 'All', ['60108266-ece4d8f7-7b028286-a7b61f25-c6d33f0b', 'c4c1fcc9-ae63f793-40cbcf25-fbd3efe5-ad72ff06', 'e2a7df26-99673e0f-05aa84cd-c89677c0-634a2a96']),
    ('Instance', None, None, 'All', ['22dcf059-8fd3ade7-efb39ca3-7f46b248-0200abc9', 'da2024f5-606f9e83-41b012bb-9dced1ea-77bcd599', '348befe7-5be5ff53-70120381-3baa0cc2-e4e04220']),
    # On query
    ('Patient', {}, None, 'All', [a_patient.IDENTIFIER]),
    ('Patient', {'PatientID': '*'}, None, 'All', [a_patient.IDENTIFIER]),
    ('Patient', {'PatientID': 'NOT_EXISTING_PATIENT'}, None, 'All', []),
    # On labels
    ('Patient', None, LABEL_PATIENT, 'All', [a_patient.IDENTIFIER]),
    ('Patient', None, [LABEL_PATIENT], 'All', [a_patient.IDENTIFIER]),
    ('Patient', None, '', 'All', [a_patient.IDENTIFIER]),
    ('Patient', None, [], 'All', [a_patient.IDENTIFIER]),
    ('Patient', None, ['NOT_EXISTING_LABEL'], 'All', []),
    # On labels_constraint
    ('Patient', None, [LABEL_PATIENT], 'All', [a_patient.IDENTIFIER]),
    ('Patient', None, [LABEL_PATIENT, 'BAD_LABEL'], 'All', []),
    ('Patient', None, [LABEL_PATIENT, 'BAD_LABEL'], 'Any', [a_patient.IDENTIFIER]),
    ('Patient', None, [LABEL_PATIENT], 'None', []),
    ('Patient', None, None, 'None', [a_patient.IDENTIFIER]),
])
def test_query_orthanc(client_with_data_and_labels, level, query, labels, labels_constraint, expected):
    result = query_orthanc(
        client=client_with_data_and_labels,
        level=level,
        query=query,
        labels=labels,
        labels_constraint=labels_constraint,
    )

    assert [resource.id_ for resource in result] == expected


@pytest.mark.parametrize('level, labels_constraint', [
    ('bad_level', 'All'),
    ('Patient', 'bad_constraint'),
])
def test_query_orthanc_errors(client_with_data_and_labels, level, labels_constraint):
    with pytest.raises(ValueError):
        query_orthanc(
            client=client_with_data_and_labels,
            level=level,
            labels_constraint=labels_constraint
        )
