import unittest

from pyorthanc import Orthanc
from tests.setup_server import ORTHANC_1, ORTHANC_2, add_modality, clear_data, setup_data

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


class TestDicomMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.orthanc = Orthanc(ORTHANC_1.url, username=ORTHANC_1.username, password=ORTHANC_1.password)
        if ORTHANC_2.AeT not in self.orthanc.get_modalities():
            add_modality(ORTHANC_1, ORTHANC_2.AeT, 'orthanc2', 4242)
            add_modality(ORTHANC_2, ORTHANC_1.AeT, 'orthanc1', 4242)

    def tearDown(self) -> None:
        clear_data(ORTHANC_1)
        clear_data(ORTHANC_2)

    def given_patient_in_orthanc_server(self):
        setup_data(ORTHANC_1)

    def given_patient_in_second_orthanc_server(self):
        setup_data(ORTHANC_2)

    def test_whenEchoOnModality_thenResultIsTrue(self):
        # Assert not throw
        self.orthanc.post_modalities_id_echo(MODALITY)

    def test_givenDataInSecondServerAndPayload_whenQuerying_thenQueryHasExpectingContent(self):
        self.given_patient_in_second_orthanc_server()
        expected_query_answer_content = {
            '0008,0005': {'Name': 'SpecificCharacterSet', 'Type': 'String', 'Value': 'ISO_IR 100'},
            '0008,0050': {'Name': 'AccessionNumber', 'Type': 'String', 'Value': '20090926001'},
            '0008,0052': {'Name': 'QueryRetrieveLevel', 'Type': 'String', 'Value': 'STUDY'},
            '0008,0054': {'Name': 'RetrieveAETitle', 'Type': 'String', 'Value': ORTHANC_2.AeT},
            '0010,0020': {'Name': 'PatientID', 'Type': 'String', 'Value': 'MP15-067'},
            '0020,000d': {'Name': 'StudyInstanceUID', 'Type': 'String', 'Value': '1.3.6.1.4.1.22213.2.6291.2.1'}
        }

        result = self.orthanc.post_modalities_id_query(MODALITY, PAYLOAD)

        self.assertIn('ID', result.keys())
        self.assertIn('Path', result.keys())
        self.assertEqual(
            expected_query_answer_content,
            self.orthanc.get_queries_id_answers_index_content(result['ID'], 0)
        )

    def test_givenDataInSecondServerAndQuery_whenMoving_thenDataInSecondServerIsInFirstOrthancServer(self):
        self.given_patient_in_second_orthanc_server()
        cmove_data = {'TargetAet': ORTHANC_1.AeT}
        expected_move_answer = {
            'Description': 'REST API',
            'LocalAet': ORTHANC_1.AeT,
            'RemoteAet': ORTHANC_2.AeT
        }

        query_result = self.orthanc.post_modalities_id_query(MODALITY, PAYLOAD)
        result = self.orthanc.post_queries_id_retrieve(query_result['ID'], json=cmove_data)

        try:
            del result['Query']  # On some version of Orthanc, A Query field is there
        except KeyError:
            pass
        self.assertDictEqual(expected_move_answer, result)
        resulting_patient_information = self.orthanc.get_patients_id(self.orthanc.get_patients()[0])
        self.assertEqual(
            {k: v for k, v in PATIENT_INFORMATION.items() if k != 'LastUpdate'},
            {k: v for k, v in resulting_patient_information.items() if k != 'LastUpdate'}
        )

    def test_givenInstance_whenStoreOnModality_thenResultIsExpectedDict(self):
        self.given_patient_in_orthanc_server()
        an_instance_identifier = self.orthanc.get_instances()[0]

        result = self.orthanc.post_modalities_id_store(MODALITY, data=an_instance_identifier)

        self.assertEqual(
            {k: v for k, v in result.items() if k != 'ParentResources'},
            {
                'Description': 'REST API',
                'FailedInstancesCount': 0,
                'InstancesCount': 1,
                'LocalAet': ORTHANC_1.AeT,
                'RemoteAet': ORTHANC_2.AeT
            }
        )
