import httpx
import pytest

from .setup_server import ORTHANC_1, ORTHANC_2, setup_data

MODALITY = 'Orthanc2'
PAYLOAD = {'Level': 'Study', 'Query': {'PatientID': 'MP*'}}
PATIENT_INFORMATION = {
    'ID': '50610f37-9df85809-faaec921-9c829c41-e5261ca2',
    'IsStable': False,
    'Labels': [],
    'LastUpdate': 'THIS_ALWAYS_VARY',
    'MainDicomTags': {
        'PatientBirthDate': '',
        'PatientID': 'MP15-067',
        'PatientName': 'DVH_Phantom',
        'PatientSex': 'O'
    },
    'Studies': ['1e21052b-c7b6ea5c-e1c7e4ec-672ca250-0c54d47e'],
    'Type': 'Patient'
}


def test_echo(modality):
    result = modality.echo()

    assert result


def test_find(modality):
    setup_data(ORTHANC_2)
    expected_query_answer = [{
        'SpecificCharacterSet': 'ISO_IR 100',
        'AccessionNumber': '20090926001',
        'QueryRetrieveLevel': 'STUDY',
        'RetrieveAETitle': 'ORTHANC',
        'PatientID': 'MP15-067',
        'StudyInstanceUID': '1.3.6.1.4.1.22213.2.6291.2.1'
    }]

    response = modality.find(PAYLOAD)

    assert isinstance(response['ID'], str)
    assert response['answers'] == expected_query_answer


def test_query(modality):
    assert modality.query == modality.find


def test_failed_find(modality):
    bad_payload = {'Level': 'Study', 'Query': {'BadTag': 'MP*'}}

    with pytest.raises(httpx.HTTPError):
        modality.find(bad_payload)


def test_move(modality):
    expected_move_answer = {
        'Description': 'REST API',
        'LocalAet': ORTHANC_1.AeT,
        'RemoteAet': ORTHANC_2.AeT,
        'Query': [{
            '0008,0050': '20090926001',
            '0008,0052': 'STUDY',
            '0010,0020': 'MP15-067',
            '0020,000d': '1.3.6.1.4.1.22213.2.6291.2.1'
        }],
    }
    setup_data(ORTHANC_2)

    response = modality.find(PAYLOAD)
    result = modality.move(response['ID'])

    assert result == expected_move_answer

    resulting_patient_information = modality.client.get_patients_id(
        modality.client.get_patients()[0]
    )

    assert {k: v for k, v in PATIENT_INFORMATION.items() if k not in ['LastUpdate']} == \
           {k: v for k, v in resulting_patient_information.items() if k not in ['LastUpdate']}


def test_move_to_target_modality(modality):
    cmove_data = {'TargetAet': ORTHANC_1.AeT}
    expected_move_answer = {
        'Description': 'REST API',
        'LocalAet': ORTHANC_1.AeT,
        'RemoteAet': ORTHANC_2.AeT,
        'Query': [{
            '0008,0050': '20090926001',
            '0008,0052': 'STUDY',
            '0010,0020': 'MP15-067',
            '0020,000d': '1.3.6.1.4.1.22213.2.6291.2.1'
        }],
    }
    setup_data(ORTHANC_2)

    response = modality.find(PAYLOAD)
    result = modality.move(response['ID'], cmove_data)

    assert result == expected_move_answer

    resulting_patient_information = modality.client.get_patients_id(
        modality.client.get_patients()[0]
    )

    assert {k: v for k, v in PATIENT_INFORMATION.items() if k not in ['LastUpdate']} == \
           {k: v for k, v in resulting_patient_information.items() if k not in ['LastUpdate']}


def test_store(modality):
    setup_data(ORTHANC_1)
    an_instance_identifier = modality.client.get_instances()[0]

    result = modality.store(an_instance_identifier)

    assert {k: v for k, v in result.items() if k != 'ParentResources'} == \
           {
               'Description': 'REST API',
               'FailedInstancesCount': 0,
               'InstancesCount': 1,
               'LocalAet': ORTHANC_1.AeT,
               'RemoteAet': ORTHANC_2.AeT
           }
