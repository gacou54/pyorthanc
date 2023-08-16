import pytest

from ..setup_server import ORTHANC_1, ORTHANC_2, setup_data

MODALITY = ORTHANC_1.AeT
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


@pytest.mark.parametrize('modality_aet', [ORTHANC_1.AeT])
def test_modality_echo(client, modality, modality_aet):
    result = client.post_modalities_id_echo(modality_aet)

    assert result == {}  # Means it has not raised


@pytest.mark.parametrize('modality_aet', [ORTHANC_1.AeT])
def test_modality_query(client, modality, modality_aet):
    setup_data(ORTHANC_2)
    expected_query_answer = {
        '0008,0005': {'Name': 'SpecificCharacterSet', 'Type': 'String', 'Value': 'ISO_IR 100'},
        '0008,0050': {'Name': 'AccessionNumber', 'Type': 'String', 'Value': '20090926001'},
        '0008,0052': {'Name': 'QueryRetrieveLevel', 'Type': 'String', 'Value': 'STUDY'},
        '0008,0054': {'Name': 'RetrieveAETitle', 'Type': 'String', 'Value': 'ORTHANC'},
        '0010,0020': {'Name': 'PatientID', 'Type': 'String', 'Value': 'MP15-067'},
        '0020,000d': {'Name': 'StudyInstanceUID', 'Type': 'String', 'Value': '1.3.6.1.4.1.22213.2.6291.2.1'}
    }

    result = client.post_modalities_id_query(MODALITY, PAYLOAD)

    assert 'ID' in result.keys()
    assert 'Path' in result.keys()
    assert client.get_queries_id_answers_index_content(result['ID'], 0) == expected_query_answer


@pytest.mark.parametrize('modality_aet', [ORTHANC_1.AeT])
def test_modality_move(client, modality, modality_aet):
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

    query_result = client.post_modalities_id_query(modality_aet, PAYLOAD)
    result = client.post_queries_id_retrieve(query_result['ID'], json=cmove_data)

    assert result == expected_move_answer

    resulting_patient_information = client.get_patients_id(
        client.get_patients()[0]
    )

    assert {k: v for k, v in PATIENT_INFORMATION.items() if k not in ['LastUpdate']} == \
           {k: v for k, v in resulting_patient_information.items() if k not in ['LastUpdate']}


@pytest.mark.parametrize('modality_aet', [ORTHANC_1.AeT])
def test_modality_store(client, modality, modality_aet):
    setup_data(ORTHANC_1)
    an_instance_identifier = client.get_instances()[0]

    result = client.post_modalities_id_store(modality_aet, data=an_instance_identifier)

    assert {k: v for k, v in result.items() if k != 'ParentResources'} == \
           {
               'Description': 'REST API',
               'FailedInstancesCount': 0,
               'InstancesCount': 1,
               'LocalAet': ORTHANC_1.AeT,
               'RemoteAet': ORTHANC_2.AeT
           }
