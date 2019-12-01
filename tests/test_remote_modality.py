# coding: utf-8
# author: Gabriel Couture
import unittest

from pyorthanc import Orthanc, RemoteModality
from tests import setup_server

MODALITY = 'SecondOrthanc'
PAYLOAD = {'Level': 'Study', 'Query': {'PatientID': 'MP*'}}
PATIENT_INFORMATION = {
    'ID': '50610f37-9df85809-faaec921-9c829c41-e5261ca2',
    'IsStable': False,
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


class TestRemoteModality(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global orthanc_subprocess
        global second_orthanc_subprocess
        orthanc_subprocess = setup_server.setup_orthanc_server()
        second_orthanc_subprocess = setup_server.setup_second_orthanc_server()

    @classmethod
    def tearDownClass(cls) -> None:
        global orthanc_subprocess
        global second_orthanc_subprocess
        setup_server.stop_orthanc_server_and_remove_data_directory(orthanc_subprocess)
        setup_server.stop_second_orthanc_server_and_remove_data_directory(second_orthanc_subprocess)
        del orthanc_subprocess
        del second_orthanc_subprocess

    def setUp(self) -> None:
        self.orthanc = Orthanc(setup_server.ORTHANC_URL)
        self.remote = RemoteModality(self.orthanc, MODALITY)

    def tearDown(self) -> None:
        self.orthanc = None
        self.remote = None
        setup_server.clear_data()
        setup_server.clear_data_of_second_orthanc()

    def given_patient_in_second_orthanc_server(self):
        setup_server.setup_data_for_second_orthanc()

    def test_whenDoingAnEcho_thenResultIsTrue(self):
        result = self.remote.echo()

        self.assertTrue(result)

    def test_givenDataInSecondServerAndPayload_whenQuerying_thenQueryHasExpectingContent(self):
        self.given_patient_in_second_orthanc_server()
        expected_query_answer_content = {
            '0008,0005': {
                'Name': 'SpecificCharacterSet',
                'Type': 'String',
                'Value': 'ISO_IR 100'
            },
            '0008,0050': {
                'Name': 'AccessionNumber',
                'Type': 'String',
                'Value': '20090926001'
            },
            '0008,0052': {
                'Name': 'QueryRetrieveLevel',
                'Type': 'String',
                'Value': 'STUDY'
            },
            '0010,0020': {
                'Name': 'PatientID',
                'Type': 'String',
                'Value': 'MP15-067'
            },
            '0020,000d': {
                'Name': 'StudyInstanceUID',
                'Type': 'String',
                'Value': '1.3.6.1.4.1.22213.2.6291.2.1'
            }
        }

        result = self.remote.query(PAYLOAD)

        self.assertIn('ID', result.keys())
        self.assertIn('Path', result.keys())
        self.assertEqual(
            expected_query_answer_content,
            self.orthanc.get_content_of_specified_query_answer(result['ID'], 0)
        )

    def test_givenDataInSecondServerAndQuery_whenMoving_thenDataInSecondServerIsInFirstOrthancServer(self):
        self.given_patient_in_second_orthanc_server()
        cmove_data = {'TargetAet': 'FirstOrthanc'}
        expected_move_answer = {
            'Description': 'REST API',
            'LocalAet': 'FIRSTORTHANC',
            'RemoteAet': 'SECONDORTHANC'
        }

        query_result = self.remote.query(PAYLOAD)
        result = self.remote.move(query_result['ID'], cmove_data)

        try:
            del result['Query']  # On some version of Orthanc, A Query field is there
        except KeyError:
            pass
        self.assertDictEqual(expected_move_answer, result)
        resulting_patient_information = self.orthanc.get_patient_information(self.orthanc.get_patients()[0])
        self.assertEqual(
            {k: v for k, v in PATIENT_INFORMATION.items() if k != 'LastUpdate'},
            {k: v for k, v in resulting_patient_information.items() if k != 'LastUpdate'}
        )
